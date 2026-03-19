"""
Tool 2 — DuckDB query over Rwanda LFS parquet datasets.

Three views are registered on each call:
  lfs2022 — 70,424 rows  (survey year 2022)
  lfs2023 — 71,849 rows  (survey year 2023)
  lfs2024 — 102,562 rows (survey year 2024)

All tables share 170 common columns.
Only SELECT statements are allowed; results are capped at 500 rows.
"""
import duckdb

from api.config import PARQUET


def _run_query(sql: str) -> str:
    """Execute a SQL SELECT against the LFS parquet files and return a text table."""
    sql = sql.strip()
    if not sql.upper().lstrip().startswith("SELECT"):
        return "Error: only SELECT statements are permitted."

    con = duckdb.connect()
    try:
        for name, path in PARQUET.items():
            con.execute(
                f"CREATE VIEW {name} AS SELECT * FROM read_parquet('{path}')"
            )
        result = con.execute(sql).fetchdf()
    except Exception as exc:
        return f"Query error: {exc}"
    finally:
        con.close()

    if result.empty:
        return "Query returned no results."

    return result.head(500).to_string(index=False)
