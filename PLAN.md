# Company Data API - Project Plan

## Project Overview
Build a complete API solution for company financial data that can be used as a developer skills assessment challenge.

## Data Structure Summary

**Source**: 1,442 CSV files across 7 directories for 222 companies
- **balance_sheet/** - Financial position (assets, liabilities, equity) - 2015-2024
- **cash_flow_statement/** - Cash flows by activity type - 2015-2024
- **income_statement/** - Revenue, expenses, profitability - 2015-2024
- **company_info/** - Registration details, address, contact
- **industries/** - SIC codes and classifications (multiple per company)
- **operations/** - Business description text
- **people/** - Executives/directors with titles and responsibilities

**Key**: All data linked by DUNS number (D&B company identifier)

---

## Implementation Phases

### Phase 1: Database Schema Design & Data Import
- [ ] Design SQLite schema with proper normalization
- [ ] Create data import scripts to parse all CSV files
- [ ] Handle data cleaning (currency formatting, percentages, null values)
- [ ] Validate imported data integrity

**Database Tables**:
1. `companies` - Core company info (DUNS as PK)
2. `balance_sheet` - Financial position data
3. `cash_flow_statement` - Cash flow data
4. `income_statement` - P&L data
5. `industries` - Industry classifications (many-to-one)
6. `operations` - Business descriptions
7. `people` - Personnel (many-to-one)

### Phase 2: API Development
- [ ] Set up FastAPI project structure
- [ ] Create database connection layer
- [ ] Implement CRUD endpoints for each entity
- [ ] Add filtering, pagination, and search
- [ ] Implement proper error handling

**API Endpoints** (RESTful design):
```
GET  /companies                    - List all companies
GET  /companies/{duns}             - Get company details
GET  /companies/{duns}/balance-sheet       - Financial position
GET  /companies/{duns}/cash-flow           - Cash flow statements
GET  /companies/{duns}/income-statement    - P&L data
GET  /companies/{duns}/industries          - Industry classifications
GET  /companies/{duns}/operations          - Business description
GET  /companies/{duns}/people              - Personnel

# Aggregate/Filter endpoints
GET  /companies?industry={code}    - Filter by industry
GET  /companies?year={year}        - Filter financials by year
GET  /balance-sheet?year={year}    - All balance sheets for year
GET  /income-statement?year={year} - All income statements for year
GET  /people?title={title}         - Search by title
```

### Phase 3: Documentation
- [ ] Auto-generate OpenAPI/Swagger docs
- [ ] Add endpoint descriptions and examples
- [ ] Create README with setup instructions
- [ ] Document data dictionary

### Phase 4: Deployment
- [ ] Package application for deployment
- [ ] Deploy to hosting platform
- [ ] Test all endpoints in production
- [ ] Generate shareable API documentation URL

---

## Recommended Hosting Options

### For This Simple Use Case (SQLite + Python API):

| Platform | Pros | Cons | Cost |
|----------|------|------|------|
| **Railway.app** | Simple deployment, free tier, auto-scales | Limited free hours | Free tier available |
| **Render.com** | Free tier, auto-deploys from Git, easy | Spins down on inactivity | Free tier available |
| **Fly.io** | Persistent volumes for SQLite, global | Slightly more complex setup | Free tier (3 VMs) |
| **PythonAnywhere** | Python-focused, simple | Limited customization | Free tier available |
| **Vercel** | Great for APIs, serverless | SQLite not ideal (stateless) | Free tier |

### Recommendation: **Render.com** or **Railway.app**
- Both support Python/FastAPI natively
- Free tiers suitable for assessment
- Auto-deploy from GitHub
- Built-in HTTPS
- Easy environment variables
- Good for SQLite with persistent storage (Railway better for this)

**Alternative for Production**: If scaling needed, migrate to PostgreSQL on Supabase (free tier) or Neon.

---

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI (async, auto-docs, modern)
- **Database**: SQLite (local) - can migrate to PostgreSQL for production
- **ORM**: SQLAlchemy (flexibility) or raw SQL
- **Documentation**: OpenAPI/Swagger (built into FastAPI)
- **Deployment**: Railway.app or Render.com

---

## File Structure
```
APItest/
├── CompanyData/          # Source data (provided)
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── database.py       # DB connection & session
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # Database operations
│   └── routers/
│       ├── companies.py
│       ├── financials.py
│       └── people.py
├── scripts/
│   └── import_data.py    # Data import script
├── company_data.db       # SQLite database
├── requirements.txt
├── README.md
└── PLAN.md
```

---

## Success Criteria
1. All 222 companies imported with complete data
2. All endpoints functional and documented
3. API accessible via public URL
4. Swagger/OpenAPI docs available at /docs
5. Response times < 500ms for typical queries
