import db


def test_save_and_read_back(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()

    db.save_query("Honda Shine, Delhi", {
        "status": "ok",
        "facts": {"estimated_price": 39807, "fair_range": [30711, 50926],
                  "listed_price": 45000, "verdict": "fair", "unsure": False},
    })
    db.save_query("Yamaha R15, Mumbai", {"status": "need_more_info"})

    rows = db.get_history()
    assert len(rows) == 2
    assert rows[0]["input_text"] == "Yamaha R15, Mumbai"
    assert rows[0]["estimated_price"] is None
    assert rows[1]["verdict"] == "fair"
    assert rows[1]["unsure"] == 0