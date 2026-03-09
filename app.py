import streamlit as st
import base64
import os
import time

st.set_page_config(
    page_title="M-FLO | Workflow", 
    page_icon="⚕️", 
    layout="wide"
)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo_medical.png")

# --- UI STYLING (The Dribbble Effect) ---
st.markdown(f"""
    <style>
    /* 1. Background Gradient */
    .stApp {{
        background: radial-gradient(circle at top right, #F7FFF9, #FFFFFF) !important;
    }}

    /* 2. Dribbble Spring Animation */
    @keyframes springBounce {{
        0% {{ opacity: 0; transform: scale(0.9) translateY(40px); }}
        60% {{ transform: scale(1.03) translateY(-10px); }}
        80% {{ transform: scale(0.98) translateY(2px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    /* Staggered entrance classes */
    .stagger-1 {{ animation: springBounce 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; opacity: 0; }}
    .stagger-2 {{ animation: springBounce 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s forwards; opacity: 0; }}
    .stagger-3 {{ animation: springBounce 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s forwards; opacity: 0; }}

    /* 3. Floating "Glass" Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(8px);
        border: 1.5px solid rgba(147, 197, 114, 0.1) !important;
        border-radius: 30px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04) !important;
        padding: 25px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-10px) scale(1.02);
        border-color: #93C572 !important;
        box-shadow: 0 30px 60px rgba(147, 197, 114, 0.15) !important;
    }}

    /* 4. Custom Login Card (Preserved from your reference) */
    .login-card {{
        border: 3px solid #93C572;
        border-radius: 40px;
        padding: 50px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 500px;
        margin: auto;
    }}

    /* 5. Clean Buttons & Inputs */
    div.stButton > button {{
        background: linear-gradient(90deg, #98FFD9, #7CFFCC) !important;
        color: #124D41 !important;
        border: none !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        padding: 12px 20px !important;
        transition: 0.3s;
    }}

    .mflo-title {{
        color: #124D41;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 20px;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
        border-right: 1px solid #F0F0F0;
    }}
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# --- AUTHENTICATION LOGIC ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{logo_b64}" style="width:280px;"></div>' if logo_b64 else ""

    st.markdown(f"""
        <div class="login-card">
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
                st.error("Access Denied.")

else:
    # --- DASHBOARD (Dribbble Layout) ---
    with st.sidebar:
        if logo_b64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="100"></div>', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.button("🏥 Dashboard", use_container_width=True)
        st.button("📁 Patient Files", use_container_width=True)
        st.button("⚙️ Settings", use_container_width=True)
        st.divider()
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    # Header with Bouncy Entrance
    st.markdown('<div class="stagger-1"><p class="mflo-title">Clinical Workspace</p></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 2], gap="large")

    with col_a:
        st.markdown('<div class="stagger-2">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### **Active Patient**")
            st.caption("Jane Doe • ID #9921")
            st.divider()
            st.error("💊 **Allergy:** Penicillin")
            st.info("📊 **Condition:** Hypertension")
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Full Medical History", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="stagger-3">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### **Clinical Orders**")
            st.write("Review and verify the following orders:")
            st.checkbox("Lisinopril 10mg - 1x Daily", value=True)
            st.checkbox("Blood Analysis - CBC", value=True)
            st.checkbox("Chest X-Ray - Routine", value=False)
            st.divider()
            st.button("✨ Sync with Hospital Records", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Full Width Bottom Card
    st.markdown('<div class="stagger-3">', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("### **AI Insight Summary**")
        st.success("Patient showing stable vital signs. No immediate intervention required.")
    st.markdown('</div>', unsafe_allow_html=True)
