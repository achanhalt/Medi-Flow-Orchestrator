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

COMMUNITY_POSTS = [
    {"user": "u/Cardio_Lead", "title": "Hypertension resistance protocols", "content": "Recent studies suggest..."},
    {"user": "u/Heart_Monitor", "title": "M-FLO v2.1 Beta Feedback", "content": "The new UI is much cleaner..."}
]

RESERVATIONS_DB = [
    {"Time": "09:00 AM", "Patient": "Alice Tan", "Status": "Confirmed"},
    {"Time": "11:30 AM", "Patient": "Bob Smith", "Status": "Pending"},
    {"Time": "02:00 PM", "Patient": "Charlie Dean", "Status": "Confirmed"}
]

MESSAGES_DB = {
    "Dr. Sarah Smith": ["Hello Doctor, regarding the lab results...", "I've updated the patient chart."],
    "Nurse Mike": ["Patient in Room 402 is ready for rounds.", "Vitals are stable."]
}

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")

# 3. SESSION STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"
if "active_chat" not in st.session_state:
    st.session_state.active_chat = list(MESSAGES_DB.keys())[0]

# 4. BRUTE-FORCE ALIGNMENT CSS
st.markdown(f"""
    <style>
    /* KILL STREAMLIT TOP SPACE */
    [data-testid="stHeader"] {{ display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        overflow: {"hidden" if not st.session_state.auth else "auto"};
        height: 100vh !important;
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }}

    /* CENTERED LOGIN BOX LOGIC */
    .main .block-container {{
        padding: {"0" if not st.session_state.auth else "2rem"} !important;
        margin: 0 !important;
        height: 100vh;
        display: {"flex" if not st.session_state.auth else "block"};
        align-items: center;
        justify-content: center;
    }}

    div[data-testid="stForm"] {{
        border: 4px solid #93C572 !important; 
        border-radius: 40px !important; 
        padding: 40px !important; 
        background-color: #FFFFFF !important; 
        width: 480px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.05) !important;
        text-align: center;
    }}

    .mflo-header {{ color: #124D41; font-size: 55px; font-weight: 900; margin: 0; letter-spacing: -3px; line-height: 1; }}
    .podcast-header {{ color: #93C572; font-weight: 800; font-size: 20px; margin-bottom: 5px; }}

    /* TOP BAR GREETING */
    .user-greeting {{
        color: #124D41;
        font-size: 20px;
        font-weight: 700;
        margin: 0;
        padding-top: 10px;
    }}

    .stTextInput > div > div {{
        background-color: #f8f9fa !important;
        border: 1.5px solid #93C572 !important;
        border-radius: 10px !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, #93C572, #A8E6CF) !important;
        color: #124D41 !important;
        font-weight: 700 !important;
        border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. GLOBAL SEARCH LOGIC (PRESERVED)
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
    # --- LOGIN VIEW ---
    with st.form("login_form", clear_on_submit=False):
        if logo_b64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:110px; margin-bottom:15px;"></div>', unsafe_allow_html=True)
        st.markdown('<p class="podcast-header">67+2 PODCAST</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="mflo-header">M-FLO</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#888; font-size:11px; margin-bottom:20px;">Medi-Flow Orchestrator v2.1 | Secure Portal</p>', unsafe_allow_html=True)

        u = st.text_input("Physician ID", placeholder="Enter ID", label_visibility="collapsed")
        p = st.text_input("Security Key", type="password", placeholder="Security Key", label_visibility="collapsed")

        submit = st.form_submit_button("AUTHENTICATE SYSTEM")
        if submit:
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied")
        st.markdown('<p style="color:#93C572; font-size:10px; margin-top:10px;">Auth: MD-Level Encrypted Access Only</p>', unsafe_allow_html=True)

else:
    # --- TOP BAR (GREETING + SEARCH) ---
    top_l, top_c, top_r = st.columns([1, 2, 1])
    
    with top_l:
        st.markdown(f'<p class="user-greeting">Hello, {user_name} 👋</p>', unsafe_allow_html=True)
    
    with top_c:
        sq = st.text_input("search", placeholder="Search functions...", key="g_search", label_visibility="collapsed")
        matches = run_global_search(sq)
        if matches:
            for m in matches[:3]:
                if st.button(f"🔍 {m['title']}", key=f"s_{m['title']}", use_container_width=True):
                    st.session_state.current_page = m['page']
                    st.rerun()

    # --- SIDEBAR NAVIGATION (PRESERVED) ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # Dynamic Page Loading
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_page == "Homepage":
        st.line_chart({"bpm": [72, 75, 78, 74, 80]})
    
    elif st.session_state.current_page == "Reservation":
        st.write("### Upcoming Appointments")
        st.table(RESERVATIONS_DB)
        
    elif st.session_state.current_page == "Messages":
        st.write("Messages module loaded.")
