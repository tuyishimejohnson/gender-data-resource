import streamlit as st

from src.filters import apply_study_filters, filter_resources_by_type
from src.loaders import get_data_dir, load_all_data

st.title("Discovery")
st.caption(f"Data source: `{get_data_dir()}`")

studies, resources, quality = load_all_data()
# Avoid merge suffix collisions with similarly named study fields.
quality_map = quality[["study_id", "quality_flags", "missing_field_count"]].rename(
    columns={
        "quality_flags": "quality_flags_quality",
        "missing_field_count": "missing_field_count_quality",
    }
)

query = st.text_input("Search by title/abstract", "")
years = st.columns(2)
year_min = years[0].number_input("Year from", value=2000, step=1)
year_max = years[1].number_input("Year to", value=2026, step=1)
resource_type = st.selectbox("Resource type", ["all"] + sorted(resources["type"].fillna("unknown").astype(str).str.lower().unique().tolist()))

filtered = apply_study_filters(studies, query=query, year_min=int(year_min), year_max=int(year_max))
res_filtered = filter_resources_by_type(resources, resource_type)

merged = filtered.merge(quality_map, on="study_id", how="left")
merged = merged.merge(
    res_filtered.groupby("study_id", as_index=False)["url"].count().rename(columns={"url": "matching_resources"}),
    on="study_id",
    how="left",
)
merged["matching_resources"] = merged["matching_resources"].fillna(0).astype(int)
merged["quality_flags_display"] = merged.get("quality_flags_quality", "").fillna(
    merged.get("quality_flags", "")
)
merged["missing_field_count_display"] = (
    merged.get("missing_field_count_quality", 0).fillna(merged.get("missing_field_count", 0)).fillna(0).astype(int)
)

st.subheader("Results")
st.dataframe(
    merged[
        [
            "study_id",
            "title",
            "year",
            "matching_resources",
            "missing_field_count_display",
            "quality_flags_display",
            "url",
            "get_microdata_url",
        ]
    ],
    use_container_width=True,
)

