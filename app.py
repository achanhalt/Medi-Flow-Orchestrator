import streamlit as st
import base64
import os

# 1. PAGE CONFIG
st.set_page_config(
    page_title="M-FLO | Healthcare Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. GLOBAL VARIABLES (Fixes NameError)
user_name = "Dr. John Doe" 

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

# 4. REFINED PROFESSIONAL CSS (Balanced Scaling)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    .stApp { background: #FDFDFD !important; }

    /* SEARCH BAR FIX: VERTICAL CENTERING WITHOUT CLIPPING */
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
        line-height: normal !important;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #93C572 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(147, 197, 114, 0.1) !important;
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
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding-left: 20px !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #F1F8F1 !important;
        color: #93C572 !important;
        border-color: #93C572 !important;
        transform: translateX(5px);
    }

    /* CARDS & HEADINGS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        padding: 30px !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        border: 1px solid #EEE !important;
    }

    h1 { font-size: 38px !important; font-weight: 800 !important; color: #124D41; }
    h2 { font-size: 26px !important; font-weight: 700 !important; }
    h3 { font-size: 20px !important; font-weight: 600 !important; }

    .main .block-container { padding-top: 100px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. APP LOGIC
if not st.session_state.auth:
    # --- LOGIN PAGE ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:250px;">' if logo_b64 else "<h1>M-FLO</h1>"
    
    with st.container(border=True):
        st.markdown(f"<div style='text-align:center;'>{logo_html}<br><h3>67+2 PODCAST | M-FLO</h3></div>", unsafe_allow_html=True)
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        # Centered Search (Functional)
        search_val = st.text_input("search", placeholder="Search functions or patients...", label_visibility="collapsed", key="top_search")
        if search_val:
            pages = ["Homepage", "Patients", "Reservation", "Messages", "Community"]
            for p in pages:
                if search_val.lower() in p.lower():
                    st.session_state.current_page = p

    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:700; font-size:18px; padding-top:10px;'>Hello, {user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR (LOGO + MENU) ---
    with st.sidebar:
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        
        st.markdown('<p class="sidebar-label">Main Menu</p>', unsafe_allow_html=True)
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"

        st.markdown('<p class="sidebar-label">Analytics</p>', unsafe_allow_html=True)
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- MAIN CONTENT AREA ---
    st.markdown(f"<h1>{st.session_state.current_page} Overview</h1>", unsafe_allow_html=True)
    
    if st.session_state.current_page == "Community":
        with st.container(border=True):
            st.markdown("### **Medical Forum**")
            st.text_area("Share a clinical insight...", height=100)
            st.button("Post to Community", type="primary")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.write("**u/Cardio_Expert:** Tips for high-fidelity dashboards?")
            st.button("🔼 254 Upvotes", key="uv1")

    elif st.session_state.current_page == "Homepage":
        c_left, c_right = st.columns([2, 1], gap="medium")
        with c_left:
            with st.container(border=True):
                st.markdown("### Heart Rate Performance")
                st.line_chart({"bpm": [72, 75, 71, 80, 78, 82, 74]})
        with c_right:
            with st.container(border=True):
                st.markdown("### Today's Schedule")
                st.info("09:30 AM - Jane Doe")
                st.success("11:00 AM - John Wick")

    else:
        with st.container(border=True):
            st.write(f"Content for {st.session_state.current_page} is loading...")
