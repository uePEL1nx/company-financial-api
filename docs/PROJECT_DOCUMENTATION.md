# Company Financial Data API - Complete Project Documentation

## Project Overview

This project is a complete REST API solution for serving company financial data, built as both:
1. A functional API for accessing Australian company financial data
2. A reference implementation for a developer skills assessment

**Created**: December 2024
**Tech Stack**: Python, FastAPI, SQLite, SQLAlchemy, Pydantic

---

## Live Deployment

| Resource | URL |
|----------|-----|
| **API Base** | https://company-financial-api-production.up.railway.app |
| **Swagger Documentation** | https://company-financial-api-production.up.railway.app/docs |
| **ReDoc Documentation** | https://company-financial-api-production.up.railway.app/redoc |
| **OpenAPI JSON** | https://company-financial-api-production.up.railway.app/openapi.json |
| **GitHub Repository** | https://github.com/uePEL1nx/company-financial-api |
| **Railway Dashboard** | https://railway.com/project/33222dd0-30f6-4137-9c8e-4d41ce772a03 |

---

## Data Summary

### Source Data Structure

The raw data is stored in `CompanyData/` folder with 7 subdirectories:

```
CompanyData/
├── balance_sheet/          (222 CSV files)
├── cash_flow_statement/    (222 CSV files)
├── company_info/           (222 CSV files)
├── income_statement/       (222 CSV files)
├── industries/             (222 CSV files)
├── operations/             (218 CSV files)
└── people/                 (218 CSV files)
```

Each file is named by DUNS number (e.g., `740039581.csv`).

### Database Statistics

| Table | Records | Description |
|-------|---------|-------------|
| companies | 222 | Core company information |
| balance_sheets | 132,120 | Assets, liabilities, equity (2015-2024) |
| cash_flow_statements | 66,060 | Operating, investing, financing flows |
| income_statements | 103,494 | Revenue, expenses, profitability |
| industries | 717 | SIC industry classifications |
| operations | 24 | Business descriptions |
| people | 1,457 | Executives and directors |
| **Total** | **303,872** | |

### Data Time Coverage

- Financial statements: 2015-2024 (10 years)
- Company info, industries, people: Current snapshot

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│    companies    │
├─────────────────┤
│ duns (PK)       │──────┬──────┬──────┬──────┬──────┬──────┐
│ physical_address│      │      │      │      │      │      │
│ telephone_number│      │      │      │      │      │      │
│ acn             │      │      │      │      │      │      │
│ company_type    │      │      │      │      │      │      │
│ primary_sic     │      │      │      │      │      │      │
└─────────────────┘      │      │      │      │      │      │
                         │      │      │      │      │      │
    ┌────────────────────┘      │      │      │      │      │
    │                           │      │      │      │      │
    ▼                           ▼      │      │      │      │
┌─────────────────┐  ┌─────────────────┐│     │      │      │
│ balance_sheets  │  │cash_flow_statmts││     │      │      │
├─────────────────┤  ├─────────────────┤│     │      │      │
│ id (PK)         │  │ id (PK)         ││     │      │      │
│ duns (FK)       │  │ duns (FK)       ││     │      │      │
│ line_item       │  │ line_item       ││     │      │      │
│ year            │  │ year            ││     │      │      │
│ value           │  │ value           ││     │      │      │
│ numeric_value   │  │ numeric_value   ││     │      │      │
└─────────────────┘  └─────────────────┘│     │      │      │
                                        │     │      │      │
    ┌───────────────────────────────────┘     │      │      │
    │                                         │      │      │
    ▼                                         ▼      │      │
┌─────────────────┐               ┌─────────────────┐│     │
│income_statements│               │   industries    ││     │
├─────────────────┤               ├─────────────────┤│     │
│ id (PK)         │               │ id (PK)         ││     │
│ duns (FK)       │               │ duns (FK)       ││     │
│ line_item       │               │ industry_code   ││     │
│ year            │               │ industry_desc   ││     │
│ value           │               │ is_primary      ││     │
│ numeric_value   │               └─────────────────┘│     │
└─────────────────┘                                  │     │
                                                     │     │
    ┌────────────────────────────────────────────────┘     │
    │                                                      │
    ▼                                                      ▼
┌─────────────────┐                         ┌─────────────────┐
│   operations    │                         │     people      │
├─────────────────┤                         ├─────────────────┤
│ id (PK)         │                         │ id (PK)         │
│ duns (FK)       │                         │ duns (FK)       │
│ field_name      │                         │ person_name     │
│ field_value     │                         │ title           │
└─────────────────┘                         │ responsibilities│
                                            └─────────────────┘
