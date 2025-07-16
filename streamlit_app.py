import streamlit as st
import datetime
import random
from io import BytesIO
import json
import base64

def run_full_auto_task(chan):
    import time

    # Simulate or replace with real AI calls
    prompt = f"Auto-script for {chan} about kindness and faith."
    image_link = "https://via.placeholder.com/300x180.png?text=Thumbnail"
    audio_link = "https://example.com/audio/output.mp3"
    video_link = "https://example.com/video/final.mp4"

    # Simulate wait
    time.sleep(2)

    # Save as prompt
    st.session_state.prompts[chan].append({
        "prompt": prompt,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": video_link,
        "status": "✅ Finalized",
        "image": None,
        "tags": ["auto", "full-task", "pipeline"]
    })

    # Log
    st.session_state.logs.append({
        "channel": chan,
        "status": "✅ Completed Auto Task",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": video_link
    })

st.set_page_config(page_title="Halal Control Panel v1.5", layout="wide")

# Session state
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}

# UI
st.markdown("---")
st.markdown("## 🕌 Halal Control Panel v1.5\nWelcome, **Puchu** 👋")
selected = st.radio("", ["Little Ummahs", "Sunnah Mindset"], horizontal=True)
chan = selected
key = chan.replace(" ", "_").lower()

st.markdown(f"## ▶️ {chan} Controls")

