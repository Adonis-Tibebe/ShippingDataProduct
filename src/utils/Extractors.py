import re
import re
from typing import List

def classify_message(text: str) -> dict:
    """
    Given a Telegram post `text`, classify it and (optionally) extract product names.

    Returns one of:
        {"type": "vacancy", "products": []}
        {"type": "product", "products": [list‑of‑names]}
        {"type": "other",   "products": []}
    """

    # ---------------- helpers & static data ----------------
    VACANCY_KW = {
        "vacancy", "position", "apply", "experience", "salary", "license",
        "gp", "druggist", "pharmacist", "internal specialist", "urgent vacancy",
        "cpd"  # training / license renewal ads
    }

    PRODUCT_HINTS = {
        "new arrival", "new arrivals", "update", "stock update",
        "mg", "ml", "tab", "tabs", "cap", "caps", "syrup", "inj",
        "susp", "strip", "cassette", "kit", "test", "tube", "pcs"
    }

    PRODUCT_EMOJI = {"💊", "✅", "✔️", "🔥", "⭐️", "⭕️", "📈", "📦", "⏳", "#"}

    # regex: up to 4 capitalised tokens, allows digits, (), %, ‑, /
    PRODUCT_RE = re.compile(
        r"(?:^|[\s#💊✅✔️⭐️🔥⭕️📈📦⏳\-\*•])\s*"
        r"([A-Z][A-Za-z0-9()/%\-]+(?:\s+[A-Z0-9][A-Za-z0-9()/%\-]+){0,3})"
    )

    STOPWORDS = {
        "New", "NEW", "ARRIVAL", "ARRIVALS", "Update", "UPDATES", "Available",
        "Stock", "Items", "Medical", "Supplies", "Equipment", "Exp", "Exp.",
        "Round", "Cutting", "Powder", "free", "Blue", "Color",
        "Che-Med",
        "Brand",
        "First","Elastic",
        "Are",
        "Real-Time Inventory Tracking",
        "Expiry Alerts",
        "Seamless Collaboration",
        "Increased Efficiency",
        "Import)",
        "Aug-27Bulk",
        "Dec-27",
        "A)",
        "Multiple",
        "Also Available",
        "Non-drowsy",
        "VivaMedPharma",
        "StockAlert",
        "PharmaEthiopia",
        "QualityFirst",
        "HealthSolutions",
        "AllergyRelief",
        "SkinCareEssentials",
        "Size16",
        "NEW ARRIVALSALMAZ GIRMA",
        "Tounge",
        "Join",
        "Ns",
        "Rl",
        "Himed Sales091 160",
        "Tikvah Sales",
        "Jul-27",
        "VivaMed Pharma",
        "High Quality",
        "Available Now",
        "Telegram",
        "IMPORTEgens",
        "Pharmacy",
        "Track",
        "Get",
        "Streamline",
        "Boost"
    }

    pattern = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}(?:Bulk)?\b",
    re.I
    )

    # ---------------- quick vacancy test -------------------
    if isinstance(text, tuple):
        low = text[0].lower()
    else:
        low = text.lower()
    if any(kw in low for kw in VACANCY_KW):
        return {"type": "vacancy", "products": []}

    # ---------------- product‑post heuristics ---------------
    hint_hits = sum(kw in low for kw in PRODUCT_HINTS)
    emoji_hits = sum(e in text for e in PRODUCT_EMOJI)
    is_product_post = (hint_hits + emoji_hits) >= 2          # tweak if noisy

    if not is_product_post:
        return {"type": "other", "products": []}

    # ---------------- extract product names ----------------
    products, seen = [], set()
    for m in PRODUCT_RE.finditer(text):
        name = m.group(1).rstrip(",;:")
        if name in STOPWORDS or len(name.split()) > 4:
            continue

        # keep only if dosage/unit word nearby OR starts with emoji/hash
        tail_ok = any(u in low[m.end():m.end()+40] for u in PRODUCT_HINTS)
        lead_ok = text[m.start()] in PRODUCT_EMOJI or text[m.start()] == "#"

        if tail_ok or lead_ok:
            if name not in seen:
                name = pattern.sub("",name)
                products.append(name.replace("\n", ""))
                seen.add(name)

    return {"type": "product", "products": products}

