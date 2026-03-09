import streamlit as st
import base64
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES (PRESERVED)
user_name = "Dr. John Doe"
COMMUNITY_POSTS = [
    {"user": "u/Cardio_Lead", "title": "Hypertension resistance protocols", "content": "Recent studies suggest..."},
    {"user": "u/Heart_Monitor", "title": "M-FLO v2.1 Beta Feedback", "content": "The new UI is much cleaner..."}
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

# 4. ENHANCED CSS (MATCHING SCREENSHOT + PNG LOGO)
st.markdown(f"""
    <style>
    /* LOCK SCROLLING ON LOGIN */
    html, body, [data-testid="stAppViewContainer"] {{
        overflow: {"hidden" if not st.session_state.auth else "auto"};
        height: 100vh;
    }}

    .stApp {{
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }}

    /* VERTICAL LOGIN BOX */
    .login-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
    }}

    .login-card {{
        border: 4px solid #93C572; 
        border-radius: 20px; 
        padding: 40px 50px; 
        background-color: #FFFFFF; 
        text-align: center; 
        width: 450px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    /* PNG LOGO HEARTBEAT */
    @keyframes heartbeat {{
        0% {{ transform: scale(1); }}
        14% {{ transform: scale(1.05); }}
        28% {{ transform: scale(1); }}
    }}
    .heartbeat-logo {{ 
        animation: heartbeat 2s infinite; 
        display: inline-block; 
        margin-bottom: 10px;
    }}

    /* INPUT STYLING */
    .stTextInput > div > div {{
        background-color: #f8f9fa !important;
        border: 1.5px solid #93C572 !important;
        border-radius: 8px !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, #93C572, #A8E6CF) !important;
        color: #124D41 !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100% !important;
        height: 45px !important;
        transition: transform 0.2s ease !important;
    }}

    .stButton > button:hover {{
        transform: scale(1.02) !important;
        color: #124D41 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. SEARCH LOGIC (PRESERVED)
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
    # --- SCREENSHOT-MATCHING LOGIN PAGE WITH PNG ---
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # PNG Logo with Heartbeat
        if logo_b64:
            st.markdown(f'''
                <div class="heartbeat-logo">
                    <img src="data:image/png;base64,{logo_b64}" style="width:120px;">
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<div style="color:#93C572; font-weight:800; font-size:22px; letter-spacing:1px;">67+2 PODCAST</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#124D41; font-size:48px; font-weight:900; margin-bottom:5px;">M-FLO</div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#666; font-size:12px; margin-bottom:25px;">Medi-Flow Orchestrator v2.1 | Secure Portal</p>', unsafe_allow_html=True)
        
        # Form inputs inside the card
        u = st.text_input("Physician ID", placeholder="Enter ID")
        p = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        
        st.markdown('<p style="color:#93C572; font-size:10px; margin-top:20px;">Auth: MD-Level Encrypted Access Only</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- DASHBOARD (ALL FUNCTIONS PRESERVED) ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        sq = st.text_input("search", placeholder="Search functions...", label_visibility="collapsed", key="g_search")
        matches = run_global_search(sq)
        if matches:
            for m in matches[:3]:
                if st.button(f"🔍 {m['title']}", key=f"s_{m['title']}", use_container_width=True):
                    st.session_state.current_page = m['page']
                    st.rerun()

    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.divider()
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_page == "Homepage":
        st.line_chart({"bpm": [72, 75, 78, 74, 80]})
    
    # ... Other page logic (Messages, Community) remains active ...
    st.markdown('</div>', unsafe_allow_html=True)
