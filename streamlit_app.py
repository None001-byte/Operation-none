import streamlit as st
import datetime

# Initialize task state and logs
if "task_status" not in st.session_state:
    st.session_state.task_status = {
        "Little Ummahs": False,
        "Sunnah Mindset": False
    }

if "logs" not in st.session_state:
    st.session_state.logs = []

st.title("🕌 Halal Control Panel v1.1 – Task Tracker")

st.markdown("Track your daily progress for each YouTube channel. All actions are logged. More automation coming soon.")

today = datetime.date.today().strftime("%Y-%m-%d")

col1, col2 = st.columns(2)

# Task tracker for Little Ummahs
with col1:
    st.subheader("📺 Little Ummahs")
    if not st.session_state.task_status["Little Ummahs"]:
        if st.button("✅ Mark Little Ummahs as Done"):
            st.session_state.task_status["Little Ummahs"] = True
            st.session_state.logs.append({
                "channel": "Little Ummahs",
                "status": "✅ Completed",
                "date": today,
                "time": datetime.datetime.now().strftime("%H:%M:%S")
            })
            st.success("Marked as done!")
    else:
        st.info("✅ Task already marked as done for today.")

# Task tracker for Sunnah Mindset
with col2:
    st.subheader("🧠 Sunnah Mindset")
    if not st.session_state.task_status["Sunnah Mindset"]:
        if st.button("✅ Mark Sunnah Mindset as Done"):
            st.session_state.task_status["Sunnah Mindset"] = True
            st.session_state.logs.append({
                "channel": "Sunnah Mindset",
                "status": "✅ Completed",
                "date": today,
                "time": datetime.datetime.now().strftime("%H:%M:%S")
            })
            st.success("Marked as done!")
    else:
        st.info("✅ Task already marked as done for today.")

st.markdown("---")
st.subheader("📜 Daily Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(
            f"**{log['date']} {log['time']}** — {log['channel']} → {log['status']}"
        )
else:
    st.info("No tasks logged yet.")
