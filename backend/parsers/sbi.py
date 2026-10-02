import io
import re
import pdfplumber
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class SBIParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            pdf_file = io.BytesIO(file_bytes)
            with pdfplumber.open(pdf_file, password=password if password else '') as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue
                        
                    lines = text.split('\n')
                    for line in lines:
                        # Simplified parsing for SBI statements
                        match = re.match(r'^(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s+(.+?)\s+([\d,]+\.\d{2})\s*$', line)
                        if match:
                            date_str, desc, amount_str = match.groups()
                            try:
                                dt = datetime.strptime(date_str, '%d %b %Y')
                            except ValueError:
                                continue
                                
                            date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                            amount_cents = int(float(amount_str.replace(',', '')) * 100)
                            
                            tx_type = 'debit'
                            if 'CREDIT' in line or 'By Transfer' in desc:
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
            raise ValueError(f"SBI Parser Error: {str(e)}")
            
        return transactions
