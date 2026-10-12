import json
from extract import extract_listing

tests = [
    "Splendor 100, 10 saal purani, 60000 km chali hai, Jaipur, 2nd owner, 25k mein",
    "bullet 350 3rd owner Delhi 12 yrs old, 85,000 kms asking 90k",
    "Harley Davidson Street 750, 5 years, 12000 km, Bangalore, 4 lakh",
    "KTM Duke 390, 1 year old, 3000 km, Chandigarh, first owner, 2.5 lakh",
    "Honda Shine, 5 years, 25 thousand km, Delhi, price 40k",
    "selling my bike, please call me",
]

for t in tests:
    print(t)
    print(json.dumps(extract_listing(t), indent=2))
    print("-" * 40)