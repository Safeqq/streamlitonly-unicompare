import streamlit as st
from utils.api import get_admin_users, delete_admin_user, get_universities, get_university_detail, create_admin_university, update_admin_university, delete_admin_university, update_admin_university_programs
from utils.auth import is_admin, get_token

def app():
    if not is_admin(): st.warning("Halaman ini hanya untuk admin"); return
    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Admin Panel</h1>', unsafe_allow_html=True)
    st.markdown("---")
    token = get_token()
    tab1, tab2 = st.tabs(["Users", "Universitas"])
    with tab1:
        data, err = get_admin_users(token)
        if not err:
            users = data if isinstance(data, list) else []
            st.markdown(f'<div style="margin-bottom:1rem;">Pengguna <span class="neo-badge neo-badge-yellow">{len(users)}</span></div>', unsafe_allow_html=True)
            for u in users:
                is_self = u["username"] == st.session_state.user.get("username")
                st.markdown(f'<div class="neo-card" style="padding:0.75rem 1rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between;"><span style="font-weight:700;">{u["username"]}</span><span class="neo-badge {"neo-badge-red" if u["role"]=="admin" else "neo-badge-blue"}">{u["role"]}</span></div>', unsafe_allow_html=True)
                if not is_self and st.button(f"Hapus {u['username']}", key=f"del_{u['username']}"):
                    if not delete_admin_user(token, u["username"])[1]: st.rerun()
    with tab2:
        data, err = get_universities()
        if not err:
            unis = data.get("universities", [])
            st.markdown(f'<div style="margin-bottom:1rem;">Universitas <span class="neo-badge neo-badge-yellow">{len(unis)}</span></div>', unsafe_allow_html=True)
            for u in unis:
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                with c1:
                    st.markdown(f'<div style="font-weight:700;">{u["name"]}</div><div style="font-size:0.75rem;color:#666;">{u["id"]} — {u["program_count"]} program</div>', unsafe_allow_html=True)
                with c2:
                    if st.button("Edit", key=f"edit_{u['id']}"):
                        st.session_state.edit_univ = u["id"]
                        if "edit_programs_univ" in st.session_state: del st.session_state.edit_programs_univ
                        st.rerun()
                with c3:
                    if st.button("Skor", key=f"skor_{u['id']}"):
                        st.session_state.edit_programs_univ = u["id"]
                        if "edit_univ" in st.session_state: del st.session_state.edit_univ
                        st.rerun()
                with c4:
                    if st.button("Hapus", key=f"del_{u['id']}"):
                        if not delete_admin_university(token, u["id"])[1]: st.rerun()
        st.markdown("---")
        with st.expander("Tambah Universitas"):
            with st.form("add_univ_form"):
                uid = st.text_input("ID", placeholder="itb")
                uname = st.text_input("Nama", placeholder="Institut Teknologi Bandung")
                srcs = st.text_input("Sumber (koma)", placeholder="snbp, sbmptn, mandiri")
                if st.form_submit_button("Simpan", type="primary", use_container_width=True) and uid and uname:
                    sources = [s.strip() for s in srcs.split(",") if s.strip()] if srcs else []
                    if not create_admin_university(token, uid, uname, sources)[1]: st.success("Ditambahkan!"); st.rerun()
        if "edit_univ" in st.session_state:
            st.markdown("---")
            ed = st.session_state.edit_univ
            for u in unis:
                if u["id"] == ed:
                    with st.form("edit_univ_form"):
                        new_name = st.text_input("Nama", value=u["name"])
                        new_srcs = st.text_input("Sumber (koma)", value=", ".join(u.get("sources", [])))
                        if st.form_submit_button("Update", type="primary", use_container_width=True) and new_name:
                            ns = [s.strip() for s in new_srcs.split(",") if s.strip()] if new_srcs else []
                            if not update_admin_university(token, ed, new_name, ns)[1]: del st.session_state.edit_univ; st.rerun()
                    if st.button("Batal"):
                        del st.session_state.edit_univ; st.rerun()
                    break
        if "edit_programs_univ" in st.session_state:
            st.markdown("---")
            ed = st.session_state.edit_programs_univ
            detail, derr = get_university_detail(ed)
            if not derr:
                progs = detail.get("programs", [])
                st.markdown(f'<h3 class="neo-title">Edit Skor: {detail["name"]}</h3>', unsafe_allow_html=True)
                with st.form("edit_scores_form"):
                    updates = []
                    for p in progs:
                        cols = st.columns([3, 2, 2])
                        with cols[0]: st.markdown(f'**{p["name"]}**')
                        with cols[1]: new_score = st.text_input(f"Skor", value=str(p.get("score", "") or ""), key=f"sc_{p['name']}", label_visibility="collapsed", placeholder="Nilai")
                        with cols[2]: new_text = st.text_input(f"Teks", value=p.get("score_text", ""), key=f"txt_{p['name']}", label_visibility="collapsed", placeholder="Teks skor")
                        score_val = float(new_score) if new_score.strip() else None
                        updates.append({"id": p["id"], "score": score_val, "score_text": new_text})
                    if st.form_submit_button("Simpan Skor", type="primary", use_container_width=True):
                        if not update_admin_university_programs(token, ed, updates)[1]: del st.session_state.edit_programs_univ; st.rerun()
                if st.button("Batal"):
                    del st.session_state.edit_programs_univ; st.rerun()
