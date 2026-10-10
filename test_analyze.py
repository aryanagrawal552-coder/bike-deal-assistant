import json
from analyze import analyze

tests = [
    "Honda Shine 125cc, 4 years old, 20,000 km, Delhi, first owner, asking 45000",
    "Yamaha R15, Mumbai, 2 years, 8000 km",
    "Harley Davidson, 5 years, 12000 km, Delhi, first owner, 150cc, asking 1 lakh",
]

for t in tests:
    print(t)
    print(json.dumps(analyze(t), indent=2, ensure_ascii=False))
    print("-" * 50)