import streamlit as st
from utils.auth import do_login, do_register, is_authenticated, get_username, do_logout

def app():
    if is_authenticated():
        user = st.session_state.user
        st.markdown('<h1 class="neo-title" style="font-size:2rem;">Akun Saya</h1>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1.5rem;background:#fff;border:2px solid #000;box-shadow:4px 4px 0 0 #000;padding:2rem;margin-bottom:1rem;">
            <div style="width:64px;height:64px;background:#FFD000;border:3px solid #000;box-shadow:3px 3px 0 0 #000;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:1.8rem;flex-shrink:0;">{get_username()[0].upper()}</div>
            <div><div style="font-weight:900;font-size:1.3rem;text-transform:uppercase;">{get_username()}</div><span class="neo-badge {'neo-badge-orange' if user.get('role')=='admin' else 'neo-badge-blue'}">{user.get('role','user')}</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type="primary", use_container_width=True): do_logout()
    else:
        st.markdown('<h1 class="neo-title" style="font-size:2rem;">Akun</h1>', unsafe_allow_html=True)
        st.markdown("---")
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            with st.form("login_form"):
                st.text_input("Username", placeholder="Masukkan username", key="l_user")
                st.text_input("Password", type="password", placeholder="Masukkan password", key="l_pass")
                if st.form_submit_button("Login", type="primary", use_container_width=True):
                    if not st.session_state.l_user or not st.session_state.l_pass:
                        st.error("Username dan password wajib diisi")
                    else:
                        err = do_login(st.session_state.l_user, st.session_state.l_pass)
                        if err: st.error(err)
                        else: st.success("Login berhasil!"); st.rerun()
        with tab2:
            with st.form("register_form"):
                st.text_input("Username", placeholder="Minimal 3 karakter", key="r_user")
                st.text_input("Password", type="password", placeholder="Minimal 4 karakter", key="r_pass")
                st.text_input("Konfirmasi Password", type="password", key="r_pass2")
                if st.form_submit_button("Register", type="primary", use_container_width=True):
                    u, p, p2 = st.session_state.r_user, st.session_state.r_pass, st.session_state.r_pass2
                    if not u or not p: st.error("Username dan password wajib diisi")
                    elif len(u) < 3: st.error("Username minimal 3 karakter")
                    elif len(p) < 4: st.error("Password minimal 4 karakter")
                    elif p != p2: st.error("Password tidak cocok")
                    else:
                        err = do_register(u, p)
                        if err: st.error(err)
                        else: st.success("Registrasi berhasil!"); st.rerun()
