import streamlit as st
from utils.api import get_universities, search_universities, get_university_detail

def app():
    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Universitas</h1>', unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2 = st.tabs(["Semua Universitas", "Cari & Detail"])

    with tab1:
        limit = st.number_input("Maksimal", min_value=0, max_value=500, value=100, step=10, label_visibility="collapsed")
        list_data, list_err = get_universities(limit=int(limit))
        if not list_err:
            unis = list_data.get("universities", [])
            st.markdown(f'<div style="margin-bottom:1rem;">Total <span class="neo-badge neo-badge-yellow">{list_data.get("total",0)}</span></div>', unsafe_allow_html=True)
            for i in range(0, len(unis), 3):
                cols = st.columns(3)
                for j, u in enumerate(unis[i:i+3]):
                    with cols[j]:
                        st.markdown(f"""
                        <div class="neo-card" style="margin-bottom:1rem;">
                            <h3 style="font-weight:900;text-transform:uppercase;font-size:0.9rem;margin:0;">{u['name']}</h3>
                            <div style="font-size:0.75rem;color:#888;margin-top:0.3rem;">ID: {u['id']}</div>
                            <div style="margin-top:0.75rem;padding-top:0.75rem;border-top:1px solid #ddd;">
                                <span class="neo-badge neo-badge-blue">{u['program_count']} program</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    with tab2:
        q = st.text_input("", placeholder="Contoh: ui, Universitas Indonesia", label_visibility="collapsed")
        if q:
            search_data, search_err = search_universities(q)
            if not search_err:
                results = search_data.get("universities", [])
                if results:
                    st.markdown(f'<div style="margin-bottom:1rem;">Ditemukan <span class="neo-badge neo-badge-yellow">{len(results)}</span> hasil</div>', unsafe_allow_html=True)
                    for u in results:
                        with st.expander(f"**{u['name']}** ({u['id']})"):
                            detail, detail_err = get_university_detail(u['id'])
                            if not detail_err:
                                progs = detail.get("programs", [])
                                if progs:
                                    for pi in range(0, len(progs), 2):
                                        cols = st.columns(2)
                                        for pi2, p in enumerate(progs[pi:pi+2]):
                                            with cols[pi2]:
                                                deg = f"({p.get('degree','')})" if p.get('degree') else ""
                                                st.markdown(f"""
                                                <div class="neo-card" style="padding:0.75rem;margin-bottom:0.5rem;
                                                    display:flex;justify-content:space-between;align-items:center;">
                                                    <span style="font-weight:700;font-size:0.85rem;">{p['name']} {deg}</span>
                                                    <span class="neo-badge neo-badge-yellow">{p.get('score_text',p.get('score','-'))}</span>
                                                </div>
                                                """, unsafe_allow_html=True)
                else:
                    st.markdown('<div style="background:#FFD000;border:2px solid #000;padding:1.5rem;text-align:center;font-weight:700;">Tidak ada hasil</div>', unsafe_allow_html=True)
