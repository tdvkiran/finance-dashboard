import io
import pandas as pd
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class GooglePayParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            df = pd.read_csv(io.BytesIO(file_bytes))
            for _, row in df.iterrows():
                date_str = str(row.get('Date', ''))
                desc = str(row.get('Description', ''))
                amount_str = str(row.get('Amount', ''))
                status = str(row.get('Status', ''))
                
                if status.lower() not in ['completed', 'success']:
                    continue
                    
                if not date_str or not amount_str:
                    continue
                    
                # Parse date, e.g., 2024-01-01 14:00:00
                try:
                    dt = pd.to_datetime(date_str)
                    date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                except Exception:
                    continue
                
                amount_val = float(amount_str.replace('₹', '').replace(',', ''))
                amount_cents = int(amount_val * 100)
                
                # Try to determine debit/credit
                tx_type = 'debit'
                if amount_val > 0: # Some formats use positive/negative
                    # If it's always positive, need to parse description
                    if 'received' in desc.lower():
                        tx_type = 'credit'
                else:
                    tx_type = 'debit'
                    amount_cents = abs(amount_cents)
                    
                transactions.append(ParsedTransaction(
                    date=date_iso,
                    description=desc.strip(),
                    amount=amount_cents,
                    transaction_type=tx_type,
                    merchant=desc[:50].strip(),
                    raw_text=f"{date_str} {desc} {amount_str}"
                ))
        except Exception as e:
            raise ValueError(f"Google Pay Parser Error: {str(e)}")
            
        return transactions
