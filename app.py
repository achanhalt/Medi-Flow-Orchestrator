import streamlit as st
import base64
import os

st.set_page_config(
    page_title="M-FLO | Workspace", 
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

# --- SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"

# --- BIG & BOLD UI STYLING ---
st.markdown(f"""
    <style>
    /* 1. Scale up the base font */
    html, body, [class*="css"] {{
        font-size: 110% !important;
    }}

    .stApp {{ background: radial-gradient(circle at top right, #F0FFF4, #FFFFFF) !important; }}

    /* 2. OVERSIZED TOP BAR */
    header[data-testid="stHeader"] {{
        height: 100px !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(15px);
        border-bottom: 3px solid #93C572;
    }}

    /* 3. BIG LOGO & TEXT */
    .big-logo-text {{
        font-size: 42px !important;
        font-weight: 900 !important;
        color: #124D41;
        letter-spacing: -2px;
    }}

    /* 4. TALL SEARCH BAR */
    .stTextInput input {{
        height: 60px !important;
        font-size: 20px !important;
        border-radius: 20px !important;
        border: 2px solid #93C572 !important;
        padding-left: 25px !important;
    }}

    /* 5. LARGE FLOATING CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 40px !important;
        padding: 45px !important; /* Huge internal padding */
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08) !important;
        border: 1.5px solid rgba(147, 197, 114, 0.2) !important;
        margin-bottom: 30px !important;
    }}

    /* 6. BIG SIDEBAR BUTTONS */
    section[data-testid="stSidebar"] {{
        width: 350px !important;
    }}
    
    div[data-testid="stSidebarNav"] {{
        padding-top: 120px !important;
    }}

    .stButton > button {{
        height: 65px !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        border-radius: 20px !important;
        margin-bottom: 15px !important;
    }}

    /* Oversized Headings */
    h1 {{ font-size: 65px !important; font-weight: 900 !important; letter-spacing: -3px !important; }}
    h2 {{ font-size: 45px !important; font-weight: 800 !important; }}
    h3 {{ font-size: 32px !important; font-weight: 700 !important; }}

    /* Spring Animation */
    @keyframes springPop {{
        0% {{ opacity: 0; transform: scale(0.9) translateY(40px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .pop-in {{ animation: springPop 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    # --- PISTACHIO LOGIN (Oversized) ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:350px;">' if logo_b64 else '<h1 class="big-logo-text">M-FLO</h1>'
    st.markdown(f'<div style="border: 4px solid #93C572; border-radius: 60px; padding: 80px; background-color: #F9FFF9; text-align: center; max-width: 700px; margin: auto;">{logo_html}<div style="color: #93C572; font-weight: 800; font-size: 35px; margin-top: 20px;">67+2 PODCAST</div><div style="color: #124D41; font-size: 80px; font-weight: 900; margin: 0; letter-spacing: -4px;">M-FLO</div></div>', unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()

else:
    # --- TOP BAR (LOGO TOP LEFT, SEARCH CENTER, GREETING RIGHT) ---
    t1, t2, t3 = st.columns([1.5, 3, 1.5])
    
    with t1:
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", width=180) # Big Logo
        else:
            st.markdown('<div class="big-logo-text">M-FLO</div>', unsafe_allow_html=True)

    with t2:
        # Tall Search Bar with Suggestions
        search_val = st.text_input("", placeholder="🔍 Search clinical functions...", label_visibility="collapsed")
        if search_val:
            pages = ["Homepage", "Messages", "Patients", "Reservation", "Community"]
            suggestions = [p for p in pages if search_val.lower() in p.lower()]
            if suggestions:
                cols = st.columns(len(suggestions))
                for idx, s in enumerate(suggestions):
                    if cols[idx].button(f"Go to {s}", key=f"sug_{s}", use_container_width=True):
                        st.session_state.current_page = s
                        st.rerun()

    with t3:
        st.markdown(f"<div style='text-align:right; padding-top:20px; color:#124D41; font-size:24px;'>Hello, <b>{user_name}</b></div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("👤 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT AREA ---
    st.markdown(f'<div class="pop-in">', unsafe_allow_html=True)
    
    if st.session_state.current_page == "Community":
        st.markdown("<h1>Medical Community</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### Create Post")
            st.text_area("What's on your mind?", height=150, label_visibility="collapsed")
            st.button("Post to Forum", type="primary", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### **u/Cardio_Expert**")
            st.write("Does anyone have tips for scaling high-fidelity dashboards in Streamlit?")
            c1, c2, _ = st.columns([0.2, 0.2, 0.6])
            c1.button("🔼 254", use_container_width=True)
            c2.button("💬 86", use_container_width=True)

    elif st.session_state.current_page == "Homepage":
        st.markdown("<h1>Clinical Dashboard</h1>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            with st.container(border=True):
                st.markdown("### **Next Patient**")
                st.write("Jane Doe • 09:45 AM")
                st.button("Start Consultation", use_container_width=True)
        with col_b:
            with st.container(border=True):
                st.markdown("### **System Status**")
                st.success("M-FLO Engine: Active")
                st.info("2 Messages Waiting")

    st.markdown('</div>', unsafe_allow_html=True)