```

### Table Definitions

#### companies
```sql
CREATE TABLE companies (
    duns VARCHAR(20) PRIMARY KEY,
    physical_address TEXT,
    telephone_number VARCHAR(50),
    acn VARCHAR(20),
    company_type VARCHAR(100),
    primary_sic VARCHAR(200)
);
```

#### balance_sheets
```sql
CREATE TABLE balance_sheets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    line_item VARCHAR(200),
    year INTEGER,
    value VARCHAR(100),        -- Original formatted value
    numeric_value FLOAT        -- Parsed numeric value
);
CREATE INDEX ix_balance_sheet_duns_year ON balance_sheets(duns, year);
```

#### cash_flow_statements
```sql
CREATE TABLE cash_flow_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    line_item VARCHAR(200),
    year INTEGER,
    value VARCHAR(100),
    numeric_value FLOAT
);
CREATE INDEX ix_cash_flow_duns_year ON cash_flow_statements(duns, year);
```

#### income_statements
```sql
CREATE TABLE income_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    line_item VARCHAR(200),
    year INTEGER,
    value VARCHAR(100),
    numeric_value FLOAT
);
CREATE INDEX ix_income_statement_duns_year ON income_statements(duns, year);
```

#### industries
```sql
CREATE TABLE industries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    industry_code VARCHAR(20),
    industry_description VARCHAR(200),
    is_primary BOOLEAN
);
```

#### operations
```sql
CREATE TABLE operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    field_name VARCHAR(100),
    field_value TEXT
);
```

#### people
```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duns VARCHAR(20) REFERENCES companies(duns),
    person_name VARCHAR(200),
    title VARCHAR(200),
    responsibilities TEXT
);
```

---

## API Endpoints Reference

### Root & Utility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check (returns `{"status": "healthy"}`) |
| GET | `/stats` | Database statistics (record counts) |

### Company Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List all companies (paginated) |
| GET | `/companies/{duns}` | Get company with industries, operations, people |
| GET | `/companies/{duns}/industries` | Get company's industry classifications |
| GET | `/companies/{duns}/operations` | Get company's operations description |
| GET | `/companies/{duns}/people` | Get company's personnel |
| GET | `/companies/{duns}/balance-sheet` | Get company's balance sheet data |
| GET | `/companies/{duns}/cash-flow` | Get company's cash flow data |
| GET | `/companies/{duns}/income-statement` | Get company's income statement data |

### Aggregate Financial Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/balance-sheets` | List all balance sheet records |
| GET | `/balance-sheets/line-items` | List unique line items with counts |
| GET | `/balance-sheets/years` | List available years |
| GET | `/cash-flows` | List all cash flow records |
| GET | `/cash-flows/line-items` | List unique line items with counts |
| GET | `/cash-flows/years` | List available years |
| GET | `/income-statements` | List all income statement records |
| GET | `/income-statements/line-items` | List unique line items with counts |
| GET | `/income-statements/years` | List available years |

### People & Industries Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/people` | List all personnel (paginated, filterable) |
| GET | `/people/titles` | List unique job titles with counts |
| GET | `/people/responsibilities` | List unique responsibilities with counts |
| GET | `/industries` | List all industry classifications |
| GET | `/industries/codes` | List unique SIC codes with company counts |

### Query Parameters

#### Pagination
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 50, max: 100)

#### Filtering
- `year` - Filter financial data by year (2015-2024)
- `line_item` - Partial match filter for line item name
- `industry_code` - Filter companies by SIC code
- `company_type` - Filter by company type
- `search` - Search in address or primary SIC
- `title` - Filter people by job title
- `name` - Filter people by name
- `responsibilities` - Filter by responsibility type
- `primary_only` - Only show primary industry classifications (boolean)

#### Aggregate Endpoints
- `limit` - Maximum records (default: 100, max: 1000)
- `offset` - Pagination offset

---

## Example API Requests

### Get API Info
```bash
curl https://company-financial-api-production.up.railway.app/
```

### List Companies (First Page)
```bash
curl "https://company-financial-api-production.up.railway.app/companies?page=1&page_size=10"
```

### Get Single Company with All Related Data
```bash
curl https://company-financial-api-production.up.railway.app/companies/740039581
```

### Get Company Balance Sheet for 2024
```bash
curl "https://company-financial-api-production.up.railway.app/companies/740039581/balance-sheet?year=2024"
```

### Search People by Title
```bash
curl "https://company-financial-api-production.up.railway.app/people?title=Director&page_size=20"
```

### Get Companies in Specific Industry
```bash
curl "https://company-financial-api-production.up.railway.app/companies?industry_code=7389"
```

### Get All Available Years
```bash
curl https://company-financial-api-production.up.railway.app/balance-sheets/years
```

### Get Unique Line Items
```bash
curl https://company-financial-api-production.up.railway.app/income-statements/line-items
```

---

## Project File Structure

```
C:\Users\jd\APItest\
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # SQLite connection & session management
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py
│       ├── companies.py     # Company-related endpoints
│       ├── financials.py    # Balance sheet, cash flow, income endpoints
│       ├── people.py        # Personnel endpoints
│       └── industries.py    # Industry classification endpoints
├── scripts/
│   └── import_data.py       # CSV to SQLite import script
├── docs/
│   └── PROJECT_DOCUMENTATION.md  # This file
├── CompanyData/             # Source CSV files (not in git)
│   ├── balance_sheet/
│   ├── cash_flow_statement/
│   ├── company_info/
│   ├── income_statement/
│   ├── industries/
│   ├── operations/
│   └── people/
├── company_data.db          # SQLite database (50MB)
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway/Heroku deployment config
├── runtime.txt              # Python version specification
├── .gitignore
├── README.md                # Quick start documentation
├── PLAN.md                  # Implementation plan
└── CANDIDATE_BRIEF.md       # Assessment instructions for candidates
```

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/uePEL1nx/company-financial-api.git
cd company-financial-api

