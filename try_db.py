import db

db.DB_PATH = "test_history.db"   # use a throwaway file, not the real one
db.init_db()

db.save_query("Honda Shine, Delhi", {
    "status": "ok",
    "facts": {"estimated_price": 39807, "fair_range": [30711, 50926],
              "listed_price": 45000, "verdict": "fair", "unsure": False},
})
db.save_query("Yamaha R15, Mumbai", {"status": "need_more_info"})

for row in db.get_history():
    print(row)