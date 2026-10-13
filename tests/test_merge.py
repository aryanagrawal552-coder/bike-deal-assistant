from analyze import merge_listings


def test_new_values_override_old_ones():
    old = {"brand": "Honda", "age": 4, "listed_price": 45000}
    new = {"brand": None, "age": None, "listed_price": 80000}
    merged = merge_listings(old, new)
    assert merged["listed_price"] == 80000
    assert merged["brand"] == "Honda"
    assert merged["age"] == 4