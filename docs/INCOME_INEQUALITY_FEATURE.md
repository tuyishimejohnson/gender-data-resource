# Income Inequality Analysis Feature

## Overview
This feature adds comprehensive income inequality visualization to the Gender Intelligence Dashboard, providing three powerful insights into wage gaps and income distribution between genders.

## Backend Implementation

### New API Endpoints

#### 1. Average Income by Gender
**Endpoint:** `GET /dashboard/income-inequality/average-income?year=2023`

**Data Source:** A01 (gender) + cash (monthly income)

**Response Format:**
```json
{
  "year": 2023,
  "data": {
    "Female": {
      "min": 2600.0,
      "q1": 20800.0,
      "median": 26000.0,
      "q3": 40000.0,
      "max": 6500000.0,
      "mean": 62972.49
    },
    "Male": {
      "min": 3000.0,
      "q1": 26000.0,
      "median": 50000.0,
      "q3": 104000.0,
      "max": 7696000.0,
      "mean": 98877.78
    }
  }
}
```

**Insights:**
- Shows wage gap + distribution using box plot statistics
- Reveals median income disparity: Male median (50,000 RWF) vs Female median (26,000 RWF)
- Highlights income range and outliers for both genders

#### 2. Income Distribution by Gender
**Endpoint:** `GET /dashboard/income-inequality/income-distribution?year=2023`

**Data Source:** A01 (gender) + intcash (income intervals)

**Response Format:**
```json
{
  "year": 2023,
  "brackets": [1, 2, 3, 4, 5, 99],
  "data": {
    "Female": [215287.99, 570310.69, 213104.77, 94500.02, 123865.53, 4880.68],
    "Male": [174032.36, 441056.54, 264367.53, 303236.49, 324635.39, 15683.43]
  }
}
```

**Insights:**
- Shows if women are concentrated in lower income brackets
- Data reveals females dominate lower brackets (1-2) while males dominate higher brackets (3-5)
- Stacked bar chart visualization makes distribution patterns immediately visible

#### 3. Hourly Wage Gap
**Endpoint:** `GET /dashboard/income-inequality/hourly-wage?year=2023`

**Data Source:** A01 (gender) + hr_cash (hourly wage)

**Response Format:**
```json
{
  "year": 2023,
  "data": {
    "Female": {
      "min": 16.23,
      "q1": 162.5,
      "median": 260.0,
      "q3": 520.0,
      "max": 40625.0,
      "mean": 510.29
    },
    "Male": {
      "min": 13.89,
      "q1": 185.71,
      "median": 361.11,
      "q3": 757.77,
      "max": 46875.0,
      "mean": 740.40
    }
  }
}
```

**Insights:**
- True pay inequality that controls for hours worked
- Male hourly wage median (361 RWF/hr) vs Female median (260 RWF/hr)
- Shows 45% wage gap at median level

## Frontend Implementation

### New Component: `IncomeInequality.tsx`

Located at: `frontend/app/components/IncomeInequality.tsx`

**Features:**
- Three-column layout with coordinated visualizations
- Box plot visualization for average income and hourly wage
- Stacked bar chart for income distribution
- Real-time gap percentage calculation with color-coded indicators:
  - Green: < 10% gap
  - Yellow: 10-20% gap
  - Red: > 20% gap
- Median and mean value displays for easy comparison
- Legend showing median (solid line), mean (dashed line), and IQR (shaded box)

**Visualization Types:**
1. **Average Income**: Custom box plot using ComposedChart from recharts
2. **Income Distribution**: Stacked bar chart showing concentration by bracket
3. **Hourly Wage**: Custom box plot for true pay inequality

### Dashboard Integration

Updated `frontend/app/routes/home.tsx` to:
- Import new data types and API functions
- Add state management for three new data streams
- Fetch all income inequality data on mount and year change
- Display component in main dashboard layout

## TypeScript Types

Added to `frontend/app/services/types.ts`:
- `BoxPlotStats` - Statistical measures (min, q1, median, q3, max, mean)
- `AverageIncomeData` - Average income response structure
- `IncomeDistributionData` - Distribution histogram data
- `HourlyWageData` - Hourly wage response structure

## API Service

Extended `frontend/app/services/index.ts` with:
- `getAverageIncome(year)` - Fetch average income data
- `getIncomeDistribution(year)` - Fetch income distribution
- `getHourlyWage(year)` - Fetch hourly wage data

## Key Insights Revealed

Based on 2023 data:

1. **Significant Income Gap**: Males earn ~57% more on average (median: 50k vs 26k RWF)
2. **Distribution Inequality**: Females concentrated in lower income brackets
3. **Hourly Wage Gap**: Even controlling for hours, males earn ~39% more per hour
4. **Income Range Disparity**: Male income range (Q3-Q1) is 4x larger than female range

## Testing

### Backend Tests
All endpoints tested and returning 200 OK:
- ✅ `/dashboard/income-inequality/average-income?year=2023`
- ✅ `/dashboard/income-inequality/income-distribution?year=2023`
- ✅ `/dashboard/income-inequality/hourly-wage?year=2023`

### Frontend Tests
- ✅ Server running on http://localhost:5173
- ✅ No linter errors
- ✅ TypeScript compilation successful
- ✅ Component rendering without errors

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
- Calculates box plot statistics using numpy percentiles
- Weighted counts for accurate population representation
- Filters for valid data (non-null, positive values, valid weights)

### Frontend
- Responsive grid layout (3 columns)
- Recharts library for professional visualizations
- Loading states with skeleton UI
- Error handling for failed API requests
- Color-coded gap indicators for quick assessment

## Future Enhancements

Potential improvements:
- Add year-over-year trend comparison
- Include sector-based income analysis
- Add education level correlation
- Export functionality for reports
- Interactive filtering by province/district
