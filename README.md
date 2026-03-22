# ParityMetrics

> AI-powered gender equality analytics platform for Rwanda

**Team Members:**
- Aristide Isingizwe
- Johnson Tuyishime
- Ken Ganza

## 📋 Project Overview

ParityMetrics is a comprehensive gender data intelligence platform that transforms Rwanda's Labour Force Survey (LFS) microdata into actionable insights. The platform helps policymakers, researchers, and advocates understand multi-dimensional patterns of gender inequality across income, sectors, occupations, and geography.

### Key Objectives

- **Data Accessibility**: Make complex gender statistics easy to understand and navigate
- **Multi-dimensional Analysis**: Reveal patterns across income, employment, sectors, and geography
- **Gap Analysis**: Identify and quantify gender disparities with precision
- **Policy Support**: Provide evidence-based insights for advocacy and decision-making
- **Real-time Intelligence**: AI-powered analytics for instant insights and trend analysis

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Dashboard   │  │ Visualizations│  │   AI Chat Interface │  │
│  │   Controls   │  │  (Recharts)   │  │  (Streaming SSE)    │  │
│  └──────┬───────┘  └──────┬────────┘  └──────────┬──────────┘  │
│         │                 │                       │              │
│         └─────────────────┴───────────────────────┘              │
│                            │                                     │
│                      REST API / SSE                              │
└────────────────────────────┼────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Dashboard Router                        │   │
│  │  • KPIs  • Trends  • Income  • Sectors  • Geography     │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                            │
│  ┌─────────────────┴────────────────────────────────────────┐   │
│  │                    AI Agent (OpenAI GPT-4)                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │   RAG      │  │  DuckDB    │  │   Web Search     │   │   │
│  │  │  Search    │  │  Query     │  │   (Tavily)       │   │   │
│  │  │ (Reports)  │  │ (LFS Data) │  │  (Live Data)     │   │   │
│  │  └─────┬──────┘  └─────┬──────┘  └────────┬─────────┘   │   │
│  │        │                │                   │             │   │
│  └────────┼────────────────┼───────────────────┼─────────────┘   │
│           │                │                   │                 │
└───────────┼────────────────┼───────────────────┼─────────────────┘
            ↓                ↓                   ↓
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Pinecone   │  │   Parquet    │  │   Internet   │
    │  (Vectors)   │  │   Files      │  │   Sources    │
    │   Reports    │  │  LFS 2022-24 │  │  News/Stats  │
    └──────────────┘  └──────────────┘  └──────────────┘
```

### Data Flow Architecture

```
User Query → AI Agent → Tool Selection → Data Processing → Response

┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                              │
│                                                                  │
│  1. Dashboard Filters (Year, Region, etc.)                      │
│  2. AI Chat Query                                               │
└──────────────────────┬───────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                   REQUEST ROUTING                                │
│                                                                  │
│  Dashboard Request? → Direct to DuckDB Query                    │
│  AI Chat Request?   → Agent Tool Calling                        │
└──────────────────────┬───────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                   TOOL EXECUTION                                 │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  search_gender_reports()                               │     │
│  │  • Query: User question                                │     │
│  │  • Vector search in Pinecone                          │     │
│  │  • Returns: Report excerpts with context             │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  query_lfs_data()                                      │     │
│  │  • Query: SQL string                                   │     │
│  │  • Execute on DuckDB (parquet files)                  │     │
│  │  • Returns: Structured data (JSON)                    │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  web_search()                                          │     │
│  │  • Query: Search terms                                 │     │
│  │  • Tavily API for current information                 │     │
│  │  • Returns: Recent news/stats                         │     │
│  └───────────────────────────────────────────────────────┘     │
└──────────────────────┬───────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│                   RESPONSE GENERATION                            │
│                                                                  │
│  • LLM synthesizes tool outputs                                 │
│  • Formats answer with context                                  │
│  • Streams response to frontend                                 │
└──────────────────────┬───────────────────────────────────────────┘
                       ↓
                   User sees result
