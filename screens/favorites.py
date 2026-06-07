import streamlit as st
from utils.api import get_favorites, add_favorite, remove_favorite
from utils.auth import is_authenticated, get_token

def app():
    if not is_authenticated():
        st.warning("Silakan login untuk menggunakan fitur Favorit"); return

    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Favorit Saya</h1>', unsafe_allow_html=True)
    st.markdown("---")

    token = get_token()
    tab1, tab2 = st.tabs(["Daftar Favorit", "Tambah Favorit"])

    with tab1:
        data, err = get_favorites(token)
        if not err:
            favs = data.get("favorites", [])
            if favs:
                st.markdown(f'<div style="margin-bottom:1rem;">Anda memiliki <span class="neo-badge neo-badge-yellow">{len(favs)}</span> favorit</div>', unsafe_allow_html=True)
                for f in favs:
                    c1, c2 = st.columns([5, 1])
                    with c1: st.markdown(f'<div class="neo-card" style="padding:0.75rem 1rem;"><span style="font-weight:700;text-transform:uppercase;">{f}</span></div>', unsafe_allow_html=True)
                    with c2:
                        if st.button("Hapus", key=f"del_{f}"):
                            if not remove_favorite(token, f)[1]: st.rerun()
            else:
                st.markdown('<div style="background:#FFD000;border:2px solid #000;padding:2rem;text-align:center;font-weight:700;">Belum ada favorit.</div>', unsafe_allow_html=True)

    with tab2:
        with st.form("add_fav_form"):
            univ_name = st.text_input("Nama Universitas", placeholder="UI, ITB, ...")
            if st.form_submit_button("Simpan", type="primary", use_container_width=True) and univ_name:
                if not add_favorite(token, univ_name)[1]: st.success(f"Ditambahkan!"); st.rerun()
