import json
from extract import extract_listing
from validate import validate, guess_brand
from predict import predict_range, get_verdict
from llm import ask

EXPLAIN_PROMPT = """You explain a used-bike price check to a buyer or seller in 2-3 short sentences.
Use ONLY the numbers and facts in the JSON you are given. Never invent prices, percentages, or reasons.
Mention the fair range, and the verdict if there is one.
If 'unsure' is true, say the estimate is less reliable for this kind of bike.
If there are warnings, mention them briefly.
Write rupee amounts with commas. Plain text only.
Do not mention warnings if there are none."""

FIELD_QUESTIONS = {
    "brand": "Which brand is the bike?",
    "age": "How many years old is it?",
    "kms_driven": "How many kilometres has it run?",
    "power": "What is the engine size in cc?",
    "city": "Which city is it in?",
    "owner": "Is it a first, second, third or fourth owner bike?",
}

FIELDS = ["brand", "age", "kms_driven", "power", "city", "owner", "listed_price"]


def merge_listings(previous, new):
    merged = dict(previous or {})
    for key in FIELDS:
        if new.get(key) is not None:
            merged[key] = new[key]
        else:
            merged.setdefault(key, None)
    return merged


def num(x):
    if x is None:
        return None
    return int(x) if float(x).is_integer() else x


def analyze(text, previous=None):
    new = extract_listing(text)

    new_brand = new.get("brand") or guess_brand(text)
    if previous and new_brand and new_brand != previous.get("brand"):
        previous = None  # a different bike, so start fresh

    merged = merge_listings(previous, new)
    listing, missing, warnings = validate(merged, text)

    if missing:
        return {
            "status": "need_more_info",
            "questions": [FIELD_QUESTIONS[f] for f in missing],
            "listing": listing,
        }

    point, lower, upper, unsure = predict_range(listing)
    verdict = get_verdict(listing.get("listed_price"), lower, upper)

    facts = {
        "bike": f"{listing['brand']}, {num(listing['age'])} years old, {num(listing['kms_driven'])} km, "
                f"{num(listing['power'])}cc, {listing['city']}, {listing['owner']}",
        "estimated_price": round(point),
        "fair_range": [round(lower), round(upper)],
        "listed_price": num(listing.get("listed_price")),
        "verdict": verdict,
        "unsure": unsure,
        "warnings": warnings,
    }
    explanation = ask(EXPLAIN_PROMPT, json.dumps(facts))

    return {
        "status": "ok",
        "facts": facts,
        "explanation": explanation,
        "listing": listing,
    }