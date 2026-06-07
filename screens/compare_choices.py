import streamlit as st
from utils.api import compare_choices, get_universities, get_university_programs

def load_univ_list():
    data, err = get_universities(limit=200)
    if err: return []
    unis = {}
    for u in data.get("universities", []):
        unis[u["name"]] = u["id"]
    return unis

def load_prog_list(univ_id):
    data, err = get_university_programs(univ_id)
    if err: return []
    return data.get("programs", [])

def app():
    st.markdown('<h1 class="neo-title" style="font-size:2rem;">Bandingkan Pilihan</h1>', unsafe_allow_html=True)
    st.markdown('<div style="background:#fff;border:3px solid #000;box-shadow:6px 6px 0 0 #000;padding:1.5rem;margin:1rem 0;">Pilih dua program studi dari universitas berbeda untuk dibandingkan secara langsung.</div>', unsafe_allow_html=True)
    st.markdown("---")

    unis = load_univ_list()
    if not isinstance(unis, dict) or not unis:
        st.warning("Tidak dapat memuat daftar universitas. Pastikan backend berjalan.")
        return
    univ_names = list(unis.keys())
    univ_ids = list(unis.values())

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <h3 style="font-weight:900;text-transform:uppercase;font-size:0.9rem;padding:0.5rem 1rem;
                   background:#0b2406;color:#fff;border:3px solid #000;box-shadow:4px 4px 0 0 #000;">
            Pilihan Pertama
        </h3>
        """, unsafe_allow_html=True)
        u1_idx = st.selectbox("Perguruan Tinggi Negeri", range(len(univ_names)),
                              format_func=lambda i: univ_names[i] if i < len(univ_names) else "",
                              key="u1", label_visibility="collapsed")
        u1_id = univ_ids[u1_idx]
        progs1 = load_prog_list(u1_id)
        if progs1:
            p1_labels = [f"{p['name']} ({p.get('score_text', '-')})" for p in progs1]
            p1_idx = st.selectbox("Program Studi", range(len(p1_labels)),
                                  format_func=lambda i: p1_labels[i] if i < len(p1_labels) else "",
                                  key="p1", label_visibility="collapsed")
            p1_name = progs1[p1_idx]["name"] if p1_idx < len(progs1) else ""
        else:
            p1_name = ""
            st.info("Program tidak tersedia")

    with col2:
        st.markdown("""
        <h3 style="font-weight:900;text-transform:uppercase;font-size:0.9rem;padding:0.5rem 1rem;
                   background:#1f0b24;color:#fff;border:3px solid #000;box-shadow:4px 4px 0 0 #000;">
            Pilihan Kedua
        </h3>
        """, unsafe_allow_html=True)
        u2_idx = st.selectbox("Perguruan Tinggi Negeri", range(len(univ_names)),
                              format_func=lambda i: univ_names[i] if i < len(univ_names) else "",
                              key="u2", label_visibility="collapsed")
        u2_id = univ_ids[u2_idx]
        progs2 = load_prog_list(u2_id)
        if progs2:
            p2_labels = [f"{p['name']} ({p.get('score_text', '-')})" for p in progs2]
            p2_idx = st.selectbox("Program Studi", range(len(p2_labels)),
                                  format_func=lambda i: p2_labels[i] if i < len(p2_labels) else "",
                                  key="p2", label_visibility="collapsed")
            p2_name = progs2[p2_idx]["name"] if p2_idx < len(progs2) else ""
        else:
            p2_name = ""
            st.info("Program tidak tersedia")

    st.markdown("---")

    if st.button("🔄 Bandingkan", type="primary", use_container_width=True) and p1_name and p2_name:
        choices = [
            {"universitas": u1_id, "program": p1_name},
            {"universitas": u2_id, "program": p2_name},
        ]
        with st.spinner("Membandingkan..."):
            data, err = compare_choices(choices)
            if not err:
                hasil = data.get("pilihan", [])
                perbandingan = data.get("perbandingan", {})

                st.markdown(f"""
                <div style="background:#fff;border:3px solid #000;box-shadow:4px 4px 0 0 #000;
                            padding:1rem;margin:1rem 0;font-weight:700;text-align:center;">
                    {len(hasil)} pilihan berhasil dibandingkan
                </div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                for idx, h in enumerate(hasil):
                    with [c1, c2][idx]:
                        u = h.get("universitas", {})
                        p = h.get("program", {})
                        score_val = p.get("score_text", "") or str(p.get("score", "-"))
                        deg = f"({p.get('degree', '')})" if p.get('degree') else ""
                        st.markdown(f"""
                        <div class="neo-card" style="text-align:center;height:100%;">
                            <div style="font-weight:700;font-size:0.75rem;text-transform:uppercase;color:#888;">
                                {u.get('name', u.get('id', '?'))}
                            </div>
                            <div style="font-weight:900;font-size:1.2rem;margin:0.75rem 0;">
                                {p.get('name', '?')} {deg}
                            </div>
                            <div class="neo-badge neo-badge-yellow" style="font-size:1.5rem;padding:0.3rem 1.5rem;">
                                {score_val}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                if perbandingan:
                    st.markdown("---")
                    st.markdown("""
                    <h3 style="font-weight:900;text-transform:uppercase;font-size:1rem;
                               border-left:6px solid #FFCC00;padding-left:1rem;margin:1rem 0;">
                        Hasil Perbandingan
                    </h3>
                    """, unsafe_allow_html=True)

                    t = perbandingan.get("tertinggi", {})
                    r = perbandingan.get("terendah", {})
                    selisih = perbandingan.get("selisih")
                    selisih_str = f"{selisih:.1f}" if selisih is not None else "-"

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"""
                        <div class="neo-card" style="text-align:center;">
                            <div style="font-weight:700;text-transform:uppercase;font-size:0.7rem;color:#888;">Tertinggi</div>
                            <div style="font-weight:900;font-size:1.1rem;">{t.get('program', '-')}</div>
                            <div style="font-size:0.8rem;">{t.get('universitas', '')}</div>
                            <span class="neo-badge neo-badge-red" style="margin-top:0.5rem;">{t.get('score', '-')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        <div class="neo-card" style="text-align:center;">
                            <div style="font-weight:700;text-transform:uppercase;font-size:0.7rem;color:#888;">Terendah</div>
                            <div style="font-weight:900;font-size:1.1rem;">{r.get('program', '-')}</div>
                            <div style="font-size:0.8rem;">{r.get('universitas', '')}</div>
                            <span class="neo-badge neo-badge-blue" style="margin-top:0.5rem;">{r.get('score', '-')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"""
                        <div class="neo-card" style="text-align:center;">
                            <div style="font-weight:700;text-transform:uppercase;font-size:0.7rem;color:#888;">Selisih</div>
                            <div style="font-weight:900;font-size:2rem;color:#FF3333;">{selisih_str}</div>
                            <div style="font-size:0.8rem;">poin</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="background:#FF3333;color:#fff;border:3px solid #000;box-shadow:4px 4px 0 0 #000;
                                padding:1.5rem;text-align:center;font-weight:900;font-size:1.1rem;margin-top:1rem;">
                        Kesimpulan: {t.get('universitas', '-')} unggul {selisih_str} poin
                        dari {r.get('universitas', '-')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(data.get("error", "Gagal membandingkan"))
