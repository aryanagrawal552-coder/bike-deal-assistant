from predict import predict_range, get_verdict

LISTINGS = [
    {"brand": "Honda", "city": "Delhi", "owner": "First Owner", "age": 4, "kms_driven": 20000, "power": 125},
    {"brand": "Royal Enfield", "city": "Pune", "owner": "Second Owner", "age": 3, "kms_driven": 15000, "power": 350},
    {"brand": "Harley-Davidson", "city": "Bangalore", "owner": "Third Owner", "age": 5, "kms_driven": 1500, "power": 600},
]


def test_verdict_labels():
    assert get_verdict(30000, 40000, 50000) == "underpriced"
    assert get_verdict(45000, 40000, 50000) == "fair"
    assert get_verdict(60000, 40000, 50000) == "overpriced"
    assert get_verdict(None, 40000, 50000) is None


def test_verdict_boundaries_count_as_fair():
    assert get_verdict(40000, 40000, 50000) == "fair"
    assert get_verdict(50000, 40000, 50000) == "fair"


def test_range_always_contains_the_estimate():
    for listing in LISTINGS:
        point, lower, upper, _ = predict_range(listing)
        assert lower <= point <= upper