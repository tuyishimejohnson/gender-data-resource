import pandas as pd
import plotly.express as px
import streamlit as st

from src.loaders import get_data_dir

st.set_page_config(
    page_title="Gender Intelligence Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


from src.navigation import render_top_nav

render_top_nav()

st.divider()

st.title("Gender Intelligence Dashboard")
st.caption(
    f"Rwanda · Real-time gender equity analytics powered by AI · Data source: `{get_data_dir()}`"
)

st.markdown(
    """
    <style>
    .block-container {
        width: 100%;
        max-width: 98% !important;
        padding-top: 1.2rem;
        padding-bottom: 1.8rem;
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
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f7f9fc;
        border: 1px solid #e3e8f2;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 14px;
    }
    .small-pill {
        display: inline-block;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 12px;
        border: 1px solid #d8deeb;
        background: #ffffff;
        color: #44506a;
    }
    .kpi-card {
        border: 1px solid #e4e9f4;
        border-radius: 14px;
        background: #ffffff;
        padding: 12px 14px;
        min-height: 130px;
    }
    .kpi-title {
        color: #6c7794;
        font-size: 12px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .kpi-value {
        color: #1b2440;
        font-size: 36px;
        font-weight: 700;
        line-height: 1.05;
    }
    .kpi-sub {
        color: #6a738f;
        font-size: 12px;
    }
    .section-card {
        border: 1px solid #e4e9f4;
        border-radius: 14px;
        background: #ffffff;
        padding: 12px 14px;
    }
    .panel-title {
        font-size: 15px;
        font-weight: 700;
        color: #1f2744;
        margin-bottom: 4px;
    }
    .panel-subtitle {
        color: #7a839f;
        font-size: 12px;
        margin-bottom: 8px;
    }
    .insight-panel {
        border-radius: 14px;
        border: 1px solid #18224e;
        background: linear-gradient(180deg, #1a2453 0%, #161d42 100%);
        padding: 14px;
        color: #f5f7ff;
        min-height: 360px;
    }
    .insight-item {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 10px;
        padding: 10px;
        margin-top: 8px;
    }
    .insight-item strong {
        font-size: 13px;
    }
    .insight-item div {
        font-size: 12px;
        opacity: 0.92;
    }
    .chip {
        display: inline-block;
        border: 1px solid #dce2ee;
        color: #54607b;
        border-radius: 999px;
        font-size: 11px;
        padding: 3px 8px;
        margin-right: 6px;
    }
    .ai-chat-shell {
        border: 1px solid #dfe5f1;
        border-radius: 18px;
        overflow: hidden;
        background: #ffffff;
        min-height: 415px;
    }
    .ai-chat-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 14px;
        border-bottom: 1px solid #e9edf6;
        background: #ffffff;
    }
    .ai-chat-title {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    .ai-chat-logo {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: linear-gradient(135deg, #5f4df4, #8d7cff);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
    }
    .ai-chat-body {
        min-height: 250px;
        padding: 12px;
        background: #ffffff;
    }
    .ai-chat-msg {
        background: #edf1f7;
        border-radius: 16px;
        padding: 14px;
        color: #1f2f51;
        font-size: 14px;
        line-height: 1.45;
    }
    .ai-chip-row {
        border-top: 1px solid #e9edf6;
        background: #f9fbff;
        padding: 10px;
        white-space: nowrap;
        overflow-x: auto;
    }
    .ai-input-row {
        border-top: 1px solid #e9edf6;
        background: #f9fbff;
        display: flex;
        gap: 8px;
        align-items: center;
        padding: 10px;
    }
    .ai-input {
        flex: 1;
        border-radius: 16px;
        border: 1px solid #d5ddea;
        padding: 11px 14px;
        color: #607092;
        font-size: 14px;
        background: #f5f8fd;
    }
    .ai-send {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: linear-gradient(135deg, #8f85f4, #b0a9ff);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 17px;
    }
    .footer-card {
        border-top: 1px solid #e1e7f2;
        margin-top: 22px;
        padding-top: 18px;
    }
    .footer-title {
        font-weight: 700;
        color: #28324f;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .footer-link {
        font-size: 13px;
        color: #4e5b79;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-header">
      <div><span class="small-pill">Last updated: Jun 2024</span></div>
      <div><span class="small-pill">Pro Plan</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

variables_df = pd.read_csv("data/datasets/Variables_description_RW_LFS2023.csv")

# remove all the NaN values in the dataframe
variable_df = variables_df.dropna(subset="NaN")

print("variables_df head:", variables_df.head())
# filter gender


total_variables = len(variables_df)
numeric_variables = int(variables_df[variables_df["isnumeric"] == 1].shape[0])
categorical_variables = total_variables - numeric_variables
gender_related_variables = int(
    variables_df["varlab"]
    .fillna("")
    .str.contains("sex|gender|female|male|woman|women|men", case=False, regex=True)
    .sum()
)
print(gender_related_variables)

print(variables_df.columns)


filter_col_1, filter_col_2, filter_col_3, filter_col_4 = st.columns(
    [2.6, 1.2, 1.4, 1.2]
)

with filter_col_1:
    indicator = st.selectbox(
        "Indicator",
        [
            "Wage (Monthly Avg)",
            "Employment Rate (%)",
            "Literacy Rate (%)",
            "Healthcare Access (%)",
            "Business Ownership (%)",
        ],
    )
with filter_col_2:
    year = st.selectbox("Year", [2023, 2022, 2021, 2020, 2019, 2018], index=0)
with filter_col_3:
    region = st.selectbox(
        "Region",
        ["All Regions", "Western", "Southern", "Northern", "Kigali City", "Eastern"],
    )
with filter_col_4:
    st.markdown(
        "<div style='padding-top:30px;color:#7a839f;font-size:12px;'>5 data points loaded</div>",
        unsafe_allow_html=True,
    )

st.markdown("")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.markdown(
    f"""
    <div class="kpi-card">
      <div class="kpi-title">Total Variables</div>
      <div class="kpi-value">{total_variables}</div>
      <div class="kpi-sub">Indicators available in RW LFS 2023</div>
    </div>
    """,
    unsafe_allow_html=True,
)
kpi2.markdown(
    f"""
    <div class="kpi-card">
      <div class="kpi-title">Numeric Variables</div>
      <div class="kpi-value">{numeric_variables}</div>
      <div class="kpi-sub">Ready for direct statistical analysis</div>
    </div>
    """,
    unsafe_allow_html=True,
)
kpi3.markdown(
    f"""
    <div class="kpi-card">
      <div class="kpi-title">Categorical Variables</div>
      <div class="kpi-value">{categorical_variables}</div>
      <div class="kpi-sub">Suitable for group comparisons & gaps</div>
    </div>
    """,
    unsafe_allow_html=True,
)
kpi4.markdown(
    f"""
    <div class="kpi-card">
      <div class="kpi-title">Gender‑Related Variables</div>
      <div class="kpi-value">{gender_related_variables}</div>
      <div class="kpi-sub">Variables explicitly referencing sex or gender</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# ── Variables description dataset overview ───────────────────────────────────────

meta_col1, meta_col2 = st.columns(2)

type_counts = (
    variables_df["type"]
    .fillna("unknown")
    .astype(str)
    .value_counts()
    .reset_index()
    .rename(columns={"index": "type", "type": "count"})
)

section_counts = (
    variables_df["name"]
    .fillna("")
    .astype(str)
    .str[0]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "section", "name": "count"})
    .sort_values("section")
)

