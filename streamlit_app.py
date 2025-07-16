import streamlit as st
import datetime
import random

# Setup state
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
This is your personal halal automation dashboard. Control, store, and inspect everything from here.
""")

tab1, tab2 = st.tabs(["🎬 Little Ummahs", "📖 Sunnah Mindset"])

def channel_ui(channel_name, key_prefix):
    st.subheader(f"▶️ {channel_name} Controls")

    if st.button(f"Run {channel_name} Task", key=f"{key_prefix}_run"):
        log = run_task(f"{channel_name} Video")
        st.success(f"Task completed: {log['status']}")
        st.markdown(f"[🔗 View Output]({log['link']})")

    st.text_area(f"✍️ Script for {channel_name}",
                 value=st.session_state.scripts[channel_name],
                 height=200,
                 key=f"{key_prefix}_script")

    if st.button(f"💾 Save {channel_name} Script", key=f"{key_prefix}_save_script"):
        st.session_state.scripts[channel_name] = st.session_state[f"{key_prefix}_script"]
        st.success("Script saved!")

    st.divider()
    st.markdown(f"🎞️ **Prompt Tracker** — Describe visuals for generation")
    st.text_area(f"🎨 New visual prompt for {channel_name}",
                 placeholder="e.g., Umm Jamil storms through Mecca holding a rock...",
                 key=f"{key_prefix}_prompt")

    video_link = st.text_input(f"📹 Output video link (optional)", key=f"{key_prefix}_link")

    if st.button(f"📌 Save Prompt for {channel_name}", key=f"{key_prefix}_save_prompt"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_prompt = {
            "prompt": st.session_state[f"{key_prefix}_prompt"],
            "link": video_link,
            "time": timestamp
        }
        st.session_state.prompts[channel_name].append(new_prompt)
        st.success("Prompt saved!")

    if st.session_state.prompts[channel_name]:
        st.markdown("🗂️ **Previous Prompts**")
        for p in reversed(st.session_state.prompts[channel_name][-5:]):  # show latest 5
            st.markdown(f"`{p['time']}` — {p['prompt']} [🔗 Link]({p['link']})" if p['link'] else f"`{p['time']}` — {p['prompt']}")
    else:
        st.info("No prompts saved yet.")

with tab1:
    channel_ui("Little Ummahs", "ummahs")

with tab2:
    channel_ui("Sunnah Mindset", "sunnah")

st.divider()
st.subheader("📜 Activity Logs")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['task']}** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet. Trigger a task to begin.")
