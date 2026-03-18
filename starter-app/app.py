import streamlit as st

st.set_page_config(page_title="Gender Data Visibility Starter", layout="wide")

st.title("Gender Data Visibility Starter App")
st.write(
    "This starter is a runnable baseline for hackathon teams. "
    "Use the sidebar pages for discovery, dashboard views, and data quality checks."
)

st.subheader("Quick start")
st.markdown(
    """
1. Install dependencies from `requirements.txt`
2. Run `streamlit run app.py`
3. Open **Discovery** page first
4. Use `data/sample/` by default, then switch to full data if needed
"""
)

st.subheader("Ready demo scenario")
st.info(
    "Try searching for `labour`, filter by a recent year range, and review quality flags "
    "for missing metadata before presenting a policy-relevant insight."
)

