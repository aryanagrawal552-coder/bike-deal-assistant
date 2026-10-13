# 🏍️ Bike Deal Assistant

Describe a used bike listing in plain English and find out whether the asking price is fair. An LLM reads the message, validation code checks it, and trained XGBoost models estimate a fair price range.

🔗 **[Try the live app](https://bike-deal-assistant-jus5qrjykv6gaypupknybb.streamlit.app/)** · **[API docs](https://bike-deal-assistant.onrender.com/docs)**

> Both run on free hosting and sleep when idle, so the first request can take up to a minute.

Built on top of my earlier project, [Bike Resale Price Predictor](https://github.com/aryanagrawal552-coder/bike-price-prediction), which trained the models used here.

## Example

> **You:** Yamaha R15, Mumbai, 2 years, 8000 km
>
> **Assistant:** I need a bit more information: What is the engine size in cc? Is it a first, second, third or fourth owner bike?
>
> **You:** 155cc, first owner, asking 1.4 lakh
>
> **Assistant:** Estimated price ₹95,955, fair range ₹74,296 to ₹126,604. Verdict: overpriced, because the listed price of ₹140,000 is above the range.

**Follow-ups work too.** The app remembers the bike you described:

> **You:** is 80000 fair?
>
> **Assistant:** Same bike, same fair range, but ₹80,000 is above it, so it looks overpriced.

## How it works

```
message → LLM extraction → merge with remembered listing → validation → XGBoost models → verdict → LLM explanation → chat UI
```

- **The LLM never calculates prices.** It turns text into structured fields and puts results into words. Every number comes from the trained models.
- **Missing details are never guessed.** Unstated fields become `null`, and the app asks follow-up questions.
- **Exact rules live in code, not in the prompt.** Brand lookup from model names (e.g. Splendor → Hero), city mapping, and sanity checks (km per year, engine size for premium brands).
- **Conversation memory in code, not in the LLM.** The app keeps the listing as structured fields and merges each new message into it, so a follow-up like "what if the price is 80000?" updates one field. Naming a different brand starts a fresh listing. The client sends the previous listing back with each request, so the API validates it with Pydantic before use.
- **Range safeguard.** The point model and the 10th/90th percentile models are trained separately and can disagree on unusual bikes. The range is widened to include the estimate, and the result is flagged as less reliable.
- **Backend:** FastAPI with Pydantic request validation, separate handling of bad input (422) and server errors (500), an LLM timeout, a global rate limit, SQLite query history, and an admin-key-protected `/history` endpoint.

## Tech stack

Python, FastAPI, Pydantic, Streamlit, Groq API, XGBoost, scikit-learn, pandas, SQLite, pytest. Hosted on Render (API) and Streamlit Community Cloud (frontend).

## Run locally

```bash
git clone https://github.com/aryanagrawal552-coder/bike-deal-assistant.git
cd bike-deal-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements-api.txt
pip install -r requirements.txt
```

Create a `.env` file with your own keys:

```
GROQ_API_KEY=your-groq-key
ADMIN_KEY=any-long-random-string
```

Then run the API and the frontend in two terminals:

```bash
uvicorn api:app --reload
streamlit run frontend.py
```

Run the tests with `python -m pytest -q`. The 15 tests cover validation, prediction logic, conversation merging and the database, and make no LLM calls.

## Limitations

- The models were trained on a 2021 public dataset, so prices reflect that period.
- Only 23 brands and 15 major cities are modeled. Other cities are grouped as "Other".
- Estimates for rare or premium bikes are less reliable. The fair range covered about 73% of test listings against an 80% target.
- LLM extraction was checked by hand on a small set of phrasings, not measured at scale, and it can misread unusual wording.
- If the input looks suspicious (e.g. a 150cc Harley-Davidson), a warning is shown, but a verdict is still given and shouldn't be trusted.
- The reset between bikes relies on recognizing a new brand. Switching to another bike without naming a recognized brand can carry over details from the previous one, so the sidebar shows what the app currently remembers.
- On free hosting the services sleep when idle, and the SQLite history resets when the API restarts.

## Future improvements

- Hide or soften the verdict when inputs trigger warnings
- Build a labeled set of test messages to measure extraction accuracy
- Refresh the data with newer listings
- Containerize with Docker
