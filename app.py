import streamlit as st
import base64
import os

# 1. PAGE SETUP
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL DATA & VARIABLES (Fixes NameError)
user_name = "Dr. John Doe"

# Mock Community Data for keyword search
COMMUNITY_POSTS = [
    {"user": "u/Cardio_Lead", "title": "Hypertension resistance protocols", "content": "Recent studies suggest..."},
    {"user": "u/Heart_Monitor", "title": "M-FLO v2.1 Beta Feedback", "content": "The new UI is much cleaner..."},
    {"user": "u/Clinical_Tech", "title": "Software Engineering in Clinics", "content": "Integrating Python with EHR..."}
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

# 4. BALANCED PROFESSIONAL CSS
st.markdown("""
    <style>
    /* Website-Standard Scaling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    .stApp { background: #FDFDFD !important; }

    /* SEARCH BAR FIX: FLEXBOX CENTERING (No Cutting) */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 50px !important; 
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
        line-height: normal !important; /* Prevents vertical clipping */
    }

    /* AI SUGGESTION BOX */
    .search-suggestion-box {
        background-color: white;
        border: 1px solid #EEE;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        padding: 10px;
        margin-top: 5px;
        position: relative;
        z-index: 999;
    }

    /* SIDEBAR & BUTTONS */
    section[data-testid="stSidebar"] { width: 320px !important; }
    
    .sidebar-label {
        color: #888;
        font-size: 12px;
        font-weight: 700;
        margin: 20px 0 8px 15px;
        text-transform: uppercase;
    }

    .stButton > button {
        height: 48px !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding-left: 20px !important;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #93C572 !important;
        background-color: #F9FFF9 !important;
        color: #93C572 !important;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        padding: 30px !important;
        background: white !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        border: 1px solid #EEE !important;
    }

    h1 { font-size: 38px !important; font-weight: 800 !important; }
    .main .block-container { padding-top: 100px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. SEARCH ENGINE LOGIC
def run_global_search(query):
    if not query: return None
    results = []
    
    # Check Pages (Functions)
    nav_items = ["Homepage", "Patients", "Reservation", "Messages", "Community"]
    for item in nav_items:
        if query.lower() in item.lower():
            results.append({"type": "Function", "title": f"Open {item}", "page": item})
            
    # Check Community Content (Keywords)
    for post in COMMUNITY_POSTS:
        if query.lower() in post["title"].lower() or query.lower() in post["content"].lower():
            results.append({"type": "Community", "title": post["title"], "page": "Community"})
            
    return results

# 6. APP FLOW
if not st.session_state.auth:
    # --- LOGIN SCREEN ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align:center;'>M-FLO Authentication</h2>", unsafe_allow_html=True)
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV & AI SEARCH ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        # Search Bar with Fixed Centering
        sq = st.text_input("search", placeholder="Search functions, patients, or keywords...", label_visibility="collapsed", key="global_search")
        
        matches = run_global_search(sq)
        if matches:
            st.markdown('<div class="search-suggestion-box">', unsafe_allow_html=True)
            for m in matches[:4]: # Limit to 4 results
                btn_label = f"[{m['type']}] {m['title']}"
                if st.button(btn_label, key=f"s_{m['title']}", use_container_width=True):
                    st.session_state.current_page = m['page']
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:700; padding-top:10px;'>Hello, {user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        if logo_b64: st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        st.markdown('<p class="sidebar-label">Main Menu</p>', unsafe_allow_html=True)
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        
        st.markdown('<p class="sidebar-label">Analytics</p>', unsafe_allow_html=True)
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ROUTING ---
    st.markdown(f"<h1>{st.session_state.current_page} Overview</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_page == "Homepage":
        c_l, c_r = st.columns([2, 1])
        with c_l:
            with st.container(border=True):
                st.markdown("### Heart Performance")
                st.line_chart({"bpm": [72, 75, 71, 80, 78]})
        with c_r:
            with st.container(border=True):
                st.markdown("### My Schedule")
                st.info("09:30 AM - Jane Doe")
                st.success("11:00 AM - Approved: John Wick")

    elif st.session_state.current_page == "Community":
        st.markdown("### **Active Forum Discussions**")
        for post in COMMUNITY_POSTS:
            with st.container(border=True):
                st.write(f"**{post['user']}**: {post['title']}")
                st.caption(post['content'])
                st.button("Upvote", key=f"up_{post['user']}")

    else:
        with st.container(border=True):
            st.write(f"The module for {st.session_state.current_page} is ready for data integration.")
