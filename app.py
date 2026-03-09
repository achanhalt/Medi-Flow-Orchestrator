import streamlit as st
import base64
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES
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

# 4. ENHANCED ANIMATION & COLOR THEME CSS
st.markdown("""
    <style>
    /* SOFT THEME BACKGROUND */
    .stApp {
        background: radial-gradient(circle at top right, #F9FFF9, #FDFDFD) !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    /* KEYFRAMES FOR MOTIONS */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes buttonPop {
        0% { transform: scale(1); }
        50% { transform: scale(0.98); }
        100% { transform: scale(1); }
    }

    .page-transition { animation: fadeInUp 0.5s ease-out forwards; }

    /* SEARCH BAR FIX: NO CLIPPING */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        height: 50px !important; 
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1.5px solid #E0E0E0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }

    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 16px !important;
        height: 100% !important;
        line-height: 50px !important; 
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }

    /* LOGIN PAGE DESIGN (PRESERVED) */
    .login-card {
        border: 6px solid #93C572; 
        border-radius: 80px; 
        padding: 100px; 
        background-color: #F9FFF9; 
        text-align: center; 
        max-width: 900px; 
        margin: auto;
        box-shadow: 0 20px 50px rgba(147, 197, 114, 0.15);
    }

    /* BUTTON MOTIONS */
    .stButton > button {
        height: 48px !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding-left: 15px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        background-color: white !important;
        border: 1px solid #EEE !important;
    }

    .stButton > button:hover {
        border-color: #93C572 !important;
        color: #93C572 !important;
        background-color: #F9FFF9 !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(147, 197, 114, 0.1) !important;
    }

    .stButton > button:active {
        transform: scale(0.95) !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] { 
        width: 320px !important; 
        background-color: white !important;
        border-right: 1px solid #F0F0F0;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        padding: 30px !important;
        background: white !important;
        border: 1px solid #EEE !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important;
    }
    
    .main .block-container { padding-top: 80px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. SEARCH LOGIC
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
    # --- PRESERVED LOGIN DESIGN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:300px;">' if logo_b64 else ""
    
    st.markdown(f"""
        <div class="login-card">
            {logo_html}
            <div style="color: #93C572; font-weight: 800; font-size: 35px; margin-top: 20px;">67+2 PODCAST</div>
            <div style="color: #124D41; font-size: 100px; font-weight: 900; margin: 0; letter-spacing: -5px;">M-FLO</div>
        </div>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV & SEARCH ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        sq = st.text_input("search", placeholder="Search functions...", label_visibility="collapsed", key="g_search")
        matches = run_global_search(sq)
        if matches:
            st.markdown('<div class="page-transition">', unsafe_allow_html=True)
            for m in matches[:3]:
                if st.button(f"🔍 {m['title']}", key=f"s_{m['title']}", use_container_width=True):
                    st.session_state.current_page = m['page']
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:700; padding-top:10px;'>Hello, {user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR (ANIMATED BUTTONS) ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT AREA (WITH TRANSITION ANIMATION) ---
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)

    if st.session_state.current_page == "Messages":
        m1, m2 = st.columns([1, 2.5])
        with m1:
            st.markdown("### Contacts")
            for contact in MESSAGES_DB.keys():
                if st.button(f"👤 {contact}", key=f"c_{contact}", use_container_width=True):
                    st.session_state.active_chat = contact
        with m2:
            with st.container(height=400, border=True):
                st.markdown(f"**Chat: {st.session_state.active_chat}**")
                for msg in MESSAGES_DB[st.session_state.active_chat]:
                    st.markdown(f'<div style="background:#F1F8F1; padding:12px; border-radius:10px; margin-bottom:8px; border:1px solid #EEE;">{msg}</div>', unsafe_allow_html=True)
            st.text_input("Reply...", key="chat_in", label_visibility="collapsed")
            st.button("Send Message ➔")

    elif st.session_state.current_page == "Homepage":
        with st.container(border=True):
            st.markdown("### Heart Rate Telemetry")
            st.line_chart({"bpm": [72, 75, 78, 74, 80]})
    
    elif st.session_state.current_page == "Community":
        for post in COMMUNITY_POSTS:
            with st.container(border=True):
                st.write(f"**{post['user']}**: {post['title']}")
                st.button("Upvote 🔼", key=f"up_{post['user']}")

    st.markdown('</div>', unsafe_allow_html=True)
