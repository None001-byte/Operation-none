import streamlit as st
import datetime
from io import BytesIO
import json
import base64
import pandas as pd

# Set layout for widescreen monitors (e.g. 1080p)
st.set_page_config(page_title="Halal Control Panel", layout="wide")

# Session initialization
if "logs" not in st.session_state:
    st.session_state.logs = []
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}
if "selected_channel" not in st.session_state:
    st.session_state.selected_channel = "Little Ummahs"

# Channel selector
st.markdown("<h1 style='text-align: center;'>🕌 Halal Control Panel</h1>", unsafe_allow_html=True)
selected = st.radio("Select Channel", ["Little Ummahs", "Sunnah Mindset"], horizontal=True)
chan = selected
key = chan.replace(" ", "_").lower()
st.session_state.selected_channel = chan

# Auto run task simulation
def run_full_auto_task(channel):
    prompt = f"This is an auto-generated script for {channel}."
    video_link = "https://example.com/video/final.mp4"

    st.session_state.prompts[channel].append({
        "prompt": prompt,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": video_link,
        "status": "✅ Finalized",
        "image": None,
        "tags": ["auto", "full-task"]
    })

    st.session_state.logs.append({
        "channel": channel,
        "status": "✅ Completed Auto Task",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "link": video_link
    })

# Layout: three responsive columns
col_left, col_center, col_right = st.columns([1, 4, 1])

# 👉 CENTER: Auto Run Button + Logs
with col_center:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("## ⚙️ Full Auto Video Task")
    if st.button(f"▶️ Run Auto Task for {chan}"):
        run_full_auto_task(chan)
        st.rerun()

    st.markdown("### 📜 Logs")
    if st.session_state.logs:
        for log in reversed(st.session_state.logs):
            st.markdown(f"`{log['time']}` — **{log['channel']}** → {log['status']} [🔗 Link]({log['link']})")
    else:
        st.info("No logs yet.")
     st.markdown("</div>", unsafe_allow_html=True)

# 👉 LEFT COLUMN: Prompt + Status + Tags
with col_left:
    st.markdown("### 📝 Prompt Input")
    prompt_input = st.text_area(
        "Describe your scene",
        value=st.session_state.scripts[chan],
        key=f"{key}_prompt"
    )

    st.markdown("### 📌 Set Status")
    status_options = ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"]
    if f"{key}_selected_status" not in st.session_state:
        st.session_state[f"{key}_selected_status"] = status_options[0]
    status_cols = st.columns(len(status_options))
    for i, label in enumerate(status_options):
        if status_cols[i].button(label, key=f"{key}_statusbtn_{i}"):
            st.session_state[f"{key}_selected_status"] = label
    selected_status = st.session_state[f"{key}_selected_status"]
    st.markdown(f"Selected: **{selected_status}**")

    st.markdown("### 🏷️ Tags")
    tag_input = st.text_input("Comma-separated tags", key=f"{key}_tags")
    
# 👉 RIGHT COLUMN: Thumbnail + JSON Export/Import
with col_right:
    st.markdown("### 🖼️ Thumbnail")
    uploaded_image = st.file_uploader(
        "Upload image (optional)",
        type=["png", "jpg", "jpeg"],
        key=f"{key}_image"
    )

    st.markdown("### 📤 Export Prompts")
    def prepare_prompt_for_export(p):
        out = p.copy()
        if p.get("image"):
            out["image"] = base64.b64encode(p["image"]).decode("utf-8")
        return out

    export_data = {
        "Little Ummahs": [prepare_prompt_for_export(p) for p in st.session_state.prompts["Little Ummahs"]],
        "Sunnah Mindset": [prepare_prompt_for_export(p) for p in st.session_state.prompts["Sunnah Mindset"]]
    }

    export_bytes = BytesIO()
    export_bytes.write(json.dumps(export_data, indent=2).encode("utf-8"))
    export_bytes.seek(0)

    st.download_button(
        "📥 Download JSON",
        data=export_bytes,
        file_name="halal_prompts.json",
        mime="application/json"
    )

    st.markdown("### 📂 Import Prompts")
    import_file = st.file_uploader("Upload prompt JSON", type=["json"])
    if import_file:
        try:
            data = json.load(import_file)
            count = 0
            for ch in ["Little Ummahs", "Sunnah Mindset"]:
                for new_p in data.get(ch, []):
                    if "image" in new_p and new_p["image"]:
                        new_p["image"] = base64.b64decode(new_p["image"])
                    st.session_state.prompts[ch].append(new_p)
                    count += 1
            st.success(f"Imported {count} prompts.")
        except Exception as e:
            st.error(f"Import failed: {e}")

# 🔍 Status Filter
st.markdown("---")
st.markdown("### 🔎 Filter Prompts by Status")

status_labels = ["All"] + status_options
filter_cols = st.columns(len(status_labels))

if f"{key}_filter_choice" not in st.session_state:
    st.session_state[f"{key}_filter_choice"] = "All"

for i, label in enumerate(status_labels):
    if filter_cols[i].button(label, key=f"{key}_status_filter_{i}"):
        st.session_state[f"{key}_filter_choice"] = label
status_filter = st.session_state[f"{key}_filter_choice"]

# 🔍 Tag Filter
st.markdown("### 🧠 Filter Prompts by Tag")
all_tags = set()
for p in st.session_state.prompts[chan]:
    all_tags.update(p.get("tags", []))
tag_list = sorted(list(all_tags))

if f"{key}_tag_filter" not in st.session_state:
    st.session_state[f"{key}_tag_filter"] = "All"

tag_cols = st.columns(min(len(tag_list) + 1, 6))
if tag_cols[0].button("All Tags", key=f"{key}_tag_all"):
    st.session_state[f"{key}_tag_filter"] = "All"

for i, tag in enumerate(tag_list):
    if tag_cols[(i + 1) % 6].button(tag, key=f"{key}_tag_{i}"):
        st.session_state[f"{key}_tag_filter"] = tag

tag_filter = st.session_state[f"{key}_tag_filter"]

# 📂 Prompt History
st.markdown("### 📚 Previous Prompts")
filtered = [
    p for p in st.session_state.prompts[chan]
    if (status_filter == "All" or p.get("status") == status_filter)
    and (tag_filter == "All" or tag_filter in p.get("tags", []))
]

if filtered:
    for i, entry in enumerate(reversed(filtered)):
        col1, col2 = st.columns([6, 1])
        with col1:
            status = entry.get("status", "📝 Draft")
            st.markdown(f"`{entry['timestamp']}` — {status} — {entry['prompt']}")
            if entry.get("tags"):
                st.markdown("🏷️ Tags: " + ", ".join(entry["tags"]))
            if entry.get("image"):
                st.image(entry["image"], width=80)
        with col2:
            reuse_key = f"{key}_reuse_{i}"
            if st.button("🔁", key=reuse_key):
                st.session_state.scripts[chan] = entry["prompt"]
                st.rerun()
else:
    st.info("No saved prompts yet for this filter.")

# 📅 Calendar View
st.markdown("### 📅 Prompt Calendar")
def get_calendar_df():
    all_data = []
    for c in ["Little Ummahs", "Sunnah Mindset"]:
        for p in st.session_state.prompts[c]:
            dt = pd.to_datetime(p["timestamp"])
            all_data.append({"date": dt.date(), "channel": c})
    return pd.DataFrame(all_data)

calendar_df = get_calendar_df()
if not calendar_df.empty:
    count_by_date = calendar_df["date"].value_counts().sort_index()
    st.bar_chart(count_by_date)
else:
    st.info("No prompt activity yet.")
