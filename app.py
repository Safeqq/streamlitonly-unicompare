import streamlit as st
from utils.auth import do_logout, get_username, init_session, is_admin, is_authenticated

st.set_page_config(
    page_title="Unicompare",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp { background: #faf9f6; }

    .neo-card {
        background: #fff;
        border: 4px solid #000;
        box-shadow: 6px 6px 0 0 #000;
        padding: 1.5rem;
        border-radius: 0;
        transition: all 0.2s;
    }
    .neo-card:hover {
        transform: translate(-2px, -2px);
        box-shadow: 8px 8px 0 0 #000;
    }

    .neo-btn {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 3px solid #000;
        box-shadow: 4px 4px 0 0 #000;
        background: #FFCC00;
        color: #000 !important;
        cursor: pointer;
        transition: all 0.15s;
        text-decoration: none;
        font-size: 0.875rem;
    }
    .neo-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0 0 #000;
    }
    .neo-btn-red {
        background: #FF3333;
        color: #fff !important;
    }
    .neo-btn-blue {
        background: #40A9FF;
        color: #fff !important;
    }
    .neo-btn-white {
        background: #fff;
        color: #000 !important;
    }

    .neo-badge {
        display: inline-block;
        padding: 0.2rem 0.75rem;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        border: 3px solid #000;
        box-shadow: 3px 3px 0 0 #000;
    }
    .neo-badge-yellow { background: #FFCC00; }
    .neo-badge-red { background: #FF3333; color: #fff; }
    .neo-badge-blue { background: #40A9FF; color: #fff; }

    .neo-input {
        border: 3px solid #000 !important;
        box-shadow: 4px 4px 0 0 #000 !important;
        border-radius: 0 !important;
        transition: all 0.15s;
    }
    .neo-input:focus {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0 0 #000 !important;
    }

    .neo-title {
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .neo-section-title {
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -0.02em;
        border-left: 6px solid #FFCC00;
        padding-left: 1rem;
    }

    div[data-testid="stSidebar"] {
        background: #fff;
        border-right: 3px solid #000;
    }
    .sidebar-btn {
        display: block;
        width: 100%;
        padding: 0.65rem 1rem;
        margin-bottom: 6px;
        background: #fff;
        border: 3px solid #000;
        box-shadow: 4px 4px 0 0 #000;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.02em;
        text-align: left;
        text-decoration: none;
        color: #000;
        transition: all 0.15s;
        cursor: pointer;
    }
    .sidebar-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0 0 #000;
    }

    div.stButton > button {
        border: 3px solid #000 !important;
        border-radius: 0 !important;
        box-shadow: 4px 4px 0 0 #000 !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.15s !important;
        text-align: left !important;
    }
    div.stButton > button:hover {
        transform: translate(2px, 2px) !important;
        box-shadow: 2px 2px 0 0 #000 !important;
    }

    div.stTextInput input {
        border: 3px solid #000 !important;
        border-radius: 0 !important;
        box-shadow: 4px 4px 0 0 #000 !important;
    }
    div.stTextInput input:focus {
        box-shadow: 2px 2px 0 0 #000 !important;
    }

    div.stNumberInput input {
        border: 3px solid #000 !important;
        border-radius: 0 !important;
        box-shadow: 4px 4px 0 0 #000 !important;
    }

    div[data-baseweb="select"] > div {
        border: 3px solid #000 !important;
        border-radius: 0 !important;
        box-shadow: 4px 4px 0 0 #000 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 3px solid #000;
    }
    .stTabs [data-baseweb="tab"] {
        border: 3px solid #000 !important;
        border-bottom: none !important;
        border-radius: 0 !important;
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    .stTabs [aria-selected="true"] {
        background: #FFCC00 !important;
        color: #000 !important;
    }

    .stMetric {
        background: #fff;
        border: 3px solid #000;
        box-shadow: 4px 4px 0 0 #000;
        padding: 1rem;
    }
    .stMetric label {
        font-weight: 700;
        text-transform: uppercase;
        font-size: 0.7rem;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-weight: 900;
        font-size: 1.5rem;
    }

    hr { border-top: 3px solid #000 !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <div style="width:40px;height:40px;background:#FFCC00;border:3px solid #000;
                        box-shadow:4px 4px 0 0 #000;display:flex;align-items:center;justify-content:center;">
                <span style="color:#000;font-weight:900;font-size:1.2rem;">U</span>
            </div>
            <div>
                <div style="font-weight:900;text-transform:uppercase;letter-spacing:-0.02em;font-size:1.1rem;">UNICOMPARE</div>
                <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#666;">PBKK FINAL PROJECT</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    pages_list = [
        (" Beranda", "home"),
        (" Universitas", "universities"),
        (" Bandingkan Skor", "compare"),
        (" Bandingkan Pilihan", "compare_choices"),
    ]
    if is_admin():
        pages_list.append((" Admin", "admin"))
    pages_list.append((" Akun", "auth"))

    if "page" not in st.session_state:
        st.session_state.page = "home"

    for label, key in pages_list:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    if is_authenticated():
        st.markdown("---")
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:8px;padding:8px 0;">
                <div style="width:32px;height:32px;background:#FF3333;border:3px solid #000;
                            display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.85rem;color:#fff;">
                    {get_username()[0].upper()}
                </div>
                <span style="font-weight:700;font-size:0.85rem;">{get_username()}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button(" Logout", use_container_width=True):
            do_logout()

PAGES = {
    "home": "screens.home",
    "universities": "screens.universities",
    "compare": "screens.compare",
    "compare_choices": "screens.compare_choices",

    "admin": "screens.admin",
    "auth": "screens.auth",
}

page_key = st.session_state.page
if page_key in PAGES:
    page_module = __import__(PAGES[page_key], fromlist=["app"])
    page_module.app()
