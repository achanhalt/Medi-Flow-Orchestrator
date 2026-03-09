import streamlit as st
import base64
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES (RESTORED ALL)
user_name = "Dr. John Doe"

DOCTOR_BIO = {
    "title": "Senior Consultant Cardiologist",
    "desc": "Specializing in interventional cardiology and structural heart disease with over 15 years of clinical excellence.",
    "certs": ["MD, Harvard Medical School", "Board Certified in Cardiovascular Disease", "FACC Fellowship"],
    "achievements": ["Best Clinician Award 2025", "50+ Published Research Papers", "Lead Researcher - Project HeartBeat"]
}

# Restored Community & Messages Data
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

# 3. SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"
if "todos" not in st.session_state:
    st.session_state.todos = ["Review Lab Results", "Surgery Consultation", "Department Meeting"]
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0
if "active_chat" not in st.session_state:
    st.session_state.active_chat = list(MESSAGES_DB.keys())[0]

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")

# 4. CSS (MINT THEME + ANIMATIONS)
st.markdown(f"""
    <style>
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stAppViewContainer"] {{ background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important; }}

    /* MINT SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: #E8F5E9 !important;
        background-image: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%) !important;
    }}
    
    /* CARDS */
    .profile-card, .community-card {{
        background: white; padding: 30px; border-radius: 25px; border: 1px solid #E0E0E0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); animation: slideUp 0.6s ease-out;
    }}
    .todo-container {{
        background: #F1F8E9; padding: 10px 15px; border-radius: 12px;
        border-left: 5px solid #93C572; margin-bottom: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. GLOBAL SEARCH (RESTORED ALL NAV ITEMS)
def run_global_search(query):
    if not query: return None
    results = []
    nav_items = ["Homepage", "Patients", "Reservation", "Messages", "Community"]
    for item in nav_items:
        if query.lower() in item.lower():
            results.append({"type": "Function", "title": f"Open {item}", "page": item})
    return results

# 6. APP FLOW
if not st.session_state.auth:
    with st.form("login_form"):
        st.markdown('<h1 style="text-align:center; color:#124D41;">M-FLO</h1>', unsafe_allow_html=True)
        u = st.text_input("ID", placeholder="doctor1")
        p = st.text_input("Key", type="password", placeholder="mediflow2026")
        if st.form_submit_button("AUTHENTICATE"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True; st.rerun()
else:
    # --- TOP BAR ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t1: st.markdown(f'<p style="color:#124D41; font-weight:700; font-size:18px;">Hello, {user_name} 👋</p>', unsafe_allow_html=True)
    with t2:
        sq = st.text_input("search", placeholder="Search dashboard...", key="g_search", label_visibility="collapsed")
        matches = run_global_search(sq)
        if matches and sq:
            for m in matches[:2]:
                if st.button(f"🔍 {m['title']}", key=f"s_{m['title']}"):
                    st.session_state.current_page = m['page']; st.rerun()

    # --- MINT SIDEBAR (ALL FUNCTIONS RESTORED) ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

    # --- PAGES ---
    if st.session_state.current_page == "Homepage":
        c_main, c_plan = st.columns([2.2, 1], gap="large")
        with c_main:
            st.markdown(f'<div class="profile-card"><h2>{user_name}</h2><p>{DOCTOR_BIO["desc"]}</p></div>', unsafe_allow_html=True)
        with c_plan:
            st.markdown("### 📝 Planning")
            total = len(st.session_state.todos) + st.session_state.completed_count
            st.progress(st.session_state.completed_count / total if total > 0 else 0)
            for i, task in enumerate(st.session_state.todos):
                col1, col2 = st.columns([4, 1])
                col1.markdown(f'<div class="todo-container">{task}</div>', unsafe_allow_html=True)
                if col2.button("✔️", key=f"d_{i}"):
                    st.session_state.todos.pop(i); st.session_state.completed_count += 1; st.rerun()

    elif st.session_state.current_page == "Community":
        st.title("🤝 Medical Community")
        for post in COMMUNITY_POSTS:
            st.markdown(f'<div class="community-card"><h4>{post["title"]}</h4><p>{post["content"]}</p></div>', unsafe_allow_html=True)

    elif st.session_state.current_page == "Messages":
        st.title("✉️ Physician Inbox")
        st.write(MESSAGES_DB[st.session_state.active_chat])

    elif st.session_state.current_page == "Reservation":
        st.table(RESERVATIONS_DB)
