from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ParsedTransaction:
    date: str
    description: str
    amount: int
    transaction_type: str # 'debit' or 'credit'
    merchant: str
    raw_text: str

class BaseParser(ABC):
    """
    Abstract base class for all bank statement parsers.
    """
    @abstractmethod
    def parse(self, file_bytes: bytes, password: Optional[str] = None) -> List[ParsedTransaction]:
        """
        Parses a file and returns a list of ParsedTransaction objects.
        
        Args:
            file_bytes (bytes): The raw bytes of the file.
            password (str, optional): The password for the file, if applicable.
            
        Returns:
            List[ParsedTransaction]: The extracted transactions.
        """
        pass
