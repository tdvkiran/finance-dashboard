import io
import re
import pdfplumber
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class PhonePeParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            pdf_file = io.BytesIO(file_bytes)
            open_kwargs = {}
            if password:
                open_kwargs['password'] = password
            
            with pdfplumber.open(pdf_file, **open_kwargs) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    full_text += "\n" + page_text

            # Parse transactions from consolidated text
            transactions = self._parse_from_text(full_text)

        except Exception as e:
            raise ValueError(f"PhonePe Parser Error: {str(e)}")
            
        return transactions

    def _parse_from_text(self, text: str) -> List[ParsedTransaction]:
        transactions: List[ParsedTransaction] = []
        if not text:
            return transactions

        # Remove header noise / footers
        cleaned_text = re.sub(r'Page \d+ of \d+', '', text)
        cleaned_text = re.sub(r'This is a (?:system|automatically) generated statement.*?(?=(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\Z))', '', cleaned_text, flags=re.DOTALL)
        
        # Split into blocks starting with date pattern: "MMM DD, YYYY" or "DD/MM/YYYY" or "YYYY-MM-DD"
        date_pattern = r'(?=(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s*\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2}))'
        blocks = re.split(date_pattern, cleaned_text)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            txn = self._parse_block(block)
            if txn:
                transactions.append(txn)

        return transactions

    def _parse_block(self, block: str) -> Optional[ParsedTransaction]:
        # Normalize whitespace while preserving essential structure
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            return None

        full_block_text = " ".join(lines)

        # 1. Extract Amount (handle "Debit INR 100.00" or "Debit INR \n 10000.00" or "₹100.00")
        amount_match = re.search(r'(?:Debit|Credit)?\s*(?:INR|Rs\.?|₹)\s*([\d,]+\.?\d*)', full_block_text, re.IGNORECASE)
        if not amount_match:
            # Fallback to any standalone currency amount
            amount_match = re.search(r'(?:₹|INR|Rs\.?|\b)\s*([\d,]+\.\d{2})\b', full_block_text, re.IGNORECASE)
            if not amount_match:
                return None

        amount_str = amount_match.group(1).replace(',', '')
        try:
            amount_val = float(amount_str)
            amount_cents = int(round(amount_val * 100))
            if amount_cents <= 0:
                return None
        except ValueError:
            return None

        # 2. Extract Date & Time
        date_iso = None
        # Format: MMM DD, YYYY (e.g. Sep 01, 2026)
        d_match = re.search(r'([A-Za-z]{3,9}\s+\d{1,2},\s*\d{2,4})', full_block_text)
        if d_match:
            try:
                date_clean = d_match.group(1).replace(',', '')
                # Check for optional time (e.g. 10:13 AM)
                t_match = re.search(r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)', full_block_text)
                if t_match:
                    try:
                        time_str = t_match.group(1).strip()
                        dt = datetime.strptime(f"{date_clean} {time_str}", '%b %d %Y %I:%M %p')
                        date_iso = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        pass
                if not date_iso:
                    dt = datetime.strptime(date_clean, '%b %d %Y')
                    date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
            except ValueError:
                pass

        # DD/MM/YYYY or DD-MM-YYYY fallback
        if not date_iso:
            d_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', full_block_text)
            if d_match:
                date_val = d_match.group(1).replace('-', '/')
                fmt = '%d/%m/%Y' if len(date_val.split('/')[-1]) == 4 else '%d/%m/%y'
                try:
                    dt = datetime.strptime(date_val, fmt)
                    date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                except ValueError:
                    pass

        # YYYY-MM-DD fallback
        if not date_iso:
            d_match = re.search(r'(\d{4}-\d{2}-\d{2})', full_block_text)
            if d_match:
                try:
                    dt = datetime.strptime(d_match.group(1), '%Y-%m-%d')
                    date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                except ValueError:
                    pass

        if not date_iso:
            return None

        # 3. Transaction Type (Debit or Credit)
        tx_type = 'debit'
        if re.search(r'\b(?:Credit|Received from|Refund|Cashback|Credited to)\b', full_block_text, re.IGNORECASE):
            # Verify it's not "Debited from ... Credited to" where user is payer
            if re.search(r'\b(?:Received from|Credited to)\b', full_block_text, re.IGNORECASE) and not re.search(r'\bDebited from\b', full_block_text, re.IGNORECASE):
                tx_type = 'credit'
            elif re.search(r'\bCredit\s+(?:INR|₹)', full_block_text, re.IGNORECASE):
                tx_type = 'credit'

        # 4. Extract Merchant / Party Name
        merchant = ""
        # Check "Paid to <Merchant>" or "Received from <Sender>"
        m_party = re.search(r'(?:Paid to|Received from|Paid)\s+([^:\n\r]+?)(?=\s+(?:Transaction ID|UTR|Debited|Credited|Debit|Credit|Type|$))', full_block_text, re.IGNORECASE)
        if m_party and m_party.group(1).strip():
            merchant = m_party.group(1).strip()
        else:
            # Fallback to first line after date/time
            desc_lines = [l for l in lines if not re.search(r'^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{1,2}:|Transaction ID|UTR|Debited|Credited|Page|Date)', l, re.IGNORECASE)]
            merchant = desc_lines[0] if desc_lines else full_block_text[:40]

        merchant = re.sub(r'^(?:Paid to|Received from|Paid)\s*', '', merchant, flags=re.IGNORECASE).strip()
        if not merchant:
            merchant = "PhonePe Transfer"

        # Build clean description
        description = f"{'Received from' if tx_type == 'credit' else 'Paid to'} {merchant}"

        return ParsedTransaction(
            date=date_iso,
            description=description,
            amount=amount_cents,
            transaction_type=tx_type,
            merchant=merchant[:60].strip(),
            raw_text=full_block_text
        )

