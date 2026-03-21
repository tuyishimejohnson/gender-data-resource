# Sector & Job Type Segregation Feature

## Overview
This feature adds comprehensive sector and job type segregation analysis to the Gender Intelligence Dashboard, revealing patterns of occupational clustering and employment type distribution by gender.

## Backend Implementation

### New API Endpoints

#### 1. Employment by Sector
**Endpoint:** `GET /dashboard/sector-segregation/employment-by-sector?year=2023`

**Data Source:** A01 (gender) + main_sect (economic sector)

**Response Format:**
```json
{
  "year": 2023,
  "data": [
    {
      "sector": "Agriculture",
      "Female": 944802.83,
      "Male": 785546.73,
      "female_percentage": 54.6,
      "male_percentage": 45.4
    },
    {
      "sector": "Industry",
      "Female": 151423.35,
      "Male": 514290.24,
      "female_percentage": 22.7,
      "male_percentage": 77.3
    },
    {
      "sector": "Services",
      "Female": 700047.72,
      "Male": 889053.54,
      "female_percentage": 44.1,
      "male_percentage": 55.9
    }
  ]
}
```

**Insights:**
- Women concentrated in Agriculture (54.6% female representation)
- Industry heavily male-dominated (77.3% male)
- Services sector more balanced but still male-leaning (55.9% male)
- Reveals sectoral segregation patterns

#### 2. Formal vs Informal Employment
**Endpoint:** `GET /dashboard/sector-segregation/formal-informal?year=2023`

**Data Source:** A01 (gender) + IEV2 (formal/informal employment status)

**Response Format:**
```json
{
  "year": 2023,
  "data": [
    {
      "category": "Formal",
      "Female": 139374.74,
      "Male": 221428.06,
      "female_percentage": 7.8,
      "male_percentage": 10.2
    },
    {
      "category": "Informal",
      "Female": 1633876.33,
      "Male": 1942016.20,
      "female_percentage": 91.7,
      "male_percentage": 89.2
    },
    {
      "category": "Other",
      "Female": 8856.61,
      "Male": 13264.57,
      "female_percentage": 0.5,
      "male_percentage": 0.6
    }
  ]
}
```

**Insights:**
- Both genders highly concentrated in informal sector
- Women slightly more in informal (91.7% vs 89.2%)
- Formal sector access limited for both, worse for women (7.8% vs 10.2%)
- Shows vulnerability to economic shocks

#### 3. Occupation Segregation
**Endpoint:** `GET /dashboard/sector-segregation/occupation-segregation?year=2023`

**Data Source:** A01 (gender) + isco2digit (ISCO-08 2-digit occupation codes)

**Response Format:**
```json
{
  "year": 2023,
  "data": [
    {
      "code": 92,
      "occupation": "Agricultural Laborers",
      "Female": 841996.53,
      "Male": 651305.89,
      "female_percentage": 56.4,
      "male_percentage": 43.6,
      "total": 1493302.42
    },
    {
      "code": 52,
      "occupation": "Sales Workers",
      "Female": 300484.47,
      "Male": 175567.25,
      "female_percentage": 63.1,
      "male_percentage": 36.9,
      "total": 476051.72
    },
    // ... more occupations
  ]
}
```

**Insights:**
- Strong gender-based job clustering
- Women dominate: Agricultural Laborers (56.4%), Sales Workers (63.1%), Cleaners (66.6%)
- Men dominate: Construction Laborers (87.4%), Drivers (majority), Technical trades
- Top 10 occupations shown, sorted by total employment

## Frontend Implementation

### New Component: `SectorSegregation.tsx`

Located at: `frontend/app/components/SectorSegregation.tsx`

**Features:**
- Three-column layout with coordinated visualizations
- Stacked bar chart for employment by sector
- Dual pie charts for formal/informal comparison
- Horizontal grouped bar chart for occupation segregation
- Dynamic insights showing female-dominated and male-dominated occupations
- Color-coded indicators for quick assessment

**Visualization Types:**
1. **Employment by Sector**: Stacked bar chart showing gender distribution across Agriculture, Industry, and Services
2. **Formal vs Informal**: Side-by-side pie charts comparing employment type distribution for each gender
3. **Occupation Segregation**: Horizontal grouped bar chart showing top 10 occupations by ISCO codes

### Dashboard Integration

Updated `frontend/app/routes/home.tsx` to:
- Import new data types and API functions
- Add state management for three new data streams
- Fetch all sector segregation data on mount and year change
- Display component in main dashboard layout (positioned after Income Inequality)

## TypeScript Types

