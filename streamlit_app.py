import streamlit as st
import datetime
import random

# Initialize logs & scripts
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {
        "Little Ummahs": "",
        "Sunnah Mindset": ""
    }

def run_task(task_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outcome = random.choice(["✅ Success", "⚠️ Warning", "❌ Failed"])
    link = f"https://example.com/output/{random.randint(1000, 9999)}"
    log_entry = {
        "task": task_name,
        "status": outcome,
        "time": timestamp,
        "link": link
    }
    st.session_state.logs.append(log_entry)
    return log_entry

st.set_page_config(page_title="Halal Control Panel", layout="wide")
st.title("🕌 Halal Control Panel v1.5")

st.markdown("""
Welcome, **Puchu** 👋  
This is your mobile-friendly control panel for automating halal content generation.
""")

tab1, tab2 = st.tabs(["🎬 Little Ummahs", "📖 Sunnah Mindset"])

with tab1:
    st.subheader("▶️ Little Ummahs Controls")
    if st.button("Run Little Ummahs Task"):
        log = run_task("Little Ummahs Video")
        st.success(f"Task completed: {log['status']}")
        st.markdown(f"[🔗 View Output]({log['link']})")

    st.text_area("✍️ Script for Little Ummahs",
                 value=st.session_state.scripts["Little Ummahs"],
                 height=200,
                 key="script_ummahs")
    
    if st.button("💾 Save Little Ummahs Script"):
        st.session_state.scripts["Little Ummahs"] = st.session_state.script_ummahs
        st.success("Script saved!")

with tab2:
    st.subheader("▶️ Sunnah Mindset Controls")
    if st.button("Run Sunnah Mindset Task"):
        log = run_task("Sunnah Mindset Video")
        st.success(f"Task completed: {log['status']}")
        st.markdown(f"[🔗 View Output]({log['link']})")

    st.text_area("✍️ Script for Sunnah Mindset",
                 value=st.session_state.scripts["Sunnah Mindset"],
                 height=200,
                 key="script_sunnah")
    
    if st.button("💾 Save Sunnah Script"):
        st.session_state.scripts["Sunnah Mindset"] = st.session_state.script_sunnah
        st.success("Script saved!")

st.divider()
st.subheader("📜 Activity Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['task']}** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet. Click a run button to test a task.")
