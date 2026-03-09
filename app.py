import streamlit as st
import base64
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES (ALL PRESERVED)
user_name = "Dr. John Doe"

DOCTOR_BIO = {
    "title": "Senior Consultant Cardiologist",
    "desc": "Specializing in interventional cardiology and structural heart disease with over 15 years of clinical excellence.",
    "certs": ["MD, Harvard Medical School", "Board Certified in Cardiovascular Disease", "FACC Fellowship"],
    "achievements": ["Best Clinician Award 2025", "50+ Published Research Papers", "Lead Researcher - Project HeartBeat"]
}

# 3. SESSION STATE (PRESERVED & EXPANDED)
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"
if "todos" not in st.session_state:
    st.session_state.todos = ["Review Lab Results - Patient #402", "Surgery Consultation @ 2PM", "Department Meeting"]
if "completed_count" not in st.session_state:
    st.session_state.completed_count = 0

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")

# 4. ENHANCED CSS (MINT THEME + MOTION + PROGRESS)
st.markdown(f"""
    <style>
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    
    [data-testid="stHeader"] {{ display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }}

    /* MINT SIDEBAR */
    [data-testid="stSidebar"] {{
        background-color: #E8F5E9 !important;
        background-image: linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%) !important;
    }}

    /* PROFILE CARD */
    .profile-card {{
        background: white;
        padding: 35px;
        border-radius: 30px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        animation: slideUp 0.6s ease-out;
    }}

    .cert-pill {{
        background: #E8F5E9; color: #2E7D32; padding: 6px 14px; border-radius: 20px;
        font-size: 13px; font-weight: 600; display: inline-block; margin: 4px;
    }}

    /* TO-DO ITEM STYLING */
    .todo-container {{
        background: #F1F8E9; padding: 12px 18px; border-radius: 15px;
        border-left: 6px solid #93C572; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }}

    /* PROGRESS BAR STYLING */
    .stProgress > div > div > div > div {{
        background-color: #93C572 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. GLOBAL SEARCH LOGIC (PRESERVED)
def run_global_search(query):
    if not query: return None
    results = []
    nav_items = ["Homepage", "Patients", "Reservation", "Messages"]
    for item in nav_items:
        if query.lower() in item.lower():
            results.append({"type": "Function", "title": f"Open {item}", "page": item})
    return results

# 6. APP FLOW
if not st.session_state.auth:
    # --- LOGIN PAGE (PRESERVED) ---
    with st.form("login_form"):
        if logo_b64: st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:110px;"></div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; color:#124D41; letter-spacing:-2px;">M-FLO</h1>', unsafe_allow_html=True)
        u = st.text_input("Physician ID", placeholder="Enter ID", label_visibility="collapsed")
        p = st.text_input("Security Key", type="password", placeholder="Security Key", label_visibility="collapsed")
        if st.form_submit_button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True; st.rerun()

else:
    # --- TOP BAR ---
    top_l, top_c, top_r = st.columns([1, 2, 1])
    with top_l: st.markdown(f'<p style="color:#124D41; font-weight:700; font-size:20px;">Hello, {user_name} 👋</p>', unsafe_allow_html=True)
    with top_c:
        sq = st.text_input("search", placeholder="Search dashboard...", key="g_search", label_visibility="collapsed")
        matches = run_global_search(sq)
        if matches and sq:
            for m in matches[:3]:
                if st.button(f"🔍 {m['title']}", key=f"s_{m['title']}", use_container_width=True):
                    st.session_state.current_page = m['page']; st.rerun()

    # --- SIDEBAR (MINT) ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

    # --- HOMEPAGE CONTENT ---
    if st.session_state.current_page == "Homepage":
        col_main, col_plan = st.columns([2.2, 1], gap="large")

        with col_main:
            st.markdown(f"""
                <div class="profile-card">
                    <div style="display: flex; align-items: center; gap: 25px;">
                        <div style="width: 110px; height: 110px; background: linear-gradient(135deg, #93C572, #2E7D32); border-radius: 30px; display: flex; align-items: center; justify-content: center; color: white; font-size: 50px; box-shadow: 0 10px 20px rgba(147,197,114,0.3);">👨‍⚕️</div>
                        <div>
                            <h1 style="margin:0; color:#124D41; font-size:32px;">{user_name}</h1>
                            <p style="color:#93C572; font-weight:700; font-size:18px; margin:0;">{DOCTOR_BIO['title']}</p>
                        </div>
                    </div>
                    <hr style="border:0; border-top:1px solid #eee; margin: 25px 0;">
                    <p style="color:#444; font-size:16px; line-height:1.7;">{DOCTOR_BIO['desc']}</p>
                    <h4 style="color:#124D41;">Credentials & Achievements</h4>
                    {''.join([f'<span class="cert-pill">{c}</span>' for c in DOCTOR_BIO['certs']])}
                    <ul style="color:#444; font-size:15px; line-height:1.8; margin-top:15px;">
                        {''.join([f'<li>{a}</li>' for a in DOCTOR_BIO['achievements']])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
        with col_plan:
            st.markdown("### 📅 Clinical Calendar")
            st.date_input("Schedule", label_visibility="collapsed")
            
            st.divider()
            st.markdown("### 📝 Planning Progress")
            
            # PROGRESS CALCULATION
            total_tasks = len(st.session_state.todos) + st.session_state.completed_count
            progress = (st.session_state.completed_count / total_tasks) if total_tasks > 0 else 0
            st.progress(progress)
            st.caption(f"{st.session_state.completed_count} tasks completed today")

            # Input to add new tasks
            t_input_col, t_btn_col = st.columns([3, 1])
            with t_input_col:
                new_task = st.text_input("Add task", placeholder="New task...", label_visibility="collapsed", key="task_entry")
            with t_btn_col:
                if st.button("Add", use_container_width=True):
                    if new_task: st.session_state.todos.append(new_task); st.rerun()

            # Task List Logic
            for i, task in enumerate(st.session_state.todos):
                c1, c2 = st.columns([5, 1])
                with c1: st.markdown(f'<div class="todo-container">{task}</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("✔️", key=f"done_{i}"):
                        st.session_state.todos.pop(i)
                        st.session_state.completed_count += 1
                        st.rerun()

    elif st.session_state.current_page == "Reservation":
        st.title("Patient Reservations")
        st.info("Your reservation management functions are active.")
