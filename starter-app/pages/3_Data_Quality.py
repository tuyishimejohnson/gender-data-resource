import streamlit as st

from src.loaders import get_data_dir, load_all_data
from src.quality_badges import parse_quality_flags, quality_level

st.title("Data Quality")
st.caption(f"Data source: `{get_data_dir()}`")

_, _, quality = load_all_data()
quality = quality.copy()
quality["missing_field_count"] = quality["missing_field_count"].fillna(0).astype(int)
quality["quality_level"] = quality["missing_field_count"].apply(quality_level)
quality["parsed_flags"] = quality["quality_flags"].fillna("").apply(parse_quality_flags)
quality["parsed_flags"] = quality["parsed_flags"].apply(lambda x: ", ".join(x))

st.subheader("Quality overview")
st.dataframe(
    quality[["study_id", "title", "missing_field_count", "quality_level", "parsed_flags"]],
    use_container_width=True,
)

