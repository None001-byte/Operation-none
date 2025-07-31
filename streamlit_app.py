import streamlit as st
import datetime
import random
from io import BytesIO
import json
import base64
import requests

st.set_page_config(page_title="Halal Control Panel v2.0", layout="wide")

# --- Session State ----
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}
if "tag_filters" not in st.session_state:
    st.session_state.tag_filters = {"Little Ummahs": "All", "Sunnah Mindset": "All"}

# --- Layout ---
st.markdown("""
    <h1 style='text-align: center; font-size: 3em;'>🕌 Halal Control Panel v2.0</h1>
    <hr style='margin-bottom: 20px;'>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 2, 1])

with left:
    st.subheader("🔧 Select Channel")
    selected = st.radio("", ["Little Ummahs", "Sunnah Mindset"])

chan = selected
key = chan.replace(" ", "_").lower()

with right:
    st.subheader("📥 JSON Import")
    uploaded_json = st.file_uploader("Import JSON", type=["json"])
    if uploaded_json:
        try:
            content = json.load(uploaded_json)
            restored = 0
            for channel in ["Little Ummahs", "Sunnah Mindset"]:
                for new_entry in content.get(channel, []):
                    if not any(e["timestamp"] == new_entry["timestamp"] and e["prompt"] == new_entry["prompt"] for e in st.session_state.prompts[channel]):
                        if "image" in new_entry and new_entry["image"]:
                            new_entry["image"] = base64.b64decode(new_entry["image"])
                        st.session_state.prompts[channel].append(new_entry)
                        restored += 1
            st.success(f"✅ {restored} prompts imported.")
        except Exception as e:
            st.error(f"❌ Import failed: {e}")

with center:
    st.subheader(f"🎬 {chan} Dashboard")

    if st.button(f"🚀 Run {chan} Auto Task"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = {"channel": chan, "status": "✅ Success", "time": ts, "link": "https://example.com/view"}
        st.session_state.logs.append(log)
        st.success("Automated task triggered.")

    st.markdown("---")
    st.markdown(f"### ✍️ Script Prompt for {chan}")

    prompt_input = st.text_area("Scene Description", value=st.session_state.scripts[chan], key=f"{key}_prompt")

    st.markdown("#### 📌 Prompt Status")
    status_options = ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"]
    if f"{key}_status" not in st.session_state:
        st.session_state[f"{key}_status"] = status_options[0]

    status_cols = st.columns(len(status_options))
    for i, label in enumerate(status_options):
        if status_cols[i].button(label, key=f"{key}_statusbtn_{i}"):
            st.session_state[f"{key}_status"] = label

    selected_status = st.session_state[f"{key}_status"]
    st.write(f"Selected Status: **{selected_status}**")

    tag_input = st.text_input("🏷️ Tags (comma-separated)", key=f"{key}_tags")
    uploaded_image = st.file_uploader("🖼️ Thumbnail (optional)", type=["png", "jpg", "jpeg"], key=f"{key}_image")

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
        st.success("Prompt saved!")

    if prompt_input.strip():
        buf = BytesIO()
        buf.write(prompt_input.encode("utf-8"))
        buf.seek(0)
        st.download_button("📥 Download Script", buf, file_name=f"{key}_{datetime.date.today()}.txt")

    st.markdown("---")
    st.markdown("### 🔍 Prompt History")

    st.markdown("#### Filter by Status")
    filter_cols = st.columns(len(status_options) + 1)
    status_labels = ["All"] + status_options

    if f"{key}_status_filter" not in st.session_state:
        st.session_state[f"{key}_status_filter"] = "All"

    for i, label in enumerate(status_labels):
        if filter_cols[i].button(label, key=f"{key}_filter_status_{i}"):
            st.session_state[f"{key}_status_filter"] = label

    st.markdown("#### Filter by Tags")
    all_tags = sorted({tag for p in st.session_state.prompts[chan] for tag in p.get("tags", [])})
    tag_cols = st.columns(min(6, len(all_tags) + 1))

    if tag_cols[0].button("All", key=f"{key}_tagbtn_all"):
        st.session_state.tag_filters[chan] = "All"

    for i, tag in enumerate(all_tags):
        if tag_cols[(i + 1) % 6].button(tag, key=f"{key}_tagbtn_{i}"):
            st.session_state.tag_filters[chan] = tag

    filtered = [p for p in st.session_state.prompts[chan] if
                (st.session_state[f"{key}_status_filter"] == "All" or p.get("status") == st.session_state[f"{key}_status_filter"]) and
                (st.session_state.tag_filters[chan] == "All" or st.session_state.tag_filters[chan] in p.get("tags", []))]

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
                st.session_state.scripts[chan] = entry["prompt"]
                st.rerun()

# JSON Export
st.markdown("### 📤 Export Prompts")

def prepare_export(prompt):
    p = prompt.copy()
    if p.get("image"):
        p["image"] = base64.b64encode(p["image"]).decode("utf-8")
    return p

export_data = {
    "Little Ummahs": [prepare_export(p) for p in st.session_state.prompts["Little Ummahs"]],
    "Sunnah Mindset": [prepare_export(p) for p in st.session_state.prompts["Sunnah Mindset"]]
}

buf = BytesIO()
buf.write(json.dumps(export_data, indent=2).encode("utf-8"))
buf.seek(0)
st.download_button("📥 Download JSON", buf, file_name="halal_prompts.json", mime="application/json")

# Logs
st.markdown("### 📜 Activity Logs")
if st.session_state.logs:
    for log in reversed(st.session_state.logs):
        st.markdown(f"`{log['time']}` — **{log['channel']}** → {log['status']} [🔗 Link]({log['link']})")
else:
    st.info("No logs yet.")
