import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from analyze import analyze
from db import init_db, save_query, get_history

logger = logging.getLogger("api")
app = FastAPI(title="Bike Deal Assistant API")
init_db()


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_listing(request: AnalyzeRequest):
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
def history(limit: int = Query(20, ge=1, le=100)):
    return get_history(limit)