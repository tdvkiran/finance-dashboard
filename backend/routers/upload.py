from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from database import get_db
from models import Transaction
from parsers import (
    HDFCParser, SBIParser, IDFCParser, CentralBankParser,
    PhonePeParser, GooglePayParser, CredParser
)
from services.categorization import categorize_transaction

router = APIRouter()

PARSERS = {
    "hdfc": HDFCParser(),
    "sbi": SBIParser(),
    "idfc": IDFCParser(),
    "central_bank": CentralBankParser(),
    "phonepe": PhonePeParser(),
    "google_pay": GooglePayParser(),
    "cred": CredParser()
}

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    password: Optional[str] = Form(None),
    source_bank: Optional[str] = Form(None),
    username: Optional[str] = Form("default"),
    db: AsyncSession = Depends(get_db)
):
    # Normalize source_bank if provided
    if source_bank:
        source_bank = source_bank.lower().strip().replace(" ", "_")
        aliases = {
            "gpay": "google_pay",
            "googlepay": "google_pay",
            "google_pay": "google_pay",
            "central": "central_bank",
            "centralbank": "central_bank",
            "idfc_first": "idfc",
            "cred_upi": "cred"
        }
        source_bank = aliases.get(source_bank, source_bank)

    # Auto-detect bank from filename if not provided
    if not source_bank:
        filename = file.filename.lower()
        alias_matches = {
            "hdfc": "hdfc",
            "sbi": "sbi",
            "idfc": "idfc",
            "central": "central_bank",
            "phonepe": "phonepe",
            "google": "google_pay",
            "gpay": "google_pay",
            "cred": "cred"
        }
        for term, bank_key in alias_matches.items():
            if term in filename:
                source_bank = bank_key
                break

    if not source_bank or source_bank not in PARSERS:
        raise HTTPException(
            status_code=400,
            detail=f"Could not auto-detect bank from filename '{file.filename}'. Please select your bank/app from the dropdown."
        )

    parser = PARSERS[source_bank]
    try:
        content = await file.read()
        parsed_txns = parser.parse(content, password)
        
        if not parsed_txns:
            raise HTTPException(
                status_code=422,
                detail="0 transactions found in this statement. Please check if the PDF is password-protected or if the wrong bank parser was selected."
            )

        # Fetch existing transactions to prevent duplicate entries
        from sqlalchemy.future import select
        existing_result = await db.execute(select(Transaction.date, Transaction.amount, Transaction.type, Transaction.merchant))
        existing_keys = set(existing_result.all())

        db_txns = []
        total_debits = 0
        total_credits = 0
        duplicates_skipped = 0
        
        for pt in parsed_txns:
            key = (pt.date, pt.amount, pt.transaction_type, pt.merchant)
            if key in existing_keys:
                duplicates_skipped += 1
                continue
            
            existing_keys.add(key)
            category, _ = categorize_transaction(pt.description)
            
            db_txn = Transaction(
                date=pt.date,
                description=pt.description,
                amount=pt.amount,
                type=pt.transaction_type,
                category=category,
                merchant=pt.merchant,
                source_bank=source_bank,
                username=username or "default",
                raw_text=pt.raw_text
            )
            db_txns.append(db_txn)
            
            if pt.transaction_type == 'debit':
                total_debits += pt.amount
            else:
                total_credits += pt.amount
                
        if db_txns:
            db.add_all(db_txns)
            await db.commit()
        
        # Calculate summary
        dates = [pt.date for pt in parsed_txns]
        date_range = {"start": min(dates), "end": max(dates)} if dates else None
        
        return {
            "status": "success",
            "bank": source_bank.replace("_", " ").title(),
            "transactions_parsed": len(parsed_txns),
            "transactions_inserted": len(db_txns),
            "duplicates_skipped": duplicates_skipped,
            "date_range": date_range,
            "total_debits": total_debits,
            "total_credits": total_credits
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
