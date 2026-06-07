import streamlit as st
from utils.api import get_admin_users, delete_admin_user
from utils.auth import is_admin, get_token

def app():
    if not is_admin(): st.warning("Halaman ini hanya untuk admin"); return
    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Admin Panel</h1>', unsafe_allow_html=True)
    st.markdown("---")
    token = get_token()
    data, err = get_admin_users(token)
    if not err:
        users = data if isinstance(data, list) else []
        st.markdown(f'<div style="margin-bottom:1rem;">Pengguna <span class="neo-badge neo-badge-yellow">{len(users)}</span></div>', unsafe_allow_html=True)
        for u in users:
            is_self = u["username"] == st.session_state.user.get("username")
            st.markdown(f'<div class="neo-card" style="padding:0.75rem 1rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between;"><span style="font-weight:700;">{u["username"]}</span><span class="neo-badge {"neo-badge-orange" if u["role"]=="admin" else "neo-badge-blue"}">{u["role"]}</span></div>', unsafe_allow_html=True)
            if not is_self and st.button(f"Hapus {u['username']}", key=f"del_{u['username']}"):
                if not delete_admin_user(token, u["username"])[1]: st.rerun()
