import streamlit as st
import base64
import os
import time

st.set_page_config(
    page_title="M-FLO | Clinical Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo_medical.png")

# --- PREMIUM DRIBBBLE STYLING ---
st.markdown(f"""
    <style>
    /* 1. Fluid Background */
    .stApp {{
        background: radial-gradient(circle at 20% 20%, #F0FFF4 0%, #FFFFFF 50%, #F7FFF9 100%) !important;
    }}

    /* 2. Dribbble "Spring" Animation Physics */
    @keyframes dribbblePop {{
        0% {{ opacity: 0; transform: scale(0.7) translateY(60px); filter: blur(10px); }}
        60% {{ opacity: 1; transform: scale(1.03) translateY(-10px); filter: blur(0px); }}
        80% {{ transform: scale(0.98) translateY(2px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    /* Staggered Entrance */
    .pop-1 {{ animation: dribbblePop 1s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; opacity: 0; }}
    .pop-2 {{ animation: dribbblePop 1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s forwards; opacity: 0; }}
    .pop-3 {{ animation: dribbblePop 1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s forwards; opacity: 0; }}

    /* 3. Floating Glass Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(15px) saturate(180%) !important;
        border: 1px solid rgba(147, 197, 114, 0.15) !important;
        border-radius: 32px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.05) !important;
        padding: 30px !important;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        transform: translateY(-12px) scale(1.01);
        box-shadow: 0 40px 80px -15px rgba(147, 197, 114, 0.2) !important;
        border-color: #93C572 !important;
    }}

    /* 4. Minimalist Navigation Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid #F0F0F0;
    }}

    /* 5. Typography & Accents */
    .workspace-title {{
        color: #124D41;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 5px;
    }}
    
    .status-badge {{
        background: #E8F5E9;
        color: #2E7D32;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 20px;
    }}

    /* Input & Button Refinement */
    div.stButton > button {{
        background: linear-gradient(135deg, #98FFD9 0%, #7CFFCC 100%) !important;
        color: #124D41 !important;
        border: none !important;
        font-weight: 800 !important;
        border-radius: 18px !important;
        padding: 18px !important;
        box-shadow: 0 10px 20px -5px rgba(124, 255, 204, 0.4) !important;
    }}

    .login-card {{
        border: 2px solid #93C572;
        border-radius: 40px;
        padding: 60px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 500px;
        margin: auto;
    }}
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

# --- APP NAVIGATION ---
if not st.session_state.auth:
    # --- PISTACHIO LOGIN ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{logo_b64}" style="width:280px;"></div>' if logo_b64 else ""

    st.markdown(f"""
        <div class="login-card">
            {logo_html}
            <div style="color: #93C572; font-weight: 800; font-size: 28px; margin-top: 15px;">67+2 PODCAST</div>
            <div style="color: #124D41; font-size: 55px; font-weight: 900; margin: 0; letter-spacing: -2px;">M-FLO</div>
            <hr style="border-top: 1px solid #93C572; opacity: 0.2; margin: 30px 0;">
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
    # --- DRIBBBLE-STYLE DASHBOARD ---
    with st.sidebar:
        if logo_b64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="110"></div>', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.button("🏥 Overview", use_container_width=True)
        st.button("📁 Records", use_container_width=True)
        st.button("⚙️ Settings", use_container_width=True)
        st.divider()
        if st.button("Secure Logout"):
            st.session_state.auth = False
            st.rerun()

    # Header section
    st.markdown('<div class="pop-1"><span class="status-badge">● SYSTEM ACTIVE</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="pop-1"><p class="workspace-title">Clinical Intelligence</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1.2, 2], gap="large")

    with col_a:
        st.markdown('<div class="pop-2">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### **Active Patient**")
            st.caption("Jane Doe • 45 Y.O. • Female")
            st.divider()
            st.error("💊 **Critical Allergy:** Penicillin")
            st.info("📊 **Vitals:** Normal (Last Sync 2m ago)")
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("Open Electronic Health Record", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="pop-3">', unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("### **Smart Orders**")
            st.write("AI-detected clinical actions for verification:")
            
            # Interactive Order Cards
            st.checkbox("Lisinopril 10mg Oral Tablet", value=True)
            st.checkbox("Metabolic Panel (Blood Test)", value=True)
            st.checkbox("Schedule 6-Month Follow-up", value=False)
            
            st.divider()
            st.button("✨ Approve & Dispatch Orders", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Bottom Full-Width Section
    st.markdown('<div class="pop-3">', unsafe_allow_html=True)
    with st.container(border=True):
        st.write("### **Intelligence Summary**")
        st.success("All clinical databases are in sync. System suggests reviewing the latest lab results for potential electrolyte imbalance.")
    st.markdown('</div>', unsafe_allow_html=True)
