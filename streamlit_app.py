import streamlit as st
import datetime
import random
from io import BytesIO
import json
import base64
import pandas as pd

# === PAGE CONFIG ===
st.set_page_config(page_title="Halal Control Panel", layout="wide")

# === SESSION STATE INIT ===
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}
if "current_view" not in st.session_state:
    st.session_state.current_view = "Dashboard Overview"

# === HEADER ===
st.markdown("""
    <h1 style='text-align: center; font-size: 42px;'>🕌 Halal Control Panel</h1>
    <p style='text-align: center;'>Welcome, <strong>Puchu</strong> 👋</p>
""", unsafe_allow_html=True)

# === NAVIGATION TOGGLE ===
view_options = ["Dashboard Overview", "Sunnah Mindset", "Little Ummahs"]
view = st.selectbox("Select View", view_options, index=view_options.index(st.session_state.current_view))
st.session_state.current_view = view

# === VIEW ROUTING ===
if view == "Dashboard Overview":
    st.markdown("### 📊 Dashboard Overview")
    st.info("Welcome to the central dashboard. Use the toggle above to switch views.")
    st.markdown("### 📜 Activity Logs")
    if st.session_state.logs:
        for log in reversed(st.session_state.logs):
            st.markdown(f"`{log['time']}` — **{log['channel']} Video** → {log['status']} [🔗 Link]({log['link']})")
    else:
        st.info("No logs yet. Start a task to see results.")

    st.markdown("### 📅 Prompt Timeline Calendar")

    def get_calendar_data():
        data = []
        for channel in ["Little Ummahs", "Sunnah Mindset"]:
            for p in st.session_state.prompts[channel]:
                dt = pd.to_datetime(p["timestamp"])
                data.append({"date": dt.date(), "channel": channel})
        return pd.DataFrame(data)

    calendar_data = get_calendar_data()
    if not calendar_data.empty:
        dates = calendar_data["date"].value_counts().sort_index()
        st.bar_chart(dates)
    else:
        st.info("No prompt history available for calendar.")

elif view in ["Little Ummahs", "Sunnah Mindset"]:
    chan = view
    key = chan.replace(" ", "_").lower()

    st.markdown(f"## ▶️ {chan} Controls")

    if st.button(f"Run {chan} Task"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = {"channel": chan, "status": "✅ Success", "time": ts, "link": "https://example.com/view"}
        st.session_state.logs.append(log)
        st.success("Task completed: ✅ Success")
        st.markdown(f"[🔗 View Output]({log['link']})")

    # Prompt / script
    st.markdown(f"### 📝 Script / Prompt for {chan}")
    prompt_input = st.text_area("🎨 Describe your scene", value=st.session_state.scripts[chan], key=f"{key}_prompt")

    # Image
    uploaded_image = st.file_uploader("🖼️ Upload thumbnail image (optional)", type=["png", "jpg", "jpeg"], key=f"{key}_image")

    # Status
    status_options = ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"]
    if f"{key}_selected_status" not in st.session_state:
        st.session_state[f"{key}_selected_status"] = status_options[0]

    st.markdown("### 📌 Set Prompt Status")
    status_cols = st.columns(len(status_options))
    for i, label in enumerate(status_options):
        if status_cols[i].button(label, key=f"{key}_statusbtn_{i}"):
            st.session_state[f"{key}_selected_status"] = label

    selected_status = st.session_state[f"{key}_selected_status"]
    st.write(f"Selected: **{selected_status}**")

    # Tags
    tag_input = st.text_input("🏷️ Add tags (comma-separated)", key=f"{key}_tags")

    if st.button("📌 Save Prompt"):
        st.session_state.scripts[chan] = prompt_input
        image_bytes = uploaded_image.read() if uploaded_image else None
        entry = {
            "prompt": prompt_input,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "link": "https://example.com/output",
            "status": selected_status,
            "image": image_bytes,
            "tags": [tag.strip() for tag in tag_input.split(",") if tag.strip()]
        }
        st.session_state.prompts[chan].append(entry)
        st.success("Prompt saved with status and thumbnail!")

    # Download Script
    if prompt_input.strip():
        fname = f"{chan.replace(' ', '_')}_{datetime.date.today()}.txt"
        buf = BytesIO()
        buf.write(prompt_input.encode("utf-8"))
        buf.seek(0)
        st.download_button("📥 Download Script", buf, file_name=fname, mime="text/plain")

    # Filters
    st.markdown("### 🔍 Filter Prompts by Status")
    if f"{key}_filter_choice" not in st.session_state:
        st.session_state[f"{key}_filter_choice"] = "All"

    filter_cols = st.columns(len(status_options) + 1)
    for i, label in enumerate(["All"] + status_options):
        if filter_cols[i].button(label, key=f"{key}_filter_{i}"):
            st.session_state[f"{key}_filter_choice"] = label

    filter_choice = st.session_state[f"{key}_filter_choice"]

    # Tag Filter
    st.markdown("### 🧠 Filter Prompts by Tags")
    all_tags = sorted(set(tag for p in st.session_state.prompts[chan] for tag in p.get("tags", [])))
    if f"{key}_tag_filter" not in st.session_state:
        st.session_state[f"{key}_tag_filter"] = "All"

    tag_cols = st.columns(min(len(all_tags) + 1, 6))
    if tag_cols[0].button("All", key=f"{key}_tagbtn_all"):
        st.session_state[f"{key}_tag_filter"] = "All"
    for i, tag in enumerate(all_tags):
        if tag_cols[(i + 1) % 6].button(tag, key=f"{key}_tagbtn_{i}"):
            st.session_state[f"{key}_tag_filter"] = tag

    selected_tag = st.session_state[f"{key}_tag_filter"]

    # Filtered View
    filtered = [p for p in st.session_state.prompts[chan]
                if (filter_choice == "All" or p.get("status", "📝 Draft") == filter_choice)
                and (selected_tag == "All" or selected_tag in p.get("tags", []))]

    # History
    st.markdown("### 📂 Previous Prompts")
    if filtered:
        for i, entry in enumerate(reversed(filtered)):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"`{entry['timestamp']}` — {entry['status']} — {entry['prompt']}")
                if entry.get("tags"):
                    st.markdown("🏷️ Tags: " + ", ".join(entry["tags"]))
                if entry.get("image"):
                    st.image(entry["image"], width=80)
            with col2:
                if st.button("🔁", key=f"reuse_{key}_{i}"):
                    st.session_state.scripts[chan] = entry['prompt']
                    st.rerun()
    else:
        st.info("No prompts saved yet.")
