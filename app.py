import streamlit as st
import base64
import os

st.set_page_config(
    page_title="M-FLO | Healthcare", 
    page_icon="⚕️", 
    layout="wide"
)

# --- REFINED PROFESSIONAL CSS ---
st.markdown("""
    <style>
    /* 1. Standard Website Scaling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 16px !important;
        color: #124D41;
    }

    .stApp { background: #FDFDFD !important; }

    /* 2. SEARCH BAR FIX: NO CLIPPING */
    /* We target the container to force vertical centering */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
        height: 52px !important; /* Professional standard height */
        background-color: #F4F4F4 !important;
        border-radius: 12px !important;
        border: 1px solid #E0E0E0 !important;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input {
        height: 100% !important;
        font-size: 16px !important;
        text-align: center !important;
        padding: 0 20px !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .stTextInput > div > div:focus-within {
        border-color: #93C572 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(147, 197, 114, 0.1) !important;
    }

    /* 3. SIDEBAR: PROFESSIONAL NAV */
    section[data-testid="stSidebar"] {
        width: 300px !important;
    }

    .sidebar-label {
        color: #888;
        font-size: 12px;
        font-weight: 700;
        margin: 20px 0 8px 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton > button {
        height: 48px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        text-align: left !important;
        padding-left: 15px !important;
        margin-bottom: 4px !important;
        border: 1px solid transparent !important;
    }

    .stButton > button:hover {
        background-color: #F1F8F1 !important;
        color: #93C572 !important;
        border-color: #93C572 !important;
    }

    /* 4. DASHBOARD CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        padding: 30px !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        border: 1px solid #EEE !important;
    }

    /* 5. TITLES */
    h1 { font-size: 36px !important; font-weight: 800 !important; }
    h2 { font-size: 24px !important; font-weight: 700 !important; }
    h3 { font-size: 18px !important; font-weight: 600 !important; }

    /* Top bar adjustment */
    .main .block-container { padding-top: 100px !important; }
    </style>
    """, unsafe_allow_html=True)

# Logic for Auth
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # Minimalist Login
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h2 style='text-align:center;'>M-FLO Access</h2>", unsafe_allow_html=True)
        u = st.text_input("Physician ID")
        p = st.text_input("Security Key", type="password")
        if st.button("Sign In", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
else:
    # --- TOP NAV ---
    t1, t2, t3 = st.columns([1, 2, 1])
    with t2:
        # Centered Search (Fixed Clipping)
        st.text_input("search", placeholder="Search patients or records...", label_visibility="collapsed")
    with t3:
        st.markdown(f"<p style='text-align:right; font-weight:600; padding-top:10px;'>{user_name}</p>", unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### M-FLO")
        st.markdown('<p class="sidebar-label">Menu</p>', unsafe_allow_html=True)
        st.button("📊 Dashboard", use_container_width=True)
        st.button("👥 Patients", use_container_width=True)
        st.button("📅 Appointments", use_container_width=True)
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- CONTENT ---
    st.markdown("<h1>Dashboard Overview</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1], gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown("### Clinical Performance")
            st.line_chart({"Metric": [10, 25, 20, 40, 35, 50]})
    with c2:
        with st.container(border=True):
            st.markdown("### Notifications")
            st.write("Welcome to the refined workspace.")
