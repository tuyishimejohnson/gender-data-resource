# ParityMetrics - System Architecture

## Overview

ParityMetrics is built on a modern microservices architecture with a React frontend, FastAPI backend, and multiple data sources. The system uses AI-powered analysis to provide deep insights into gender inequality patterns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            USER LAYER                                    │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                      Web Browser                                │    │
│  │  • Chrome/Firefox/Safari/Edge (Modern browsers)                │    │
│  │  • Responsive design (Desktop/Tablet/Mobile)                   │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  │ HTTP/HTTPS
                                  │ REST API + Server-Sent Events (SSE)
                                  ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                                  │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                   React Frontend (Port 5173)                    │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │    │
│  │  │  Dashboard   │  │ Visualization │  │   AI Chat           │ │    │
│  │  │  Components  │  │   Components  │  │   Component         │ │    │
│  │  │              │  │               │  │                     │ │    │
│  │  │ • KPI Cards  │  │ • Charts      │  │ • Message UI        │ │    │
│  │  │ • Filters    │  │ • Maps        │  │ • Streaming         │ │    │
│  │  │ • Tables     │  │ • Heatmaps    │  │ • Suggestions       │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘ │    │
│  │                                                                  │    │
│  │  Technologies:                                                   │    │
│  │  • React Router v7 (SSR)                                        │    │
│  │  • TypeScript                                                   │    │
│  │  • Recharts (visualizations)                                    │    │
│  │  • Tailwind CSS                                                 │    │
│  │  • Axios (HTTP client)                                          │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  │ REST API Calls
                                  │ • /dashboard/* endpoints
                                  │ • /chat endpoints (SSE)
                                  │ • /health
                                  ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                                  │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                  FastAPI Backend (Port 8000)                    │    │
│  │  ┌──────────────────────────────────────────────────────────┐  │    │
│  │  │                    API Routes                              │  │    │
│  │  │  ┌────────────────────┐  ┌──────────────────────────┐    │  │    │
│  │  │  │  Dashboard Router  │  │    Chat Router           │    │  │    │
│  │  │  │                    │  │                          │    │  │    │
│  │  │  │ • /kpis           │  │ • POST /chat             │    │  │    │
│  │  │  │ • /trend          │  │ • POST /chat/stream      │    │  │    │
│  │  │  │ • /core-metrics   │  │ • DELETE /chat/{id}      │    │  │    │
│  │  │  │ • /income-*       │  │                          │    │  │    │
│  │  │  │ • /sector-*       │  │                          │    │  │    │
│  │  │  │ • /geography-*    │  │                          │    │  │    │
│  │  │  └────────────────────┘  └──────────────────────────┘    │  │    │
│  │  └──────────────┬───────────────────┬───────────────────────┘  │    │
│  │                 │                   │                           │    │
│  │                 ↓                   ↓                           │    │
│  │  ┌──────────────────────┐  ┌──────────────────────────────┐   │    │
│  │  │  DuckDB Query Layer  │  │    AI Agent Layer            │   │    │
│  │  │                      │  │    (OpenAI GPT-4)            │   │    │
│  │  │ • SQL generation     │  │                              │   │    │
│  │  │ • Aggregations       │  │  Tool Orchestration:         │   │    │
│  │  │ • Weighted stats     │  │  ┌─────────────────────┐    │   │    │
│  │  │                      │  │  │ search_gender_      │    │   │    │
│  │  └──────────┬───────────┘  │  │ reports()           │    │   │    │
│  │             │              │  │                     │    │   │    │
│  │             │              │  │ query_lfs_data()    │    │   │    │
│  │             │              │  │                     │    │   │    │
│  │             │              │  │ web_search()        │    │   │    │
│  │             │              │  └─────────────────────┘    │   │    │
│  │             │              └──────────────┬───────────────┘   │    │
│  │             │                             │                   │    │
│  └─────────────┼─────────────────────────────┼───────────────────┘    │
└─────────────────┼─────────────────────────────┼─────────────────────────┘
                  │                             │
                  ↓                             ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │  DuckDB In-Mem   │  │  Pinecone Cloud  │  │  External APIs   │     │
│  │                  │  │                  │  │                  │     │
│  │ Parquet Files:   │  │  Vector Store:   │  │  Web Sources:    │     │
│  │ • lfs2022        │  │  • Gender reports│  │  • Tavily API    │     │
│  │ • lfs2023        │  │  • Policy docs   │  │  • News/Stats    │     │
│  │ • lfs2024        │  │  • Text chunks   │  │                  │     │
│  │                  │  │  • Embeddings    │  │                  │     │
│  │ ~72k rows/year   │  │  1536-dim vecs   │  │  Rate limited    │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### 1. Dashboard Data Request Flow

```
User Action (Select Year)
        │
        ↓
┌───────────────────────────────────────┐
│  React Component State Update         │
│  setSelectedYear(2023)                │
└───────────────┬───────────────────────┘
                │
                ↓
┌───────────────────────────────────────┐
│  useEffect Hook Triggered             │
│  Fetches all dashboard data           │
└───────────────┬───────────────────────┘
                │
                ↓
┌───────────────────────────────────────┐
│  Promise.all() - Parallel Requests    │
│  ┌─────────────────────────────────┐  │
│  │ 14 concurrent API calls:        │  │
│  │ • getKPIs(2023)                 │  │
│  │ • getTrend()                    │  │
│  │ • getTimeseries()               │  │
│  │ • getRegional(2023)             │  │
│  │ • getIndicators(2023)           │  │
│  │ • getCoreMetrics()              │  │
│  │ • getAverageIncome(2023)        │  │
│  │ • getIncomeDistribution(2023)   │  │
│  │ • getHourlyWage(2023)           │  │
│  │ • getSectorEmployment(2023)     │  │
│  │ • getFormalInformal(2023)       │  │
│  │ • getOccupationSegregation(2023)│  │
│  │ • getProvinceEmployment(2023)   │  │
│  │ • getUrbanRuralGap(2023)        │  │
│  └─────────────────────────────────┘  │
└───────────────┬───────────────────────┘
                │
                ↓ (HTTP GET requests)
┌───────────────────────────────────────┐
│  FastAPI Backend Receives Requests    │
│  Router dispatches to handlers        │
└───────────────┬───────────────────────┘
                │
                ↓
┌───────────────────────────────────────┐
│  DuckDB Query Execution               │
│  ┌─────────────────────────────────┐  │
│  │ 1. Connect to DuckDB            │  │
│  │ 2. Create views from parquets   │  │
│  │ 3. Execute SQL query            │  │
│  │    SELECT A01, status1, ...     │  │
│  │    FROM lfs2023                 │  │
│  │    WHERE weight2 > 0            │  │
│  │    GROUP BY A01                 │  │
│  │ 4. Aggregate with weights       │  │
│  │ 5. Calculate percentages        │  │
│  │ 6. Format JSON response         │  │
│  └─────────────────────────────────┘  │
└───────────────┬───────────────────────┘
                │
                ↓ (JSON response)
┌───────────────────────────────────────┐
│  React State Updated                  │
│  setKpiData(kpis)                     │
│  setTrendData(trend)                  │
│  ... (all 14 states updated)          │
└───────────────┬───────────────────────┘
                │
                ↓
┌───────────────────────────────────────┐
│  Components Re-render                 │
│  • Charts update                      │
│  • Tables refresh                     │
│  • Loading states removed             │
└───────────────────────────────────────┘
```

### 2. AI Chat Query Flow

```
User Types Message: "What's the wage gap in Rwanda?"
        │
        ↓
┌─────────────────────────────────────────────────────┐
│  Frontend: Message State Updated                    │
│  messages.push({role: "user", content: query})     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓ (POST /chat/stream)
┌─────────────────────────────────────────────────────┐
│  Backend: FastAPI Receives Request                  │
│  • Extracts message                                 │
│  • Retrieves session history                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│  AI Agent: Build Context                            │
│  ┌───────────────────────────────────────────────┐  │
│  │ System Prompt:                                │  │
│  │ "You are ParityMetrics AI analyst..."        │  │
│  │                                               │  │
│  │ Conversation History:                         │  │
│  │ [previous messages...]                        │  │
│  │                                               │  │
│  │ Current Query:                                │  │
│  │ "What's the wage gap in Rwanda?"             │  │
│  │                                               │  │
│  │ Available Tools:                              │  │
│  │ • search_gender_reports                       │  │
│  │ • query_lfs_data                             │  │
│  │ • web_search                                  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓ (OpenAI API call)
┌─────────────────────────────────────────────────────┐
│  OpenAI GPT-4: Analysis & Tool Selection            │
│  ┌───────────────────────────────────────────────┐  │
│  │ LLM decides:                                  │  │
│  │ "Need statistical data about wage gap"       │  │
│  │                                               │  │
│  │ Tool Call Request:                            │  │
│  │ {                                             │  │
│  │   "name": "query_lfs_data",                  │  │
│  │   "arguments": {                              │  │
│  │     "query": "SELECT A01, AVG(hr_cash)..."  │  │
│  │   }                                           │  │
│  │ }                                             │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│  Tool Execution: query_lfs_data()                   │
│  ┌───────────────────────────────────────────────┐  │
│  │ 1. Parse SQL query from LLM                  │  │
│  │ 2. Connect to DuckDB                         │  │
│  │ 3. Execute query on lfs2023                  │  │
│  │ 4. Get results:                              │  │
│  │    Gender | Avg Hourly Wage                  │  │
│  │    Female | 510.29 RWF                       │  │
│  │    Male   | 740.40 RWF                       │  │
│  │ 5. Format as JSON                            │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓ (Tool result back to LLM)
┌─────────────────────────────────────────────────────┐
│  OpenAI GPT-4: Synthesize Response                  │
│  ┌───────────────────────────────────────────────┐  │
│  │ Analyzes tool results                         │  │
│  │ Calculates: (740-510)/740 = 31% gap         │  │
│  │                                               │  │
│  │ Generates response:                           │  │
│  │ "Based on the latest data, there's a        │  │
│  │  31% wage gap in Rwanda. Women earn          │  │
│  │  510 RWF/hr while men earn 740 RWF/hr..."   │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓ (Streaming response)
┌─────────────────────────────────────────────────────┐
│  Backend: Stream Response to Frontend               │
│  • Server-Sent Events (SSE)                         │
│  • Chunks sent as generated                         │
│  • data: {"t": "Based"}                            │
│  • data: {"t": " on"}                              │
│  • data: {"t": " the"}                             │
│  • ... (word by word)                               │
│  • data: [DONE]                                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│  Frontend: Display Streaming Response               │
│  • Receives chunks via EventSource                  │
│  • Appends to message buffer                        │
│  • Updates UI in real-time                          │
│  • Shows typing indicator during stream             │
│  • Renders markdown when complete                   │
└─────────────────────────────────────────────────────┘
                  │
                  ↓
        User sees answer
```

### 3. Tool Selection Decision Tree

```
                    User Query
                        │
                        ↓
            ┌───────────────────────┐
            │  LLM Analyzes Intent  │
            └───────────┬───────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ↓              ↓              ↓
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │Statistical│ │ Policy/  │   │ Current │
    │   Data?   │ │Context?  │   │  News?  │
    └─────┬─────┘ └────┬─────┘   └────┬────┘
          │            │              │
          ↓            ↓              ↓
    ┌─────────────┐ ┌──────────────┐ ┌──────────┐
    │query_lfs_   │ │search_gender_│ │web_      │
    │data()       │ │reports()     │ │search()  │
    └─────┬───────┘ └──────┬───────┘ └────┬─────┘
          │                │               │
          │                │               │
          └────────────────┴───────────────┘
                        │
                        ↓
              ┌──────────────────┐
              │  Synthesize All  │
              │     Results      │
              └────────┬─────────┘
                       │
                       ↓
                 Final Answer

Examples:

Query: "What's the employment rate?"
→ query_lfs_data() → Direct stat

Query: "Why do women earn less?"
→ search_gender_reports() → Policy context
→ query_lfs_data() → Supporting numbers

Query: "Latest gender equality news?"
→ web_search() → Recent articles
```

## Component Architecture

### Frontend Component Hierarchy

```
App (home.tsx)
│
├── Header
│   ├── Logo
│   ├── Navigation
│   └── User Menu
│
├── DashboardFilters
│   └── Year Selector
│
├── Main Dashboard
│   │
│   ├── StatsCards (KPIs)
│   │   ├── Avg Gender Gap
│   │   ├── Female Avg
│   │   ├── Male Avg
│   │   └── Regions Tracked
│   │
│   ├── CoreMetrics
│   │   ├── Employment Rate Chart
│   │   ├── Unemployment Rate Chart
│   │   └── LFPR Chart
│   │
│   ├── IncomeInequality
│   │   ├── Average Income Box Plot
│   │   ├── Income Distribution Histogram
│   │   └── Hourly Wage Box Plot
│   │
│   ├── SectorSegregation
│   │   ├── Employment by Sector Chart
│   │   ├── Formal/Informal Pie Charts
│   │   └── Occupation Segregation Chart
│   │
│   ├── GeographyInequality
│   │   ├── Employment by Province Chart
│   │   └── Urban vs Rural Chart
│   │
│   ├── GenderGapChart (Trend)
│   ├── MaleVsFemaleChart (Timeseries)
│   ├── RegionalDisparityChart
│   └── IndicatorsTable
│
└── Sidebar
    ├── AskIntelligence (AI Chat)
    └── AIInsights
```

### Backend Module Organization

```
api/
│
├── main.py (FastAPI app)
│   ├── CORS middleware
│   ├── Dashboard router
│   ├── Chat endpoints
│   └── Health check
│
├── routers/
│   └── dashboard.py
│       ├── /kpis
│       ├── /trend
│       ├── /income-inequality/*
│       ├── /sector-segregation/*
│       └── /geography/*
│
├── agent.py (AI orchestration)
│   ├── run_agent()
│   ├── stream_agent()
│   ├── Tool definitions
│   └── System prompt
│
├── tools/
│   ├── data.py (DuckDB queries)
│   ├── rag.py (Pinecone search)
│   └── search.py (Tavily web)
│
├── config.py (Environment vars)
│
└── db/
    └── parquets/
        ├── RW_LFS2022_reduced.parquet
        ├── RW_LFS2023_reduced.parquet
        ├── RW_LFS2024_reduced.parquet
        └── Variables_description_RW_LFS2023.csv
```

## Database Schema (DuckDB Views)

### LFS Tables Structure

```
lfs2023 View (72,849 rows)
│
├── Demographics
│   ├── A01: Gender (1=Male, 2=Female)
│   ├── A04: Age
│   ├── province: Province code (1-5)
│   ├── Code_UR: Urban/Rural (1=Urban, 2=Rural)
│   └── weight2: Annual population weight
│
├── Employment
│   ├── status1: Employment status
│   │   ├── 1 = Employed
│   │   ├── 2 = Unemployed
│   │   └── 3 = Not in labor force
│   ├── employed16: Employment flag
│   ├── main_sect: Economic sector
│   │   ├── 1 = Agriculture
│   │   ├── 2 = Industry
│   │   └── 3 = Services
│   └── IEV2: Formal/Informal
│       ├── 1 = Formal
│       ├── 2 = Informal
│       └── 3 = Other
│
├── Income
│   ├── cash: Monthly income (RWF)
│   ├── intcash: Income bracket (1-5, 99)
│   └── hr_cash: Hourly wage (RWF)
│
├── Occupation
│   ├── isco2digit: ISCO-08 2-digit code
│   └── indd01: ISCO high level
│
└── Labor Metrics (calculated)
    ├── LFPR: Labor Force Participation Rate
    ├── unemployment_rate: % unemployed
    └── employment_rate: % employed
```

### Query Patterns

**Employment Rate by Gender:**
```sql
SELECT
    A01 as gender,
    SUM(CASE WHEN status1 = 1 THEN weight2 ELSE 0 END)
        / NULLIF(SUM(weight2), 0) * 100 AS emp_rate
FROM lfs2023
WHERE weight2 > 0
GROUP BY A01
```

**Income Statistics:**
```sql
SELECT
    A01 as gender,
    AVG(cash) as avg_income,
    MEDIAN(cash) as median_income,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY cash) as q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY cash) as q3
FROM lfs2023
WHERE cash > 0 AND weight2 > 0
GROUP BY A01
```

## API Endpoint Reference

### Dashboard Endpoints

| Endpoint | Method | Query Params | Description |
|----------|--------|--------------|-------------|
| `/dashboard/kpis` | GET | `year=2023` | Basic KPI summary |
| `/dashboard/trend` | GET | None | Gender gap trend with forecast |
| `/dashboard/timeseries` | GET | None | Historical employment rates |
| `/dashboard/regional` | GET | `year=2023` | Gender gap by province |
| `/dashboard/indicators` | GET | `year=2023` | Indicators overview |
| `/dashboard/core-metrics` | GET | None | Employment/unemployment/LFPR |

### Income Inequality Endpoints

| Endpoint | Method | Query Params | Description |
|----------|--------|--------------|-------------|
| `/dashboard/income-inequality/average-income` | GET | `year=2023` | Box plot statistics |
| `/dashboard/income-inequality/income-distribution` | GET | `year=2023` | Histogram data |
| `/dashboard/income-inequality/hourly-wage` | GET | `year=2023` | Hourly wage stats |

### Sector Segregation Endpoints

| Endpoint | Method | Query Params | Description |
|----------|--------|--------------|-------------|
| `/dashboard/sector-segregation/employment-by-sector` | GET | `year=2023` | Sector breakdown |
| `/dashboard/sector-segregation/formal-informal` | GET | `year=2023` | Employment type |
| `/dashboard/sector-segregation/occupation-segregation` | GET | `year=2023` | ISCO codes |

### Geography Endpoints

| Endpoint | Method | Query Params | Description |
|----------|--------|--------------|-------------|
| `/dashboard/geography/employment-by-province` | GET | `year=2023` | Provincial data |
| `/dashboard/geography/urban-rural-gap` | GET | `year=2023` | Urban-rural comparison |

### AI Chat Endpoints

| Endpoint | Method | Body | Description |
|----------|--------|------|-------------|
| `/chat` | POST | `{message, session_id}` | Standard chat |
| `/chat/stream` | POST | `{message, session_id}` | Streaming SSE |
| `/chat/{session_id}` | DELETE | None | Clear history |

## Technology Stack Details

### Frontend Stack

- **React Router v7**: Server-side rendering, data loading
- **TypeScript**: Type safety across codebase
- **Recharts**: Data visualization library
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client with interceptors
- **Vite**: Fast build tool and dev server
- **Lucide React**: Icon library

### Backend Stack

- **FastAPI**: High-performance async Python framework
- **DuckDB**: In-memory analytical database
- **PyArrow**: Parquet file reading
- **Pandas**: Data manipulation
- **OpenAI SDK**: GPT-4 integration
- **Pinecone**: Vector database for RAG
- **Tavily**: Web search API
- **Uvicorn**: ASGI server

### Development Tools

- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **pytest**: Python testing
- **Docker**: Containerization (optional)

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│              Production Deployment                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │         Load Balancer / CDN                │    │
│  │         (CloudFlare / AWS)                 │    │
│  └───────────────┬────────────────────────────┘    │
│                  │                                  │
│         ┌────────┴────────┐                         │
│         ↓                 ↓                         │
│  ┌─────────────┐   ┌─────────────┐                │
│  │  Frontend   │   │  Backend    │                │
│  │  (Static)   │   │  (Docker)   │                │
│  │             │   │             │                │
│  │  Vercel/    │   │  AWS ECS/   │                │
│  │  Netlify    │   │  Railway    │                │
│  └─────────────┘   └─────┬───────┘                │
│                           │                         │
│                    ┌──────┴──────┐                 │
│                    ↓              ↓                 │
│            ┌──────────────┐ ┌──────────┐           │
│            │  Pinecone    │ │  OpenAI  │           │
│            │  (Cloud)     │ │  (API)   │           │
│            └──────────────┘ └──────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Performance Considerations

### Frontend Optimization

- **Code Splitting**: Route-based lazy loading
- **Memoization**: React.memo for expensive components
- **Virtualization**: For large lists/tables
- **Image Optimization**: Lazy loading, WebP format
- **Bundle Size**: Tree shaking, minimal dependencies

### Backend Optimization

- **Connection Pooling**: Reuse DuckDB connections
- **Caching**: LRU cache for frequent queries
- **Async Operations**: Non-blocking I/O
- **Query Optimization**: Indexed parquet files
- **Rate Limiting**: Prevent API abuse

### Database Performance

- **DuckDB Advantages**:
  - Columnar storage (parquet)
  - In-memory processing
  - Parallel query execution
  - No network overhead

- **Query Patterns**:
  - Filtered aggregations
  - Weighted statistics
  - Time-range queries

## Security Considerations

- **API Keys**: Environment variables only
- **CORS**: Restricted origins
- **Rate Limiting**: Per-session/IP limits
- **Input Validation**: Pydantic models
- **SQL Injection**: Parameterized queries
- **XSS Prevention**: React escaping
- **HTTPS**: Enforced in production

## Monitoring & Observability

### Metrics to Track

- API response times
- Error rates by endpoint
- OpenAI token usage
- User session duration
- Query complexity
- Cache hit rates

### Logging Strategy

- Structured JSON logging
- Request/response logging
- Error tracking (Sentry)
- Performance profiling
- User analytics (privacy-respecting)

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Team**: ParityMetrics