# for CheMed123 channel

def extract_chemed_products(text: str) -> list[str]:
    """
    Rules‑based extractor for Che‑Med123 posts.
    Returns product names (Latin script) or [] if none were found.
    No ML, only regex + small stop‑lists.
    """

    # ------------------------------------------------------------------
    # 1.  candidate finder  – up to 4 capitalised tokens (allows digits,
    #     hyphen, %, parentheses, & and single‑letter tokens like 'C').
    # ------------------------------------------------------------------
    _PROD_RE = re.compile(
        r"""
        (?:^|[\s🌞🔵🟠⭐️💊✅✔️🔥✨📦📌👉#\*•-])      # line start or common bullet/emoji
        \s*
        ([A-Z][A-Za-z0-9()/%&\-']*                 # first token
           (?:\s+[A-Z0-9][A-Za-z0-9()/%&\-']*){0,3})   # plus ≤3 more
        """,
        re.VERBOSE,
    )

    # ------------------------------------------------------------------
    # 2. words/phrases that are *never* products in this channel
    # ------------------------------------------------------------------
    _BLACKLIST = {
        "Notice", "Dear", "Customers", "Che", "Med", "Che-Med",
        "Call", "Center", "Follow", "Order", "Buy", "Get", "Due",
        "Delivery", "Service", "Services", "Trivia", "Source",
        "Pharmaceutical", "Industry", "Supports", "Product", "Products",
        "Supplements", "Supplement", "Assistant", "Website",
        "Che-Med",
        "Brand",
        "First",
        "Elastic",
        "Are",
        "Real-Time Inventory Tracking",
        "Expiry Alerts",
        "Seamless Collaboration",
        "Increased Efficiency",
        "Import)",
        "Aug-27Bulk",
        "Dec-27",
        "A)",
        "B)",
        "Multiple",
        "Also Available",
        "Non-drowsy",
        "VivaMedPharma",
        "StockAlert",
        "PharmaEthiopia",
        "QualityFirst",
        "HealthSolutions",
        "AllergyRelief",
        "SkinCareEssentials",
        "Size16",
        "NEW ARRIVALSALMAZ GIRMA",
        "Tounge",
        "Join",
        "Ns",
        "Rl",
        "Himed Sales091 160",
        "Tikvah Sales",
        "Jul-27",
        "VivaMed Pharma",
        "High Quality",
        "Available Now",
        "Telegram",
        "IMPORTEgens",
        "Pharmacy",
        "Track",
        "Get",
        "Streamline",
        "Boost"
    }

    pattern = re.compile(
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{1,2}(?:Bulk)?\b",
    re.I
    )

    # ------------------------------------------------------------------
    # 3.  keep a hit only if the 50‑char window *after* it contains a
    #     giveaway keyword (mg, supplement, etc.)  – this filters out
    #     most random capitalised words in Amharic sentences.
    # ------------------------------------------------------------------
    _CONTEXT = {
        "mg", "ml", "mcg", "IU", "susp", "caps", "capsule", "tablet",
        "tab", "inj", "syrup", "drop", "cream", "ointment", "gel",
        "supplement", "product", "relief"
    }

    if isinstance(text, tuple):
        flat = text[0].replace("\n", " ")           # single‑line scan
    else:
        flat = text.replace("\n", " ")   
    hits, seen = [], set()
    for m in _PROD_RE.finditer(flat):
        name = m.group(1).rstrip(",;:").strip()

        if name in _BLACKLIST or len(name) < 2:
            continue

        # context test
        tail = flat[m.end(): m.end() + 50].lower()
        if not any(k in tail for k in _CONTEXT):
            continue

        # deduplicate while preserving order
        if name not in seen:
            name = pattern.sub("",name)
            hits.append(name)
            seen.add(name)

    return hits

