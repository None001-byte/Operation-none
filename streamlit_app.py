import streamlit as st
import datetime
import random
import openai
import os

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Simulated Logs
if "logs" not in st.session_state:
    st.session_state.logs = []

# Function to generate AI script
def generate_script(channel_name):
    prompt = ""
    if channel_name == "Little Ummahs":
        prompt = (
            "Create a short, friendly Islamic educational script for children aged 5–10. "
            "It should be authentic, simple, and based on verified hadith or Quran. Format it with emojis."
        )
    elif channel_name == "Sunnah Mindset":
        prompt = (
            "Create a motivational Islamic script focused on mindset, habits, or emotional control. "
            "Use authentic references from Quran and Sahih Hadith. Target teens and young adults."
        )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Islamic educator and motivational speaker."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating script: {e}"

# Function to simulate task execution with AI
def run_task(task_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script = generate_script(task_name)
    log_entry = {
        "task": task_name,
        "status": "✅ AI Script Generated",
        "time": timestamp,
        "link": "-",
        "script": script
    }
    st.session_state.logs.append(log_entry)
    return log_entry

# App title
st.title("🕌 Halal Control Panel v1.0")

st.markdown("""
Welcome, Puchu 👋 This is your personal halal income automation dashboard.
Click a button below to generate real Islamic video scripts with AI.
""")

# Task Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Run Little Ummahs"):
        log = run_task("Little Ummahs")
        st.success(log['status'])
        st.markdown(f"### 📜 Script Output:\n{log['script']}")

with col2:
    if st.button("▶️ Run Sunnah Mindset"):
        log = run_task("Sunnah Mindset")
        st.success(log['status'])
        st.markdown(f"### 📜 Script Output:\n{log['script']}")

# Logs Section
st.subheader("📜 Activity Logs")

if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"**{log['time']}** — *{log['task']}* → {log['status']}")
else:
    st.info("No logs yet. Start a task to see results.")
