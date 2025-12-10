# Company Financial Data API

A RESTful API providing access to comprehensive financial data for 222 Australian companies.

## Data Overview

| Category | Description | Records |
|----------|-------------|---------|
| Companies | Basic info (address, phone, ACN, type) | 222 |
| Balance Sheets | Assets, liabilities, equity (2015-2024) | 132,120 |
| Cash Flow Statements | Operating, investing, financing flows | 66,060 |
| Income Statements | Revenue, expenses, profitability | 103,494 |
| Industries | SIC industry classifications | 717 |
| Operations | Business descriptions | 24 |
| People | Executives and directors | 1,457 |

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Import data (first time only)
python scripts/import_data.py

# Run the API
uvicorn app.main:app --reload

# Access documentation
open http://localhost:8000/docs
```

### API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Companies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List all companies (paginated) |
| GET | `/companies/{duns}` | Get company details with industries, operations, people |
| GET | `/companies/{duns}/industries` | Get company industry classifications |
| GET | `/companies/{duns}/operations` | Get company operations description |
| GET | `/companies/{duns}/people` | Get company personnel |

### Financial Statements
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies/{duns}/balance-sheet` | Get company balance sheet |
| GET | `/companies/{duns}/cash-flow` | Get company cash flow statement |
| GET | `/companies/{duns}/income-statement` | Get company income statement |
| GET | `/balance-sheets` | List all balance sheet records |
| GET | `/balance-sheets/line-items` | List unique balance sheet line items |
| GET | `/balance-sheets/years` | List available years |
| GET | `/cash-flows` | List all cash flow records |
| GET | `/cash-flows/line-items` | List unique cash flow line items |
| GET | `/cash-flows/years` | List available years |
| GET | `/income-statements` | List all income statement records |
| GET | `/income-statements/line-items` | List unique income statement line items |
| GET | `/income-statements/years` | List available years |

### People & Industries
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/people` | List all personnel (filterable) |
| GET | `/people/titles` | List unique job titles |
| GET | `/people/responsibilities` | List unique responsibilities |
| GET | `/industries` | List all industry classifications |
| GET | `/industries/codes` | List unique industry codes with counts |

### Utility
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/stats` | Database statistics |

## Query Parameters

### Pagination
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 50, max: 100)

### Filtering
- `year`: Filter financial data by year (2015-2024)
- `line_item`: Filter by line item name (partial match)
- `industry_code`: Filter companies by SIC code
- `company_type`: Filter by company type
- `search`: Search in address or primary SIC
- `title`: Filter people by job title
- `name`: Filter people by name
- `responsibilities`: Filter by responsibility type

## Example Requests

```bash
# List companies
curl "http://localhost:8000/companies?page=1&page_size=10"

# Get company details
curl "http://localhost:8000/companies/740039581"

# Get balance sheet for specific year
curl "http://localhost:8000/companies/740039581/balance-sheet?year=2024"

# Search people by title
curl "http://localhost:8000/people?title=Director&page_size=20"

# Get companies in specific industry
curl "http://localhost:8000/companies?industry_code=7389"
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Deployment

### Railway.app

1. Push to GitHub
2. Connect repository to Railway
3. Deploy (auto-detects Python)

### Render.com

1. Push to GitHub
2. Create new Web Service
3. Connect repository
4. Set build command: `pip install -r requirements.txt && python scripts/import_data.py`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Project Structure

```
APItest/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── routers/
│       ├── companies.py  # Company endpoints
│       ├── financials.py # Financial statement endpoints
│       ├── people.py     # People endpoints
│       └── industries.py # Industry endpoints
├── scripts/
│   └── import_data.py    # Data import script
├── CompanyData/          # Source CSV files
├── company_data.db       # SQLite database
├── requirements.txt
├── Procfile              # Deployment config
└── README.md
```

## Data Source

Data is provided in CSV format in the `CompanyData/` directory:
- `balance_sheet/` - Balance sheet data by DUNS
- `cash_flow_statement/` - Cash flow data by DUNS
- `income_statement/` - Income statement data by DUNS
- `company_info/` - Company details by DUNS
- `industries/` - Industry classifications by DUNS
- `operations/` - Operations descriptions by DUNS
- `people/` - Personnel information by DUNS

## License

Proprietary - For assessment purposes only.
