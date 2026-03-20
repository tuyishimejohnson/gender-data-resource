import streamlit as st


def render_top_nav() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f4f6fb;
        }

        section[data-testid="stSidebar"] {
            display: none !important;
        }

        [data-testid="collapsedControl"] {
            display: none !important;
        }

        .block-container {
            max-width: 100% !important;
            padding-top: 0 !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-bottom: 0 !important;
            margin-top: 4rem !important;
        }

        .st-key-top_nav {
            background: #ffffff;
            border-bottom: 1px solid #e8ecf3;
            padding: 18px 28px;
            position: sticky;
            top: 0;
            z-index: 999;
        }

        .st-key-top_nav > div {
            padding: 0 !important;
        }

        div[data-testid="column"] > div {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        /* ---------- Brand ---------- */
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 14px;
            min-height: 44px;
        }

        .nav-brand-logo {
            width: 44px;
            height: 44px;
            border-radius: 14px;
            background: linear-gradient(180deg, #6b4efc 0%, #583af4 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 18px rgba(91, 67, 241, 0.16);
            flex-shrink: 0;
        }

        .nav-brand-logo svg {
            width: 21px;
            height: 21px;
        }

        .nav-brand-text {
            display: flex;
            flex-direction: column;
            line-height: 1.02;
        }

        .nav-brand-title {
            margin: 0;
            color: #17233d;
            font-size: 16px;
            font-weight: 800;
        }

        .nav-brand-subtitle {
            margin-top: 3px;
            color: #6554f6;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        /* ---------- Nav links ---------- */
        div[data-testid="stPageLink"] a,
        div[data-testid="stPageLinkCurrent"] a {
            display: inline-flex !important;
            align-items: center;
            justify-content: center;
            width: 100%;
            min-height: 42px;
            padding: 0 18px;
            border: none !important;
            border-radius: 14px;
            background: transparent !important;
            color: #61708d !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            text-decoration: none !important;
            box-shadow: none !important;
            white-space: nowrap;
            transition: all 0.18s ease;
        }

        div[data-testid="stPageLink"] a:hover {
            background: #f5f7fc !important;
            color: #3b4b66 !important;
        }

        div[data-testid="stPageLinkCurrent"] a {
            background: #eef0ff !important;
            color: #4e43e5 !important;
        }

        /* ---------- Right controls ---------- */
        .nav-right-wrap {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 12px;
            min-height: 44px;
        }

        .live-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            height: 30px;
            padding: 0 14px;
            border-radius: 999px;
            background: #ecfbf2;
            border: 1px solid #caedd9;
            color: #0f9b62;
            font-size: 14px;
            font-weight: 700;
            white-space: nowrap;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #33c374;
            display: inline-block;
        }

        .bell-wrap {
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #93a0b8;
        }

        .bell-wrap svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
        }

        div.stButton > button {
            height: 44px !important;
            border-radius: 16px !important;
            border: none !important;
            background: linear-gradient(180deg, #5d46f5 0%, #4d39e6 100%) !important;
            color: #ffffff !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            padding: 0 20px !important;
            box-shadow: 0 8px 16px rgba(77, 57, 230, 0.2) !important;
        }

        div.stButton > button:hover {
            background: linear-gradient(180deg, #553ff0 0%, #4332d8 100%) !important;
            color: #ffffff !important;
        }

        /* ---------- Profile dropdown trigger ---------- */
        .profile-dropdown {
            position: relative;
            display: inline-block;
            min-width: 100%;
        }

        .profile-dropdown details {
            position: relative;
            width: 100%;
        }

        .profile-dropdown summary {
            list-style: none;
            display: flex;
            align-items: center;
            gap: 12px;
            justify-content: flex-start;
            width: 100%;
            min-width: 165px;
            height: 44px;
            padding: 0 14px 0 10px;
            border: 1px solid #e5e9f0;
            border-radius: 16px;
            background: #ffffff;
            cursor: pointer;
            user-select: none;
            box-sizing: border-box;
        }

        .profile-dropdown summary::-webkit-details-marker {
            display: none;
        }

        .profile-dropdown summary:hover {
            border-color: #dbe1ea;
            background: #ffffff;
        }

        .profile-dropdown details[open] summary {
            border-color: #e2e7ef;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
        }

        .profile-avatar {
            width: 30px;
            height: 30px;
            border-radius: 999px;
            background: #6549f6;
            color: #ffffff;
            font-size: 14px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .profile-name {
            color: #33425d;
            font-size: 15px;
            font-weight: 600;
            line-height: 1;
        }

        .profile-chevron {
            margin-left: auto;
            display: flex;
            align-items: center;
            color: #98a3b6;
        }

        .profile-chevron svg {
            width: 16px;
            height: 16px;
            stroke: currentColor;
            transition: transform 0.2s ease;
        }

        .profile-dropdown details[open] .profile-chevron svg {
            transform: rotate(180deg);
        }

        /* ---------- Dropdown menu ---------- */
        .dropdown-menu {
            position: absolute;
            top: 58px;
            right: 0;
            width: 240px;
            background: #ffffff;
            border: 1px solid #edf0f5;
            border-radius: 22px;
            box-shadow: 0 14px 36px rgba(18, 28, 45, 0.1);
            padding: 8px 0;
            z-index: 1001;
            display: none;
            overflow: hidden;
        }

        .profile-dropdown details[open] .dropdown-menu {
            display: block;
        }

        .dropdown-item {
            display: flex;
            align-items: center;
            gap: 14px;
            height: 46px;
            padding: 0 20px;
            color: #4a5a75;
            font-size: 15px;
            font-weight: 500;
            text-decoration: none;
            background: #ffffff;
            box-sizing: border-box;
        }

        .dropdown-item:hover {
            background: #f7f9fc;
        }

        .dropdown-item svg {
            width: 18px;
            height: 18px;
            stroke: #94a5c1;
            stroke-width: 1.8;
            flex-shrink: 0;
        }

        hr {
            margin: 0 !important;
            border-color: #e9edf5 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav = st.container(key="top_nav")

    with nav:
        brand_col, links_col, actions_col = st.columns([1.3, 2.2, 1.7])

        with brand_col:
            st.markdown(
                """
                <div class="nav-brand">
                    <div class="nav-brand-logo">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M12 4L19 8L12 12L5 8L12 4Z" stroke="white" stroke-width="1.8" stroke-linejoin="round"/>
                            <path d="M5 12L12 16L19 12" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M5 16L12 20L19 16" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div class="nav-brand-text">
                        <div class="nav-brand-title">EquiStat</div>
                        <div class="nav-brand-subtitle">AI PLATFORM</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with links_col:
            c1, c2, c3, c4 = st.columns([1, 1, 1.15, 0.9], gap="small")
            with c1:
                st.page_link("pages/2_Dashboard.py", label="Dashboard")
            with c2:
                st.page_link("pages/1_Discovery.py", label="Datasets")
            with c3:
                st.page_link("pages/3_Data_Quality.py", label="Methodology")
            with c4:
                st.page_link("pages/reports.py", label="Reports")

        with actions_col:
            live_col, bell_col, export_col, user_col = st.columns(
                [1.05, 0.28, 0.95, 1.45], gap="small"
            )

            with live_col:
                st.markdown(
                    """
                    <div class="nav-right-wrap">
                        <div class="live-pill">
                            <span class="live-dot"></span>
                            <span>Live Data</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with bell_col:
                st.markdown(
                    """
                    <div class="nav-right-wrap">
                        <div class="bell-wrap">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M15 17H9M18 17V11C18 7.686 15.314 5 12 5C8.686 5 6 7.686 6 11V17L4.5 18.5H19.5L18 17Z"
                                      stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with export_col:
                st.button("↓ Export", use_container_width=True)

            with user_col:
                st.markdown(
                    """
                    <div class="nav-right-wrap">
                        <div class="profile-dropdown">
                            <details>
                                <summary>
                                    <div class="profile-avatar">R</div>
                                    <div class="profile-name">Researcher</div>
                                    <div class="profile-chevron">
                                        <svg viewBox="0 0 24 24" fill="none">
                                            <path d="M6 9L12 15L18 9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </div>
                                </summary>

                                <div class="dropdown-menu">
                                    <a href="#" class="dropdown-item">
                                        <svg viewBox="0 0 24 24" fill="none">
                                            <path d="M12 8.5A3.5 3.5 0 1 0 12 15.5A3.5 3.5 0 1 0 12 8.5Z"/>
                                            <path d="M19.4 15A1.6 1.6 0 0 0 19.72 16.76L19.78 16.82A2 2 0 1 1 16.95 19.65L16.89 19.59A1.6 1.6 0 0 0 15.13 19.27A1.6 1.6 0 0 0 14.2 20.73V20.9A2 2 0 1 1 10.2 20.9V20.81A1.6 1.6 0 0 0 9.15 19.34A1.6 1.6 0 0 0 7.45 19.67L7.39 19.73A2 2 0 1 1 4.56 16.9L4.62 16.84A1.6 1.6 0 0 0 4.95 15.14A1.6 1.6 0 0 0 3.49 14.21H3.32A2 2 0 1 1 3.32 10.21H3.41A1.6 1.6 0 0 0 4.88 9.16A1.6 1.6 0 0 0 4.55 7.46L4.49 7.4A2 2 0 1 1 7.32 4.57L7.38 4.63A1.6 1.6 0 0 0 9.08 4.96H9.2A1.6 1.6 0 0 0 10.13 3.5V3.32A2 2 0 1 1 14.13 3.32V3.41A1.6 1.6 0 0 0 15.18 4.88A1.6 1.6 0 0 0 16.88 4.55L16.94 4.49A2 2 0 1 1 19.77 7.32L19.71 7.38A1.6 1.6 0 0 0 19.38 9.08V9.2A1.6 1.6 0 0 0 20.84 10.13H21.02A2 2 0 1 1 21.02 14.13H20.93A1.6 1.6 0 0 0 19.46 15.18L19.4 15Z"/>
                                        </svg>
                                        <span>Settings</span>
                                    </a>

                                    <a href="#" class="dropdown-item">
                                        <svg viewBox="0 0 24 24" fill="none">
                                            <ellipse cx="12" cy="6" rx="7" ry="3"/>
                                            <path d="M5 6V12C5 13.657 8.134 15 12 15C15.866 15 19 13.657 19 12V6"/>
                                            <path d="M5 12V18C5 19.657 8.134 21 12 21C15.866 21 19 19.657 19 18V12"/>
                                        </svg>
                                        <span>Data Sources</span>
                                    </a>

                                    <a href="#" class="dropdown-item">
                                        <svg viewBox="0 0 24 24" fill="none">
                                            <path d="M12 3L18 5V10C18 14.5 15.2 18.74 12 20C8.8 18.74 6 14.5 6 10V5L12 3Z"/>
                                            <path d="M9.5 11.5L11.2 13.2L14.8 9.6" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                        <span>Security</span>
                                    </a>

                                    <a href="#" class="dropdown-item">
                                        <svg viewBox="0 0 24 24" fill="none">
                                            <path d="M15 17L20 12L15 7" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M20 12H9" stroke-linecap="round"/>
                                            <path d="M12 19H7C5.895 19 5 18.105 5 17V7C5 5.895 5.895 5 7 5H12" stroke-linecap="round"/>
                                        </svg>
                                        <span>Sign Out</span>
                                    </a>
                                </div>
                            </details>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
