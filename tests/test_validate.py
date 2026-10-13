from validate import validate, guess_brand


def base():
    return {"brand": "Honda", "age": 4, "kms_driven": 20000, "power": 125,
            "city": "Delhi", "owner": "First Owner", "listed_price": 45000}


def test_clean_listing_has_no_issues():
    listing, missing, warnings = validate(base(), "Honda Shine")
    assert missing == []
    assert warnings == []


def test_guess_brand_from_model_name():
    assert guess_brand("Splendor 100, Jaipur") == "Hero"
    assert guess_brand("some unknown bike") is None


def test_brand_filled_from_model_name_when_missing():
    data = base()
    data["brand"] = None
    listing, _, _ = validate(data, "Splendor 100 for sale")
    assert listing["brand"] == "Hero"


def test_unknown_city_becomes_other():
    data = base()
    data["city"] = "Chandigarh"
    listing, _, _ = validate(data, "x")
    assert listing["city"] == "Other"


def test_city_match_ignores_case():
    data = base()
    data["city"] = "delhi"
    listing, _, _ = validate(data, "x")
    assert listing["city"] == "Delhi"


def test_missing_fields_are_reported():
    data = base()
    data["power"] = None
    data["owner"] = None
    _, missing, _ = validate(data, "x")
    assert missing == ["power", "owner"]


def test_unrealistic_km_per_year_warns():
    data = base()
    data["kms_driven"] = 400000
    data["age"] = 3
    _, _, warnings = validate(data, "x")
    assert any("km per year" in w for w in warnings)


def test_premium_brand_with_small_engine_warns():
    data = base()
    data["brand"] = "Harley-Davidson"
    data["power"] = 150
    _, _, warnings = validate(data, "x")
    assert any("250cc" in w for w in warnings)


def test_input_dictionary_is_not_modified():
    data = base()
    data["city"] = "Chandigarh"
    validate(data, "x")
    assert data["city"] == "Chandigarh"
    
def test_invalid_owner_is_treated_as_missing():
    data = base()
    data["owner"] = "1st owner"
    listing, missing, _ = validate(data, "x")
    assert "owner" in missing
    assert listing["owner"] is None