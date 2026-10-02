import io
import re
import pandas as pd
import pdfplumber
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class IDFCParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            # Try to read as CSV first
            try:
                df = pd.read_csv(io.BytesIO(file_bytes))
                for _, row in df.iterrows():
                    # Assuming typical IDFC CSV columns
                    date_str = str(row.get('Transaction Date', row.get('Date', '')))
                    desc = str(row.get('Description', row.get('Narration', '')))
                    debit = row.get('Debit', 0)
                    credit = row.get('Credit', 0)
                    
                    if not date_str or date_str == 'nan':
                        continue
                    
                    dt = datetime.strptime(date_str, '%d-%b-%Y')
                    date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                    
                    amount_val = 0
                    tx_type = 'debit'
                    if pd.notna(debit) and float(debit) > 0:
                        amount_val = float(debit)
                    elif pd.notna(credit) and float(credit) > 0:
                        amount_val = float(credit)
                        tx_type = 'credit'
                        
                    if amount_val > 0:
                        transactions.append(ParsedTransaction(
                            date=date_iso,
                            description=desc.strip(),
                            amount=int(amount_val * 100),
                            transaction_type=tx_type,
                            merchant=desc[:50].strip(),
                            raw_text=f"{date_str} {desc} {amount_val}"
                        ))
                return transactions
            except Exception:
                pass
                
            # If CSV fails, try PDF
            pdf_file = io.BytesIO(file_bytes)
            with pdfplumber.open(pdf_file, password=password if password else '') as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    lines = text.split('\n')
                    for line in lines:
                        match = re.match(r'^(\d{2}-[a-zA-Z]{3}-\d{4})\s+(.+?)\s+([\d,]+\.\d{2})\s*$', line)
                        if match:
                            date_str, desc, amount_str = match.groups()
                            dt = datetime.strptime(date_str, '%d-%b-%Y')
                            date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                            amount_cents = int(float(amount_str.replace(',', '')) * 100)
                            
                            tx_type = 'debit'
                            if 'CR' in line:
                                tx_type = 'credit'
                                
                            transactions.append(ParsedTransaction(
                                date=date_iso,
                                description=desc.strip(),
                                amount=amount_cents,
                                transaction_type=tx_type,
                                merchant=desc[:50].strip(),
                                raw_text=line
                            ))
        except Exception as e:
            raise ValueError(f"IDFC Parser Error: {str(e)}")
            
        return transactions
