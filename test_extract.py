import json
from extract import extract_listing

tests = [
    "Honda Shine 125cc, 4 years old, 20,000 km, Delhi, first owner, asking 45000",
    "second owner Royal Enfield Classic 350 from Pune, ran 15k km, 3 yrs old, wants 1.2 lakh",
    "Yamaha R15, Mumbai, 2 years, 8000 km",
]

for t in tests:
    print(t)
    print(json.dumps(extract_listing(t), indent=2))
    print("-" * 40)