def extract_channel_products(text: str, channel_name: str) -> list[str]:
    """
    Routes product name extraction based on channel-specific logic.
    
    Args:
        text (str or tuple): Message text from telegram_messages
        channel_name (str): Source channel name (e.g. CheMed123)
    
    Returns:
        List[str]: Extracted product names
    """

    if channel_name.lower() == "chemed123":
        return extract_chemed_products(text)

    elif channel_name.lower() == "tikvahpharma":
        result = classify_message(text)
        return result["products"] if result["type"] == "product" else []

    elif channel_name.lower() == "lobelia4cosmetics":
        if isinstance(text, tuple):
            text = text[0]
        first_line = text.split('\n', 1)[0]
        return [first_line.strip()] if first_line.strip() else []

    # Optional fallback
    return []

def extract_price(text: str) -> List[float]:
    # Normalize text
    text = text.lower().replace(",", "")  # removes commas for easier parsing

    # Combined pattern to match various price formats
    price_patterns = [
        r"price[:\s]*([\d]+)",                           # Price 5000
        r"([\d]+)\s*(birr|etb|ብር)",                      # 5000 birr
        r"([\d]+)[–\-~]\s*([\d]+)\s*(birr|etb|ብር)",       # 70 - 500 birr
        r"💵?\s*([\d]+)\s*ብር"                            # 💵700ብር
    ]

    results = []
    for pattern in price_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Handle different tuple shapes 
            if isinstance(match, tuple):
                # Range like 70-500
                nums = [int(val) for val in match if val.isdigit()]
                results.extend(nums)
            else:
                results.append(float(match))

    return list(set(results))  # de-duplicate


def extract_health_flag(text: str) -> bool:
    """
    Flags whether a Telegram post is health-related based on English and Amharic keywords.
    """
    if isinstance(text, tuple):
        text = text[0]

    # Normalize text (lowercase + preserve Amharic)
    text = text.lower()
    
    # Remove symbols but keep Amharic and Latin letters
    text = re.sub(r"[^\w\s\u1200-\u137F]", " ", text)  # keep Amharic unicode range
    text = re.sub(r"\s+", " ", text)  # collapse extra spaces

    # English keywords
    eng_keywords = {
        "medicine", "medical", "pharmacy", "pharmacist", "clinic", "hospital",
        "doctor", "treatment", "therapy", "medication", "healthcare", "drug",
        "prescription", "injection", "syrup", "tablet", "capsule", "ointment",
        "vitamin", "supplement", "ml", "mg", "painkiller", "antibiotic", "delivery", 
        "health", "contraceptive", "pregnancy", "fertility", "immune", "pain relief"
    }

    # Amharic keywords (expand this as needed)
    amharic_keywords = {
        "መድሃኒት", "ህክምና", "ሐኪም", "መከላከያ", "እንቅስቃሴ", "ክሊኒክ", "ኦስፒታል",
        "ፋርማሲ", "የእርግዝና", "መድሀኒት", "የጤና", "ድርብ ነቃቃ", "አንቲባዮቲክ", "ቫይታሚን",
        "ህክምና", "ሕክምና", "ጤና", "መድሃኒት ቤት", "ሴቶች ጤና", "የህፃናት"
    }

    # Known English health product/brand names
    health_products = {
        "wellman", "seven seas", "centrum", "pregnacare", "feroglobin", "vitabiotics",
        "amoxicillin", "paracetamol", "diclofenac", "neurobion", "omeprazole",
        "blackmores", "glucophage", "zincovit", "ors", "iron supplement", "lobelia"
    }

    all_keywords = eng_keywords.union(health_products).union(amharic_keywords)

    return any(re.search(rf"\b{re.escape(word)}\b", text) for word in all_keywords)