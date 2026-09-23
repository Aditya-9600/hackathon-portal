import streamlit as st
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
import qrcode
import requests
from io import BytesIO
import urllib.parse
import uuid
import datetime
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & INITIALIZATION
# ==============================================================================
st.set_page_config(
    page_title="WCE Electrical Dept | Hackathon 2026",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session States
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_ps' not in st.session_state:
    st.session_state.selected_ps = None
if 'active_ps' not in st.session_state:
    st.session_state.active_ps = None  
if 'ps_locked' not in st.session_state:
    st.session_state.ps_locked = False

def navigate_to(page_name, ps_title=None):
    st.session_state.page = page_name
    if page_name == 'home':
        st.session_state.ps_locked = False
        
    if ps_title:
        st.session_state.selected_ps = ps_title
        st.session_state.ps_locked = True
        
    st.session_state.active_ps = None 

# Function to load Lottie animations (Lightweight JSON graphics)
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ==============================================================================
# 2. THEME STYLING (GLASSMORPHISM & ANIMATIONS)
# ==============================================================================
st.markdown("""
<style>
    /* HIDE STREAMLIT ICONS */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    .stDeployButton {display:none !important;}

    /* Modern Background */
    .stApp {
        background-color: #F8FAFC !important;
        background-image: radial-gradient(#CBD5E1 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Global Text Color */
    .stApp p, .stApp span, .stApp label, .stApp div, .stApp h3, .stApp h4 { 
        color: #0F172A; 
    }

    /* Animated Hero Banner */
    @keyframes gradientPan {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-banner {
        background: linear-gradient(-45deg, #05234A, #0F4C81, #001233, #1E3A8A);
        background-size: 300% 300%;
        animation: gradientPan 10s ease infinite;
        border-radius: 16px;
        padding: 3rem 4rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 40px -10px rgba(5, 35, 74, 0.4);
        border-bottom: 5px solid #FF9933;
        position: relative;
    }
    .hero-banner h1, .hero-banner p, .hero-banner div {
        color: #FFFFFF !important;
    }
    .inst-tag {
        display: inline-block;
        background: rgba(255, 153, 51, 0.9);
        backdrop-filter: blur(5px);
        color: #FFFFFF !important;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-size: 3.5rem; font-weight: 900; line-height: 1.1; margin: 0; letter-spacing: -1px;
    }
    .hero-sub {
        font-size: 1.2rem; opacity: 0.9; margin-top: 1rem; font-weight: 400; line-height: 1.5;
    }
    
    /* Hover Effects for Cards (Glassmorphism) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
    }

    /* Category Badges */
    .badge-hw {
        background-color: #E6F4EA; color: #137333 !important; padding: 6px 16px;
        border-radius: 50px; font-weight: 800; font-size: 0.85rem; border: 1px solid #CEEAD6;
    }
    .badge-sw {
        background-color: #E8F0FE; color: #1967D2 !important; padding: 6px 16px;
        border-radius: 50px; font-weight: 800; font-size: 0.85rem; border: 1px solid #D2E3FC;
    }

    /* Pulsating Primary Buttons */
    @keyframes pulse-btn {
        0% { box-shadow: 0 4px 10px rgba(255, 153, 51, 0.4); }
        50% { box-shadow: 0 8px 20px rgba(255, 153, 51, 0.7); }
        100% { box-shadow: 0 4px 10px rgba(255, 153, 51, 0.4); }
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #FF9933 0%, #E67E22 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 800;
        padding: 0.6rem 2rem;
        animation: pulse-btn 2.5s infinite;
        transition: transform 0.2s;
    }
    .stButton>button[kind="primary"]:hover {
        transform: scale(1.02);
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. PROBLEM STATEMENTS DATABASE (Unchanged)
# ==============================================================================
PROBLEM_STATEMENTS = [
    # DOMAIN 01: Smart Cities & Urbanization
    {"id": 1, "domain": "Smart Cities & Urbanization", "title": "Smart Street Environment & Noise Monitoring", "category": "HARDWARE",
     "desc": "Develop an IoT-based system that dynamically controls streetlight brightness based on real-time pedestrian/vehicle activity while continuously monitoring urban noise levels.",
     "components": ["ESP32-WROOM-32 Dev Board", "MAX9814 Electret Mic Module with AGC", "LDR Photoresistor Module", "IRF520 MOSFET Driver Module", "12V LED Spotlight / Strip", "LM2596 Buck Converter"]},
    # ... (Keep your entire list of 69 problem statements here exactly as you have it) ...
    {"id": 69, "domain": "Agriculture & Aquaculture", "title": "Aquaculture Feeding Rate Optimization Engine", "category": "SOFTWARE",
     "desc": "Develop an algorithmic feeding controller adjusting feeding schedules dynamically based on water temperature, dissolved oxygen, and fish biomass growth.",
     "components": []}
]

ps_titles = [f"PS #{ps['id']:02d}: {ps['title']}" for ps in PROBLEM_STATEMENTS]


# ==============================================================================
# VIEW 1: HOME PAGE (LISTING WITH EXCLUSIVE ACCORDIONS)
# ==============================================================================
if st.session_state.page == 'home':
    
    # Hero Section with Graphic Animation
    st.markdown("""
    <div class="hero-banner">
        <div class="inst-tag">Organized by Department of Electrical Engineering</div>
        <div class="hero-title">WCE National Technical Hackathon 2026</div>
        <div class="hero-sub">Official Portal for Problem Statements, Prototyping Hardware Specifications, and Team Registration. Hosted by Walchand College of Engineering, Sangli.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Insert Lottie Animation below header to save vertical space but add visual flair
    lottie_coding = load_lottieurl("https://lottie.host/e2eb4237-7756-4c46-8dd3-cdbbdd62a26c/zF22eN5D6z.json")
    if lottie_coding:
        colA, colB, colC = st.columns([1, 2, 1])
        with colB:
            st_lottie(lottie_coding, height=200, key="coding_anim")

    # Document Preview & Download
    doc_filename = "Problem_Statements_Updated.docx"
    with st.expander("👁️ Click here to Preview the Official Compendium Document", expanded=False):
        encoded_doc_name = urllib.parse.quote(doc_filename)
        github_raw_url = f"https://github.com/Aditya-9600/hackathon-portal/raw/main/{encoded_doc_name}"
        viewer_url = f"https://docs.google.com/viewer?url={github_raw_url}&embedded=true"
        components.iframe(viewer_url, height=580, scrolling=True)

    if os.path.exists(doc_filename):
        with open(doc_filename, "rb") as fp:
            st.download_button("⬇️ Download Compendium (.docx)", data=fp, file_name=doc_filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    st.markdown("---")
    
    # Filter UI
    f_col1, f_col2, f_col3 = st.columns([1.5, 1, 1.5])
    domains = ["All Domains"] + sorted(list(set(ps["domain"] for ps in PROBLEM_STATEMENTS)))
    with f_col1:
        selected_domain = st.selectbox("Filter by Domain", domains)
    with f_col2:
        selected_cat = st.selectbox("Category", ["All Categories", "HARDWARE", "SOFTWARE"])
    with f_col3:
        search_query = st.text_input("Search Keyword or Title", placeholder="e.g. EV, Solar, Drone")

    filtered_list = PROBLEM_STATEMENTS
    if selected_domain != "All Domains":
        filtered_list = [ps for ps in filtered_list if ps["domain"] == selected_domain]
    if selected_cat != "All Categories":
        filtered_list = [ps for ps in filtered_list if ps["category"] == selected_cat]
    if search_query:
        q = search_query.lower()
        filtered_list = [ps for ps in filtered_list if q in ps["title"].lower() or q in ps["desc"].lower()]

    st.write(f"Showing **{len(filtered_list)}** problem statement(s):")

    # ==========================================
    # CUSTOM ACCORDION (ONLY 1 OPEN AT A TIME)
    # ==========================================
    for ps in filtered_list:
        with st.container(border=True):
            # Header Row: [ Title ] [ Badge ] [ Button ]
            row_c1, row_c2, row_c3 = st.columns([5, 1.5, 2])
            
            with row_c1:
                st.markdown(f"<h4 style='margin-bottom: 0px;'>PS #{ps['id']:02d}: {ps['title']}</h4>", unsafe_allow_html=True)
            
            with row_c2:
                c_tag = "badge-hw" if ps['category'] == "HARDWARE" else "badge-sw"
                st.markdown(f'<div style="margin-top: 5px;"><span class="{c_tag}">{ps["category"]}</span></div>', unsafe_allow_html=True)
                
            with row_c3:
                is_active = st.session_state.active_ps == ps['id']
                btn_lbl = "🔼 Hide Details" if is_active else "🔽 View Details"
                if st.button(btn_lbl, key=f"tgl_{ps['id']}", use_container_width=True, type="secondary"):
                    if is_active:
                        st.session_state.active_ps = None
                    else:
                        st.session_state.active_ps = ps['id']
                    st.rerun() 

            # Expanded Details Content
            if st.session_state.active_ps == ps['id']:
                st.markdown("<hr style='margin: 15px 0px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                st.markdown(f'<span class="{c_tag}">{ps["category"]}</span> &nbsp; <b style="color:#05234A; font-size: 1.1rem;">Domain: {ps["domain"]}</b>', unsafe_allow_html=True)
                st.markdown(f"<p style='margin-top: 15px; font-size: 1.05rem; line-height: 1.6;'>{ps['desc']}</p>", unsafe_allow_html=True)
                
                if ps["category"] == "SOFTWARE":
                    st.info("ℹ️ **There is no hardware or components for this problem statement.** Evaluation will be based on software architecture and performance.")
                else:
                    st.markdown("#### 📦 Expected Prototyping Hardware Components:")
                    col_c1, col_c2 = st.columns(2)
                    mid_pt = (len(ps['components']) + 1) // 2
                    with col_c1:
                        for comp in ps['components'][:mid_pt]:
                            st.markdown(f"🔹 {comp}")
                    with col_c2:
                        for comp in ps['components'][mid_pt:]:
                            st.markdown(f"🔹 {comp}")

                st.markdown("<br>", unsafe_allow_html=True)
                ps_formatted_title = f"PS #{ps['id']:02d}: {ps['title']}"
                
                st.button(
                    f"🚀 Register Now for PS #{ps['id']:02d}", 
                    type="primary", 
                    key=f"btn_reg_{ps['id']}", 
                    on_click=navigate_to, 
                    args=('registration', ps_formatted_title)
                )


# ==============================================================================
# VIEW 2: REGISTRATION & PAYMENT (Unchanged Logic)
# ==============================================================================
elif st.session_state.page == 'registration':
    st.button("⬅️ Back to Problem Statements", on_click=navigate_to, args=('home',))
    
    st.subheader("Team Registration & Checkout")
    st.write("Complete the details below to register your team. **All 5 team members are compulsory**.")
    st.info("💳 **Registration Fee: ₹350 per team**")

    default_ps_index = 0
    if st.session_state.selected_ps in ps_titles:
        default_ps_index = ps_titles.index(st.session_state.selected_ps)

    with st.form("team_registration_form"):
        st.markdown("#### 1. Team Profile")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            team_name = st.text_input("Team Name *", placeholder="e.g. Walchand Innovators")
        with col_t2:
            is_ps_locked = st.session_state.get('ps_locked', False)
            assigned_ps = st.selectbox(
                "Allocated Problem Statement *", 
                ps_titles, 
                index=default_ps_index,
                disabled=is_ps_locked
            )
            if is_ps_locked:
                st.caption("🔒 *Locked based on your selection. To change, go back.*")

        st.markdown("---")
        st.markdown("#### 2. Core Members (All 5 Compulsory)")
        
        st.markdown("**Member 1 (Team Leader)**")
        col_m1a, col_m1b, col_m1c = st.columns(3)
        with col_m1a:
            leader_name = st.text_input("Leader Full Name *")
        with col_m1b:
            leader_email = st.text_input("Leader Email *")
        with col_m1c:
            leader_phone = st.text_input("Leader Phone Number *")

        col_m2, col_m3 = st.columns(2)
        with col_m2:
            m2_name = st.text_input("Member 2 Full Name *")
            m4_name = st.text_input("Member 4 Full Name *")
        with col_m3:
            m3_name = st.text_input("Member 3 Full Name *")
            m5_name = st.text_input("Member 5 Full Name *")

        st.markdown("---")
        st.markdown("#### 3. Custom Component Requests (Optional)")
        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            cat_boards = st.text_input("Microcontrollers & Boards")
            cat_sensors = st.text_input("Sensors & Modules")
            cat_power = st.text_input("Power & Batteries")
        with cat_col2:
            cat_motors = st.text_input("Motors, Relays & Actuators")
            cat_displays = st.text_input("Displays & Indicators")
            cat_misc = st.text_input("Misc / Passives / Wiring")

        st.markdown("---")
        submit_btn = st.form_submit_button("Proceed to Payment Checkout (₹350)", type="primary")

    if submit_btn:
        if not team_name.strip():
            st.error("⚠️ Team Name is required.")
        elif not leader_name.strip() or not leader_email.strip() or not leader_phone.strip():
            st.error("⚠️ Team Leader Name, Email, and Phone Number are all compulsory.")
        elif not m2_name.strip() or not m3_name.strip() or not m4_name.strip() or not m5_name.strip():
            st.error("⚠️ All 5 team member names are compulsory.")
        else:
            hardware_summary = f"""Boards: {cat_boards.strip() or 'None'} | Sensors: {cat_sensors.strip() or 'None'} | Power: {cat_power.strip() or 'None'} | Actuators: {cat_motors.strip() or 'None'} | Displays: {cat_displays.strip() or 'None'} | Misc: {cat_misc.strip() or 'None'}"""
            
            order_id = f"WCE_{uuid.uuid4().hex[:6].upper()}"
            st.session_state["registration_record"] = {
                "order_id": order_id,
                "team_name": team_name,
                "ps": assigned_ps,
                "leader_name": leader_name,
                "leader_email": leader_email,
                "leader_phone": leader_phone,
                "m2_name": m2_name,
                "m3_name": m3_name,
                "m4_name": m4_name,
                "m5_name": m5_name,
                "custom_components": hardware_summary,
                "amount": 350.00,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("✅ Team registration profile validated! Please complete the UPI checkout below.")

    if "registration_record" in st.session_state:
        rec = st.session_state["registration_record"]
        st.markdown("---")
        st.subheader("UPI Payment & 12-Digit UTR Verification")

        col_pay1, col_pay2 = st.columns([1, 1.5])
        with col_pay1:
            upi_id = "9322753587@ptyes"  
            payee_name = "WCE Hackathon 2026"
            upi_string = f"upi://pay?pa={upi_id}&pn={urllib.parse.quote(payee_name)}&am=350.00&cu=INR&tn={rec['order_id']}"

            qr = qrcode.QRCode(version=1, box_size=8, border=3)
            qr.add_data(upi_string)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#05234A", back_color="white")

            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Scan via GPay, PhonePe, or Paytm", width=240)

        with col_pay2:
            st.markdown(f"""
            **Order ID:** `{rec['order_id']}`  
            **Registered Team:** {rec['team_name']}  
            **Selected Statement:** {rec['ps']}  
            **Registration Fee:** **₹350.00**  

            **Instructions:**
            1. Open any UPI application.
            2. Scan the QR code or transfer to the designated UPI ID.
            3. Copy the **12-digit UTR / UPI Transaction Reference Number** from your receipt.
            """)

        with st.form("utr_verification_form"):
            utr_input = st.text_input("Enter 12-Digit UPI Transaction ID / UTR Number *", max_chars=12)
            submit_utr = st.form_submit_button("Submit UTR & Finalize Registration", type="primary")

            if submit_utr:
                if not utr_input.isdigit() or len(utr_input) != 12:
                    st.error("❌ Invalid UTR format. Please provide a valid 12-digit numeric UPI reference number.")
                else:
                    with st.spinner("Connecting to WCE database..."):
                        payload = rec.copy()
                        payload['utr'] = utr_input
                        
                        webhook_url = "https://script.google.com/macros/s/YOUR_APPS_SCRIPT_WEBHOOK_URL_HERE/exec"
                        
                        try:
                            res = requests.post(webhook_url, json=payload, timeout=10)
                            if res.status_code == 200:
                                st.success(f"🎉 Payment reference successfully recorded for Team **{rec['team_name']}**!")
                                st.balloons()
                                st_lottie(load_lottieurl("https://lottie.host/7e09961d-728b-494b-9d41-450f7574548d/7Y2Vd9U0f2.json"), height=150)
                                del st.session_state["registration_record"]
                            else:
                                st.error("Database sync failed.")
                        except Exception as e:
                            st.error("Webhook Error: Ensure your Apps Script Webhook is active.")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1rem 0;">
    Walchand College of Engineering, Sangli • Department of Electrical Engineering<br>
    Built with Python & Streamlit • Autonomous Engineering Institute
</div>
""", unsafe_allow_html=True)
