import streamlit as st
import base64
import os
import time

# 1. Page Config
st.set_page_config(
    page_title="M-FLO | Dashboard", 
    page_icon="⚕️", 
    layout="wide"
)

# 2. Logo Handling with Error Catching
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return "" # Return empty if not found

logo_b64 = get_base64("logo_medical.png")
user_name = "Dr. John Doe" 

# 3. Session State Init
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"

# 4. Global CSS
st.markdown(f"""
    <style>
    /* Global Background */
    .stApp {{ background: radial-gradient(circle at top right, #F0FFF4, #FFFFFF) !important; }}

    /* FIXED TOP BAR - Forced Visibility */
    .top-bar-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        background: #FFFFFF !important;
        border-bottom: 2px solid #93C572;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999999; /* Extremely high to stay on top */
        height: 80px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}

    .logo-box {{ width: 150px; display: flex; align-items: center; }}
    
    .search-box-mid {{
        flex-grow: 1;
        display: flex;
        justify-content: center;
    }}

    .search-bar-input {{
        width: 100%;
        max-width: 500px;
        padding: 12px 20px;
        border-radius: 12px;
        border: 1.5px solid #93C572;
        background: #F9FFF9;
    }}

    .user-profile-right {{
        width: 200px;
        text-align: right;
        color: #124D41;
        font-weight: 700;
        font-size: 18px;
    }}

    /* Main Content Offset so it doesn't hide under top bar */
    .main-wrapper {{
        margin-top: 100px; 
    }}

    /* Dribbble Pop Animation */
    @keyframes springPop {{
        0% {{ opacity: 0; transform: scale(0.9) translateY(30px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .pop-in {{ animation: springPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }}

    /* Sidebar Padding */
    section[data-testid="stSidebar"] {{
        padding-top: 100px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 5. Routing Logic
if not st.session_state.auth:
    # --- PISTACHIO LOGIN PAGE ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:280px;">' if logo_b64 else "<h1>M-FLO</h1>"
    
    st.markdown(f"""
        <div style="border: 3px solid #93C572; border-radius: 40px; padding: 50px; background-color: #F9FFF9; text-align: center; max-width: 500px; margin: auto;">
            {logo_html}
            <div style="color: #93C572; font-weight: 800; font-size: 28px; margin-top: 10px;">67+2 PODCAST</div>
            <div style="color: #124D41; font-size: 55px; font-weight: 900; margin: 0;">M-FLO</div>
            <hr style="border-top: 2px solid #93C572; opacity: 0.2; margin: 30px 0;">
        </div>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        u = st.text_input("Physician ID", placeholder="Enter ID")
        p = st.text_input("Security Key", type="password")
        if st.button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials")

else:
    # --- TOP BAR (Only visible after login) ---
    logo_src = f'data:image/png;base64,{logo_b64}' if logo_b64 else ""
    logo_display = f'<img src="{logo_src}" style="height:45px;">' if logo_b64 else '<b style="color:#93C572;">M-FLO ⚕️</b>'

    st.markdown(f"""
        <div class="top-bar-container">
            <div class="logo-box">{logo_display}</div>
            <div class="search-box-mid">
                <input type="text" class="search-bar-input" placeholder="Search patients or community...">
            </div>
            <div class="user-profile-right">Hello, {user_name}</div>
        </div>
        <div class="main-wrapper"></div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        if st.button("🏠 Homepage", use_container_width=True):
            st.session_state.current_page = "Homepage"
        if st.button("💬 Messages", use_container_width=True):
            st.session_state.current_page = "Messages"
        if st.button("👤 Patients", use_container_width=True):
            st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True):
            st.session_state.current_page = "Reservation"
        if st.button("🤝 Community", use_container_width=True):
            st.session_state.current_page = "Community"
        st.divider()
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ROUTER ---
    if st.session_state.current_page == "Community":
        st.markdown('<div class="pop-in"><h1 style="color: #124D41;">Doctor Community</h1></div>', unsafe_allow_html=True)
        # Reddit Feed Example
        with st.container(border=True):
            st.markdown("### **u/General_Surgeon**")
            st.write("Has anyone used the M-FLO v2.1 for laparoscopic updates?")
            c1, c2, _ = st.columns([1,1,5])
            c1.button("🔼 24")
            c2.button("💬 8")
    
    elif st.session_state.current_page == "Homepage":
        st.markdown('<div class="pop-in"><h1 style="color: #124D41;">Welcome to M-FLO Workspace</h1></div>', unsafe_allow_html=True)
        st.write("Select a menu item from the sidebar to begin.")
