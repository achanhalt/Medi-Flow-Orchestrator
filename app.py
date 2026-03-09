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
    "specialty": "Interventional Cardiology & Electrophysiology",
    "desc": """Dr. John Doe is a world-renowned specialist in structural heart disease with over 15 years of clinical excellence. 
    He pioneered the use of minimally invasive valve replacements at M-FLO General and currently serves as the Head of Cardiovascular Research.""",
    "certs": ["MD, Harvard Medical School", "Board Certified in Cardiovascular Disease", "FACC Fellowship", "European Society of Cardiology Member"],
    "stats": [
        {"label": "Surgeries", "value": "1,200+"},
        {"label": "Papers", "value": "84"},
        {"label": "Rating", "value": "4.9/5"}
    ]
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

# 3. FILE ENCODING (PRESERVED)
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

# 4. SESSION STATE (PRESERVED)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"
if "show_alerts" not in st.session_state:
    st.session_state.show_alerts = False

if "urgent_patients" not in st.session_state:
    st.session_state.urgent_patients = [
        {"Room": "402", "Name": "Alice Tan", "Issue": "Tachycardia Spike"},
        {"Room": "ICU-1", "Name": "Bob Smith", "Issue": "Post-Op Arrhythmia"},
        {"Room": "ER-3", "Name": "Charlie Day", "Issue": "Unstable Angina"}
    ]

if "daily_tasks" not in st.session_state:
    st.session_state.daily_tasks = {
        str(date.today()): ["Review Lab Results", "Surgery Consultation", "Department Meeting"]
    }
if "completed_counts" not in st.session_state:
    st.session_state.completed_counts = {}

# 5. CSS (PRESERVED GRADIENT & DESIGN)
st.markdown(f"""
    <style>
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }}
    
    /* SIDEBAR GREEN GRADIENT */
    [data-testid="stSidebar"] {{ 
        background-image: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%) !important; 
    }}

    .stat-box {{ 
        background: #F1F8E9; border-radius: 20px; padding: 20px; text-align: center; border: 1px solid #E1EDD8;
        height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center;
    }}
    .stat-val {{ font-size: 24px; font-weight: 800; color: #124D41; margin: 0; }}
    .stat-lbl {{ font-size: 12px; color: #666; text-transform: uppercase; margin: 0; }}
    
    .profile-card {{ background: white; padding: 40px; border-radius: 35px; border: 1px solid #E0E0E0; box-shadow: 0 15px 50px rgba(0,0,0,0.05); }}
    .profile-img {{ width: 140px; height: 140px; border-radius: 30px; object-fit: cover; border: 4px solid #93C572; }}
    
    .alert-card {{ background: #FFF5F5; border-left: 5px solid #E57373; padding: 15px; border-radius: 12px; margin-bottom: 10px; }}
    .todo-item {{ background:#F1F8E9; padding:12px; border-radius:12px; border-left:5px solid #93C572; margin-bottom:10px; }}
    </style>
    """, unsafe_allow_html=True)

# 6. APP FLOW
if not st.session_state.auth:
    with st.form("login_form"):
        if logo_b64: st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:110px;"></div>', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#124D41; text-align:center;">M-FLO</h1>', unsafe_allow_html=True)
        u = st.text_input("ID", placeholder="Enter ID", label_visibility="collapsed")
        p = st.text_input("Key", type="password", placeholder="Security Key", label_visibility="collapsed")
        if st.form_submit_button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026": st.session_state.auth = True; st.rerun()
