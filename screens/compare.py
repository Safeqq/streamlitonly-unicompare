import streamlit as st
from utils.api import compare_score

def app():
    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Bandingkan Skor</h1>', unsafe_allow_html=True)
    st.markdown('<div style="background:#fff;border:2px solid #000;box-shadow:4px 4px 0 0 #000;padding:1.5rem;margin:1rem 0;">Masukkan skor UTBK Anda untuk melihat program studi yang sesuai dengan kemampuanmu.</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1: user_score = st.number_input("Skor UTBK", min_value=0.0, max_value=1000.0, value=500.0, step=0.5)
    with col2: search_q = st.text_input("Filter", placeholder="Nama/program")
    with col3: limit = st.number_input("Maksimal", min_value=1, max_value=500, value=50, step=10)

    univ_filter = st.text_input("Filter universitas (koma)", placeholder="ui, itb, ugm")

    if st.button("Cari", type="primary", use_container_width=True):
        with st.spinner("Mencari..."):
            data, err = compare_score(score=user_score, q=search_q, universities=univ_filter, limit=int(limit))
            if not err:
                st.markdown(f'<div style="display:flex;align-items:center;gap:1rem;margin:1rem 0;background:#fff;border:2px solid #000;box-shadow:3px 3px 0 0 #000;padding:1rem;"><span style="font-weight:700;">Skor kamu:</span><span class="neo-badge neo-badge-orange" style="font-size:1.2rem;">{data["user_score"]}</span><span style="color:#888;">{data.get("total",0)} universitas</span></div>', unsafe_allow_html=True)
                for u in data.get("universities", []):
                    with st.expander(f"**{u['name']}** - {u['eligible_count']} program cocok"):
                        for p in u.get("eligible_programs", []):
                            deg = f"({p.get('degree','')})" if p.get('degree') else ""
                            st.markdown(f'<div class="neo-card" style="padding:0.75rem;margin-bottom:0.5rem;display:flex;justify-content:space-between;align-items:center;"><span style="font-weight:700;font-size:0.85rem;">{p["name"]} {deg}</span><span class="neo-badge neo-badge-yellow">{p.get("score","-")}</span></div>', unsafe_allow_html=True)
            else:
                st.error(data.get("error", "Gagal"))
