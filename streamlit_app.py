import streamlit as st
import datetime
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "logs" not in st.session_state:
    st.session_state.logs = []

def generate_script(channel_name):
    prompt = (
        "Create a short, authentic Islamic script for children aged 5–10 with Quran/Hadith references."
        if channel_name == "Little Ummahs"
        else "Write a motivational Islamic script for youth based on Quran and authentic Sunnah."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Islamic speaker and educator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"GPT Error: {e}")
        return "❌ Script generation failed."

def run_task(task_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script = generate_script(task_name)
    log_entry = {
        "task": task_name,
        "status": "✅ Script generated",
        "time": timestamp,
        "link": "-",
        "script": script
    }
    st.session_state.logs.append(log_entry)
    return log_entry

st.title("🕌 Halal Control Panel v1.0")

st.markdown("""
Welcome, Puchu 👋 This is your halal income automation dashboard.
Click a button to generate a full Islamic video script using AI.
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Run Little Ummahs"):
        log = run_task("Little Ummahs")
        st.success(log["status"])
        st.markdown(f"### 📜 Script Output\n{log['script']}")

with col2:
    if st.button("▶️ Run Sunnah Mindset"):
        log = run_task("Sunnah Mindset")
        st.success(log["status"])
        st.markdown(f"### 📜 Script Output\n{log['script']}")

st.subheader("📜 Activity Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"**{log['time']}** — *{log['task']}* → {log['status']}")
else:
    st.info("No logs yet. Click a button above to generate a script.")
