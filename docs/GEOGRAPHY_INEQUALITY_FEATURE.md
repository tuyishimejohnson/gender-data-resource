# Geography-Based Gender Inequality Feature

## Overview
This feature adds geographic analysis of gender inequality to the Gender Intelligence Dashboard, revealing regional disparities and urban-rural differences in employment across Rwanda.

## Backend Implementation

### New API Endpoints

#### 1. Employment by Province
**Endpoint:** `GET /dashboard/geography/employment-by-province?year=2023`

**Data Source:** province + A01 (gender) + status1 (employment status)

**Response Format:**
```json
{
  "year": 2023,
  "data": [
    {
      "province": "Eastern",
      "code": 1,
      "Female": 32.4,
      "Male": 44.4,
      "gap": 12.0,
      "female_employed": 315340.57,
      "male_employed": 414691.88
    },
    {
      "province": "Kigali City",
      "code": 2,
      "Female": 23.4,
      "Male": 30.6,
      "gap": 7.2,
      "female_employed": 366983.67,
      "male_employed": 450973.12
    }
    // ... other provinces
  ]
}
```

**Insights:**
- Shows employment rates by gender for all 5 provinces
- Reveals regional inequality patterns
- Eastern Province has highest gap (12%)
- Kigali and Western have lowest gaps (7.2%)

#### 2. Urban vs Rural Gender Gap
**Endpoint:** `GET /dashboard/geography/urban-rural-gap?year=2023`

**Data Source:** Code_UR (urban/rural) + A01 (gender) + status1 (employment status)

**Response Format:**
```json
{
  "year": 2023,
  "data": [
    {
      "area": "Urban",
      "Female": 30.6,
      "Male": 41.6,
      "gap": 11.0,
      "female_employed": 617462.51,
      "male_employed": 788263.60,
      "female_total": 2015406.94,
      "male_total": 1893176.05
    },
    {
      "area": "Rural",
      "Female": 24.0,
      "Male": 30.8,
      "gap": 6.9,
      "female_employed": 1178811.40,
      "male_employed": 1400626.91,
      "female_total": 4914008.98,
      "male_total": 4540266.15
    }
  ]
}
```

**Insights:**
- Urban areas have LARGER gender gap (11%) than rural (6.9%)
- Surprising finding: rural women relatively better off (though both genders have lower employment in rural)
- Urban employment higher overall for both genders
- Shows absolute employment numbers and population totals

## Frontend Implementation

### New Component: `GeographyInequality.tsx`

Located at: `frontend/app/components/GeographyInequality.tsx`

**Features:**
- Two-column layout with complementary visualizations
- Grouped bar chart for province-by-province comparison
- Side-by-side bar chart for urban vs rural comparison
- Color-coded gap indicators (red >10%, yellow 5-10%, green <5%)
- Detailed statistics cards for urban and rural areas
- Dynamic insights showing highest/lowest gap provinces
- Y-axis labels showing "Employment Rate (%)"

**Visualization Types:**
1. **Employment by Province**: Grouped bar chart with provinces sorted by gap (highest first)
2. **Urban vs Rural**: Side-by-side grouped bars for easy comparison

### Dashboard Integration

Updated `frontend/app/routes/home.tsx` to:
- Import new data types and API functions
- Add state management for two new data streams
- Fetch all geography data on mount and year change
- Display component in main dashboard layout (positioned after Sector Segregation)

## TypeScript Types

Added to `frontend/app/services/types.ts`:
- `ProvinceEmploymentPoint` - Province employment data with gaps
- `ProvinceEmploymentData` - Province employment response structure
- `UrbanRuralPoint` - Urban/rural data with totals
- `UrbanRuralData` - Urban/rural response structure

## API Service

Extended `frontend/app/services/index.ts` with:
- `getProvinceEmployment(year)` - Fetch employment by province data
- `getUrbanRuralGap(year)` - Fetch urban vs rural gap data

## Key Insights Revealed

Based on 2023 Rwanda LFS data:

### Provincial Disparities
**Ranked by Gender Gap (Highest to Lowest):**

1. **Eastern Province**: 12.0% gap (F: 32.4%, M: 44.4%)
   - Highest inequality
   - Predominantly rural/agricultural

2. **Southern Province**: 8.1% gap (F: 25.8%, M: 33.9%)

3. **Northern Province**: 7.4% gap (F: 23.2%, M: 30.6%)

4. **Kigali City**: 7.2% gap (F: 23.4%, M: 30.6%)
   - Surprisingly not the best despite being capital
   - Urban advantages offset by other factors

