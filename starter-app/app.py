# import streamlit as st

# st.set_page_config(
#     page_title="Gender Data Resource Discovery", page_icon=":bar-chart:", layout="wide"
# )

# st.title("Gender Data Resource Discovery")
# st.write(
#     "This starter is a runnable baseline for hackathon teams. "
#     "Use the sidebar pages for discovery, dashboard views, and data quality checks."
# )

# st.subheader("Quick start")
# st.markdown(
#     """
# 1. Install dependencies from `requirements.txt`
# 2. Run `streamlit run app.py`
# 3. Open **Discovery** page first
# 4. Use `data/sample/` by default, then switch to full data if needed
# """
# )

# st.subheader("Ready demo scenario")
# st.info(
#     "Try searching for `labour`, filter by a recent year range, and review quality flags "
#     "for missing metadata before presenting a policy-relevant insight."
# )


import pandas as pd
import plotly.express as px
import streamlit as st
from pages.ai_assistant import render_ai_assistant
from src.navigation import render_top_nav


st.set_page_config(
    page_title="Gender Intelligence Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Make the project "home" render the polished dashboard page.
# This also avoids the older mixed-layout code below.
st.switch_page("pages/2_Dashboard.py")
