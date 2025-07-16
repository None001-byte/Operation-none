import streamlit as st
import datetime
import random
from io import BytesIO
import json
import base64

st.set_page_config(page_title="Halal Control Panel v1.5", layout="wide")

# Session state
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}

# UI
st.markdown("# 🕌 Halal Control Panel v1.5\nWelcome, **Puchu** 👋")
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

# Prompt / script
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
st.markdown("### 📌 Set Prompt Status")

if f"{key}_selected_status" not in st.session_state:
    st.session_state[f"{key}_selected_status"] = status_options[0]

status_cols = st.columns(len(status_options))
for i, label in enumerate(status_options):
    if status_cols[i].button(label, key=f"{key}_statusbtn_{i}"):
        st.session_state[f"{key}_selected_status"] = label

selected_status = st.session_state[f"{key}_selected_status"]
st.write(f"Selected: **{selected_status}**")

if st.button("📌 Save Prompt"):
    st.session_state.scripts[chan] = prompt_input

    image_bytes = uploaded_image.read() if uploaded_image else None

    entry = {
        "prompt": prompt_input,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": "https://example.com/output",
        "status": selected_status,
        "image": image_bytes
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
st.markdown("### 🔍 Filter Prompts by Status")
filter_cols = st.columns(len(status_options) + 1)
status_filter_labels = ["All"] + status_options

if f"{key}_filter_choice" not in st.session_state:
    st.session_state[f"{key}_filter_choice"] = "All"

for i, label in enumerate(status_filter_labels):
    if filter_cols[i].button(label, key=f"{key}_filter_{i}"):
        st.session_state[f"{key}_filter_choice"] = label

filter_choice = st.session_state[f"{key}_filter_choice"]

filtered = [p for p in st.session_state.prompts[chan]
            if filter_choice=="All" or p.get("status","📝 Draft")==filter_choice]

# History
st.markdown("### 📂 Previous Prompts")
if filtered:
    for i, entry in enumerate(reversed(filtered)):
        col1, col2 = st.columns([6, 1])
        with col1:
            status = entry.get("status", "📝 Draft")
            st.markdown(f"`{entry['timestamp']}` — {status} — {entry['prompt']}")
            if entry.get("image"):
                st.image(entry["image"], width=80)
        with col2:
            if st.button("🔁", key=f"reuse_{key}_{i}"):
                st.session_state.scripts[chan] = entry['prompt']
                st.rerun()
else:
    st.info("No prompts saved yet.")

#JSON
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
st.markdown("### 📜 Activity Logs")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['channel']} Video** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet. Start a task to see results.")
