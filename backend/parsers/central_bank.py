import io
import re
import pdfplumber
import pytesseract
from PIL import Image
from typing import List, Optional
from datetime import datetime
from .base import BaseParser, ParsedTransaction

class CentralBankParser(BaseParser):
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        transactions = []
        try:
            pdf_file = io.BytesIO(file_bytes)
            with pdfplumber.open(pdf_file, password=password if password else '') as pdf:
                for page in pdf.pages:
                    # Try text extraction first
                    text = page.extract_text()
                    if not text:
                        # Fallback to OCR if no text found
                        img = page.to_image(resolution=300).original
                        text = pytesseract.image_to_string(img)
                        
                    if not text:
                        continue
                        
                    lines = text.split('\n')
                    for line in lines:
                        # Simple match for typical bank dates
                        match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.\d{2})', line)
                        if match:
                            date_str, desc, amount_str = match.groups()
                            try:
                                dt = datetime.strptime(date_str, '%d/%m/%Y')
                            except ValueError:
                                continue
                                
                            date_iso = dt.strftime('%Y-%m-%dT00:00:00Z')
                            amount_cents = int(float(amount_str.replace(',', '')) * 100)
                            
                            tx_type = 'debit'
                            if 'Cr' in line or 'Deposit' in desc:
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
            raise ValueError(f"Central Bank Parser Error: {str(e)}")
            
        return transactions
