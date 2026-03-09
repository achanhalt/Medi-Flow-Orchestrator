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

COMMUNITY_POSTS = [
    {"user": "u/Cardio_Lead", "title": "Hypertension resistance protocols", "content": "Recent studies suggest..."},
    {"user": "u/Heart_Monitor", "title": "M-FLO v2.1 Beta Feedback", "content": "The new UI is much cleaner..."}
]

RESERVATIONS_DB = [
    {"Time": "09:00 AM", "Patient": "Alice Tan", "Status": "Confirmed"},
    {"Time": "11:30 AM", "Patient": "Bob Smith", "Status": "Pending"}
]

MESSAGES_DB = {
    "Dr. Sarah Smith": ["Hello Doctor, regarding the lab results...", "I've updated the patient chart."],
    "Nurse Mike": ["Patient in Room 402 is ready for rounds.", "Vitals are stable."]
}

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

# 4. SESSION STATE (LINKED CALENDAR & PLANNING)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"

# New Dictionary to store tasks per date
if "daily_tasks" not in st.session_state:
    st.session_state.daily_tasks = {
        str(date.today()): ["Review Lab Results", "Surgery Consultation", "Department Meeting"]
    }
if "completed_counts" not in st.session_state:
    st.session_state.completed_counts = {}

# 5. CSS (UNIFIED DESIGN PRESERVED)
st.markdown(f"""
    <style>
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
        overflow: {"hidden" if not st.session_state.auth else "auto"};
    }}
    .main .block-container {{
        padding: {"0" if not st.session_state.auth else "2rem"} !important;
        display: {"flex" if not st.session_state.auth else "block"};
        align-items: center; justify-content: center; height: 100vh;
    }}
    div[data-testid="stForm"] {{
        border: 4px solid #93C572 !important; border-radius: 40px !important; padding: 40px !important; 
        background-color: #FFFFFF !important; width: 480px !important; text-align: center;
    }}
    .mflo-header {{ color: #124D41; font-size: 55px; font-weight: 900; margin: 0; letter-spacing: -3px; }}
    .podcast-header {{ color: #93C572; font-weight: 800; font-size: 20px; }}
    [data-testid="stSidebar"] {{ background-image: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%) !important; }}
    .profile-card {{ background: white; padding: 35px; border-radius: 30px; border: 1px solid #E0E0E0; box-shadow: 0 10px 40px rgba(0,0,0,0.04); }}
    .profile-img {{ width: 110px; height: 110px; border-radius: 25px; object-fit: cover; border: 3px solid #93C572; }}
    .todo-item {{ background:#F1F8E9; padding:12px; border-radius:12px; border-left:5px solid #93C572; margin-bottom:10px; }}
    </style>
    """, unsafe_allow_html=True)

# 6. APP FLOW
if not st.session_state.auth:
    with st.form("login_form", clear_on_submit=False):
        if logo_b64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:110px; margin-bottom:15px;"></div>', unsafe_allow_html=True)
        st.markdown('<p class="podcast-header">67+2 PODCAST</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="mflo-header">M-FLO</h1>', unsafe_allow_html=True)
        u = st.text_input("ID", placeholder="Enter ID", label_visibility="collapsed")
        p = st.text_input("Key", type="password", placeholder="Security Key", label_visibility="collapsed")
        if st.form_submit_button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True; st.rerun()
else:
    t1, t2, t3 = st.columns([1, 2, 1])
    with t1: st.markdown(f'<p style="color:#124D41; font-weight:700; font-size:18px;">Hello, {user_name} 👋</p>', unsafe_allow_html=True)
    
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
        col_main, col_plan = st.columns([2.2, 1], gap="large")
        with col_main:
            img_html = f'<img src="data:image/png;base64,{doctor_b64}" class="profile-img">' if doctor_b64 else '<div class="profile-img" style="background:#93C572; display:flex; align-items:center; justify-content:center; color:white; font-size:40px;">👨‍⚕️</div>'
            st.markdown(f"""<div class="profile-card"><div style="display:flex; align-items:center; gap:25px;">{img_html}<div><h1 style="margin:0; color:#124D41;">{user_name}</h1><p style="color:#93C572; font-weight:700;">{DOCTOR_BIO['title']}</p></div></div><hr style="border:0; border-top:1px solid #eee; margin:25px 0;"><p style="color:#444; line-height:1.7;">{DOCTOR_BIO['desc']}</p><h4 style="color:#124D41;">Academic Credentials</h4>{''.join([f'<span style="background:#E8F5E9; color:#2E7D32; padding:5px 12px; border-radius:15px; font-size:12px; font-weight:600; margin:4px; display:inline-block;">{c}</span>' for c in DOCTOR_BIO['certs']])}</div>""", unsafe_allow_html=True)
            
        with col_plan:
            st.markdown("### 📅 Calendar")
            selected_date = str(st.date_input("Schedule", label_visibility="collapsed"))
            
            # --- LINKED PLANNING LOGIC ---
            if selected_date not in st.session_state.daily_tasks:
                st.session_state.daily_tasks[selected_date] = []
            if selected_date not in st.session_state.completed_counts:
                st.session_state.completed_counts[selected_date] = 0

            st.divider()
            st.markdown(f"### 📝 Planning: {selected_date}")
            
            # Add new task for specific day
            new_task = st.text_input("Add task for this day", key=f"input_{selected_date}")
            if st.button("Add", key=f"btn_{selected_date}"):
                if new_task:
                    st.session_state.daily_tasks[selected_date].append(new_task)
                    st.rerun()

            # Progress Bar for selected day
            current_tasks = st.session_state.daily_tasks[selected_date]
            comp_count = st.session_state.completed_counts[selected_date]
            total = len(current_tasks) + comp_count
            st.progress(comp_count / total if total > 0 else 0)
            
            for i, task in enumerate(current_tasks):
                c1, c2 = st.columns([5, 1])
                with c1: st.markdown(f'<div class="todo-item">{task}</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("✔️", key=f"d_{selected_date}_{i}"):
                        st.session_state.daily_tasks[selected_date].pop(i)
                        st.session_state.completed_counts[selected_date] += 1
                        st.rerun()

    elif st.session_state.current_page == "Reservation":
        st.title("📅 Reservations"); st.table(RESERVATIONS_DB)
    elif st.session_state.current_page == "Community":
        st.title("🤝 Medical Community")
        for post in COMMUNITY_POSTS: st.markdown(f'<div class="profile-card" style="margin-bottom:15px;"><strong>{post["user"]}</strong>: {post["title"]}</div>', unsafe_allow_html=True)
    elif st.session_state.current_page == "Messages":
        st.title("✉️ Messages"); st.write(MESSAGES_DB)
