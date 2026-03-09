import streamlit as st
import base64
import os
import requests
from datetime import date

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES (PRESERVED)
user_name = "Dr. John Doe"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/doctor_profile.png" 

DOCTOR_BIO = {
    "title": "Senior Consultant Cardiologist",
    "desc": "Specializing in interventional cardiology and structural heart disease with over 15 years of clinical excellence.",
    "certs": ["MD, Harvard Medical School", "Board Certified in Cardiovascular Disease", "FACC Fellowship"],
    "achievements": ["Best Clinician Award 2025", "50+ Published Research Papers", "Lead Researcher - Project HeartBeat"]
}

# NEW DATA FOR URGENT ALERTS
URGENT_PATIENTS = [
    {"Room": "402", "Name": "Alice Tan", "Issue": "Tachycardia Spike"},
    {"Room": "ICU-1", "Name": "Bob Smith", "Issue": "Post-Op Arrhythmia"},
    {"Room": "ER-3", "Name": "Charlie Day", "Issue": "Unstable Angina"}
]

# 3. FILE ENCODING
def get_base64_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
    except: return ""
    return ""

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")
doctor_b64 = get_base64_from_url(GITHUB_RAW_URL)
if not doctor_b64:
    doctor_b64 = get_base64("doctor_profile.png")

# 4. SESSION STATE (PRESERVED + ALERT TOGGLE)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"
if "doc_status" not in st.session_state:
    st.session_state.doc_status = "🟢 Available"
if "show_alerts" not in st.session_state:
    st.session_state.show_alerts = False
if "daily_tasks" not in st.session_state:
    st.session_state.daily_tasks = {str(date.today()): ["Review Lab Results", "Surgery Consultation"]}
if "completed_counts" not in st.session_state:
    st.session_state.completed_counts = {}

# 5. CSS (UNIFIED DESIGN + ALERTS)
st.markdown(f"""
    <style>
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }}
    .profile-card {{ background: white; padding: 35px; border-radius: 30px; border: 1px solid #E0E0E0; box-shadow: 0 10px 40px rgba(0,0,0,0.04); animation: slideUp 0.6s ease-out; }}
    .profile-img {{ width: 110px; height: 110px; border-radius: 25px; object-fit: cover; border: 3px solid #93C572; }}
    
    .stat-box {{ background: #F1F8E9; border-radius: 20px; padding: 20px; text-align: center; border: 1px solid #E1EDD8; cursor: pointer; }}
    .stat-val {{ font-size: 24px; font-weight: 800; color: #124D41; }}
    .stat-lbl {{ font-size: 12px; color: #666; text-transform: uppercase; }}
    
    .alert-card {{ background: #FFF5F5; border-left: 5px solid #E57373; padding: 10px; border-radius: 8px; margin-bottom: 8px; }}
    .todo-item {{ background:#F1F8E9; padding:12px; border-radius:12px; border-left:5px solid #93C572; margin-bottom:10px; }}
    </style>
    """, unsafe_allow_html=True)

# 6. APP FLOW
if not st.session_state.auth:
    with st.form("login_form"):
        st.markdown('<p style="color:#93C572; font-weight:800; font-size:20px; text-align:center;">67+2 PODCAST</p>', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#124D41; font-size:55px; font-weight:900; text-align:center; margin:0;">M-FLO</h1>', unsafe_allow_html=True)
        u = st.text_input("ID", placeholder="Enter ID", label_visibility="collapsed")
        p = st.text_input("Key", type="password", placeholder="Key", label_visibility="collapsed")
        if st.form_submit_button("AUTHENTICATE"):
            if u == "doctor1" and p == "mediflow2026": st.session_state.auth = True; st.rerun()
else:
    # --- SIDEBAR (PRESERVED) ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

    if st.session_state.current_page == "Homepage":
        # QUICK STATS ROW
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.markdown('<div class="stat-box"><p class="stat-lbl">Patients Today</p><p class="stat-val">12</p></div>', unsafe_allow_html=True)
        with s2: st.markdown('<div class="stat-box"><p class="stat-lbl">Surgeries</p><p class="stat-val">02</p></div>', unsafe_allow_html=True)
        with s3:
            # Interactive Alert Trigger
            st.markdown('<div class="stat-box"><p class="stat-lbl">Urgent Alerts</p><p class="stat-val" style="color:#E57373;">03</p></div>', unsafe_allow_html=True)
            if st.button("View Details", key="toggle_alerts"):
                st.session_state.show_alerts = not st.session_state.show_alerts
        with s4: st.markdown('<div class="stat-box"><p class="stat-lbl">System Health</p><p class="stat-val">98%</p></div>', unsafe_allow_html=True)
        
        # DISPLAY URGENT ALERTS IF TOGGLED
        if st.session_state.show_alerts:
            st.markdown("#### 🚨 High Priority Notifications")
            ac1, ac2, ac3 = st.columns(3)
            for idx, p_alert in enumerate(URGENT_PATIENTS):
                with [ac1, ac2, ac3][idx]:
                    st.markdown(f'<div class="alert-card"><strong>Room {p_alert["Room"]}</strong>: {p_alert["Name"]}<br><small>{p_alert["Issue"]}</small></div>', unsafe_allow_html=True)
            st.divider()

        col_main, col_plan = st.columns([2.2, 1], gap="large")
        with col_main:
            img_html = f'<img src="data:image/png;base64,{doctor_b64}" class="profile-img">' if doctor_b64 else '<div class="profile-img" style="background:#93C572; display:flex; align-items:center; justify-content:center; color:white; font-size:40px;">👨‍⚕️</div>'
            st.markdown(f'<div class="profile-card"><div style="display:flex; align-items:center; gap:25px;">{img_html}<div><h1 style="margin:0; color:#124D41;">{user_name}</h1><p style="color:#93C572; font-weight:700;">{DOCTOR_BIO["title"]}</p></div></div><hr style="border:0; border-top:1px solid #eee; margin:25px 0;"><p>{DOCTOR_BIO["desc"]}</p></div>', unsafe_allow_html=True)
            
            with st.expander("💼 Update My Current Status"):
                new_stat = st.segmented_control("Current Status", ["🟢 Available", "🔴 In Surgery", "🟡 In Consultation", "⚪ Away"], default=st.session_state.doc_status)
                if new_stat: st.session_state.doc_status = new_stat

        with col_plan:
            st.markdown("### 📅 Calendar")
            selected_date = str(st.date_input("Schedule", label_visibility="collapsed"))
            if selected_date not in st.session_state.daily_tasks: st.session_state.daily_tasks[selected_date] = []
            if selected_date not in st.session_state.completed_counts: st.session_state.completed_counts[selected_date] = 0

            st.divider()
            st.markdown(f"### 📝 Planning: {selected_date}")
            with st.popover("➕ Add Task"):
                t_input = st.text_input("Task Name")
                if st.button("Save Task"):
                    st.session_state.daily_tasks[selected_date].append(t_input); st.rerun()

            curr_tasks = st.session_state.daily_tasks[selected_date]
            comp = st.session_state.completed_counts[selected_date]
            total = len(curr_tasks) + comp
            st.progress(comp / total if total > 0 else 0)
            
            for i, task in enumerate(curr_tasks):
                c1, c2 = st.columns([5, 1])
                with c1: st.markdown(f'<div class="todo-item">{task}</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("✔️", key=f"d_{selected_date}_{i}"):
                        st.session_state.daily_tasks[selected_date].pop(i)
                        st.session_state.completed_counts[selected_date] += 1; st.rerun()

    elif st.session_state.current_page == "Reservation": st.title("📅 Reservations"); st.table([])