5. **Western Province**: 7.2% gap (F: 26.9%, M: 34.1%)
   - Tied for lowest gap with Kigali

### Urban vs Rural Analysis

**Urban Areas:**
- Female employment: 30.6%
- Male employment: 41.6%
- Gap: **11.0%**
- Higher overall employment for both genders
- BUT larger gender disparity

**Rural Areas:**
- Female employment: 24.0%
- Male employment: 30.8%
- Gap: **6.9%**
- Lower overall employment for both genders
- BUT smaller gender disparity

**Surprising Finding:**
- Urban areas have a LARGER gap (11% vs 6.9%)
- Challenges conventional wisdom that rural women are always more disadvantaged
- Possible explanations:
  - Urban formal sector may be more male-dominated
  - Rural women participate more in agriculture (counted as employed)
  - Urban barriers (education, networks) may disproportionately affect women
  - Different occupational structures

### Key Patterns
1. **Eastern Province outlier**: 12% gap suggests specific regional factors
2. **Urban paradox**: Higher employment BUT larger gender gap
3. **Geographic inequality**: 4.8 percentage point spread between provinces
4. **Policy targeting**: Eastern Province needs focused interventions

## Testing

### Backend Tests
All endpoints tested and returning 200 OK:
- ✅ `/dashboard/geography/employment-by-province?year=2023`
- ✅ `/dashboard/geography/urban-rural-gap?year=2023`

### Frontend Tests
- ✅ Server running on http://localhost:5173
- ✅ Hot module reloading working
- ✅ TypeScript compilation successful
- ✅ Component rendering without errors
- ✅ All API calls succeeding (logs confirm lines 778-779)

## Running the Feature

### Backend
```bash
python3 -m uvicorn api.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend && npm run dev
```

Access the dashboard at: http://localhost:5173/

## Technical Implementation Details

### Backend
- Uses DuckDB for efficient parquet file querying
- Calculates employment rates from status1 (1=employed, 2=unemployed, 3=inactive)
- Weighted counts using weight2 for accurate population representation
- Province mapping: 1=Eastern, 2=Kigali City, 3=Northern, 4=Southern, 5=Western
- Code_UR: 1=Urban, 2=Rural
- Filters for valid data (non-null, positive weights)

### Frontend
- Responsive two-column grid layout
- Recharts library for professional visualizations
- Grouped bar charts for clear comparisons
- Color-coded badges for gap severity
- Statistics cards with detailed breakdowns
- Dynamic sorting (provinces by gap)
- Y-axis labels for clarity
- Loading states with skeleton UI

### Data Processing
- Employment rate = (employed / total_population) * 100
- Gap = |male_rate - female_rate|
- Absolute numbers provided for context
- Sorted display for better insights

## Policy Implications

### Regional Targeting
**Eastern Province (12% gap):**
- Needs focused interventions
- Investigate specific barriers
- Agricultural sector analysis
- Infrastructure development
- Women's cooperatives support

**Better Performing Regions:**
- Study Kigali and Western success factors
- Replicate best practices
- Cross-province learning programs

### Urban-Rural Strategy
**Urban Areas (11% gap):**
- Despite higher overall employment, larger gender disparity
- Focus on:
  - Formal sector access for women
  - Skills training for urban markets
  - Childcare infrastructure
  - Gender bias in hiring
  - Network building programs

**Rural Areas (6.9% gap):**
- Lower gap but lower absolute employment
- Focus on:
  - Overall economic development
  - Agricultural productivity
  - Market access
  - Value chain participation
  - Rural infrastructure

### Targeted Interventions
1. **Geographic Hotspots**: Prioritize Eastern Province resources
2. **Urban Programs**: Address formal sector gender barriers
3. **Rural Development**: Boost overall employment while maintaining equity
4. **Cross-Learning**: Share strategies between regions

## Future Enhancements

Potential improvements:
- Add interactive map visualization using Rwanda GeoJSON
- District-level drill-down (currently at province level)
- Year-over-year trend analysis by region
- Sector breakdown by province
- Correlation with education levels by region
- Migration patterns analysis
- Province-specific policy recommendations
- Export regional reports
- Comparative dashboard (province vs national average)
- Heat map for quick visual assessment

## Data Notes

### Geographic Coverage
- All 5 provinces covered
- Representative sampling
- Weighted for population accuracy

### Limitations
- Province-level aggregation (not district)
- Annual snapshots (not continuous)
- Employment definition includes informal work
- Does not capture quality of employment

### Strengths
- Comprehensive geographic coverage
- Consistent methodology
- Large sample sizes
- Official national statistics
