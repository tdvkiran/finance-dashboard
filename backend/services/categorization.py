import re
from typing import Tuple

MERCHANT_RULES = {
    "Food & Dining": [
        "zomato", "swiggy", "dominos", "mcdonalds", "kfc", "pizza hut", "subway", 
        "blinkit", "zepto", "cafe", "restaurant", "hotel", "bakery", "bake", "juice",
        "delicacyz", "tosseat", "oori", "koodal virundhu", "zuchiz", "leelavathy",
        "annapoorna", "satyam food", "food zone", "aafa"
    ],
    "Sports & Fitness": [
        "sport", "sports", "turf", "badminton", "fitness", "gym", "cult",
        "elevate alliance", "puntu sports", "sport z", "cricket", "swimming"
    ],
    "Groceries": [
        "bigbasket", "instamart", "grofers", "super market", "star bazaar", 
        "open mart", "fine mart", "market", "fresh cuts", "fruits", "fruit",
        "fish & prawns", "onion shop", "pineapple", "vegetable", "daily needs"
    ],
    "Transport": [
        "uber", "ola", "rapido", "yulu", "bounce", "irctc", "redbus", "makemytrip", 
        "cleartrip", "indigo", "spicejet", "vistara", "air india", "flexiride", 
        "parking", "fuel", "petrol", "shell", "hpcl", "iocl", "bpcl"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "meesho", "nykaa", "tata cliq", 
        "shopclues", "ekart", "cell city", "mart", "stationery", "games"
    ],
    "Home & Utilities": [
        "appliances", "hardware", "electricals", "nursery", "plant", "plants",
        "airtel", "jio", "bsnl", "vodafone", "bescom", "tneb", "mahadiscom", 
        "bbmp", "water bill", "electricity", "gas", "cylinder"
    ],
    "Entertainment": [
        "netflix", "amazon prime", "hotstar", "sony liv", "zee5", "spotify", 
        "youtube premium", "bookmyshow", "pvr", "inox", "cinema", "torq"
    ],
    "Health & Medical": [
        "pharmacy", "apollo", "medplus", "1mg", "netmeds", "practo", "lybrate", 
        "thyrocare", "dr lal", "hospital", "clinic", "diagnostic"
    ],
    "Finance & Investment": [
        "insurance", "lic", "hdfc life", "max life", "sbi life", "ppf", "nps", 
        "zerodha", "groww", "upstox", "innofin"
    ],
    "ATM & Cash": ["atm", "cash withdrawal"],
    "Rent & Housing": ["narasimha rao", "rent", "maintenance", "landlord", "society"],
    "EMI & Loans": ["emi", "loan", "bajaj", "hdfc loan"],
    "Transfers": ["transfer", "sent to", "received from", "p2p"]
}

def categorize_transaction(description: str) -> Tuple[str, float]:
    """
    Categorizes a transaction based on its description.
    Returns a tuple of (Category Name, Confidence Score).
    """
    desc_lower = description.lower()
    
    for category, keywords in MERCHANT_RULES.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', desc_lower):
                return category, 0.9
                
    return "Other", 0.0

