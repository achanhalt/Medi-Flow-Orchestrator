import streamlit as st
import base64
import os
import time

st.set_page_config(
    page_title="M-FLO | Secure Access Portal", 
    page_icon="⚕️", 
    layout="wide"
)

def get_base_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base_base64("logo_medical.png")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF !important; }}

    @keyframes samsungFadeInUp {{
        from {{ opacity: 0; transform: translateY(50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animate-in {{
        animation: samsungFadeInUp 0.9s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
    }}
    
    div[data-baseweb="input"], div[data-baseweb="textarea"] {{
        background-color: #FFFFFF !important;
        border: 2px solid #93C572 !important;
        border-radius: 12px !important;
    }}
    
    input {{ color: #124D41 !important; -webkit-text-fill-color: #124D41 !important; }}

    .login-card {{
        border: 3px solid #93C572;
        border-radius: 40px;
        padding: 50px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 500px;
        margin: auto;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }}

    .mflo-header {{ 
        color: #124D41; 
        font-size: 55px; 
        font-weight: 900; 
        margin: 0; 
        letter-spacing: -2px; 
    }}

    div.stButton > button {{
        background: linear-gradient(90deg, #98FFD9, #7CFFCC) !important;
        color: #124D41 !important;
        border: none !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        width: 100%;
        padding: 15px;
        border-radius: 12px;
        transition: all 0.3s ease;
    }}
    
    div.stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(152, 255, 217, 0.5);
    }}

    label p {{ color: #124D41 !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    logo_html = f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{logo_b64}" style="width:280px;"></div>' if logo_b64 else ""

    st.markdown(f"""
        <div class="login-card">
            {logo_html}
            <div style="color: #93C572; font-weight: 800; font-size: 28px; letter-spacing: 1px; margin-top: 10px;">67+2 PODCAST</div>
            <div class="mflo-header">M-FLO</div>
            <p style="color: #124D41; font-size: 16px; font-weight: 500; opacity: 0.8;">
                Medi-Flow Orchestrator v2.1 | Secure Portal
            </p>
            <hr style="border-top: 2px solid #93C572; opacity: 0.2; margin: 30px 0;">
        </div>
    """, unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        u = st.text_input("Physician ID", placeholder="Enter ID")
        p = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied.")
        
        st.markdown("<p style='text-align:center; font-size:12px; color:gray; margin-top:20px;'>Auth: MD-Level Encrypted Access Only</p>", unsafe_allow_html=True)

else:
    with st.sidebar:
        if logo_b64:
            st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" width="120"></div>', unsafe_allow_html=True)
        st.title("M-FLO v2.1")
        st.write("Logged in: **Dr. John Doe**")
        st.divider()
        if st.button("LOGOUT / LOCK"):
            st.session_state.auth = False
            st.rerun()

    st.markdown('<div class="animate-in">', unsafe_allow_html=True)

    st.subheader("⚕️ Patient Consultation Environment")
    
    c1, c2, c3 = st.columns([1, 2, 2])
    
    with c1:
        st.markdown("#### Patient Context")
        with st.container(border=True):
            st.markdown("### **J. Doe**")
            st.caption("ID: #8821 | Male | 45yo")
            st.error("⚠️ ALLERGY: Penicillin")
            st.warning("⚠️ CONDITION: Hypertension")

    with c2:
        st.markdown("#### Clinical Interface")
        notes = st.text_area("Live Transcript", height=350, placeholder="Type notes here...")
        if st.button("EXECUTE ANALYSIS"):
            with st.spinner("Analyzing..."):
                time.sleep(1)
                st.toast("Intents Detected")

    with c3:
        st.markdown("#### AI-Generated Orders")
        st.info("Awaiting analysis...")
    
    st.markdown('</div>', unsafe_allow_html=True)
