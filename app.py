import streamlit as st
import base64
import os

# 1. Page Configuration
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

# --- THE "DRIBBBLE-STYLE" BIG & BOLD CSS ---
st.markdown(f"""
    <style>
    /* Global Scaling */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: #124D41;
    }}

    .stApp {{ background: #F8F9FA !important; }}

    /* 1. BOUNCY ENTRANCE ANIMATION */
    @keyframes springPop {{
        0% {{ opacity: 0; transform: scale(0.95) translateY(30px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .pop-in {{ animation: springPop 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }}

    /* 2. TOP BAR & CENTERED SEARCH */
    div[data-testid="stHeader"] {{
        height: 120px !important;
        background-color: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(20px);
        border-bottom: 2px solid #EAEAEA;
        z-index: 999999 !important;
    }}

    .stTextInput > div > div > input {{
        height: 75px !important;
        font-size: 24px !important;
        border-radius: 25px !important;
        border: 2px solid #F0F0F0 !important;
        background-color: #F9F9F9 !important;
        text-align: center !important; 
        padding: 0 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: #93C572 !important;
        box-shadow: 0 0 25px rgba(147, 197, 114, 0.2) !important;
        background-color: #FFFFFF !important;
    }}

    /* 3. BIG SIDEBAR & GLOWING BUTTONS */
    section[data-testid="stSidebar"] {{
        width: 420px !important;
        background-color: #FFFFFF !important;
        border-right: 1px solid #EAEAEA !important;
    }}

    .sidebar-label {{
        color: #ADADAD;
        font-size: 16px;
        font-weight: 700;
        margin: 35px 0 15px 25px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}

    .stButton > button {{
        height: 80px !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        border-radius: 22px !important;
        margin-bottom: 18px !important;
        border: 1px solid transparent !important;
        transition: all 0.3s ease-in-out !important;
        text-align: left !important;
        padding-left: 30px !important;
    }}

    .stButton > button:hover {{
        background-color: #F9FFF9 !important;
        border-color: #93C572 !important;
        color: #93C572 !important;
        transform: translateX(10px);
        box-shadow: 5px 5px 20px rgba(147, 197, 114, 0.1);
    }}

    /* 4. OVERSIZED CONTENT CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white !important;
        border-radius: 50px !important;
        padding: 60px !important;
        box-shadow: 0 40px 80px rgba(0, 0, 0, 0.05) !important;
        border: 1px solid rgba(0,0,0,0.03) !important;
    }}

    h1 {{ font-size: 80px !important; font-weight: 900 !important; letter-spacing: -4px !important; }}
    h2 {{ font-size: 55px !important; font-weight: 800 !important; letter-spacing: -2px !important; }}
    h3 {{ font-size: 38px !important; font-weight: 700 !important; }}

    /* User Greeting Style */
    .user-greet {{
        font-size: 28px;
        font-weight: 800;
        color: #124D41;
        padding-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN GATE ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:400px;">' if logo_b64 else '<h1 style="font-size:100px;">M-FLO</h1>'
    
    st.markdown(f"""
        <div style="border: 5px solid #93C572; border-radius: 70px; padding: 100px; background-color: #F9FFF9; text-align: center; max-width: 800px; margin: auto;" class="pop-in">
            {logo_html}
            <div style="color: #93C572; font-weight: 800; font-size: 40px; margin-top: 30px;">67+2 PODCAST</div>
            <div style="color: #124D41; font-size: 100px; font-weight: 900; margin: 0; letter-spacing: -6px;">M-FLO</div>
        </div>
    """, unsafe_allow_html=True)

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
    t1, t2, t3 = st.columns([1, 3, 1.5])
    with t2:
        # Perfectly Centered Search with Glow Focus
        search_val = st.text_input("search", placeholder="Search functions...", label_visibility="collapsed", key="top_search")
        if search_val:
            pages = ["Homepage", "Patients", "Reservation", "Messages", "Community", "Statistics"]
            for p in pages:
                if search_val.lower() in p.lower():
                    st.session_state.current_page = p

    with t3:
        st.markdown(f"<div class='user-greet' style='text-align:right;'>Hello, {user_name}</div>", unsafe_allow_html=True)

    # --- SIDEBAR (LOGO AT TOP) ---
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        else:
            st.markdown("<h1 style='padding-left:25px;'>M-FLO</h1>", unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-label">Main Menu</p>', unsafe_allow_html=True)
        if st.button("📊 Dashboard", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Appointments", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"

        st.markdown('<p class="sidebar-label">Other Menu</p>', unsafe_allow_html=True)
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        if st.button("📈 Statistics", use_container_width=True): st.session_state.current_page = "Statistics"
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- MAIN CONTENT ---
    st.markdown('<div class="pop-in">', unsafe_allow_html=True)
    st.markdown(f"<h1>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2.2, 1], gap="large")
    
    with col_left:
        with st.container(border=True):
            st.markdown("### **Heart Rate Performance**")
            st.line_chart({"bpm": [72, 75, 80, 77, 73, 79, 74]})
            st.markdown("#### Real-time clinical telemetry active.")

    with col_right:
        with st.container(border=True):
            st.markdown("### **Today's Schedule**")
            st.info("9:30 AM - Jane Doe (Cardiology)")
            st.success("11:00 AM - John Wick (Follow-up)")
            st.button("View Full Calendar", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