```

### Component Interaction

```
┌────────────────────────────────────────────────────────────────┐
│                      FRONTEND COMPONENTS                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │  CoreMetrics │  │ IncomeInequal│  │ SectorSegregation │   │
│  │  Component   │  │   Component  │  │    Component      │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘   │
│         │                 │                    │               │
│         └─────────────────┴────────────────────┘               │
│                           │                                    │
│                    dashboardApi                                │
│                           │                                    │
└───────────────────────────┼────────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│                    API ENDPOINTS                               │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  /dashboard/kpis                → Basic KPIs                   │
│  /dashboard/core-metrics        → Employment/LFPR              │
│  /dashboard/income-inequality/* → Income analysis              │
│  /dashboard/sector-segregation/*→ Sector/occupation           │
│  /dashboard/geography/*         → Provincial/urban-rural       │
│  /chat                          → AI assistant                 │
│  /chat/stream                   → Streaming responses          │
│                                                                 │
└───────────────────────────┬───────────────────────────────────┘
                            ↓
┌───────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                  │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  DuckDB Views:                                                 │
│  • lfs2022 → RW_LFS2022_reduced.parquet                       │
│  • lfs2023 → RW_LFS2023_reduced.parquet                       │
│  • lfs2024 → RW_LFS2024_reduced.parquet                       │
│                                                                 │
│  Key Fields:                                                   │
│  • A01 (gender), province, Code_UR (urban/rural)              │
│  • status1 (employment), cash (income), hr_cash (hourly)      │
│  • main_sect (sector), IEV2 (formal/informal)                 │
│  • isco2digit (occupation codes)                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## 👥 User Personas

### 1. Policy Maker (Primary)
**Profile:** Government official or NGO leader working on gender equality initiatives

**Needs:**
- Quick access to gender gap statistics
- Evidence for policy proposals
- Regional comparison data
- Trend analysis over time

**Use Case:** "I need to present gender employment data for Eastern Province to support a new women's empowerment program proposal."

### 2. Researcher/Analyst (Secondary)
**Profile:** Academic or data analyst studying gender economics

**Needs:**
- Detailed statistical breakdowns
- Cross-tabulation capabilities
- Access to raw data patterns
- AI-powered insights

**Use Case:** "I want to understand the correlation between education levels and income gaps across different sectors."

### 3. Advocate (Secondary)
**Profile:** Gender equality advocate or journalist

**Needs:**
- Compelling visualizations
- Quick facts and figures
- Historical trends
- Shareable insights

**Use Case:** "I need statistics showing the informal employment rate for women to include in my advocacy campaign."

## 🔄 Key Workflows

### Workflow 1: Exploring Regional Disparities

```
1. User selects year (2023) from filter
   ↓
2. Views Geography Inequality section
   ↓
3. Identifies Eastern Province has 12% gap (highest)
   ↓
4. Asks AI: "Why does Eastern Province have the highest gap?"
   ↓
5. AI analyzes sector distribution, urbanization, education
   ↓
6. User gets actionable insights for targeted interventions
```

### Workflow 2: Income Gap Analysis

```
1. User navigates to Income Inequality section
   ↓
2. Views average income box plot (Male: 50k RWF, Female: 26k RWF)
   ↓
3. Checks hourly wage gap (39% after controlling for hours)
   ↓
4. Examines income distribution histogram
   ↓
5. Discovers women concentrated in lower brackets
   ↓
6. Downloads data for policy proposal
```

### Workflow 3: Sector Segregation Investigation

```
1. User explores Sector Segregation section
   ↓
2. Sees women dominate Agriculture (54.6%)
   ↓
3. Notes men dominate Industry (77.3%)
   ↓
4. Reviews informal employment split (91.7% F vs 89.2% M)
   ↓
5. Drills into occupation codes via visualization
   ↓
6. Identifies skill training opportunities
```

### Workflow 4: AI-Powered Insights

```
1. User asks: "What are the main drivers of gender inequality?"
   ↓
2. AI agent calls multiple tools:
   - Searches reports for policy context
   - Queries LFS data for statistics
   - Web search for recent developments
   ↓
3. AI synthesizes comprehensive answer with:
   - Key statistics
   - Regional variations
   - Historical trends
   - Policy recommendations
   ↓
4. User receives actionable intelligence
```

## 🚀 Setup Instructions

### Prerequisites

- **Python**: 3.11 or 3.12
- **Node.js**: 18+ (for frontend)
- **API Keys**:
  - OpenAI API key
  - Pinecone API key
  - Tavily API key (optional, for web search)

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/tuyishimejohnson/gender-data-resource.git
cd gender-data-resource
```

#### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r api/requirements.txt

# Create .env file
cp api/.env.example api/.env
# Edit api/.env and add your API keys:
# OPENAI_API_KEY=your_key_here
# PINECONE_KEY=your_key_here
# TAVILY_API_KEY=your_key_here (optional)

# Start backend server
python3 -m uvicorn api.main:app --reload
```

Backend will be available at: **http://localhost:8000**

#### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### Quick Start (One-Line Commands)

**Terminal 1 (Backend):**
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r api/requirements.txt && uvicorn api.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend && npm install && npm run dev
```

## 📊 Features Overview

### 1. Core Gender Gap Metrics
- Employment rate by gender
- Unemployment rate trends
- Labor Force Participation Rate (LFPR)
- Year-over-year comparisons

### 2. Income Inequality Analysis
- Average income comparison (box plots)
- Income distribution by brackets
- Hourly wage gap (controls for hours worked)
- Median vs mean analysis

### 3. Sector & Job Type Segregation
- Employment by economic sector (Agriculture, Industry, Services)
- Formal vs informal employment breakdown
- Occupation segregation (40+ ISCO categories)
- Top 10 occupations by gender

### 4. Geography-Based Inequality
- Provincial employment rates (5 provinces)
- Urban vs rural gender gaps
- Regional disparity rankings
- Interactive comparisons

### 5. AI-Powered Intelligence
- Natural language queries
- Multi-source analysis (reports + data + web)
- Streaming responses
- Context-aware insights

## 🗂️ Data Sources & Provenance

### Primary Data Source

**Rwanda Labour Force Survey (LFS)**
- **Source**: National Institute of Statistics Rwanda (NISR)
- **Years**: 2022, 2023, 2024
- **Format**: Parquet files (reduced from original microdata)
- **Size**: ~72,000 records per year
- **Access**: Restricted microdata, licensed for hackathon use
- **URL**: https://statistics.gov.rw/

**Key Variables Used:**
- Demographics: A01 (gender), A04 (age), province, Code_UR (urban/rural)
- Employment: status1, employed16, main_sect, IEV2
- Income: cash, intcash, hr_cash
- Occupation: isco2digit (ISCO-08 classification)

### Secondary Data Sources

**Policy Reports & Documents**
- **Source**: Various gender equality reports
- **Storage**: Pinecone vector database
- **Access Time**: Indexed during hackathon (March 2026)
- **Purpose**: Context for AI responses

**Web Sources**
- **Source**: Tavily web search API
- **Purpose**: Current news and recent statistics
- **Restriction**: Rate-limited API access

### Data Quality Notes

- All microdata is weighted (weight2 field) for population-level estimates
- Missing values handled appropriately per field
- Income fields may have outliers (top-coded in visualizations)
- Province codes: 1=Eastern, 2=Kigali, 3=Northern, 4=Southern, 5=Western

## ⚠️ Limitations

### Technical Limitations

1. **Data Freshness**: Most recent complete data is 2023 (2024 may be partial)
2. **Computational**: Large queries on full dataset can be slow
3. **API Costs**: OpenAI API usage incurs costs per query
4. **Rate Limits**: Tavily web search has API rate limits

### Data Limitations

1. **Self-Reported Data**: LFS is survey-based, subject to reporting bias
2. **Informal Sector**: Difficult to capture accurately
3. **Seasonal Variation**: Employment patterns vary by season
4. **Geographic Granularity**: Province-level only (no district breakdown)
5. **Missing Variables**: Some socioeconomic factors not captured

### Analytical Limitations

1. **Correlation vs Causation**: Visualizations show patterns, not causes
2. **Intersectionality**: Limited multi-dimensional analysis (e.g., age + gender + region)
3. **Temporal Coverage**: Only 3 years of data for trend analysis
4. **AI Accuracy**: LLM responses should be verified for critical decisions

## 🔮 Next Steps & Roadmap

### Short-term Enhancements (0-3 months)

1. **Interactive Maps**: Add geographic visualization with Rwanda GeoJSON
2. **District-level Data**: Expand from province to district granularity
3. **Export Functionality**: PDF reports, CSV downloads
4. **User Authentication**: Save queries and custom dashboards
5. **Mobile Responsiveness**: Optimize for tablet/mobile viewing

### Medium-term Features (3-6 months)

1. **Advanced Filters**: Multi-dimensional filtering (age + education + sector)
2. **Comparison Tool**: Side-by-side province/year comparisons
3. **Scenario Modeling**: "What-if" analysis for policy interventions
4. **API for Third Parties**: Public API for data access
5. **Scheduled Reports**: Automated email reports with updates

### Long-term Vision (6-12 months)

1. **Multi-Country Support**: Expand to other East African countries
2. **Real-time Data Integration**: Connect to live data feeds
3. **Predictive Analytics**: Machine learning models for forecasting
4. **Policy Impact Tracking**: Measure effectiveness of interventions
5. **Community Collaboration**: User-submitted analyses and insights

### Research Priorities

1. Investigate urban/rural paradox (urban gap larger than rural)
2. Analyze intersectionality (gender + age + education)
3. Study informal sector dynamics
4. Evaluate policy intervention effectiveness
5. Develop gender equality composite index

## 📄 License & Attribution

This project was developed for the **GIZ Gender Data Hackathon 2026**.

**Data Attribution:**
- Rwanda LFS microdata: National Institute of Statistics Rwanda (NISR)
- Reports: Various government and NGO sources (see vector database metadata)

**Technology Stack:**
- Frontend: React Router, TypeScript, Recharts, Tailwind CSS
- Backend: FastAPI, DuckDB, OpenAI GPT-4, Pinecone
- Deployment: Docker-ready (see Dockerfile)

## 🤝 Contributing

For questions or contributions during the hackathon period, contact the team members listed above.

## 📞 Support

- **GitHub Issues**: https://github.com/tuyishimejohnson/gender-data-resource/issues
- **Documentation**: See `/docs` folder for detailed feature docs
- **Architecture**: See `/docs/architecture.md` for technical details

---

**ParityMetrics** - Measuring progress toward gender equality through data-driven insights.

Built with ❤️ for gender equity in Rwanda.
