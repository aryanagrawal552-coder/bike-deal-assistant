from predict import predict_range, get_verdict

listing = {
    "brand": "Harley-Davidson",
    "city": "Bangalore",
    "owner": "Third Owner",
    "age": 5,
    "kms_driven": 1500,
    "power": 600,
}

point, lower, upper, unsure = predict_range(listing)
print(f"Predicted: {point:,.0f}  Range: {lower:,.0f} - {upper:,.0f}  Unsure: {unsure}")

for label, price in [("low", lower * 0.8), ("mid", point), ("high", upper * 1.2)]:
    print(label, f"{price:,.0f}", "->", get_verdict(price, lower, upper))