if st.button(f"Run {chan} Task"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = {"channel": chan, "status": "✅ Success", "time": ts, "link": "https://example.com/view"}
    st.session_state.logs.append(log)
    st.success("Task completed: ✅ Success")
    st.markdown(f"[🔗 View Output]({log['link']})")
    
if st.button(f"⚙️ Full Auto Video for {chan}"):
    run_full_auto_task(chan)
    st.success("✅ Auto video task completed.")
    st.rerun()


# Task Timer
if f"{key}_start_time" not in st.session_state:
    st.session_state[f"{key}_start_time"] = None

st.markdown("---")
st.markdown("### ⏳ Task Timer")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Timer"):
        st.session_state[f"{key}_start_time"] = datetime.datetime.now()

with col2:
    if st.button("⏹ Stop Timer"):
        if st.session_state[f"{key}_start_time"]:
            elapsed = datetime.datetime.now() - st.session_state[f"{key}_start_time"]
            st.success(f"🕒 Time spent: {str(elapsed).split('.')[0]}")
            st.session_state[f"{key}_start_time"] = None
        else:
            st.warning("⏱ Timer wasn't started.")

# Prompt / script
st.markdown("---")
st.markdown(f"### 📝 Script / Prompt for {chan}")
prompt_input = st.text_area("🎨 Describe your scene",
    value=st.session_state.scripts[chan], key=f"{key}_prompt")

# Thumbnail uploader
uploaded_image = st.file_uploader(
    "🖼️ Upload thumbnail image (optional)",
    type=["png", "jpg", "jpeg"],
    key=f"{key}_image"
)

# Status selector
status_options = ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"]
st.markdown("---")
st.markdown("### 📌 Set Prompt Status")

if f"{key}_selected_status" not in st.session_state:
    st.session_state[f"{key}_selected_status"] = status_options[0]

status_cols = st.columns(len(status_options))
for i, label in enumerate(status_options):
    if status_cols[i].button(label, key=f"{key}_statusbtn_{i}"):
        st.session_state[f"{key}_selected_status"] = label

selected_status = st.session_state[f"{key}_selected_status"]
st.write(f"Selected: **{selected_status}**")

# Tag input
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

# Download script
if prompt_input.strip():
    fname = f"{chan.replace(' ', '_')}_{datetime.date.today()}.txt"
    buf = BytesIO()
    buf.write(prompt_input.encode("utf-8"))
    buf.seek(0)
    st.download_button("📥 Download Script", buf, file_name=fname, mime="text/plain")

# Filter
st.markdown("---")
st.markdown("### 🔍 Filter Prompts by Status")
filter_cols = st.columns(len(status_options) + 1)
status_filter_labels = ["All"] + status_options

if f"{key}_filter_choice" not in st.session_state:
    st.session_state[f"{key}_filter_choice"] = "All"

for i, label in enumerate(status_filter_labels):
    if filter_cols[i].button(label, key=f"{key}_filter_{i}"):
        st.session_state[f"{key}_filter_choice"] = label

filter_choice = st.session_state[f"{key}_filter_choice"]

filtered = [
    p for p in st.session_state.prompts[chan]
    if (filter_choice == "All" or p.get("status", "📝 Draft") == filter_choice)
    and (selected_tag == "All" or selected_tag in p.get("tags", []))
]


# Tag Filter Buttons
st.markdown("---")
st.markdown("### 🧠 Filter Prompts by Tags")

# Extract unique tags from current prompts
all_tags = set()
for p in st.session_state.prompts[chan]:
    all_tags.update(p.get("tags", []))

all_tags = sorted(list(all_tags))

if f"{key}_tag_filter" not in st.session_state:
    st.session_state[f"{key}_tag_filter"] = "All"

if all_tags:
    tag_cols = st.columns(min(len(all_tags) + 1, 6))
    if tag_cols[0].button("All", key=f"{key}_tagbtn_all"):
        st.session_state[f"{key}_tag_filter"] = "All"

    for i, tag in enumerate(all_tags):
        if tag_cols[(i + 1) % 6].button(tag, key=f"{key}_tagbtn_{i}"):
            st.session_state[f"{key}_tag_filter"] = tag

selected_tag = st.session_state[f"{key}_tag_filter"]

# History
st.markdown("---")
st.markdown("### 📂 Previous Prompts")
if filtered:
    for i, entry in enumerate(reversed(filtered)):
        col1, col2 = st.columns([6, 1])
        with col1:
            status = entry.get("status", "📝 Draft")
            tags = entry.get("tags", [])
            img = entry.get("image")
            completed_key = f"{key}_completed_{i}"
            mark = "✅" if st.session_state.get(completed_key, False) else ""

    with st.container():
        st.markdown(f"#### {mark} {status}")
        st.markdown(f"`{entry['timestamp']}`")
        st.markdown(entry["prompt"])
        if tags:
            st.markdown("🏷️ **Tags:** " + ", ".join(tags))
        if img:
            st.image(img, width=100)

        with col2:
            if completed_key not in st.session_state:
                st.session_state[completed_key] = False
                st.session_state[completed_key] = st.checkbox("✅ Done", value=st.session_state[completed_key], key=completed_key)

            if st.button("🔁", key=f"reuse_{key}_{i}"):
                st.session_state.scripts[chan] = entry['prompt']
                st.rerun()

else:
    st.info("No prompts saved yet.")

#JSON
st.markdown("---")
st.markdown("### 🔁 Import Prompts from JSON")

uploaded_json = st.file_uploader("📂 Upload JSON file to restore prompts", type=["json"])

if uploaded_json:
    try:
        content = json.load(uploaded_json)
        restored = 0

        for channel in ["Little Ummahs", "Sunnah Mindset"]:
            for new_entry in content.get(channel, []):
                existing = st.session_state.prompts[channel]
                # Check if already exists (based on timestamp + prompt)
                if not any(e["timestamp"] == new_entry["timestamp"] and e["prompt"] == new_entry["prompt"] for e in existing):
                    if "image" in new_entry and new_entry["image"]:
                        new_entry["image"] = base64.b64decode(new_entry["image"])
                    st.session_state.prompts[channel].append(new_entry)
                    restored += 1

        st.success(f"✅ {restored} prompts imported successfully.")
    except Exception as e:
        st.error(f"❌ Import failed: {e}")

st.markdown("---")
st.markdown("### 📤 Export All Prompts as JSON")

def prepare_prompt_for_export(prompt):
    export_entry = prompt.copy()
    if prompt.get("image"):
        export_entry["image"] = base64.b64encode(prompt["image"]).decode("utf-8")
    return export_entry

combined_export = {
    "Little Ummahs": [
        prepare_prompt_for_export(p) for p in st.session_state.prompts["Little Ummahs"]
    ],
    "Sunnah Mindset": [
        prepare_prompt_for_export(p) for p in st.session_state.prompts["Sunnah Mindset"]
    ]
}

json_bytes = BytesIO()
json_bytes.write(json.dumps(combined_export, indent=2).encode("utf-8"))
json_bytes.seek(0)

st.download_button(
    label="📥 Download All Prompts (JSON)",
    data=json_bytes,
    file_name=f"halal_prompts_export_{datetime.date.today()}.json",
    mime="application/json"
)

# Logs
st.markdown("---")
st.markdown("### 📜 Activity Logs")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['channel']} Video** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet. Start a task to see results.")
    
st.markdown("---")
st.markdown("### 📅 Prompt Timeline Calendar")

import pandas as pd

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
