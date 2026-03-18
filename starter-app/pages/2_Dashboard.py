import pandas as pd
import plotly.express as px
import streamlit as st

from src.loaders import get_data_dir, load_all_data

st.title("Dashboard")
st.caption(f"Data source: `{get_data_dir()}`")

studies, resources, quality = load_all_data()
studies["year_num"] = pd.to_numeric(studies.get("year"), errors="coerce")

col1, col2, col3 = st.columns(3)
col1.metric("Studies", len(studies))
col2.metric("Resources", len(resources))
col3.metric("Quality rows", len(quality))

st.subheader("Studies by year")
year_counts = studies.dropna(subset=["year_num"]).groupby("year_num", as_index=False)["study_id"].count()
year_counts.rename(columns={"study_id": "count"}, inplace=True)
fig = px.bar(year_counts, x="year_num", y="count")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Resource types")
type_counts = resources["type"].fillna("unknown").astype(str).str.lower().value_counts().reset_index()
type_counts.columns = ["type", "count"]
fig2 = px.pie(type_counts, names="type", values="count")
st.plotly_chart(fig2, use_container_width=True)

