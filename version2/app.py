import os, requests, streamlit as st
from dotenv import load_dotenv
from game_engine import GameEngine
load_dotenv()
st.set_page_config(page_title="Subsea Escape Room V2",page_icon="🌊")
st.title("🌊 Subsea Research Station — Version 2")
st.caption("Python-validated state · optional Gemini narration")
if "engine" not in st.session_state: st.session_state.engine=GameEngine()
if "history2" not in st.session_state: st.session_state.history2=[]
engine=st.session_state.engine
s=engine.state
def narrate(result):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key: return result
    model=os.getenv("GEMINI_MODEL","gemini-2.0-flash")
    prompt="Rewrite this validated result as one concise immersive sentence. Do not change facts or state: "+result
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    try:
        r=requests.post(url,json={"contents":[{"parts":[{"text":prompt}]}],
            "generationConfig":{"temperature":0.2,"maxOutputTokens":120}},timeout=20)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception: return result
with st.sidebar:
    st.subheader("Game state")
    st.write("Inventory",sorted(s.inventory) if s.inventory else "Empty")
    st.write("Sonar clue","Found" if s.sonar else "Missing")
    st.write("Cabinet","Open" if s.cabinet else "Locked")
    st.write("Console","Calibrated" if s.console else "Inactive")
    st.write("Oxygen","SAFE" if s.oxygen_safe else "Unstable")
    st.write("Hatch","Unlocked" if s.hatch_unlocked else "Locked")
    st.write("Escaped",s.escaped)
    if st.button("Restart game"):
        engine.reset(); st.session_state.history2=[]; st.rerun()
for m in st.session_state.history2:
    with st.chat_message(m["role"]): st.write(m["content"])
q=st.chat_input("Describe an action…")
if q:
    st.session_state.history2.append({"role":"user","content":q})
    result=engine.handle(q)
    st.session_state.history2.append({"role":"assistant","content":narrate(result)})
    st.rerun()
st.info("Goal: discover the cabinet code, collect the key and card, calibrate the console, stabilise oxygen and escape.")
