# Software Developer Assessment - Company Data API

## Overview

Build a REST API that serves company financial data from the provided CSV files. The API should be documented, tested, and deployed to a public URL.

## Time Limit

4-6 hours (estimate)

## Provided Materials

You will receive a `CompanyData/` folder containing CSV files organized into 7 subdirectories:

| Directory | Content |
|-----------|---------|
| `balance_sheet/` | Balance sheet data (assets, liabilities, equity) |
| `cash_flow_statement/` | Cash flow statements |
| `income_statement/` | Income statements (revenue, expenses, profit) |
| `company_info/` | Company details (address, phone, ACN, type) |
| `industries/` | Industry classifications (SIC codes) |
| `operations/` | Business descriptions |
| `people/` | Executive and director information |

Each file is named by DUNS number (e.g., `740039581.csv`), which is the unique identifier linking data across all categories.

## Requirements

### 1. Database (25%)

- Design and implement an appropriate database schema
- Import all CSV data
- Handle data cleaning (currency formatting, null values, etc.)

### 2. API Endpoints (40%)

Create RESTful endpoints to access:

**Minimum Required:**
- List all companies (with pagination)
- Get single company details by DUNS
- Get company's balance sheet data
- Get company's income statement data
- Get company's cash flow data
- Get company's personnel
- Get company's industry classifications

**Bonus:**
- Filter companies by industry code
- Filter financial data by year
- Search functionality
- Aggregate queries across companies

### 3. Documentation (15%)

- Auto-generated API documentation (Swagger/OpenAPI preferred)
- Clear endpoint descriptions
- Example requests/responses
- README with setup instructions

### 4. Deployment (20%)

- Deploy to a public hosting platform
- Provide the live API URL
- API must be accessible and functional

## Technical Guidelines

- **Language**: Any (Python, Node.js, Go, etc.)
- **Database**: Any (SQLite, PostgreSQL, etc.)
- **Framework**: Any (FastAPI, Express, Gin, etc.)

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| **Functionality** - All endpoints work correctly | 30% |
| **Code Quality** - Clean, readable, well-organized | 20% |
| **Database Design** - Appropriate schema, efficient queries | 20% |
| **Documentation** - Clear, complete, useful | 15% |
| **Deployment** - Successfully hosted and accessible | 15% |

## Submission

Provide:
1. GitHub repository URL (public or with access granted)
2. Live API URL
3. API documentation URL (e.g., `/docs` endpoint)

## Sample Data Structure

### company_info CSV
```
duns,field,value
740039581,Physical Address,"LEVEL 24, 300 BARANGAROO AVENUE..."
740039581,Telephone Number,02 89087900
740039581,ACN,082169060
740039581,Company Type,Publicly Unlisted
740039581,Primary SIC,"7389 - Business Services..."
```

### balance_sheet CSV
```
duns,line_item,year,value
740039581,Cash and cash equivalents ($000s),2024,"$43,079"
740039581,Total current assets ($000s),2024,"$50,370"
740039581,TOTAL ASSETS ($000s),2024,"$56,136"
```

### people CSV
```
duns,person_name,title,responsibilities
740039581,Mark Rutherglen,Director,Director
740039581,Sabine Tromeur,Director of Finance,Financial Decision Maker
```

## Notes

- The data is synthetic/anonymized for this assessment
- Focus on demonstrating clean code and good API design
- Don't over-engineer - deliver working functionality first
- Tests are a bonus, not required

## Questions?

If you have questions about the requirements, please ask before starting.

Good luck!
