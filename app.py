import streamlit as st
import time

st.set_page_config(
    page_title="M-FLO | Medi-Flow Orchestrator", 
    page_icon="⚕️", 
    layout="wide"
)

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

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF !important; color: #2F4F4F !important; }}

    @keyframes samsungFadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(40px); 
        }}
        to {{
            opacity: 1;
            transform: translateY(0); 
        }}
    }}

    .animate-in {{
        animation: samsungFadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
    }}
    
    div[data-baseweb="input"], div[data-baseweb="textarea"], .stTextArea textarea {{
        background-color: #FFFFFF !important;
        border: 2px solid #93C572 !important;
        border-radius: 10px !important;
    }}
    
    input, textarea {{
        color: #124D41 !important;
        -webkit-text-fill-color: #124D41 !important;
    }}

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

    .mflo-header {{ color: #124D41; font-size: 42px; font-weight: 900; margin: 0; }}
    label p {{ color: #124D41 !important; font-weight: bold !important; text-align: left !important; }}

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

    section[data-testid="stSidebar"] {{
        background-color: #F0F4F2 !important;
        border-right: 1px solid #93C572;
    }}
    </style>
    """, unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
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

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u = st.text_input("Physician ID", placeholder="doctor1")
        p = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE SYSTEM"):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials. Access Denied.")
        
        st.markdown("<p style='text-align:center; font-size:11px; color:gray; margin-top:15px;'>Auth: MD-Level Encrypted Access Only</p>", unsafe_allow_html=True)
        st.info("ℹ️ Demo: doctor1 / mediflow2026")

else:
    with st.sidebar:
        st.markdown(logo_svg, unsafe_allow_html=True)
        st.title("M-FLO v2.1")
        st.write("Logged in: **Dr. John Doe**")
        st.divider()
        if st.button("LOGOUT / LOCK"):
            st.session_state.auth = False
            st.rerun()

    st.markdown('<div class="animate-in">', unsafe_allow_html=True)

    st.subheader("⚕️ Patient Consultation Environment")
    
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
        notes = st.text_area("Live Transcript / Notes", height=350, placeholder="Start typing consultation context...")
        
        if st.button("EXECUTE INTENT ANALYSIS"):
            if notes:
                with st.spinner("Decoding clinical path..."):
                    time.sleep(1.5)
                    st.toast("Intents detected!")

    with col_res:
        st.markdown("#### AI-Generated Orders")
        st.info("Awaiting transcription analysis...")
    
    st.markdown('</div>', unsafe_allow_html=True)
