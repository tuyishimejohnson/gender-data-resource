import streamlit as st


def render_top_nav() -> None:
    """Render the shared top navigation used across pages."""

    st.markdown(
        """
        <style>
        .block-container {
            width: 100%;
            max-width: 98% !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }

        div[data-testid="stPageLink"] a {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 38px;
            border-radius: 999px;
            border: 1px solid #d8dfec;
            background: #ffffff;
            color: #33415f;
            font-weight: 600;
            font-size: 13px;
            text-decoration: none;
        }
        div[data-testid="stPageLink"] a:hover {
            border-color: #bcc9e0;
            color: #202e49;
            background: #f8faff;
        }
        div[data-testid="stPageLinkCurrent"] a {
            background: #ececff !important;
            border-color: #d7d8ff !important;
            color: #4037b3 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav_brand_col, nav_links_col, nav_actions_col = st.columns([1.2, 1.7, 1.3])

    with nav_brand_col:
        st.markdown(
            """
            <div style="display:flex;align-items:center;background-color:#f0f2f6;">
                <div style="pading:30px;background:#6a5cff;color:white;display:flex;align-items:center;justify-content:center;flex-direction:column;">
                    <div style="font-weight:700;color:#1d2742;font-size:18px;">EquiStat</div>
                    <div style="font-size:10px;letter-spacing:0.08em;">AI PLATFORM</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav_links_col:
        link1, link2, link3, link4 = st.columns(4)
        link1.page_link("pages/2_Dashboard.py", label="Dashboard")
        link2.page_link("pages/1_Discovery.py", label="Datasets")
        link3.page_link("pages/3_Data_Quality.py", label="Methodology")
        link4.page_link("pages/reports.py", label="Reports")

    with nav_actions_col:
        live_col, export_col, user_col = st.columns([1.1, 1.2, 1.2])
        live_col.markdown(
            "<div style='margin-top:8px; font-size:12px; color:#0b8f5d;'>● Live Data</div>",
            unsafe_allow_html=True,
        )
        export_col.button("Export", use_container_width=True)
        user_col.markdown(
            "<div style='margin-top:8px; font-size:12px; color:#4e5b79;'>Researcher</div>",
            unsafe_allow_html=True,
        )

    st.divider()
