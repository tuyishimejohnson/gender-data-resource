from __future__ import annotations

from langchain_core.tools import tool

from src.loaders import load_all_data


# these are basically test tools using the loaders i found in the project template
@tool
def get_internal_data(query: str) -> str:
    from src.agent.context import build_context_string

    studies, _, quality = load_all_data()
    return build_context_string(studies, quality, query)


@tool
def get_quality_summary(study_id: int) -> str:
    _, _, quality = load_all_data()
    row = quality[quality["study_id"] == study_id]
    if row.empty:
        return f"No quality data found for study_id {study_id}."
    return row.to_markdown(index=False)


@tool
def get_study_resources(study_id: int) -> str:
    _, resources, _ = load_all_data()
    rows = resources[resources["study_id"] == study_id]
    if rows.empty:
        return f"No resources found for study_id {study_id}."
    cols = [c for c in ["type", "name", "label", "url"] if c in rows.columns]
    return rows[cols].to_markdown(index=False)
