import io
import re
import pikepdf
import pdfplumber
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class HDFCParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            pdf_file = io.BytesIO(file_bytes)
            if password:
                pdf = pikepdf.open(pdf_file, password=password)
                temp_pdf = io.BytesIO()
                pdf.save(temp_pdf)
                temp_pdf.seek(0)
                pdf_file = temp_pdf
            
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    for line in lines:
                        # Simple regex matching for typical HDFC statement lines
                        # Format varies, but date is usually first
                        # Example: 01/01/24 Narration ... 1,000.00
                        match = re.match(r'^(\d{2}/\d{2}/\d{2,4})\s+(.+?)\s+([\d,]+\.\d{2})\s*$', line)
                        if match:
                            date_str, desc, amount_str = match.groups()
                            # Parse date
                            try:
                                dt = datetime.strptime(date_str, '%d/%m/%y')
                            except ValueError:
                                try:
                                    dt = datetime.strptime(date_str, '%d/%m/%Y')
                                except ValueError:
                                    continue
                            
                            date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                            amount_cents = int(float(amount_str.replace(',', '')) * 100)
                            
                            # Guessing debit/credit based on text (very simplified)
                            # In real parsers, tables are extracted to explicitly map debit/credit columns
                            tx_type = 'debit'
                            if 'CR' in line or 'Deposit' in desc:
                                tx_type = 'credit'
                                
                            merchant = desc[:50].strip()
                            transactions.append(ParsedTransaction(
                                date=date_iso,
                                description=desc.strip(),
                                amount=amount_cents,
                                transaction_type=tx_type,
                                merchant=merchant,
                                raw_text=line
                            ))
        except Exception as e:
            raise ValueError(f"HDFC Parser Error: {str(e)}")
            
        return transactions
