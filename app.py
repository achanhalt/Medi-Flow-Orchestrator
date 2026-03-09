import streamlit as st
import base64
import os

st.set_page_config(
    page_title="M-FLO | Intelligence Workspace", 
    page_icon="⚕️", 
    layout="wide"
)

def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_base64("logo_medical.png")
user_name = "Dr. John Doe" 

# --- SESSION STATE ---
if "auth" not in st.session_state:
    st.session_state.auth = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Homepage"

# --- UI STYLING ---
st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(circle at top right, #F0FFF4, #FFFFFF) !important; }}

    /* Top Bar Styling */
    header[data-testid="stHeader"] {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #93C572;
    }}

    /* Dribbble Animation */
    @keyframes springPop {{
        0% {{ opacity: 0; transform: scale(0.95) translateY(20px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}
    .pop-in {{ animation: springPop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards; }}

    /* Floating Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 24px !important;
        border: 1px solid rgba(147, 197, 114, 0.2) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.auth:
    # --- PISTACHIO LOGIN (Preserved) ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:280px;">' if logo_b64 else "<h1>M-FLO</h1>"
    st.markdown(f'<div style="border: 3px solid #93C572; border-radius: 40px; padding: 50px; background-color: #F9FFF9; text-align: center; max-width: 500px; margin: auto;">{logo_html}<div style="color: #93C572; font-weight: 800; font-size: 28px; margin-top: 10px;">67+2 PODCAST</div><div style="color: #124D41; font-size: 55px; font-weight: 900; margin: 0;">M-FLO</div></div>', unsafe_allow_html=True)

    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        u = st.text_input("Physician ID", placeholder="doctor1")
        p = st.text_input("Security Key", type="password", placeholder="mediflow2026")
        if st.button("AUTHENTICATE SYSTEM", use_container_width=True):
            if u == "doctor1" and p == "mediflow2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Access Denied")

else:
    # --- TOP BAR WITH SEARCH SUGGESTIONS ---
    t1, t2, t3 = st.columns([1, 2, 1])
    
    with t1:
        if logo_b64:
            st.image(f"data:image/png;base64,{logo_b64}", width=110)
        else:
            st.markdown("### **M-FLO ⚕️**")

    with t2:
        # Search Container with "Suggestions"
        search_val = st.text_input("", placeholder="🔍 Search functions...", label_visibility="collapsed")
        
        if search_val:
            pages = ["Homepage", "Messages", "Patients", "Reservation", "Community"]
            suggestions = [p for p in pages if search_val.lower() in p.lower()]
            
            if suggestions:
                cols = st.columns(len(suggestions))
                for idx, s in enumerate(suggestions):
                    if cols[idx].button(f"Go to {s}", key=f"sug_{s}"):
                        st.session_state.current_page = s
                        st.rerun()

    with t3:
        st.markdown(f"<div style='text-align:right; padding-top:10px; color:#124D41;'>Hello, <b>{user_name}</b></div>", unsafe_allow_html=True)

    st.divider()

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("### **Navigation**")
        if st.button("🏠 Homepage", use_container_width=True): st.session_state.current_page = "Homepage"
        if st.button("💬 Messages", use_container_width=True): st.session_state.current_page = "Messages"
        if st.button("👤 Patients", use_container_width=True): st.session_state.current_page = "Patients"
        if st.button("📅 Reservation", use_container_width=True): st.session_state.current_page = "Reservation"
        if st.button("🤝 Community", use_container_width=True): st.session_state.current_page = "Community"
        st.divider()
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    # --- PAGE CONTENT ---
    st.markdown(f'<div class="pop-in">', unsafe_allow_html=True)
    
    if st.session_state.current_page == "Community":
        st.markdown("## **🤝 Medical Community**")
        
        # Reddit-style Post Creator
        with st.container(border=True):
            st.write("### Create a Post")
            st.text_area("Ask a question to your peers...", placeholder="e.g. Seeking advice on post-op recovery protocols for v2.1 users", label_visibility="collapsed")
            st.button("Post to Community", type="primary")

        st.markdown("---")
        
        # Post 1
        with st.container(border=True):
            st.markdown("#### **u/Aris_Software**")
            st.write("Sharing my latest findings on the software engineering integration for clinical workflows.")
            c1, c2, _ = st.columns([0.15, 0.15, 0.7])
            if c1.button("🔼 142", key="up1"): st.toast("Upvoted!")
            if c2.button("💬 38", key="comm1"): st.info("Loading comments...")

    elif st.session_state.current_page == "Homepage":
        st.markdown("## **Workspace Overview**")
        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.write("### Recent Patients")
                st.caption("Jane Doe • ID #9921")
                st.button("View Records", key="home_p")
        with col_b:
            with st.container(border=True):
                st.write("### System Status")
                st.success("M-FLO Clinical Engine: Online")
                
    else:
        st.markdown(f"## {st.session_state.current_page}")
        st.write("This section is currently being synced with clinical data.")

    st.markdown('</div>', unsafe_allow_html=True)
