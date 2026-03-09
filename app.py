import streamlit as st
import base64
import os
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M-FLO | Medi-Flow Orchestrator", 
    page_icon="⚕️", 
    layout="wide"
)

# --- 2. LOGO ENCODER (Ensures logo stays inside the HTML frame) ---
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

logo_b64 = get_base64_image("logo_medical.png")

# --- 3. AGGRESSIVE CSS (Fixes Black Boxes & Forces Layout) ---
st.markdown(f"""
    <style>
    /* Force Light Mode Globally */
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
        padding: 40px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 480px;
        margin: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    /* Title & Label Styling */
    .mflo-header {{ color: #124D41; font-size: 42px; font-weight: 900; margin: 0; }}
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
    
    # Everything inside this <div> is styled by the .login-card CSS
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:280px;">' if logo_b64 else '<h1>67+2 PODCAST</h1>'
    
    st.markdown(f"""
        <div class="login-card">
            {logo_html}
            <div class="mflo-header">M-FLO</div>
            <p style="color: #124D41; font-size: 14px; margin-bottom: 20px;">
                Medi-Flow Orchestrator v2.1 | Secure Portal
            </p>
            <hr style="border-top: 1.5px solid #93C572; margin-bottom: 25px;">
        </div>
    """, unsafe_allow_html=True)

    # Placing Streamlit inputs just below the HTML header but aligned with the frame
    col1, col2, col3 = st.columns([1, 1.5, 1])
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
        if logo_b64:
            st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="120">', unsafe_allow_html=True)
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

    with col_trans:
        st.markdown("#### Clinical Interface")
        notes = st.text_area("Live Transcript / Notes", height=350, placeholder="Type clinical notes here...")
        
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
