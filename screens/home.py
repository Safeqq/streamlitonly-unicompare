import streamlit as st
from utils.api import get_sources, get_universities, root


def app():
    info, _ = root()

    st.markdown(
        """
    <div style="display:flex;gap:2rem;padding:3rem 0 2rem;">
        <div style="flex:2;">
            <div style="border-left:6px solid #FFCC00;padding-left:1.5rem;">
                <h1 style="font-weight:900;text-transform:uppercase;letter-spacing:-0.03em;
                           font-size:3rem;line-height:1.05;margin:0;">
                    Temukan PTN<br>dan Program Studimu
                </h1>
                <p style="font-size:1.1rem;color:#555;margin-top:1rem;max-width:500px;">
                    Bandingkan skor UTBK, jelajahi program studi, dan temukan
                    pilihan terbaik untuk masa depanmu.
                </p>
            </div>
            <div style="display:flex;gap:1rem;margin-top:2rem;flex-wrap:wrap;">
                <a href="#" style="display:inline-block;padding:0.75rem 2rem;font-weight:900;
                    text-transform:uppercase;letter-spacing:0.05em;border:3px solid #000;
                    box-shadow:5px 5px 0 0 #000;background:#FFCC00;color:#000;text-decoration:none;">
                    Mulai Bandingkan →
                </a>
                <a href="#" style="display:inline-block;padding:0.75rem 2rem;font-weight:900;
                    text-transform:uppercase;letter-spacing:0.05em;border:3px solid #000;
                    box-shadow:5px 5px 0 0 #000;background:#fff;color:#000;text-decoration:none;">
                    Lihat Universitas →
                </a>
            </div>
        </div>
        <div style="flex:1;background:#FFCC00;border:4px solid #000;box-shadow:8px 8px 0 0 #000;
                    display:flex;align-items:center;justify-content:center;padding:2rem;min-height:250px;">
            <div style="text-align:center;">
                <div style="font-weight:900;font-size:4rem;line-height:1;">🎓</div>
                <div style="font-weight:900;text-transform:uppercase;letter-spacing:0.1em;
                            font-size:0.75rem;margin-top:0.5rem;">UNICOMPARE 2026</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        '<h2 class="neo-section-title">Kenapa Unicompare?</h2>', unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    for col, (icon, title, desc) in zip(
        [col1, col2, col3],
        [
            (
                "📊",
                "Bandingkan Skor",
                "Masukkan skor UTBK dan lihat PTN serta program studi yang sesuai dengan kemampuanmu.",
            ),
            (
                "⚖️",
                "Bandingkan Pilihan",
                "Bandingkan beberapa program studi dari berbagai universitas secara side-by-side.",
            ),
            (
                "🏛️",
                "Database Lengkap",
                "Jelajahi puluhan PTN dan ratusan program studi dengan informasi skor terkini.",
            ),
        ],
    ):
        with col:
            st.markdown(
                f"""
            <div class="neo-card" style="height:100%;">
                <div style="width:48px;height:48px;background:#FFCC00;border:3px solid #000;
                            box-shadow:4px 4px 0 0 #000;display:flex;align-items:center;justify-content:center;
                            font-size:1.5rem;margin-bottom:1rem;">{icon}</div>
                <h3 style="font-weight:900;text-transform:uppercase;font-size:1rem;margin:0 0 0.5rem;">{title}</h3>
                <p style="color:#666;font-size:0.9rem;margin:0;">{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    src_data, _ = get_sources()
    univ_data, _ = get_universities(limit=200)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Program", src_data.get("total", 0) if not _ else 0)
    with c2:
        st.metric("Universitas", univ_data.get("total", 0) if not _ else 0)
    with c3:
        st.metric("Sumber Data", len(src_data.get("sources", [])) if not _ else 0)
    with c4:
        st.metric("API Status", info.get("status", "?").upper())

    st.markdown("---")
    st.markdown(
        '<h2 class="neo-section-title">Universitas Tersedia</h2>',
        unsafe_allow_html=True,
    )
    univ_data, _ = get_universities(limit=12)
    if not _:
        unis = univ_data.get("universities", [])
        for i in range(0, len(unis), 4):
            cols = st.columns(4)
            for j, u in enumerate(unis[i : i + 4]):
                with cols[j]:
                    st.markdown(
                        f"""
                    <div class="neo-card">
                        <div>
                            <h3 style="font-weight:900;text-transform:uppercase;font-size:0.85rem;
                                       margin:0;line-height:1.2;">{u["name"]}</h3>
                        </div>
                        <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px solid #ddd;
                                    display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:0.75rem;color:#888;">{u["program_count"]} program</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align:center;padding:2rem 0 0;">
        <div style="font-weight:900;text-transform:uppercase;font-size:1.5rem;">UNICOMPARE</div>
        <div style="color:#888;font-size:0.85rem;margin-top:0.5rem;">Find your path. Break the mold.</div>
        <div style="color:#aaa;font-size:0.75rem;margin-top:1rem;padding-top:1rem;border-top:1px solid #ddd;">
            &copy; 2026 · Jakarta
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
