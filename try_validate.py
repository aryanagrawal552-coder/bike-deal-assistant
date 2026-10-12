from extract import extract_listing
from validate import validate

tests = [
    "Splendor 100, 10 saal purani, 60000 km chali hai, Jaipur, 2nd owner, 25k mein",
    "Yamaha R15, Mumbai, 2 years, 8000 km",
    "KTM Duke 390, 1 year old, 3000 km, Chandigarh, first owner, 2.5 lakh",
    "Harley Davidson, 5 years, 12000 km, Delhi, first owner, 150cc",
    "Honda Shine, 3 years, 400000 km, Pune, first owner, 125cc",
]

for t in tests:
    listing, missing, warnings = validate(extract_listing(t), t)
    print(t)
    print("listing :", listing)
    print("missing :", missing)
    print("warnings:", warnings)
    print("-" * 40)