else:
    # --- SYMBOL MENU BAR ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Home", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("⚕️ Patients", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("📅 Schedule", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🌍 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🔑 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

    if st.session_state.current_page == "Homepage":
        st.markdown(f'<p style="color:#124D41; font-weight:700;">Hello, {user_name} 👋</p>', unsafe_allow_html=True)

        # STATS ROW
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.markdown('<div class="stat-box"><p class="stat-lbl">Patients Today</p><p class="stat-val">12</p></div>', unsafe_allow_html=True)
        with s2: st.markdown('<div class="stat-box"><p class="stat-lbl">Surgeries</p><p class="stat-val">02</p></div>', unsafe_allow_html=True)
        with s3:
            alert_count = len(st.session_state.urgent_patients)
            color = "#E57373" if alert_count > 0 else "#93C572"
            st.markdown(f'<div class="stat-box" style="border-color:{color};"><p class="stat-lbl">Urgent Alerts</p><p class="stat-val" style="color:{color};">{alert_count:02d}</p></div>', unsafe_allow_html=True)
            if st.button("Manage Alerts", use_container_width=True): st.session_state.show_alerts = not st.session_state.show_alerts; st.rerun()
        with s4: st.markdown('<div class="stat-box"><p class="stat-lbl">System Health</p><p class="stat-val">98%</p></div>', unsafe_allow_html=True)
        
        # URGENT ALERTS (DISMISS LOGIC PRESERVED)
        if st.session_state.show_alerts:
            st.markdown("#### 🚨 Active Urgent Cases")
            for idx, p_alert in enumerate(st.session_state.urgent_patients):
                ac1, ac2 = st.columns([4, 1])
                with ac1: st.markdown(f'<div class="alert-card"><strong>Room {p_alert["Room"]}</strong>: {p_alert["Name"]}</div>', unsafe_allow_html=True)
                with ac2: 
                    if st.button("Resolve ✅", key=f"res_{idx}", use_container_width=True):
                        st.session_state.urgent_patients.pop(idx); st.rerun()
            st.divider()

        # PROFILE & PLANNING
        col_main, col_plan = st.columns([2.3, 1], gap="large")
        with col_main:
            img_html = f'<img src="data:image/png;base64,{doctor_b64}" class="profile-img">' if doctor_b64 else '👨‍⚕️'
            stats_html = "".join([f'<div><span style="font-size:20px; font-weight:700; color:#124D41; display:block;">{s["value"]}</span><small style="color:#888;">{s["label"]}</small></div>' for s in DOCTOR_BIO['stats']])
            
            st.markdown(f"""
                <div class="profile-card">
                    <div style="display:flex; gap:35px;">
                        {img_html}
                        <div>
                            <h1 style="margin:0; color:#124D41;">{user_name}</h1>
                            <p style="color:#93C572; font-weight:700;">{DOCTOR_BIO['title']}</p>
                            <div style="display:flex; gap:30px; border-top:1px solid #f5f5f5; border-bottom:1px solid #f5f5f5; padding:10px 0; margin:15px 0;">{stats_html}</div>
                            <p style="color:#555; font-size:14px;">{DOCTOR_BIO['desc']}</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_plan:
            st.markdown("### 📅 Calendar")
            selected_date = str(st.date_input("Schedule", label_visibility="collapsed"))
            if selected_date not in st.session_state.daily_tasks: st.session_state.daily_tasks[selected_date] = []
            st.divider()
            new_task = st.text_input("Add task", key=f"input_{selected_date}")
            if st.button("Add", key=f"btn_{selected_date}"):
                if new_task: st.session_state.daily_tasks[selected_date].append(new_task); st.rerun()
            for i, task in enumerate(st.session_state.daily_tasks[selected_date]):
                c1, c2 = st.columns([5, 1])
                with c1: st.markdown(f'<div class="todo-item">{task}</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("✔️", key=f"d_{selected_date}_{i}"):
                        st.session_state.daily_tasks[selected_date].pop(i); st.rerun()

    elif st.session_state.current_page == "Reservation": st.title("📅 Reservations"); st.table(RESERVATIONS_DB)
    elif st.session_state.current_page == "Community":
        st.title("🌍 Community")
        for post in COMMUNITY_POSTS: st.markdown(f'<div class="profile-card" style="margin-bottom:15px;"><strong>{post["user"]}</strong>: {post["title"]}</div>', unsafe_allow_html=True)
    elif st.session_state.current_page == "Messages": st.title("💬 Messages"); st.write(MESSAGES_DB)
