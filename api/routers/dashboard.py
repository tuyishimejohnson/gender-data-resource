"""
Dashboard data endpoints — computed dynamically from Rwanda LFS parquet files.

Endpoints:
    GET /dashboard/kpis?year=2023         — KPI summary (gap, female avg, male avg, regions)
    GET /dashboard/trend                   — Gender gap trend + 2-year forecast
    GET /dashboard/timeseries              — Male vs female employment rate by year
    GET /dashboard/regional?year=2023     — Gender gap by province
    GET /dashboard/indicators?year=2023   — Indicators overview table
"""
import duckdb
import numpy as np
from fastapi import APIRouter, Query

from api.config import PARQUET

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Rwanda province code → label
_PROVINCE = {1: "Eastern", 2: "Kigali City", 3: "Northern", 4: "Southern", 5: "Western"}

# Survey year → DuckDB view name
_YEAR_TABLE = {2022: "lfs2022", 2023: "lfs2023", 2024: "lfs2024"}


def _connect() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    for name, path in PARQUET.items():
        con.execute(f"CREATE VIEW {name} AS SELECT * FROM read_parquet('{path}')")
    return con


def _emp_rates(con, table: str) -> tuple[float, float, float]:
    """Return (female_rate, male_rate, gap) weighted employment rates."""
    df = con.execute(f"""
        SELECT
            A01,
            SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END)
                / NULLIF(SUM(weight2), 0) * 100 AS emp_rate
        FROM {table}
        WHERE weight2 > 0
        GROUP BY A01
    """).fetchdf()
    female = df.loc[df["A01"] == 2, "emp_rate"].values
    male = df.loc[df["A01"] == 1, "emp_rate"].values
    f = round(float(female[0]), 1) if len(female) else 0.0
    m = round(float(male[0]), 1) if len(male) else 0.0
    gap = round(abs(m - f), 1)
    return f, m, gap


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.get("/kpis")
def get_kpis(year: int = Query(default=2023, description="Survey year: 2022, 2023, or 2024")):
    """Employment-rate KPIs: gender gap, female avg, male avg, and region count."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        f, m, gap = _emp_rates(con, table)
        regions = int(con.execute(f"SELECT COUNT(DISTINCT province) FROM {table}").fetchone()[0])
    finally:
        con.close()
    return {
        "avg_gender_gap": gap,
        "female_avg": f,
        "male_avg": m,
        "regions_tracked": regions,
        "year": year,
        "indicator": "Employment Rate (%)",
    }


@router.get("/trend")
def get_trend():
    """Gender gap trend across available survey years plus a 2-year linear forecast."""
    con = _connect()
    try:
        historical = []
        for year in sorted(_YEAR_TABLE):
            _, _, gap = _emp_rates(con, _YEAR_TABLE[year])
            historical.append({"year": year, "gap": gap, "segment": "Historical"})
    finally:
        con.close()

    # Linear regression forecast
    years = np.array([d["year"] for d in historical], dtype=float)
    gaps = np.array([d["gap"] for d in historical], dtype=float)
    coeffs = np.polyfit(years, gaps, 1)
    forecast = [
        {
            "year": yr,
            "gap": round(max(0.0, float(np.polyval(coeffs, yr))), 1),
            "segment": "Forecast",
        }
        for yr in [2025, 2026]
    ]
    return {"data": historical + forecast}


@router.get("/timeseries")
def get_timeseries():
    """Male and female employment rates for each available survey year."""
    con = _connect()
    try:
        rows = []
        for year in sorted(_YEAR_TABLE):
            f, m, _ = _emp_rates(con, _YEAR_TABLE[year])
            rows.append({"year": year, "Female": f, "Male": m})
    finally:
        con.close()
    return {"data": rows}


@router.get("/regional")
def get_regional(year: int = Query(default=2023)):
    """Employment rate gender gap by province for a given survey year."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                province,
                A01,
                SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END)
                    / NULLIF(SUM(weight2), 0) * 100 AS emp_rate
            FROM {table}
            WHERE weight2 > 0
            GROUP BY province, A01
        """).fetchdf()
    finally:
        con.close()

    results = []
    for code, name in _PROVINCE.items():
        pdata = df[df["province"] == code]
        female = pdata.loc[pdata["A01"] == 2, "emp_rate"].values
        male = pdata.loc[pdata["A01"] == 1, "emp_rate"].values
        if len(female) and len(male):
            gap = round(abs(float(male[0]) - float(female[0])), 1)
            results.append({"region": name, "gap": gap})

    results.sort(key=lambda x: x["gap"], reverse=True)
    return {"data": results, "year": year}


@router.get("/indicators")
def get_indicators(year: int = Query(default=2023)):
    """Indicators overview: employment rate and LFPR split by gender."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        f, m, gap = _emp_rates(con, table)
        lfpr_df = con.execute(f"""
            SELECT A01, AVG(LFPR) AS lfpr
            FROM {table}
            WHERE LFPR IS NOT NULL
            GROUP BY A01
        """).fetchdf()
    finally:
        con.close()

    def _status(g: float) -> str:
        return "🟢 On Track" if g < 6 else "🟡 Needs Attention"

    rows = [
        {
            "INDICATOR": "Employment Rate (%)",
            "FEMALE": f"{f}%",
            "MALE": f"{m}%",
            "GAP": f"{gap}%",
            "STATUS": _status(gap),
        }
    ]

    if not lfpr_df.empty:
        lfpr_f = lfpr_df.loc[lfpr_df["A01"] == 2, "lfpr"].values
        lfpr_m = lfpr_df.loc[lfpr_df["A01"] == 1, "lfpr"].values
        if len(lfpr_f) and len(lfpr_m):
            lf_f = round(float(lfpr_f[0]), 1)
            lf_m = round(float(lfpr_m[0]), 1)
            lf_gap = round(abs(lf_m - lf_f), 1)
            rows.append(
                {
                    "INDICATOR": "Labour Force Participation Rate (%)",
                    "FEMALE": f"{lf_f}%",
                    "MALE": f"{lf_m}%",
                    "GAP": f"{lf_gap}%",
                    "STATUS": _status(lf_gap),
                }
            )

    return {"data": rows, "year": year}
