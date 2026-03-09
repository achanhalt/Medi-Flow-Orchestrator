import streamlit as st
import base64
import os

# 1. Page Config
st.set_page_config(
    page_title="M-FLO | Cardiology Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")
user_name = "Dr. John Doe" 

if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"

# --- ADVANCED UI STYLING (Matching your Screenshot) ---
st.markdown(f"""
    <style>
    /* Background Gradient */
    .stApp {{
        background: #F8F9FA !important;
    }}

    /* FIXED TOP BAR */
    div[data-testid="stHeader"] {{
        height: 100px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(15px);
        border-bottom: 1px solid #E0E0E0;
        z-index: 999999 !important;
    }}

    /* SIDEBAR STYLING - Split Menu Look */
    section[data-testid="stSidebar"] {{
        width: 380px !important;
        background-color: #FFFFFF !important;
        border-right: 1px solid #EAEAEA !important;
    }}
    
    .sidebar-section-label {{
        color: #ADADAD;
        font-size: 14px;
        font-weight: 600;
        margin: 20px 0 10px 20px;
        text-transform: uppercase;
    }}

    /* TOP BAR SEARCH */
    .stTextInput > div > div > input {{
        height: 60px !important;
        font-size: 18px !important;
        border-radius: 15px !important;
        border: 1.5px solid #F0F0F0 !important;
        background-color: #F9F9F9 !important;
    }}

    /* DASHBOARD CARDS (Glassmorphism) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white !important;
        border-radius: 30px !important;
        padding: 30px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.03) !important;
        border: 1px solid #F0F0F0 !important;
    }}

    /* ACCENT COLORS (Pistachio Green) */
    .stButton > button {{
        border-radius: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        border-color: #93C572 !important;
        color: #93C572 !important;
    }}

    /* Selected Page Highlight */
    .active-nav {{
        background-color: #124D41 !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN GATE ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:300px;">' if logo_b64 else '<h1 style="color:#124D41">M-FLO</h1>'
    st.markdown(f'<div style="border: 4px solid #93C572; border-radius: 60px; padding: 80px; background-color: #F9FFF9; text-align: center; max-width: 600px; margin: auto;">{logo_html}<div style="color: #124D41; font-size: 60px; font-weight: 900; margin: 0;">M-FLO</div></div>', unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP BAR ---
    t_space, t_search, t_user = st.columns([1, 3, 2])
    with t_search:
        search_val = st.text_input("search_input", placeholder="🔍 Search clinical functions...", label_visibility="collapsed", key="top_search")
        if search_val:
            pages = ["Homepage", "Messages", "Patients", "Reservation", "Community"]
            for p in pages:
                if search_val.lower() in p.lower():
                    st.session_state.current_page = p
    with t_user:
        st.markdown(f"<div style='text-align:right; color:#124D41; font-size:22px; font-weight:700; padding-top:15px;'>Hello, {user_name}</div>", unsafe_allow_html=True)

    # --- SIDEBAR (Modular Look) ---
    with st.sidebar:
        # LOGO TOP LEFT
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", width=180)
        else:
            st.markdown("<h2 style='color:#124D41; padding-left:15px;'>M-FLO</h2>", unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-section-label">Menu</p>', unsafe_allow_html=True)
        if st.button("📊 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"

        st.markdown('<p class="sidebar-section-label">Community & Tools</p>', unsafe_allow_html=True)
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        if st.button("📈 Statistics", use_container_width=True): st.session_state.current_page = "Statistics"
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT AREA: Cardiology Dashboard Look ---
    st.markdown(f"## {st.session_state.current_page} Overview")
    
    if st.session_state.current_page == "Homepage":
        col_main, col_side = st.columns([2.5, 1], gap="medium")
        
        with col_main:
            # Cardiac Visualization Placeholder
            with st.container(border=True):
                st.markdown("### **Heart Performance Analysis**")
                st.caption("Finished analyzing: Real-time telemetry active")
                # Simulated Chart
                st.line_chart({"Heart Rate": [72, 75, 71, 78, 82, 74, 76]})
            
            with st.container(border=True):
                st.markdown("### **Blood Metrics**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Blood Status", "112/75", "Normal")
                c2.metric("Glucose Level", "230/ml", "+2%")
                c3.metric("Blood Count", "80-90", "-5%")

        with col_side:
            with st.container(border=True):
                st.markdown("### **My Schedule**")
                st.write("**Dr. Allison Joy** - 09:30 AM")
                st.write("**Dr. Ellina Roy** - 11:00 AM")
                st.button("View Full Calendar", use_container_width=True)

    elif st.session_state.current_page == "Community":
        st.markdown("### **Doctor Forum**")
        with st.container(border=True):
            st.write("**u/Cardio_Lead:** Thoughts on new M-FLO v2.1 beta?")
            st.button("🔼 Upvote (254)")