with meta_col1:
    st.markdown(
        "<div class='section-card'><div class='panel-title'>Variables by storage type</div><div class='panel-subtitle'>How many indicators are int, byte, float, etc.</div>",
        unsafe_allow_html=True,
    )
    type_fig = px.bar(type_counts, x="type", y="count", text="count", color="type")
    type_fig.update_layout(
        margin=dict(l=10, r=10, t=8, b=8),
        height=260,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="",
        yaxis_title="Variables",
    )
    type_fig.update_traces(textposition="outside")
    st.plotly_chart(type_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with meta_col2:
    st.markdown(
        "<div class='section-card'><div class='panel-title'>Variables by questionnaire section</div><div class='panel-subtitle'>First letter of variable name (A = demographics, B = education, ...)</div>",
        unsafe_allow_html=True,
    )
    section_fig = px.bar(
        section_counts,
        x="section",
        y="count",
        text="count",
        color="section",
    )
    section_fig.update_layout(
        margin=dict(l=10, r=10, t=8, b=8),
        height=260,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Section code",
        yaxis_title="Variables",
    )
    section_fig.update_traces(textposition="outside")
    st.plotly_chart(section_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

left_chart_col, insight_col = st.columns([2.25, 1.0])

trend_df = pd.DataFrame(
    {
        "year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "gap": [10.8, 9.3, 13.4, 9.8, 6.7, 5.2, 4.1, 3.0, 2.1],
        "segment": [
            "Historical",
            "Historical",
            "Historical",
            "Historical",
            "Historical",
            "Historical",
            "Forecast",
            "Forecast",
            "Forecast",
        ],
    }
)

with left_chart_col:
    st.markdown(
        "<div class='section-card'><div class='panel-title'>Gender Gap Trend & Forecast</div><div class='panel-subtitle'>2018-2023 historical · 2024-2026 ML forecast</div>",
        unsafe_allow_html=True,
    )

    df = pd.DataFrame(
        {
            "year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
            "gap": [10.8, 9.3, 13.4, 9.8, 6.7, 5.2, 4.1, 3.0, 2.1],
            "segment": [
                "Historical",
                "Historical",
                "Historical",
                "Historical",
                "Historical",
                "Historical",
                "Forecast",
                "Forecast",
                "Forecast",
            ],
        }
    )

    trend_fig = px.line(
        trend_df,
        x="year",
        y="gap",
        markers=True,
        color="segment",
        color_discrete_map={"Historical": "#5B6CFA", "Forecast": "#9AA6FF"},
    )
    trend_fig.update_layout(
        margin=dict(l=10, r=10, t=8, b=8),
        height=315,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        xaxis_title="",
        yaxis_title="",
    )
    trend_fig.update_traces(line_width=3)
    st.plotly_chart(trend_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with insight_col:
    st.markdown(
        """
        <div class="insight-panel">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div style="font-weight:700;font-size:14px;">AI Insights</div>
            <span class="small-pill" style="background:rgba(255,255,255,0.08);color:#dbe2ff;border-color:rgba(255,255,255,0.15);">Live</span>
          </div>
          <div class="insight-item"><strong>Gap Closing</strong><div>Wage (Monthly Avg) gap has decreased by 52.6% since 2018.</div></div>
          <div class="insight-item"><strong>Highest Disparity</strong><div>Western Province shows the highest gap at 11.6%.</div></div>
          <div class="insight-item"><strong>Parity Leader</strong><div>Eastern Province leads in gender parity with a 0.5% gap.</div></div>
          <div class="insight-item"><strong>Forecast Signal</strong><div>ML model projects gap decreases through 2026.</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

line_col, ask_col = st.columns([2.25, 1.0])

series_df = pd.DataFrame(
    {
        "year": [2018, 2019, 2020, 2021, 2022, 2023],
        "Female": [52.1, 51.8, 52.0, 55.4, 60.9, 62.5],
        "Male": [63.8, 62.6, 65.7, 64.9, 66.2, 67.6],
    }
)
series_long = series_df.melt(id_vars="year", var_name="group", value_name="value")

with line_col:
    st.markdown(
        "<div class='section-card'><div class='panel-title'>Male vs Female Over Time</div><div class='panel-subtitle'>Average values across all regions for selected indicator</div>",
        unsafe_allow_html=True,
    )
    line_fig = px.line(
        series_long,
        x="year",
        y="value",
        color="group",
        markers=True,
        color_discrete_map={"Female": "#F46A9B", "Male": "#32B3E5"},
    )
    line_fig.update_layout(
        margin=dict(l=10, r=10, t=8, b=8),
        height=290,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        xaxis_title="",
        yaxis_title="",
    )
    line_fig.update_traces(line_width=3)
    st.plotly_chart(line_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with ask_col:
    st.markdown(
        """
        <div class="ai-chat-shell">
            <div class="ai-chat-head">
                <div class="ai-chat-title">
                    <div class="ai-chat-logo">⌘</div>
                    <div>
                        <div style="font-size:16px;font-weight:700;color:#1d2a46;">Ask Intelligence</div>
                        <div style="font-size:12px;color:#7b88a5;">Powered by EquiStat AI</div>
                    </div>
                </div>
                <div style="font-size:12px;color:#00a46d;font-weight:600;">Online</div>
            </div>
            <div class="ai-chat-body">
                <div class="ai-chat-msg">
                    Hello! I'm your Gender Data Intelligence assistant. I can help you analyze Rwanda's gender statistics, identify trends, and uncover regional disparities. What would you like to explore today?
                </div>
                <div style="font-size:12px;color:#a8b3ca;margin-top:8px;">09:36 PM</div>
            </div>
            <div class="ai-chip-row">
                <span class="chip">Highest gap region?</span>
                <span class="chip">Show trend analysis</span>
                <span class="chip">Give me a summary</span>
                <span class="chip">Predict</span>
            </div>
          
        </div>
        """,
        unsafe_allow_html=True,
    )
    title = st.text_input(
        "Ask about trends, gaps, forecasts...",
        placeholder="Ask about trends, gaps, forecasts...",
    )
    st.write(title)

    st.button("Send", use_container_width=True)

st.markdown("")

rank_df = pd.DataFrame(
    {
        "region": ["Western", "Southern", "Northern", "Kigali City", "Eastern"],
        "gap": [11.6, 10.3, 3.2, 2.4, 0.5],
    }
)
rank_fig = px.bar(
    rank_df,
    x="gap",
    y="region",
    orientation="h",
    color="region",
    color_discrete_map={
        "Western": "#5B6CFA",
        "Eastern": "#25C997",
        "Southern": "#E3E8F2",
        "Northern": "#E3E8F2",
        "Kigali City": "#E3E8F2",
    },
)
rank_fig.update_layout(
    margin=dict(l=8, r=8, t=8, b=8),
    height=300,
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="",
    yaxis_title="",
)
rank_fig.update_traces(marker_line_width=0)
rank_fig.update_yaxes(categoryorder="total ascending")

st.markdown(
    "<div class='section-card'><div class='panel-title'>Regional Disparity Ranking</div><div class='panel-subtitle'>Gender gap by province · 2023</div>",
    unsafe_allow_html=True,
)
st.plotly_chart(rank_fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")

table_df = pd.DataFrame(
    {
        "INDICATOR": [
            "Employment Rate (%)",
            "Literacy Rate (%)",
            "Primary Education (%)",
            "Wage (Monthly Avg)",
            "Healthcare Access (%)",
            "Business Ownership (%)",
        ],
        "FEMALE": ["52.7%", "59.9%", "61.9%", "62.5%", "52.6%", "57.3%"],
        "MALE": ["57.5%", "64.8%", "70.2%", "67.6%", "62.9%", "64.0%"],
        "GAP": ["4.8%", "4.9%", "8.4%", "5.1%", "10.3%", "6.6%"],
        "STATUS": [
            "On Track",
            "On Track",
            "Needs Attention",
            "On Track",
            "Needs Attention",
            "On Track",
        ],
    }
)


def _status_label(value: str) -> str:
    if value == "On Track":
        return "🟢 On Track"
    return "🟡 Needs Attention"


table_df["STATUS"] = table_df["STATUS"].apply(_status_label)

st.markdown(
    "<div class='section-card'><div class='panel-title'>All Indicators Overview</div><div class='panel-subtitle'>Comparative gender gaps across all tracked indicators · 2023</div>",
    unsafe_allow_html=True,
)
st.dataframe(table_df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-card">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:18px;">
        <div>
          <div class="footer-title">EquiStat AI</div>
          <div class="footer-link">Empowering researchers, journalists, and policymakers with AI-driven gender analytics.</div>
          <div class="footer-link">SOC 2 Certified · GDPR Compliant</div>
        </div>
        <div>
          <div class="footer-title">Resources</div>
          <div class="footer-link">API Documentation</div>
          <div class="footer-link">Bulk CSV Export</div>
          <div class="footer-link">Research Papers</div>
        </div>
        <div>
          <div class="footer-title">Support</div>
          <div class="footer-link">Contact Experts</div>
          <div class="footer-link">Report Inaccuracy</div>
          <div class="footer-link">Request Indicator</div>
        </div>
        <div>
          <div class="footer-title">Platform</div>
          <div class="footer-link">Pricing & Plans</div>
          <div class="footer-link">Privacy Policy</div>
          <div class="footer-link">Terms of Use</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
