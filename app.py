import streamlit as st
import base64
import os

st.set_page_config(
    page_title="M-FLO | Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

# --- LOGO LOADING ---
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

# --- UPDATED CSS FOR CENTERED SEARCH ---
st.markdown(f"""
    <style>
    .stApp {{ background: #F8F9FA !important; }}

    /* TOP BAR VERTICAL ALIGNMENT */
    div[data-testid="column"] {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* CENTERED SEARCH BAR TEXT */
    .stTextInput > div > div > input {{
        height: 65px !important;
        font-size: 20px !important;
        border-radius: 20px !important;
        border: 1.5px solid #E0E0E0 !important;
        background-color: #F9F9F9 !important;
        
        /* THE MAGIC LINES FOR CENTERING */
        text-align: center !important; 
    }}

    /* SIDEBAR SECTION LABELS */
    .sidebar-label {{
        color: #ADADAD;
        font-size: 14px;
        font-weight: 700;
        margin: 25px 0 10px 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* BIG DASHBOARD CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: white !important;
        border-radius: 40px !important;
        padding: 40px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #F0F0F0 !important;
    }}
    
    /* BIG SIDEBAR BUTTONS */
    section[data-testid="stSidebar"] {{ width: 380px !important; }}
    .stButton > button {{
        height: 65px !important;
        font-size: 22px !important;
        border-radius: 18px !important;
        font-weight: 700 !important;
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
    # Using 3 columns to force the search bar into the exact center
    t1, t2, t3 = st.columns([1.5, 3, 1.5])
    
    with t2:
        search_val = st.text_input("search_input", placeholder="Search patients, messages, community...", label_visibility="collapsed", key="top_search")
        if search_val:
            pages = ["Homepage", "Patients", "Reservation", "Messages", "Community", "Statistics"]
            for p in pages:
                if search_val.lower() in p.lower():
                    st.session_state.current_page = p

    with t3:
        st.markdown(f"<div style='text-align:right; color:#124D41; font-size:24px; font-weight:700;'>Hello, {user_name}</div>", unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", use_container_width=True)
        else:
            st.markdown("<h1 style='color:#124D41; padding-left:20px;'>M-FLO</h1>", unsafe_allow_html=True)
        
        st.markdown('<p class="sidebar-label">Main Menu</p>', unsafe_allow_html=True)
        if st.button("📊 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("👥 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        
        st.markdown('<p class="sidebar-label">Analytics</p>', unsafe_allow_html=True)
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        if st.button("📈 Statistics", use_container_width=True): st.session_state.current_page = "Statistics"
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ---
    st.markdown(f"## {st.session_state.current_page} Overview")
    
    if st.session_state.current_page == "Homepage":
        with st.container(border=True):
            st.markdown("### Heart Rate Performance")
            st.line_chart({"bpm": [70, 72, 85, 78, 74, 80, 72]})