Added to `frontend/app/services/types.ts`:
- `SectorEmploymentPoint` - Sector employment by gender with percentages
- `SectorEmploymentData` - Sector employment response structure
- `FormalInformalPoint` - Employment type by gender with percentages
- `FormalInformalData` - Formal/informal response structure
- `OccupationPoint` - Occupation data with ISCO codes and percentages
- `OccupationSegregationData` - Occupation segregation response structure

## API Service

Extended `frontend/app/services/index.ts` with:
- `getSectorEmployment(year)` - Fetch employment by sector data
- `getFormalInformal(year)` - Fetch formal/informal employment data
- `getOccupationSegregation(year)` - Fetch occupation segregation data

## Key Insights Revealed

Based on 2023 Rwanda LFS data:

### Sectoral Segregation
1. **Agriculture Female-Dominated**: 54.6% of agricultural workers are women
2. **Industry Male-Dominated**: 77.3% of industrial workers are men (huge gap)
3. **Services Balanced**: 55.9% male, 44.1% female (most equitable sector)

### Formal vs Informal
1. **High Informality Overall**: 90%+ of both genders in informal sector
2. **Women More Vulnerable**: 91.7% informal vs 89.2% for men
3. **Formal Sector Gap**: Only 7.8% women in formal vs 10.2% men
4. **Limited Social Protection**: Informal workers lack benefits, job security

### Occupational Clustering
**Female-Dominated Occupations:**
- Agricultural Laborers (56.4% F)
- Sales Workers (63.1% F)
- Cleaners & Helpers (66.6% F)
- Personal Service Workers (45.2% F)

**Male-Dominated Occupations:**
- Laborers in Mining & Construction (87.4% M)
- Drivers & Mobile Operators (majority M)
- Metal & Machinery Workers (majority M)
- Building Trades Workers (majority M)

**Key Patterns:**
- Women concentrated in lower-wage, informal occupations
- Men dominate technical, construction, and transport sectors
- Strong horizontal segregation (different jobs)
- Limited crossover between gender-typical occupations

## Testing

### Backend Tests
All endpoints tested and returning 200 OK:
- ✅ `/dashboard/sector-segregation/employment-by-sector?year=2023`
- ✅ `/dashboard/sector-segregation/formal-informal?year=2023`
- ✅ `/dashboard/sector-segregation/occupation-segregation?year=2023`

### Frontend Tests
- ✅ Server running on http://localhost:5173
- ✅ Hot module reloading working
- ✅ TypeScript compilation successful
- ✅ Component rendering without errors
- ✅ All API calls succeeding

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
- Weighted counts for accurate population representation
- ISCO-08 classification for occupation codes (standardized international)
- Sector codes: 1=Agriculture, 2=Industry, 3=Services
- IEV2 codes: 1=Formal, 2=Informal, 3=Other
- Filters for valid data (non-null, positive weights)

### Frontend
- Responsive grid layout (3 columns)
- Recharts library for professional visualizations
- Side-by-side pie charts for easy comparison
- Horizontal bar chart for space-efficient occupation display
- Dynamic insights extracting male/female-dominated occupations
- Loading states with skeleton UI
- Color coding: Female (pink-500), Male (blue-500), Formal (green), Informal (amber)

### Data Mappings

**ISCO-08 Major Groups (implemented):**
- 11-14: Managers
- 21-26: Professionals
- 31-35: Technicians and Associate Professionals
- 41-44: Clerical Support Workers
- 51-54: Service and Sales Workers
- 61-62: Skilled Agricultural Workers
- 71-75: Craft and Related Trades Workers
- 81-83: Plant and Machine Operators
- 91-96: Elementary Occupations

## Policy Implications

### Sectoral Segregation
- Need targeted training programs for women in Industry
- Support for women entrepreneurs in Services sector
- Agricultural mechanization considerations for female workers

### Formal vs Informal
- Social protection expansion crucial (affects 90%+ workers)
- Formalization incentives needed
- Women's access to formal sector requires intervention
- Childcare support could help women access formal employment

### Occupational Segregation
- STEM education for girls to access technical occupations
- Challenge gender stereotypes in career guidance
- Apprenticeship programs in male-dominated trades
- Fair pay in female-dominated occupations
- Breaking occupational barriers through policy

## Future Enhancements

Potential improvements:
- Add year-over-year trend analysis
- Include provincial/district breakdowns
- Add education level correlation with occupation
- Sector-specific wage analysis
- Occupational mobility tracking
- Interactive drill-down by occupation category
- Export functionality for detailed reports
- Add occupation recommendations based on skills
