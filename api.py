import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from analyze import analyze

logger = logging.getLogger("api")
app = FastAPI(title="Bike Deal Assistant API")


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze_listing(request: AnalyzeRequest):
    try:
        return analyze(request.text)
    except ValueError:
        raise HTTPException(status_code=422, detail="Could not understand that listing. Try rephrasing it.")
    except Exception:
        logger.exception("analyze failed")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")