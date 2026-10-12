import logging
import os
import secrets
import time
from collections import deque

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

from analyze import analyze
from db import get_history, init_db, save_query

load_dotenv()

logger = logging.getLogger("api")
app = FastAPI(title="Bike Deal Assistant API")
init_db()

ADMIN_KEY = os.getenv("ADMIN_KEY")
RATE_LIMIT = 20      # max requests
RATE_WINDOW = 60     # per this many seconds, across all users
_recent = deque()


def check_rate_limit():
    now = time.time()
    while _recent and now - _recent[0] > RATE_WINDOW:
        _recent.popleft()
    if len(_recent) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="The service is busy. Please try again in a minute.")
    _recent.append(now)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_listing(request: AnalyzeRequest):
    check_rate_limit()
    try:
        result = analyze(request.text)
    except ValueError:
        raise HTTPException(status_code=422, detail="Could not understand that listing. Try rephrasing it.")
    except Exception:
        logger.exception("analyze failed")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")

    try:
        save_query(request.text, result)
    except Exception:
        logger.exception("could not save history")

    return result


@app.get("/history")
def history(limit: int = Query(20, ge=1, le=100), x_admin_key: str = Header(default="")):
    if not ADMIN_KEY or not secrets.compare_digest(x_admin_key, ADMIN_KEY):
        raise HTTPException(status_code=403, detail="Not allowed.")
    return get_history(limit)