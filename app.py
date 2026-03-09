import streamlit as st
import base64
import os

# 1. PAGE CONFIG
st.set_page_config(
    page_title="M-FLO | Global Clinical Search", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES
user_name = "Dr. John Doe" 
# This simulates your community database for search
COMMUNITY_POSTS = [
    {"user": "Cardio_Expert", "title": "High-fidelity dashboard tips", "content": "Streamlit CSS is powerful..."},
    {"user": "Nurse_Joy", "title": "Patient intake protocols", "content": "New protocols for 2026..."},
    {"user": "Dr_Strange", "title": "AI in Radiology", "content": "How M-FLO automates scans..."}
]

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

# 4. REFINED CSS (Includes Search Results Styling)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    /* SEARCH BAR VERTICAL CENTERING FIX */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        height: 54px !important; 
        background-color: #F4F4F4 !important;
        border-radius: 12px !important;
        border: 1.5px solid #E0E0E0 !important;
        padding: 0 !important;
    }

    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 16px !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
        line-height: normal !important;
    }

    /* AI SUGGESTIONS CONTAINER */
    .search-results-box {
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid #EEE;
        padding: 10px;
        margin-top: 5px;
        position: absolute;
        width: 100%;
        z-index: 1000;
    }

    /* SIDEBAR & BUTTONS */
    section[data-testid="stSidebar"] { width: 320px !important; }
    .stButton > button {
        height: 48px !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding-left: 20px !important;
    }
    
    .stButton > button:hover {
        border-color: #93C572 !important;
        color: #93C572 !important;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        padding: 30px !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. SEARCH LOGIC FUNCTION
def global_search(query):
    if not query:
        return None
    
    results = []
    # 1. Search Pages (Functions)
    pages = ["Homepage", "Patients", "Reservation", "Messages", "Community"]
    for p in pages:
        if query.lower() in p.lower():
            results.append({"type": "Function", "title": f"Go to {p}", "action": p})
    
    # 2. Search Community Keywords
    for post in COMMUNITY_POSTS:
        if query.lower() in post["title"].lower() or query.lower() in post["content"].lower():
            results.append({"type": "Community", "title": post["title"], "action": "Community"})
            
    return results

# 6. APP FLOW
if not st.session_state.auth:
    # --- LOGIN ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align:center;'>M-FLO Secure Access</h2>", unsafe_allow_html=True)
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV WITH SMART SEARCH ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        search_query = st.text_input("search", placeholder="Search functions, keywords, or AI insights...", label_visibility="collapsed", key="global_search_input")
        
        # AI Auto-Suggestions UI
        matches = global_search(search_query)
        if matches:
            with st.container():
                st.markdown('<div class="search-results-box">', unsafe_allow_html=True)
                for m in matches[:5]: # Show top 5 matches
                    label = f"[{m['type']}] {m['title']}"
                    if st.button(label, key=f"res_{m['title']}", use_container_width=True):
                        st.session_state.current_page = m['action']
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:700; padding-top:10px;'>Hello, {user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.button("🏠 Homepage", use_container_width=True, on_click=lambda: setattr(st.session_state, 'current_page', 'Homepage'))
        st.button("👥 Patients", use_container_width=True, on_click=lambda: setattr(st.session_state, 'current_page', 'Patients'))
        st.button("🤝 Community", use_container_width=True, on_click=lambda: setattr(st.session_state, 'current_page', 'Community'))
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ---
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_page == "Homepage":
        with st.container(border=True):
            st.markdown("### Clinical Overview")
            st.line_chart({"bpm": [72, 75, 78, 74, 80]})
            
    elif st.session_state.current_page == "Community":
        for post in COMMUNITY_POSTS:
            with st.container(border=True):
                st.markdown(f"**{post['user']}**: {post['title']}")
                st.write(post['content'])