# Install dependencies
pip install -r requirements.txt

# Import data (if CompanyData/ folder is present)
python scripts/import_data.py

# Run development server
uvicorn app.main:app --reload

# Access API
open http://localhost:8000/docs
```

### Dependencies

```
fastapi==0.115.6
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
python-multipart==0.0.18
```

---

## Deployment Information

### Railway.app Configuration

**Project**: company-financial-api
**Environment**: production
**Build**: Nixpacks (auto-detected Python)
**Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

The database file (`company_data.db`) is included in the deployment. For production use with frequent writes, consider:
1. Using Railway's PostgreSQL plugin
2. Mounting a persistent volume for SQLite

### Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
- `PORT` - Set automatically by Railway
- `DATABASE_PATH` - Optional: Override default database location

---

## Data Import Process

The `scripts/import_data.py` script:

1. Creates all database tables
2. Imports company info first (establishes foreign key references)
3. Imports financial data (balance sheets, cash flows, income statements)
4. Imports supporting data (industries, operations, people)
5. Handles data cleaning:
   - Currency values: `"$43,079"` → `43079.0`
   - Negative values: `"($34,984)"` → `-34984.0`
   - Percentages: `"16.47%"` → `16.47`
   - Missing values: `"-"` or blank → `null`

### Running Import
```bash
python scripts/import_data.py
```

### Expected Output
```
Data directory: C:\Users\jd\APItest\CompanyData
Database will be created at: C:\Users\jd\APItest\company_data.db

Creating database tables...

--- Importing Company Info ---
Imported 222 companies

--- Importing Balance Sheets ---
Imported 132120 balance sheet records

--- Importing Cash Flow Statements ---
Imported 66060 cash flow records

--- Importing Income Statements ---
Imported 103494 income statement records

--- Importing Industries ---
Imported 717 industry records

--- Importing Operations ---
Imported 24 operations records

--- Importing People ---
Imported 1457 people records

=== Import Complete ===

Database Summary:
  Companies: 222
  Balance Sheet Records: 132120
  Cash Flow Records: 66060
  Income Statement Records: 103494
  Industry Records: 717
  Operations Records: 24
  People Records: 1457
```

---

## Developer Assessment Usage

### For Hiring Managers

1. **Provide to candidates**:
   - `CompanyData/` folder (the raw CSV files)
   - `CANDIDATE_BRIEF.md` (assessment instructions)

2. **Do NOT provide**:
   - This repository
   - The deployed API URL (until after submission)

3. **Evaluation**:
   - Compare their solution against this reference implementation
   - Check their API at `/docs` for Swagger documentation
   - Test their endpoints against the same queries

### Assessment Criteria (from CANDIDATE_BRIEF.md)

| Criteria | Weight |
|----------|--------|
| Functionality - All endpoints work correctly | 30% |
| Code Quality - Clean, readable, well-organized | 20% |
| Database Design - Appropriate schema, efficient queries | 20% |
| Documentation - Clear, complete, useful | 15% |
| Deployment - Successfully hosted and accessible | 15% |

### Time Estimate
4-6 hours for a competent developer

---

## Maintenance Notes

### Adding New Data
1. Add CSV files to appropriate `CompanyData/` subdirectory
2. Re-run `python scripts/import_data.py` (will recreate database)
3. Redeploy with `railway up`

### Updating Dependencies
```bash
pip install --upgrade fastapi uvicorn sqlalchemy pydantic
pip freeze > requirements.txt
```

### Database Backup
```bash
cp company_data.db company_data_backup_$(date +%Y%m%d).db
```

---

## Troubleshooting

### Common Issues

**"Company not found" errors**
- Verify DUNS number exists: `curl .../companies` to list all
- DUNS numbers are strings, ensure proper formatting

**Empty financial data**
- Check year parameter: data covers 2015-2024
- Some line items may have null values for certain years

**Railway deployment issues**
- Check build logs in Railway dashboard
- Ensure `company_data.db` is committed to git
- Verify Procfile syntax

### Logs
```bash
# Railway logs
railway logs

# Local development
uvicorn app.main:app --reload --log-level debug
```

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Project Documentation | `docs/PROJECT_DOCUMENTATION.md` | Full technical reference (this file) |
| Data Dictionary | `docs/DATA_DICTIONARY.md` | All fields and data types |
| Testing & Evaluation | `docs/TESTING_AND_EVALUATION.md` | Candidate evaluation guide |
| Candidate Brief | `CANDIDATE_BRIEF.md` | Assessment instructions for candidates |
| Test Suite README | `testing/README.md` | Quick test reference |

---

## Contact & Support

**Repository**: https://github.com/uePEL1nx/company-financial-api
**Railway Project**: https://railway.com/project/33222dd0-30f6-4137-9c8e-4d41ce772a03

---

*Documentation generated December 2024*
