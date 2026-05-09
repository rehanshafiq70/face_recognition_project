import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Face Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f172a; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    .main-title {
        font-size: 2.2rem; font-weight: 800; color: #38bdf8;
        text-align: center; margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center; color: #94a3b8; font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-num { font-size: 2.5rem; font-weight: 800; color: #38bdf8; }
    .metric-lbl { font-size: 0.85rem; color: #94a3b8; margin-top: 4px; }
    .status-online {
        display: inline-block; width: 10px; height: 10px;
        background: #22c55e; border-radius: 50%;
        animation: pulse 1.5s infinite; margin-right: 6px;
    }
    @keyframes pulse {
        0%,100% { opacity: 1; } 50% { opacity: 0.3; }
    }
    .no-data-box {
        background: #1e293b; border: 1px dashed #334155;
        border-radius: 12px; padding: 3rem; text-align: center;
        color: #64748b;
    }
    div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Auto-refresh every 3 seconds ──────────────────────────────────────────────
st_autorefresh(interval=3000, key="attendance_refresh")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 Attendance System")
    st.markdown("---")

    # Date selector
    selected_date = st.date_input("📅 Tariikh chunein", value=datetime.today())
    date_str = selected_date.strftime("%d-%m-%Y")

    st.markdown("---")
    st.markdown("### 📤 CSV Upload (Optional)")
    st.caption("Agar local se attendance CSV upload karni ho:")
    uploaded_file = st.file_uploader("CSV file upload karein", type=["csv"])

    st.markdown("---")
    st.markdown(
        "<span class='status-online'></span><span style='color:#22c55e;font-size:13px'>Live • Har 3 sec refresh</span>",
        unsafe_allow_html=True
    )
    st.caption(f"Python 3.11.9 · OpenCV · KNN")

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='main-title'>🎓 Face Recognition Attendance</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-title'>Date: {date_str} — Real-time attendance dashboard</div>", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
csv_path = f"Attendance/Attendance_{date_str}.csv"
df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Uploaded CSV load ho gayi!")
    except Exception as e:
        st.error(f"CSV padhne mein error: {e}")

elif os.path.isfile(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"CSV padhne mein error: {e}")

# ── Metrics ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

if df is not None and not df.empty:
    total     = len(df)
    unique    = df["NAME"].nunique() if "NAME" in df.columns else 0
    last_time = df["TIME"].iloc[-1] if "TIME" in df.columns else "—"
    first_in  = df["TIME"].iloc[0]  if "TIME" in df.columns else "—"
else:
    total = unique = 0
    last_time = first_in = "—"

with col1:
    st.markdown(f"<div class='metric-card'><div class='metric-num'>{total}</div><div class='metric-lbl'>Total Entries</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><div class='metric-num'>{unique}</div><div class='metric-lbl'>Unique Students</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><div class='metric-num' style='font-size:1.4rem'>{first_in}</div><div class='metric-lbl'>First Entry</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><div class='metric-num' style='font-size:1.4rem'>{last_time}</div><div class='metric-lbl'>Last Entry</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Table + Chart ─────────────────────────────────────────────────────────────
if df is not None and not df.empty:
    tab1, tab2 = st.tabs(["📋 Attendance Table", "📊 Chart"])

    with tab1:
        # Search filter
        search = st.text_input("🔍 Naam se dhundho", placeholder="e.g. Ahmad")
        filtered = df[df["NAME"].str.contains(search, case=False, na=False)] if search else df
        st.dataframe(
            filtered.reset_index(drop=True),
            use_container_width=True,
            height=400
        )
        # Download button
        csv_data = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ CSV Download karein",
            data=csv_data,
            file_name=f"Attendance_{date_str}.csv",
            mime="text/csv"
        )

    with tab2:
        if "NAME" in df.columns:
            counts = df["NAME"].value_counts().reset_index()
            counts.columns = ["Name", "Count"]
            st.bar_chart(counts.set_index("Name"), color="#38bdf8")
        else:
            st.info("Chart ke liye NAME column chahiye.")
else:
    st.markdown(f"""
    <div class='no-data-box'>
        <h3 style='color:#475569'>📭 Koi Attendance Nahi Mili</h3>
        <p>{date_str} ki koi CSV file nahi mili.</p>
        <p style='font-size:13px'>
            Ya toh sidebar se CSV upload karein,<br>
            ya phir local machine pe <code>test.py</code> chalao aur 'O' dabao.
        </p>
    </div>
    """, unsafe_allow_html=True)
