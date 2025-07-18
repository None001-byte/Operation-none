# Halal Control Panel v2.0 (Inspired by Base44)
# All new layout with centralized logic, dark theme, icons, modern UI

import streamlit as st
import datetime
import base64
import json
from io import BytesIO

# ---- CONFIG ----
st.set_page_config(page_title="Halal Control Panel v2.0", layout="wide")

# ---- SESSION ----
if "prompts" not in st.session_state:
    st.session_state.prompts = {"Little Ummahs": [], "Sunnah Mindset": []}
if "scripts" not in st.session_state:
    st.session_state.scripts = {"Little Ummahs": "", "Sunnah Mindset": ""}
if "logs" not in st.session_state:
    st.session_state.logs = []

# ---- STYLING ----
st.markdown("""
    <style>
    body { background-color: #121726; }
    h1, h2, h3, h4, h5, h6, p, div { color: #FFFFFF !important; }
    .dashboard-card {
        background-color: #1e1e2f;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        color: white;
        box-shadow: 0 0 10px rgba(255,255,255,0.05);
    }
    .button-gradient button {
        background: linear-gradient(to right, #915EFF, #4E81EB);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
<h1 style='text-align: center; font-size: 48px;'>Welcome back, Puchu!</h1>
<p style='text-align: center; font-size: 18px;'>Your AI-powered halal productivity dashboard 🕌</p>
""", unsafe_allow_html=True)

# ---- CHANNEL SELECT ----
page = st.radio("", ["Dashboard Overview", "Sunnah Mindset", "Little Ummahs"], horizontal=True)
chan = page if "Overview" not in page else "Little Ummahs"
key = chan.replace(" ", "_").lower()

# ---- DASHBOARD STATS ----
total = len(st.session_state.prompts[chan])
completed = len([p for p in st.session_state.prompts[chan] if p.get("status") == "✅ Finalized"])
images = len([p for p in st.session_state.prompts[chan] if p.get("image")])
prompts = len(st.session_state.prompts[chan])

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"""
<div class='dashboard-card'>
<h3>📋 Total Tasks</h3><p>{total}</p>
</div>
""", unsafe_allow_html=True)
col2.markdown(f"""
<div class='dashboard-card'>
<h3>✅ Completed</h3><p>{completed}</p>
</div>
""", unsafe_allow_html=True)
col3.markdown(f"""
<div class='dashboard-card'>
<h3>🖼️ Images</h3><p>{images}</p>
</div>
""", unsafe_allow_html=True)
col4.markdown(f"""
<div class='dashboard-card'>
<h3>💬 All Prompts</h3><p>{prompts}</p>
</div>
""", unsafe_allow_html=True)

# ---- PROMPT INPUT ----
st.markdown("---")
st.markdown(f"## 📝 New Prompt for {chan}")

prompt = st.text_area("Describe your prompt", key=f"{key}_prompt")
image = st.file_uploader("Upload optional thumbnail", type=["jpg", "jpeg", "png"], key=f"{key}_img")
status = st.radio("Set Status", ["📝 Draft", "🔊 Voiced", "🎞️ Rendered", "✅ Finalized"], horizontal=True)
tags = st.text_input("Add tags (comma-separated)", key=f"{key}_tags")

if st.button("Save Prompt", key=f"{key}_save"):
    entry = {
        "prompt": prompt,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "image": image.read() if image else None
    }
    st.session_state.prompts[chan].append(entry)
    st.success("✅ Prompt saved!")

# ---- TIMELINE VIEW ----
st.markdown("---")
st.markdown("## 📜 Timeline")
for entry in reversed(st.session_state.prompts[chan][-5:]):
    st.markdown(f"""
    <div style='border:1px solid #333;border-radius:10px;padding:12px;margin-bottom:10px;background:#1f2335;'>
        <b>{entry['status']}</b> - {entry['timestamp']}<br>
        <span style='color:#aaa;'>{entry['prompt']}</span><br>
        {' '.join([f'<span style="background:#333;padding:3px 6px;border-radius:6px;margin-right:4px;">{t}</span>' for t in entry.get('tags', [])])}
        {('<br><img src="data:image/png;base64,' + base64.b64encode(entry['image']).decode() + '" width="100">') if entry.get('image') else ''}
    </div>
    """, unsafe_allow_html=True)

# ---- EXPORT ----
def export_data():
    def encode_entry(entry):
        e = entry.copy()
        if e.get("image"):
            e["image"] = base64.b64encode(e["image"]).decode()
        return e
    
    data = {
        "Little Ummahs": [encode_entry(e) for e in st.session_state.prompts["Little Ummahs"]],
        "Sunnah Mindset": [encode_entry(e) for e in st.session_state.prompts["Sunnah Mindset"]]
    }
    buf = BytesIO()
    buf.write(json.dumps(data, indent=2).encode())
    buf.seek(0)
    return buf

st.markdown("---")
colA, colB = st.columns(2)
with colA:
    if st.button("🔄 Refresh Dashboard", key="refresh", help="Manual reload"):
        st.experimental_rerun()
with colB:
    st.download_button("📥 Export JSON", data=export_data(), file_name="halal_dashboard.json", mime="application/json")
