import streamlit as st
from utils.auth import do_login, do_register, is_authenticated, get_username, do_logout

def app():
    if is_authenticated():
        user = st.session_state.user
        st.markdown('<h1 class="neo-title" style="font-size:2rem;">Akun Saya</h1>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1.5rem;background:#fff;border:4px solid #000;box-shadow:6px 6px 0 0 #000;padding:2rem;margin-bottom:1rem;">
            <div style="width:64px;height:64px;background:#FF3333;border:4px solid #000;box-shadow:4px 4px 0 0 #000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.8rem;flex-shrink:0;color:#fff;">{get_username()[0].upper()}</div>
            <div><div style="font-weight:900;font-size:1.3rem;text-transform:uppercase;">{get_username()}</div><span class="neo-badge {'neo-badge-red' if user.get('role')=='admin' else 'neo-badge-blue'}">{user.get('role','user')}</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type="primary", use_container_width=True): do_logout()
        return

    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Akun</h1>', unsafe_allow_html=True)
    st.markdown("---")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            lu = st.text_input("Username", placeholder="Masukkan username")
            lp = st.text_input("Password", type="password", placeholder="Masukkan password")
            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if not lu or not lp:
                    st.error("Username dan password wajib diisi")
                elif len(lp) < 6:
                    st.error("Password minimal 6 karakter")
                else:
                    err = do_login(lu, lp)
                    if err: st.error(err)

    with tab2:
        with st.form("register_form"):
            ru = st.text_input("Username", placeholder="Minimal 3 karakter")
            rp = st.text_input("Password", type="password", placeholder="Minimal 6 karakter")
            rp2 = st.text_input("Konfirmasi Password", type="password")
            if st.form_submit_button("Register", type="primary", use_container_width=True):
                if not ru or not rp:
                    st.error("Username dan password wajib diisi")
                elif len(ru) < 3:
                    st.error("Username minimal 3 karakter")
                elif len(rp) < 6:
                    st.error("Password minimal 6 karakter")
                elif rp != rp2:
                    st.error("Password tidak cocok")
                else:
                    err = do_register(ru, rp)
                    if err: st.error(err)
