# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import companies, financials, people, industries

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Company Financial Data API",
    description="""
## Company Financial Data API

This API provides access to comprehensive financial data for 222 companies, including:

### Data Categories

- **Companies** - Basic company information (address, phone, ACN, type)
- **Balance Sheets** - Financial position data (assets, liabilities, equity) from 2015-2024
- **Cash Flow Statements** - Cash flows by activity type from 2015-2024
- **Income Statements** - Revenue, expenses, and profitability metrics from 2015-2024
- **Industries** - SIC industry classifications for each company
- **Operations** - Business descriptions and operational details
- **People** - Executive and director information

### Data Structure

All data is linked by **DUNS number** (Data Universal Numbering System), a unique 9-digit identifier for businesses.

Financial data spans **10 years** (2015-2024) with detailed line items for each financial statement.

### Usage

- Use `/companies` endpoints to browse and search companies
- Use `/companies/{duns}/...` endpoints to get specific company data
- Use `/balance-sheets`, `/cash-flows`, `/income-statements` for aggregate queries
- Use `/people` and `/industries` endpoints for cross-company searches
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router)
app.include_router(financials.router)
app.include_router(people.router)
app.include_router(industries.router)


@app.get("/", tags=["Root"])
def root():
    """
    API Root - Returns basic API information and available endpoints.
    """
    return {
        "name": "Company Financial Data API",
        "version": "1.0.0",
        "description": "API for accessing company financial data",
        "documentation": "/docs",
        "endpoints": {
            "companies": "/companies",
            "balance_sheets": "/balance-sheets",
            "cash_flows": "/cash-flows",
            "income_statements": "/income-statements",
            "people": "/people",
            "industries": "/industries"
        },
        "data_summary": {
            "total_companies": 222,
            "financial_years": "2015-2024",
            "data_types": [
                "Balance Sheets",
                "Cash Flow Statements",
                "Income Statements",
                "Industry Classifications",
                "Operations Descriptions",
                "Personnel Information"
            ]
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}


@app.get("/stats", tags=["Statistics"])
def get_stats():
    """
    Get database statistics.
    """
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models import Company, BalanceSheet, CashFlowStatement, IncomeStatement, Industry, Operation, Person

    db = SessionLocal()
    try:
        return {
            "companies": db.query(Company).count(),
            "balance_sheet_records": db.query(BalanceSheet).count(),
            "cash_flow_records": db.query(CashFlowStatement).count(),
            "income_statement_records": db.query(IncomeStatement).count(),
            "industry_records": db.query(Industry).count(),
            "operation_records": db.query(Operation).count(),
            "people_records": db.query(Person).count()
        }
    finally:
        db.close()
