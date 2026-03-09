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

# Mock Data for Search & Messaging
COMMUNITY_POSTS = [
    {"user": "u/Cardio_Lead", "title": "Hypertension resistance protocols", "content": "Recent studies suggest..."},
    {"user": "u/Heart_Monitor", "title": "M-FLO v2.1 Beta Feedback", "content": "The new UI is much cleaner..."}
]

MESSAGES_DB = {
    "Dr. Sarah Smith": ["Hello Doctor, regarding the lab results...", "I've updated the patient chart."],
    "Nurse Mike": ["Patient in Room 402 is ready for rounds.", "Vitals are stable."],
    "Lab Admin": ["The pathology report for ID-992 is ready."]
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

# 4. MINIMALIST CSS
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    .stApp { background: #FDFDFD !important; }

    /* SEARCH BAR VERTICAL CENTERING (FIXED) */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        height: 48px !important; 
        background-color: #F4F4F4 !important;
        border-radius: 10px !important;
        border: 1px solid #E0E0E0 !important;
        padding: 0 !important;
    }

    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 15px !important;
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        line-height: normal !important;
    }

    /* SIDEBAR & NAVIGATION */
    section[data-testid="stSidebar"] { width: 300px !important; }
    
    .sidebar-label {
        color: #888;
        font-size: 11px;
        font-weight: 700;
        margin: 20px 0 8px 15px;
        text-transform: uppercase;
    }

    .stButton > button {
        height: 44px !important;
        border-radius: 8px !important;
        text-align: left !important;
        padding-left: 15px !important;
        font-weight: 500 !important;
        border: 1px solid transparent !important;
    }

    .stButton > button:hover {
        border-color: #93C572 !important;
        color: #93C572 !important;
        background-color: #F9FFF9 !important;
    }

    /* MESSAGING LAYOUT */
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 15px;
        background-color: #F1F1F1;
        margin-bottom: 10px;
        max-width: 80% ;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        padding: 25px !important;
        background: white !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02) !important;
        border: 1px solid #EEE !important;
    }

    h1 { font-size: 32px !important; font-weight: 800 !important; }
    .main .block-container { padding-top: 90px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. SEARCH LOGIC
def run_search(query):
    if not query: return None
    results = []
    # Indexing Pages
    nav = ["Homepage", "Patients", "Reservation", "Messages", "Community"]
    for n in nav:
        if query.lower() in n.lower():
            results.append({"type": "Nav", "title": f"Go to {n}", "page": n})
    # Indexing Community
    for p in COMMUNITY_POSTS:
        if query.lower() in p['title'].lower():
            results.append({"type": "Post", "title": p['title'], "page": "Community"})
    return results

# 6. APP FLOW
if not st.session_state.auth:
    # --- LOGIN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h3 style='text-align:center;'>M-FLO Sign In</h3>", unsafe_allow_html=True)
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        sq = st.text_input("search", placeholder="Search functions or keywords...", label_visibility="collapsed", key="search_bar")
        matches = run_search(sq)
        if matches:
            with st.container():
                for m in matches[:3]:
                    if st.button(f"[{m['type']}] {m['title']}", key=f"s_{m['title']}", use_container_width=True):
                        st.session_state.current_page = m['page']
                        st.rerun()

    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:600; padding-top:10px;'>{user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", width=120)
        st.markdown('<p class="sidebar-label">Main</p>', unsafe_allow_html=True)
        if st.button("🏠 Home", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Schedule", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("✉️ Messages", use_container_width=True): st.session_state.current_page = "Messages"
        
        st.markdown('<p class="sidebar-label">Social</p>', unsafe_allow_html=True)
        if st.button("🤝 Forum", use_container_width=True): st.session_state.current_page = "Community"
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ---
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)

    if st.session_state.current_page == "Messages":
        m_col1, m_col2 = st.columns([1, 2.5])
        
        with m_col1:
            st.markdown("### Contacts")
            for contact in MESSAGES_DB.keys():
                if st.button(f"👤 {contact}", key=f"contact_{contact}", use_container_width=True):
                    st.session_state.active_chat = contact

        with m_col2:
            st.markdown(f"### Chat with {st.session_state.active_chat}")
            with st.container(height=300, border=True):
                for msg in MESSAGES_DB[st.session_state.active_chat]:
                    st.markdown(f'<div class="chat-bubble">{msg}</div>', unsafe_allow_html=True)
            
            st.text_input("Type a message...", key="msg_input")
            st.button("Send ➔")

    elif st.session_state.current_page == "Homepage":
        c1, c2 = st.columns([2, 1])
        with c1:
            with st.container(border=True):
                st.markdown("### Heart Telemetry")
                st.line_chart({"bpm": [72, 74, 73, 75, 74]})
        with c2:
            with st.container(border=True):
                st.markdown("### Tasks")
                st.checkbox("Review lab results")
                st.checkbox("Call Sarah regarding Rounds")

    elif st.session_state.current_page == "Community":
        for post in COMMUNITY_POSTS:
            with st.container(border=True):
                st.markdown(f"**{post['user']}**: {post['title']}")
                st.button("Upvote 🔼", key=f"up_{post['user']}")

    else:
        st.write(f"The {st.session_state.current_page} module is active.")
