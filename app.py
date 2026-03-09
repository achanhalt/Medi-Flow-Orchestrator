import streamlit as st
import base64
import os

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="M-FLO | Secure Portal", layout="centered")

# --- 2. THE "FORCE LIGHT MODE" CSS FIX ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = get_base64("logo_medical.png")

st.markdown(f"""
    <style>
    /* 1. Force the entire app background to white */
    .stApp {{ background-color: #FFFFFF !important; }}

    /* 2. THE BLACK BOX FIX: Target the specific input container */
    div[data-baseweb="input"] {{
        background-color: #FFFFFF !important; /* Force background white */
        border: 1.5px solid #93C572 !important; /* Pistachio border */
        border-radius: 10px !important;
    }}

    /* 3. THE TEXT FIX: Force input text to be Dark Green/Charcoal */
    input {{
        color: #124D41 !important;
        -webkit-text-fill-color: #124D41 !important; /* Overrides browser dark mode */
    }}

    /* 4. The Pistachio Frame */
    .login-card {{
        border: 2.5px solid #93C572;
        border-radius: 20px;
        padding: 40px;
        background-color: #F9FFF9;
        text-align: center;
        max-width: 450px;
        margin: auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }}

    /* Labels styling */
    label p {{
        color: #124D41 !important;
        font-weight: bold !important;
    }}

    /* Mint Button styling */
    div.stButton > button {{
        background-color: #98FFD9 !important;
        color: #124D41 !important;
        border: 1.5px solid #93C572 !important;
        font-weight: 800 !important;
        width: 100%;
        border-radius: 10px;
        padding: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE UI ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    # We combine logo and title into the frame
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:280px;">' if logo_b64 else '<h1 style="color:#124D41;">M-FLO</h1>'
    
    st.markdown(f"""
        <div class="login-card">
            {logo_html}
            <h1 style="color: #124D41; margin-top: 0;">M-FLO</h1>
            <p style="color: #124D41; opacity: 0.8;">Medi-Flow Orchestrator v2.1 | Secure Portal</p>
            <hr style="border-top: 1px solid #93C572; margin-bottom: 25px;">
        </div>
    """, unsafe_allow_html=True)

    # Inputs (positioned to align with the frame)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user = st.text_input("Physician ID", placeholder="doctor1")
        pw = st.text_input("Security Key", type="password", placeholder="••••••••")
        
        if st.button("AUTHENTICATE SYSTEM"):
            if user == "doctor1" and pw == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        
        st.markdown("<p style='text-align:center; font-size:12px; color:gray; margin-top:10px;'>Auth: MD-Level Encrypted Access Only</p>", unsafe_allow_html=True)
        st.info("Demo: doctor1 / mediflow2026")

else:
    st.success("Access Granted. Redirecting to Dashboard...")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
