from typing import List, Dict
import numpy as np
from collections import defaultdict
from models import Transaction

def generate_insights(transactions: List[Transaction]) -> List[Dict[str, str]]:
    """
    Generate text insights based on transaction history.
    """
    insights = []
    
    # Group by merchant
    merchant_txns = defaultdict(list)
    category_amounts = defaultdict(list)
    
    for t in transactions:
        if t.type == 'debit':
            merchant_txns[t.merchant].append(t)
            category_amounts[t.category].append(t.amount)
            
    # Detect recurring transactions (same merchant, similar amount > 2 times)
    for merchant, txns in merchant_txns.items():
        if len(txns) >= 2:
            amounts = [t.amount for t in txns]
            mean_amt = np.mean(amounts)
            std_amt = np.std(amounts)
            
            # If standard deviation is low relative to mean, it's likely a fixed recurring payment
            if std_amt < (0.1 * mean_amt):
                insights.append({
                    "type": "recurring",
                    "title": f"Recurring Payment Detected: {merchant}",
                    "message": f"You frequently spend around ₹{mean_amt/100:.2f} at {merchant}."
                })
                
    # Detect large unusual transactions (>2 std dev)
    for category, amounts in category_amounts.items():
        if len(amounts) >= 5:
            mean = np.mean(amounts)
            std = np.std(amounts)
            threshold = mean + (2 * std)
            
            for t in [txn for txn in transactions if txn.category == category and txn.type == 'debit']:
                if t.amount > threshold:
                    insights.append({
                        "type": "unusual_spend",
                        "title": f"Unusual spend in {category}",
                        "message": f"₹{t.amount/100:.2f} spent at {t.merchant} is significantly higher than your average {category} spend."
                    })
                    
    return insights
