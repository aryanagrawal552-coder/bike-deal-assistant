import re

SUPPORTED_BRANDS = [
    "Bajaj", "Benelli", "BMW", "Ducati", "Harley-Davidson", "Hero", "Honda",
    "Hyosung", "Ideal", "Indian", "Jawa", "KTM", "Kawasaki", "LML", "Mahindra",
    "MV", "Rajdoot", "Royal Enfield", "Suzuki", "TVS", "Triumph", "Yamaha", "Yezdi",
]

SUPPORTED_CITIES = [
    "Ahmedabad", "Bangalore", "Chennai", "Delhi", "Faridabad", "Ghaziabad",
    "Gurgaon", "Hyderabad", "Jaipur", "Kolkata", "Ludhiana", "Mumbai",
    "Noida", "Pune", "Thane",
]

# Unambiguous model names only. Avoid words like "classic" because
# Yezdi, Jawa and Royal Enfield all have one.
MODEL_TO_BRAND = {
    "splendor": "Hero", "passion": "Hero", "glamour": "Hero",
    "shine": "Honda", "unicorn": "Honda",
    "pulsar": "Bajaj", "discover": "Bajaj", "platina": "Bajaj", "avenger": "Bajaj",
    "apache": "TVS",
    "r15": "Yamaha", "fz": "Yamaha",
    "duke": "KTM",
    "bullet": "Royal Enfield", "thunderbird": "Royal Enfield", "himalayan": "Royal Enfield",
}

PREMIUM_BRANDS = ["Ducati", "Harley-Davidson", "Triumph", "MV", "Indian", "BMW", "Kawasaki"]

REQUIRED = ["brand", "age", "kms_driven", "power", "city", "owner"]


def guess_brand(text):
    t = text.lower()
    for keyword, brand in MODEL_TO_BRAND.items():
        if re.search(rf"\b{re.escape(keyword)}\b", t):
            return brand
    return None


def validate(listing, original_text):
    listing = dict(listing)
    warnings = []

    if listing.get("brand") not in SUPPORTED_BRANDS:
        listing["brand"] = guess_brand(original_text)

    if listing.get("city"):
        match = next((c for c in SUPPORTED_CITIES if c.lower() == str(listing["city"]).lower()), None)
        listing["city"] = match if match else "Other"

    missing = [f for f in REQUIRED if listing.get(f) is None]

    age, kms, power = listing.get("age"), listing.get("kms_driven"), listing.get("power")

    if age is not None and not (1 <= age <= 30):
        warnings.append("Age is outside 1-30 years, so the estimate may be unreliable.")
    if age and kms is not None and kms / age > 50000:
        warnings.append("That's over 50,000 km per year, which looks unrealistic.")
    if power is not None and power < 100:
        warnings.append("Engine size is below 100cc, which is outside the data the model learned from.")
    if power is not None and listing.get("brand") in PREMIUM_BRANDS and power < 250:
        warnings.append(f"{listing['brand']} bikes are rarely under 250cc, so please check the engine size.")

    return listing, missing, warnings