import streamlit as st
import datetime
import random


if "logs" not in st.session_state:
    st.session_state.logs = []


def run_task(task_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outcome = random.choice(["✅ Success", "⚠️ Warning", "❌ Failed"])
    link = f"https://example.com/output/{random.randint(1000, 9999)}"
    log_entry = {
        "task": task_name,
        "status": outcome,
        "time": timestamp,
        "link": link }
    st.session_state.logs.append(log_entry)
    return log_entry


st.title("🕌 Halal Control Panel v1.0")

st.markdown("""
Welcome, Puchu 👋 This is your personal halal income automation dashboard.
Click a button below to trigger a task. Logs will appear below.
""")


col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Run Little Ummahs"):
        log = run_task("Little Ummahs Video")
        st.success(f"Task completed: {log['status']}")
        st.markdown(f"[🔗 View Output]({log['link']})")

with col2:
    if st.button("▶️ Run Sunnah Mindset"):
        log = run_task("Sunnah Mindset Video")
        st.success(f"Task completed: {log['status']}")
        st.markdown(f"[🔗 View Output]({log['link']})")

st.subheader("📜 Activity Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"{log['time']} — {log['task']} → {log['status']} 🔗")
else: st.info("No logs yet. Start a task to see results.")

