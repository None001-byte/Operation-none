import streamlit as st
import datetime
import random

st.set_page_config(page_title="Halal Control Panel v1.5", layout="wide")

# Session state setup
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {
        "Little Ummahs": "",
        "Sunnah Mindset": ""
    }
if "prompts" not in st.session_state:
    st.session_state.prompts = {
        "Little Ummahs": [],
        "Sunnah Mindset": []
    }

st.markdown("""
# 🕌 Halal Control Panel v1.5
Welcome, **Puchu** 👋  
This is your mobile-friendly control panel for automating halal content generation.
""")

# Channel selector
selected_channel = st.radio("", ["Little Ummahs", "Sunnah Mindset"], horizontal=True)
channel_name = selected_channel
key_prefix = channel_name.replace(" ", "_").lower()

st.markdown(f"## ▶️ {channel_name} Controls")

# Task Runner
if st.button(f"Run {channel_name} Task"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "channel": channel_name,
        "status": "✅ Success",
        "time": timestamp,
        "link": "https://example.com/view"
    }
    st.session_state.logs.append(log_entry)
    st.success("Task completed: ✅ Success")
    st.markdown(f"[🔗 View Output]({log_entry['link']})")

# Prompt box
st.markdown(f"### 📝 Script / Prompt for {channel_name}")
prompt_input = st.text_area(
    f"🎨 Describe your scene",
    value=st.session_state.scripts[channel_name],
    placeholder="e.g., Umm Jamil storms through Mecca holding a rock...",
    key=f"{key_prefix}_prompt"
)

# Prompt Status Options
status_options = ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"]
selected_status = st.selectbox("📌 Set Prompt Status", status_options, key=f"{key_prefix}_status")

# Save prompt with status
if st.button("📌 Save Prompt"):
    st.session_state.scripts[channel_name] = prompt_input
    new_prompt = {
        "prompt": prompt_input,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": "https://example.com/output",
        "status": selected_status
    }
    st.session_state.prompts[channel_name].append(new_prompt)
    st.success("Prompt saved with status!")

# Export Script
from io import BytesIO

if prompt_input.strip():
    filename = f"{channel_name.replace(' ', '_')}_{datetime.date.today()}.txt"
    file_buffer = BytesIO()
    file_buffer.write(prompt_input.encode("utf-8"))
    file_buffer.seek(0)

    st.download_button(
        label="📥 Download Script",
        data=file_buffer,
        file_name=filename,
        mime="text/plain"
    )

# Prompt history
st.markdown("### 🗂️ Previous Prompts")
if st.session_state.prompts[channel_name]:
    for i, entry in enumerate(reversed(st.session_state.prompts[channel_name])):
        col1, col2 = st.columns([6, 1])
        with col1:
            status = entry.get("status", "📝 Draft")
st.markdown(f"`{entry['timestamp']}` — {status} — {entry['prompt']}")
        with col2:
            if st.button("🔁", key=f"reuse_{i}"):
                st.session_state.scripts[channel_name] = entry['prompt']
                st.rerun()
else:
    st.info("No prompts saved yet.")

# Logs section
st.markdown("### 📜 Activity Logs")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['channel']} Video** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet. Start a task to see results.")
