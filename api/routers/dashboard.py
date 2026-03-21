"""
Dashboard data endpoints — computed dynamically from Rwanda LFS parquet files.

Endpoints:
    GET /dashboard/kpis?year=2023                          — KPI summary (gap, female avg, male avg, regions)
    GET /dashboard/trend                                    — Gender gap trend + 2-year forecast
    GET /dashboard/timeseries                               — Male vs female employment rate by year
    GET /dashboard/regional?year=2023                      — Gender gap by province
    GET /dashboard/indicators?year=2023                    — Indicators overview table
    GET /dashboard/core-metrics                             — Employment rate, unemployment rate, and LFPR by gender
    GET /dashboard/income-inequality/average-income?year=2023  — Average income by gender (box plot stats)
    GET /dashboard/income-inequality/income-distribution?year=2023 — Income distribution by gender (histogram)
    GET /dashboard/income-inequality/hourly-wage?year=2023     — Hourly wage gap by gender (box plot stats)
    GET /dashboard/sector-segregation/employment-by-sector?year=2023 — Employment by sector and gender (stacked bar)
    GET /dashboard/sector-segregation/formal-informal?year=2023 — Formal vs informal employment by gender
    GET /dashboard/sector-segregation/occupation-segregation?year=2023 — Occupation segregation by ISCO codes
    GET /dashboard/geography/employment-by-province?year=2023 — Employment rates by province and gender
    GET /dashboard/geography/urban-rural-gap?year=2023     — Urban vs rural employment gap by gender
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

# Economic sector codes
_SECTOR = {1: "Agriculture", 2: "Industry", 3: "Services"}

# Formal/Informal employment codes
_FORMAL_INFORMAL = {1: "Formal", 2: "Informal", 3: "Other"}

# Urban/Rural codes
_URBAN_RURAL = {1: "Urban", 2: "Rural"}

# ISCO-08 Major Groups (2-digit codes)
_ISCO_GROUPS = {
    11: "Chief Executives & Legislators",
    12: "Administrative Managers",
    13: "Production & Specialized Managers",
    14: "Hospitality & Retail Managers",
    21: "Science & Engineering Professionals",
    22: "Health Professionals",
    23: "Teaching Professionals",
    24: "Business & Admin Professionals",
    25: "ICT Professionals",
    26: "Legal & Social Professionals",
    31: "Science & Engineering Technicians",
    32: "Health Associate Professionals",
    33: "Business & Admin Associates",
    34: "Legal & Social Associates",
    35: "ICT Technicians",
    41: "General Office Clerks",
    42: "Customer Service Clerks",
    43: "Numerical Clerks",
    44: "Other Clerical Workers",
    51: "Personal Service Workers",
    52: "Sales Workers",
    53: "Personal Care Workers",
    54: "Protective Service Workers",
    61: "Market-Oriented Farmers",
    62: "Forestry & Fishery Workers",
    71: "Building Trades Workers",
    72: "Metal & Machinery Workers",
    73: "Handicraft Workers",
    74: "Electrical Workers",
    75: "Food Processing Workers",
    81: "Stationary Plant Operators",
    82: "Assemblers",
    83: "Drivers & Mobile Operators",
    91: "Cleaners & Helpers",
    92: "Agricultural Laborers",
    93: "Laborers in Mining & Construction",
    94: "Food Preparation Assistants",
    95: "Street & Related Workers",
    96: "Refuse Workers",
}


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


@router.get("/core-metrics")
def get_core_metrics():
    """Calculate Employment Rate, Unemployment Rate, and LFPR by gender across all years."""
    con = _connect()
    try:
        results = []
        for year in sorted(_YEAR_TABLE):
            table = _YEAR_TABLE[year]

            df = con.execute(f"""
                SELECT
                    A01 as gender,
                    SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END)
                        / NULLIF(SUM(weight2), 0) * 100 AS employment_rate,
                    SUM(CASE WHEN status1 = 2 THEN weight2 ELSE 0 END)
                        / NULLIF(
                            SUM(CASE WHEN status1 IN (1, 2) THEN weight2 ELSE 0 END),
                            0
                        ) * 100 AS unemployment_rate,
                    SUM(CASE WHEN status1 IN (1, 2) THEN weight2 ELSE 0 END)
                        / NULLIF(SUM(weight2), 0) * 100 AS lfpr
                FROM {table}
                WHERE weight2 > 0
                GROUP BY A01
            """).fetchdf()

            female_row = df[df["gender"] == 2]
            male_row = df[df["gender"] == 1]

            year_data = {
                "year": year,
                "employment_rate": {
                    "Female": round(float(female_row["employment_rate"].values[0]), 1) if len(female_row) else 0.0,
                    "Male": round(float(male_row["employment_rate"].values[0]), 1) if len(male_row) else 0.0
                },
                "unemployment_rate": {
                    "Female": round(float(female_row["unemployment_rate"].values[0]), 1) if len(female_row) else 0.0,
                    "Male": round(float(male_row["unemployment_rate"].values[0]), 1) if len(male_row) else 0.0
                },
                "lfpr": {
                    "Female": round(float(female_row["lfpr"].values[0]), 1) if len(female_row) else 0.0,
                    "Male": round(float(male_row["lfpr"].values[0]), 1) if len(male_row) else 0.0
                }
            }
            results.append(year_data)
    finally:
        con.close()

    return {"data": results}


@router.get("/income-inequality/average-income")
def get_average_income(year: int = Query(default=2023)):
    """Average monthly income by gender (cash field) - returns box plot statistics."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                A01 as gender,
                cash
            FROM {table}
            WHERE cash IS NOT NULL AND cash > 0 AND weight2 > 0
        """).fetchdf()
    finally:
        con.close()

    female_data = df[df["gender"] == 2]["cash"].values
    male_data = df[df["gender"] == 1]["cash"].values

    def calculate_stats(data):
        if len(data) == 0:
            return {"min": 0, "q1": 0, "median": 0, "q3": 0, "max": 0, "mean": 0}
        return {
            "min": float(np.min(data)),
            "q1": float(np.percentile(data, 25)),
            "median": float(np.percentile(data, 50)),
            "q3": float(np.percentile(data, 75)),
            "max": float(np.max(data)),
            "mean": float(np.mean(data))
        }

    return {
        "year": year,
        "data": {
            "Female": calculate_stats(female_data),
            "Male": calculate_stats(male_data)
        }
    }


@router.get("/income-inequality/income-distribution")
def get_income_distribution(year: int = Query(default=2023)):
    """Income distribution by gender (intcash intervals) - returns histogram data."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                A01 as gender,
                intcash,
                COUNT(*) as count,
                SUM(weight2) as weighted_count
            FROM {table}
            WHERE intcash IS NOT NULL AND weight2 > 0
            GROUP BY A01, intcash
            ORDER BY intcash
        """).fetchdf()
    finally:
        con.close()

    income_brackets = sorted(df["intcash"].unique())
    
    female_dist = []
    male_dist = []
    
    for bracket in income_brackets:
        female_count = df[(df["gender"] == 2) & (df["intcash"] == bracket)]["weighted_count"].sum()
        male_count = df[(df["gender"] == 1) & (df["intcash"] == bracket)]["weighted_count"].sum()
        
        female_dist.append(float(female_count))
        male_dist.append(float(male_count))

    return {
        "year": year,
        "brackets": [int(b) for b in income_brackets],
        "data": {
            "Female": female_dist,
            "Male": male_dist
        }
    }


@router.get("/income-inequality/hourly-wage")
def get_hourly_wage(year: int = Query(default=2023)):
    """Hourly wage gap by gender (hr_cash field) - returns box plot statistics."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                A01 as gender,
                hr_cash
            FROM {table}
            WHERE hr_cash IS NOT NULL AND hr_cash > 0 AND weight2 > 0
        """).fetchdf()
    finally:
        con.close()

    female_data = df[df["gender"] == 2]["hr_cash"].values
    male_data = df[df["gender"] == 1]["hr_cash"].values

    def calculate_stats(data):
        if len(data) == 0:
            return {"min": 0, "q1": 0, "median": 0, "q3": 0, "max": 0, "mean": 0}
        return {
            "min": float(np.min(data)),
            "q1": float(np.percentile(data, 25)),
            "median": float(np.percentile(data, 50)),
            "q3": float(np.percentile(data, 75)),
            "max": float(np.max(data)),
            "mean": float(np.mean(data))
        }

    return {
        "year": year,
        "data": {
            "Female": calculate_stats(female_data),
            "Male": calculate_stats(male_data)
        }
    }


@router.get("/sector-segregation/employment-by-sector")
def get_employment_by_sector(year: int = Query(default=2023)):
    """Employment by sector and gender - returns stacked bar chart data."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                main_sect,
                A01 as gender,
                SUM(weight2) as weighted_count
            FROM {table}
            WHERE main_sect IS NOT NULL AND weight2 > 0
            GROUP BY main_sect, A01
            ORDER BY main_sect, A01
        """).fetchdf()
    finally:
        con.close()

    sectors = []
    for sector_code in sorted(_SECTOR.keys()):
        sector_data = df[df["main_sect"] == sector_code]
        female_count = sector_data[sector_data["gender"] == 2]["weighted_count"].sum()
        male_count = sector_data[sector_data["gender"] == 1]["weighted_count"].sum()
        
        total = female_count + male_count
        sectors.append({
            "sector": _SECTOR[sector_code],
            "Female": float(female_count),
            "Male": float(male_count),
            "female_percentage": round(float(female_count / total * 100), 1) if total > 0 else 0,
            "male_percentage": round(float(male_count / total * 100), 1) if total > 0 else 0
        })

    return {
        "year": year,
        "data": sectors
    }


@router.get("/sector-segregation/formal-informal")
def get_formal_informal(year: int = Query(default=2023)):
    """Formal vs informal employment by gender - returns pie/stacked bar data."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                IEV2,
                A01 as gender,
                SUM(weight2) as weighted_count
            FROM {table}
            WHERE IEV2 IS NOT NULL AND weight2 > 0
            GROUP BY IEV2, A01
            ORDER BY IEV2, A01
        """).fetchdf()
    finally:
        con.close()

    categories = []
    for iev_code in sorted(_FORMAL_INFORMAL.keys()):
        cat_data = df[df["IEV2"] == iev_code]
        female_count = cat_data[cat_data["gender"] == 2]["weighted_count"].sum()
        male_count = cat_data[cat_data["gender"] == 1]["weighted_count"].sum()
        
        categories.append({
            "category": _FORMAL_INFORMAL[iev_code],
            "Female": float(female_count),
            "Male": float(male_count)
        })

    # Calculate percentages within each gender
    female_total = sum(c["Female"] for c in categories)
    male_total = sum(c["Male"] for c in categories)
    
    for cat in categories:
        cat["female_percentage"] = round(cat["Female"] / female_total * 100, 1) if female_total > 0 else 0
        cat["male_percentage"] = round(cat["Male"] / male_total * 100, 1) if male_total > 0 else 0

    return {
        "year": year,
        "data": categories
    }


@router.get("/sector-segregation/occupation-segregation")
def get_occupation_segregation(year: int = Query(default=2023)):
    """Occupation segregation by ISCO 2-digit codes - returns heatmap/grouped bar data."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                isco2digit,
                A01 as gender,
                SUM(weight2) as weighted_count
            FROM {table}
            WHERE isco2digit IS NOT NULL AND weight2 > 0
            GROUP BY isco2digit, A01
            ORDER BY isco2digit, A01
        """).fetchdf()
    finally:
        con.close()

    occupations = []
    for isco_code in sorted(_ISCO_GROUPS.keys()):
        occ_data = df[df["isco2digit"] == isco_code]
        female_count = occ_data[occ_data["gender"] == 2]["weighted_count"].sum()
        male_count = occ_data[occ_data["gender"] == 1]["weighted_count"].sum()
        
        total = female_count + male_count
        if total > 0:  # Only include occupations with data
            occupations.append({
                "code": int(isco_code),
                "occupation": _ISCO_GROUPS[isco_code],
                "Female": float(female_count),
                "Male": float(male_count),
                "female_percentage": round(float(female_count / total * 100), 1),
                "male_percentage": round(float(male_count / total * 100), 1),
                "total": float(total)
            })

    # Sort by total employment (descending) to show most significant occupations first
    occupations.sort(key=lambda x: x["total"], reverse=True)

    return {
        "year": year,
        "data": occupations
    }


@router.get("/geography/employment-by-province")
def get_employment_by_province(year: int = Query(default=2023)):
    """Employment by province and gender - returns grouped bar data for map/chart."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                province,
                A01 as gender,
                SUM(weight2) as total_population,
                SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END) as employed_count
            FROM {table}
            WHERE province IS NOT NULL AND weight2 > 0
            GROUP BY province, A01
            ORDER BY province, A01
        """).fetchdf()
    finally:
        con.close()

    provinces = []
    for prov_code in sorted(_PROVINCE.keys()):
        prov_data = df[df["province"] == prov_code]
        
        # Female data
        female_row = prov_data[prov_data["gender"] == 2]
        female_total = female_row["total_population"].sum() if len(female_row) > 0 else 0
        female_employed = female_row["employed_count"].sum() if len(female_row) > 0 else 0
        female_rate = (female_employed / female_total * 100) if female_total > 0 else 0
        
        # Male data
        male_row = prov_data[prov_data["gender"] == 1]
        male_total = male_row["total_population"].sum() if len(male_row) > 0 else 0
        male_employed = male_row["employed_count"].sum() if len(male_row) > 0 else 0
        male_rate = (male_employed / male_total * 100) if male_total > 0 else 0
        
        gap = abs(male_rate - female_rate)
        
        provinces.append({
            "province": _PROVINCE[prov_code],
            "code": int(prov_code),
            "Female": round(float(female_rate), 1),
            "Male": round(float(male_rate), 1),
            "gap": round(float(gap), 1),
            "female_employed": float(female_employed),
            "male_employed": float(male_employed)
        })

    return {
        "year": year,
        "data": provinces
    }


@router.get("/geography/urban-rural-gap")
def get_urban_rural_gap(year: int = Query(default=2023)):
    """Urban vs rural employment gap by gender - returns side-by-side bar data."""
    table = _YEAR_TABLE.get(year, "lfs2023")
    con = _connect()
    try:
        df = con.execute(f"""
            SELECT
                Code_UR,
                A01 as gender,
                SUM(weight2) as total_population,
                SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END) as employed_count
            FROM {table}
            WHERE Code_UR IS NOT NULL AND weight2 > 0
            GROUP BY Code_UR, A01
            ORDER BY Code_UR, A01
        """).fetchdf()
    finally:
        con.close()

    areas = []
    for ur_code in sorted(_URBAN_RURAL.keys()):
        ur_data = df[df["Code_UR"] == ur_code]
        
        # Female data
        female_row = ur_data[ur_data["gender"] == 2]
        female_total = female_row["total_population"].sum() if len(female_row) > 0 else 0
        female_employed = female_row["employed_count"].sum() if len(female_row) > 0 else 0
        female_rate = (female_employed / female_total * 100) if female_total > 0 else 0
        
        # Male data
        male_row = ur_data[ur_data["gender"] == 1]
        male_total = male_row["total_population"].sum() if len(male_row) > 0 else 0
        male_employed = male_row["employed_count"].sum() if len(male_row) > 0 else 0
        male_rate = (male_employed / male_total * 100) if male_total > 0 else 0
        
        gap = abs(male_rate - female_rate)
        
        areas.append({
            "area": _URBAN_RURAL[ur_code],
            "Female": round(float(female_rate), 1),
            "Male": round(float(male_rate), 1),
            "gap": round(float(gap), 1),
            "female_employed": float(female_employed),
            "male_employed": float(male_employed),
            "female_total": float(female_total),
            "male_total": float(male_total)
        })

    return {
        "year": year,
        "data": areas
    }
