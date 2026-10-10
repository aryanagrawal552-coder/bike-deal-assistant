import json
import re
from llm import ask

SYSTEM_PROMPT = """You extract used-bike listing details from a user's message.
Return ONLY a JSON object with exactly these keys:
brand, age, kms_driven, power, city, owner, listed_price

Rules:
- brand: one of Bajaj, Benelli, BMW, Ducati, Harley-Davidson, Hero, Honda, Hyosung, Ideal, Indian, Jawa, KTM, Kawasaki, LML, Mahindra, MV, Rajdoot, Royal Enfield, Suzuki, TVS, Triumph, Yamaha, Yezdi. Otherwise null.
- age: number of years, as a number.
- kms_driven: kilometres as a plain number (20k means 20000).
- power: engine size in cc, as a number.
- city: city name as text.
- owner: one of "First Owner", "Second Owner", "Third Owner", "Fourth Owner Or More".
- listed_price: asking price in rupees as a plain number (1.2 lakh means 120000).
- If a value is not stated in the message, use null. Never guess.
No explanation, no markdown, only the JSON object."""


def extract_listing(text):
    raw = ask(SYSTEM_PROMPT, text)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Model did not return JSON: {raw}")
    return json.loads(match.group())