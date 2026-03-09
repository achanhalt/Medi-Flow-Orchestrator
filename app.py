import streamlit as st
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M-FLO | Medi-Flow Orchestrator", 
    page_icon="⚕️", 
    layout="wide"
)

# --- 2. THE CODED LOGO (SVG) ---
# This replaces the PNG. It's a medical microphone icon built with code.
logo_svg = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 10px;">
    <svg width="70" height="70" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="9" y="2" width="6" height="12" rx="3" fill="#93C572"/>
        <path d="M5 10V11C5 14.866 8.13401 18 12 18V18C15.866 18 19 14.866 19 11V10" stroke="#93C572" stroke-width="2" stroke-linecap="round"/>
        <line x1="12" y1="18" x2="12" y2="22" stroke="#93C572" stroke-width="2" stroke-linecap="round"/>
        <line x1="9" y1="22" x2="15" y2="22" stroke="#93C572" stroke-width="2" stroke-linecap="round"/>
        <path d="M12 7V11M10 9H14" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    <div style="color: #93C572; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800; font-size: 22px; letter-spacing: -0.5px; margin-top: 5px;">
        67+2 <span style="color: #124D41;">PODCAST</span>
    </div>
</div>
"""

# --- 3. THE "NUCLEAR" CSS (Fixes Black Boxes & Forces Layout) ---
st.markdown(f"""
    <style>
    /* Force Pure White Background globally */
    .stApp {{ background-color: #FFFFFF !important; color: #2F4F4F !important; }}
    
    /* THE BLACK BOX FIX: Target Streamlit's internal input containers */
    div[data-baseweb="input"], div[data-baseweb="textarea"], .stTextArea textarea {{
        background-color: #FFFFFF !important;
        border: 2px solid #93C572 !important;
        border-radius: 10px !important;
    }}
    
    /* THE TEXT FIX: Force input text to be Dark Green/Charcoal */
    input, textarea {{
        color: #124D41 !important;
        -webkit-text-fill-color: #124D41 !important;
    }}

    /* The Pistachio Frame (The Card) */
    .login-card {{
        border: 2.5px solid #93C572;
        border-radius: 20px;
        padding: 35px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 480px;
        margin: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    /* Title & Label Styling */
    .mflo-header {{ color: #124D41; font-size: 42px; font-weight: 900; margin: 0; line-height: 1.1; }}
    label p {{ color: #124D41 !important; font-weight: bold !important; text-align: left !important; }}

    /* Mint Authenticate Button */
    div.stButton > button {{
        background-color: #98FFD9 !important;
        color: #124D41 !important;
        border: 1.5px solid #93C572 !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        width: 100%;
        padding: 12px;
        border-radius: 10px;
        margin-top: 10px;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #F0F4F2 !important;
        border-right: 1px solid #93C572;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "orders" not in st.session_state:
    st.session_state.orders = []

# --- 5. APP NAVIGATION ---

if not st.session_state.authenticated:
    # --- PAGE 1: LOGIN (EXACT MATCH) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Combined HTML block to keep everything inside the Pistachio frame
    st.markdown(f"""
        <div class="login-card">
            {logo_svg}
            <div class="mflo-header">M-FLO</div>
            <p style="color: #124D41; font-size: 14px; margin-bottom: 20px; font-weight: 500;">
                Medi-Flow Orchestrator v2.1 | Secure Portal
            </p>
            <hr style="border-top: 1.5px solid #93C572; margin-bottom: 25px;">
        </div>
    """, unsafe_allow_html=True)

    # Input column alignment
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        u = st.text_input("Physician ID", placeholder="doctor1")
        p = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Access Denied.")
        
        st.markdown("<p style='text-align:center; font-size:11px; color:gray; margin-top:15px;'>Auth: MD-Level Encrypted Access Only</p>", unsafe_allow_html=True)
        st.info("ℹ️ Demo: doctor1 / mediflow2026")

else:
    # --- PAGE 2: DASHBOARD (CLINICAL WORKSPACE) ---
    with st.sidebar:
        st.markdown(logo_svg, unsafe_allow_html=True)
        st.title("M-FLO v2.1")
        st.write("Logged in: **Dr. John Doe**")
        st.divider()
        if st.button("LOGOUT / LOCK"):
            st.session_state.authenticated = False
            st.session_state.orders = []
            st.rerun()

    st.subheader("⚕️ Patient Consultation Environment")
    
    # 3-Column Layout
    col_pat, col_trans, col_res = st.columns([1, 2, 2])

    with col_pat:
        st.markdown("#### Patient Context")
        with st.container(border=True):
            st.markdown("### **J. Doe**")
            st.caption("ID: #8821 | Male | 45yo")
            st.divider()
            st.error("⚠️ ALLERGY: Penicillin")
            st.warning("⚠️ CONDITION: Hypertension")
            st.info("Topic 4: Retirement Planning") # Using your specific course data

    with col_trans:
        st.markdown("#### Clinical Interface")
        notes = st.text_area("Live Transcript / Notes", height=350, placeholder="Paste clinical context here...")
        
        if st.button("EXECUTE INTENT ANALYSIS"):
            if notes:
                with st.spinner("Analyzing Clinical Data..."):
                    time.sleep(1.5)
                    st.session_state.orders = [
                        {"type": "PHARMACY", "item": "Amoxicillin 500mg", "data": "QTY: 14 | 1x BID", "dest": "Main Pharmacy"},
                        {"type": "LAB", "item": "Chest X-ray", "data": "URGENCY: STAT", "dest": "Radiology"}
                    ]
                    st.toast("Intents Detected!")

    with col_res:
        st.markdown("#### AI-Generated Orders")
        if st.session_state.orders:
            for idx, order in enumerate(st.session_state.orders):
                with st.container(border=True):
                    icon = "💊" if order['type'] == "PHARMACY" else "🔬"
                    st.markdown(f"**{icon} {order['type']} ORDER**")
                    st.code(f"ITEM: {order['item']}\nDATA: {order['data']}\nROUTE: {order['dest']}")
                    
                    c1, c2 = st.columns(2)
                    if c1.button(f"VERIFY & ROUTE", key=f"v_{idx}"):
                        st.success(f"Dispatched to {order['dest']}")
                    c2.button(f"EDIT", key=f"e_{idx}")
        else:
            st.info("Awaiting transcription analysis...")
