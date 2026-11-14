import os, requests, streamlit as st
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="Subsea Escape Room V1", page_icon="🌊")
st.title("🌊 Subsea Research Station — Version 1")
st.caption("LLM-led game master")
INTRO = """You are trapped in an underwater research station. Explore five objects: sonar panel,
specimen cabinet, control console, oxygen valve and escape hatch. Find clues, collect items and escape.
Solution: sonar reveals 2741; cabinet gives magnetic key + calibration card; console reveals 6308;
set oxygen to SAFE; use key and enter 6308."""
SYSTEM = """You are a consistent game master for a subsea research station escape room.
Sonar panel reveals 2741. Entering 2741 at specimen cabinet gives magnetic key and calibration card.
Using calibration card at control console reveals 6308. Oxygen valve must be SAFE. Magnetic key and
6308 are required at escape hatch. Do not invent objects or alter puzzle solution. Give hints gradually."""
def gemini(history):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key: return None
    model=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
    contents=[{"role":"user" if m["role"]=="user" else "model","parts":[{"text":m["content"]}]} for m in history]
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    try:
        r=requests.post(url,json={"systemInstruction":{"parts":[{"text":SYSTEM}]},"contents":contents,
                                  "generationConfig":{"temperature":0.4,"maxOutputTokens":350}},timeout=25)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception: return "Gemini is unavailable. Try an action on one of the five station objects."
def fallback(t):
    t=t.lower()
    if any(x in t for x in ["sonar","radar","ping","scan"]):
        return "Four sonar pings appear in sequence: 2, 7, 4, 1. The specimen cabinet has a keypad."
    if "2741" in t: return "The cabinet opens. You collect a magnetic key and a calibration card."
    if any(x in t for x in ["cabinet","specimen"]): return "The specimen cabinet needs a four-digit code. Inspect the sonar panel."
    if any(x in t for x in ["console","calibration","control"]): return "The calibration card activates the console. It displays the hatch code 6308."
    if any(x in t for x in ["oxygen","valve","pressure"]): return "You turn the oxygen valve until the gauge reads SAFE."
    if any(x in t for x in ["hatch","door","6308","escape"]): return "The hatch needs the magnetic key, SAFE oxygen pressure and code 6308."
    if "hint" in t or "help" in t: return "Inspect the sonar panel first. Its four pings form the cabinet code."
    return "Try inspecting the sonar panel, specimen cabinet, control console, oxygen valve or escape hatch."
st.info(INTRO)
if "history1" not in st.session_state: st.session_state.history1=[]
for m in st.session_state.history1:
    with st.chat_message(m["role"]): st.write(m["content"])
q=st.chat_input("Describe your action…")
if q:
    st.session_state.history1.append({"role":"user","content":q})
    answer=gemini(st.session_state.history1) or fallback(q)
    st.session_state.history1.append({"role":"assistant","content":answer})
    st.rerun()
if st.button("Restart V1"):
    st.session_state.history1=[]; st.rerun()
