import os
import requests
import streamlit as st


def get_api_url():
    try:
        base = st.secrets["API_URL"]
    except Exception:
        base = os.getenv("API_URL", "http://127.0.0.1:8000")
    return base.rstrip("/") + "/analyze"


API_URL = get_api_url()

VERDICT_LABEL = {
    "underpriced": "🟢 Underpriced, possibly a good deal",
    "fair": "🟡 Fair price",
    "overpriced": "🔴 Overpriced",
}


def format_result(data):
    if data["status"] == "need_more_info":
        questions = "\n".join(f"- {q}" for q in data["questions"])
        return f"I need a bit more information:\n\n{questions}"

    f = data["facts"]
    parts = [
        f"**Estimated price:** ₹{f['estimated_price']:,}",
        f"**Fair range:** ₹{f['fair_range'][0]:,} to ₹{f['fair_range'][1]:,}",
    ]
    if f["verdict"]:
        parts.append(f"**Verdict:** {VERDICT_LABEL[f['verdict']]}")
    if f["unsure"]:
        parts.append("⚠️ The estimate is less reliable for this kind of bike.")
    for w in f["warnings"]:
        parts.append(f"⚠️ {w}")
    parts.append(data["explanation"])
    return "\n\n".join(parts)


st.set_page_config(page_title="Bike Deal Assistant", page_icon="🏍️")
st.title("🏍️ Bike Deal Assistant")
st.caption("Describe a used bike listing in plain English and check whether the price is fair.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_text" not in st.session_state:
    st.session_state.pending_text = ""

if st.sidebar.button("New listing"):
    st.session_state.messages = []
    st.session_state.pending_text = ""
    st.rerun()

user_text = st.chat_input("e.g. Honda Shine 125cc, 4 years old, 20,000 km, Delhi, first owner, asking 45000")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    combined = (st.session_state.pending_text + " " + user_text).strip()

    with st.spinner("Analyzing..."):
        try:
            r = requests.post(API_URL, json={"text": combined}, timeout=90)
            if r.status_code == 200:
                data = r.json()
                reply = format_result(data)
                st.session_state.pending_text = combined if data["status"] == "need_more_info" else ""
            else:
                detail = r.json().get("detail")
                reply = detail if isinstance(detail, str) else "Please enter a longer description of the bike."
        except requests.exceptions.Timeout:
            reply = "The server is waking up from sleep, which can take up to a minute. Please send your message again."
        except requests.exceptions.RequestException:
            reply = "I can't reach the backend. Is the API server running?"

    st.session_state.messages.append({"role": "assistant", "content": reply})

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])