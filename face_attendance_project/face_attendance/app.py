import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Face Attendance System", page_icon="🎓", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"]{background:#0f172a}
[data-testid="stSidebar"]{background:#1e293b}
.mtitle{font-size:2rem;font-weight:800;color:#38bdf8;text-align:center;margin-bottom:.3rem}
.msub{text-align:center;color:#94a3b8;font-size:.9rem;margin-bottom:1.5rem}
.mcard{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:1.2rem;text-align:center}
.mnum{font-size:2.2rem;font-weight:800;color:#38bdf8}
.mlbl{font-size:.8rem;color:#94a3b8;margin-top:4px}
.nodata{background:#1e293b;border:1px dashed #334155;border-radius:12px;padding:3rem;text-align:center;color:#64748b}
</style>
""", unsafe_allow_html=True)

st_autorefresh(interval=3000, key="ar")

with st.sidebar:
    st.markdown("## 🎓 Attendance System")
    st.markdown("---")
    sel_date = st.date_input("📅 Date chunein", value=datetime.today())
    date_str = sel_date.strftime("%d-%m-%Y")
    st.markdown("---")
    st.markdown("### 📤 CSV Upload")
    st.caption("Local machine se CSV yahan upload karein:")
    uploaded = st.file_uploader("Attendance CSV", type=["csv"])
    st.markdown("---")
    st.markdown("<span style='color:#22c55e'>● Live — har 3 sec refresh</span>", unsafe_allow_html=True)

st.markdown("<div class='mtitle'>🎓 Face Recognition Attendance</div>", unsafe_allow_html=True)
st.markdown(f"<div class='msub'>Date: {date_str}</div>", unsafe_allow_html=True)

# ── SAFE DATA LOAD — kabhi crash nahi hoga ───────────────────────────────────
df = None

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        st.success("✅ CSV load ho gayi!")
    except Exception as e:
        st.error(f"Upload error: {e}")
else:
    # File exist kare tabhi padho — warna sirf message dikhao
    csv_path = os.path.join("Attendance", f"Attendance_{date_str}.csv")
    if os.path.isfile(csv_path):
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            st.error(f"CSV error: {e}")

# ── METRICS ──────────────────────────────────────────────────────────────────
total  = len(df) if df is not None else 0
unique = df["NAME"].nunique() if df is not None and "NAME" in df.columns else 0
first  = df["TIME"].iloc[0]  if df is not None and "TIME" in df.columns and total > 0 else "—"
last   = df["TIME"].iloc[-1] if df is not None and "TIME" in df.columns and total > 0 else "—"

c1,c2,c3,c4 = st.columns(4)
for col, val, lbl in [(c1,total,"Total Entries"),(c2,unique,"Unique Students"),(c3,first,"First Entry"),(c4,last,"Last Entry")]:
    col.markdown(f"<div class='mcard'><div class='mnum'>{val}</div><div class='mlbl'>{lbl}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABLE + CHART ─────────────────────────────────────────────────────────────
if df is not None and not df.empty:
    t1, t2 = st.tabs(["📋 Attendance Table", "📊 Chart"])
    with t1:
        q = st.text_input("🔍 Naam se dhundho")
        out = df[df["NAME"].str.contains(q, case=False, na=False)] if q else df
        st.dataframe(out.reset_index(drop=True), use_container_width=True, height=400)
        st.download_button("⬇️ CSV Download", out.to_csv(index=False).encode(), f"Attendance_{date_str}.csv", "text/csv")
    with t2:
        if "NAME" in df.columns:
            c = df["NAME"].value_counts().reset_index()
            c.columns = ["Name","Count"]
            st.bar_chart(c.set_index("Name"), color="#38bdf8")
else:
    st.markdown(f"""
    <div class='nodata'>
        <h3 style='color:#475569'>📭 Koi Data Nahi Mila</h3>
        <p style='margin:.5rem 0'>{date_str} ki attendance CSV nahi mili.</p>
        <p style='font-size:13px'>
            <b>Option 1:</b> Sidebar se CSV upload karein<br>
            <b>Option 2:</b> Local pe test.py chalao → O dabao → CSV ban jayegi
        </p>
    </div>""", unsafe_allow_html=True)
