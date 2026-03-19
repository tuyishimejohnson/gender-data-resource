from __future__ import annotations

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate


# this is to test the agent we will rewrite the context generation logic in the morning
def build_context_string(
    studies: pd.DataFrame,
    quality: pd.DataFrame,
    query: str,
) -> str:

    keywords = [kw for kw in query.lower().split() if len(kw) > 3]

    if keywords:
        mask = studies.apply(
            lambda row: any(kw in str(row.values).lower() for kw in keywords),
            axis=1,
        )
        relevant = studies[mask]
    else:
        relevant = pd.DataFrame()

    if relevant.empty:
        relevant = studies.head(10)

    merged = relevant.merge(
        quality[["study_id", "quality_flags", "missing_field_count"]],
        on="study_id",
        how="left",
    )

    cols = ["study_id", "title", "year", "organization", "abstract", "quality_flags", "missing_field_count"]
    cols = [c for c in cols if c in merged.columns]

    return merged[cols].to_markdown(index=False)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a gender data advisor helping institutions discover, \
interpret, and act on gender-disaggregated research data.

Your mission is to defragment scattered gender-based information — \
surfacing relevant studies, flagging data quality issues, and explaining \
the policy relevance of findings in plain language.

Guidelines:
- Always cite the study title and year when referencing data.
- If a study has quality flags (e.g. missing_study_type, generic_resource_type), \
mention them and explain what they mean for data reliability.
- If no directly relevant study is found, say so clearly and suggest what \
kind of data the institution should look for.
- Keep answers concise and institution-ready (avoid jargon).
- If any tool was called, name it


Current study catalog:
{studies_context}
""",
    ),
    ("human", "{question}"),
])
