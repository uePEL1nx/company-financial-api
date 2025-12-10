# -*- coding: utf-8 -*-
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.database import get_db
from app.models import Company, BalanceSheet, CashFlowStatement, IncomeStatement
from app.schemas import (
    BalanceSheetResponse, BalanceSheetListResponse,
    CashFlowResponse, CashFlowListResponse,
    IncomeStatementResponse, IncomeStatementListResponse,
    LineItemResponse, LineItemListResponse, YearListResponse
)

router = APIRouter(tags=["Financial Statements"])


# ============ BALANCE SHEET ENDPOINTS ============

@router.get("/balance-sheets", response_model=BalanceSheetListResponse, summary="List all balance sheet records")
def list_balance_sheets(
    year: Optional[int] = Query(None, description="Filter by year (2015-2024)"),
    line_item: Optional[str] = Query(None, description="Filter by line item (partial match)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
):
    """
    List balance sheet records across all companies.

    - **year**: Filter by fiscal year
    - **line_item**: Partial match filter for line item name
    - **limit**: Maximum records (default: 100, max: 1000)
    - **offset**: Pagination offset
    """
    query = db.query(BalanceSheet)

    if year:
        query = query.filter(BalanceSheet.year == year)
    if line_item:
        query = query.filter(BalanceSheet.line_item.ilike(f"%{line_item}%"))

    total = query.count()
    records = query.offset(offset).limit(limit).all()

    return BalanceSheetListResponse(
        total=total,
        year=year,
        records=[BalanceSheetResponse.model_validate(r) for r in records]
    )


@router.get("/balance-sheets/line-items", response_model=LineItemListResponse, summary="List unique balance sheet line items")
def list_balance_sheet_line_items(db: Session = Depends(get_db)):
    """
    Get a list of all unique line items in balance sheet data with record counts.
    """
    results = db.query(
        BalanceSheet.line_item,
        func.count(BalanceSheet.id).label('count')
    ).group_by(BalanceSheet.line_item).order_by(BalanceSheet.line_item).all()

    return LineItemListResponse(
        total=len(results),
        line_items=[LineItemResponse(line_item=r[0], record_count=r[1]) for r in results]
    )


@router.get("/balance-sheets/years", response_model=YearListResponse, summary="List available years for balance sheets")
def list_balance_sheet_years(db: Session = Depends(get_db)):
    """
    Get all available years in balance sheet data.
    """
    years = db.query(distinct(BalanceSheet.year)).order_by(BalanceSheet.year.desc()).all()
    return YearListResponse(years=[y[0] for y in years])


@router.get("/companies/{duns}/balance-sheet", response_model=BalanceSheetListResponse, summary="Get company balance sheet")
def get_company_balance_sheet(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    line_item: Optional[str] = Query(None, description="Filter by line item"),
    db: Session = Depends(get_db)
):
    """
    Get balance sheet data for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    query = db.query(BalanceSheet).filter(BalanceSheet.duns == duns)

    if year:
        query = query.filter(BalanceSheet.year == year)
    if line_item:
        query = query.filter(BalanceSheet.line_item.ilike(f"%{line_item}%"))

    records = query.order_by(BalanceSheet.year.desc(), BalanceSheet.line_item).all()

    return BalanceSheetListResponse(
        total=len(records),
        duns=duns,
        year=year,
        records=[BalanceSheetResponse.model_validate(r) for r in records]
    )


# ============ CASH FLOW STATEMENT ENDPOINTS ============

@router.get("/cash-flows", response_model=CashFlowListResponse, summary="List all cash flow records")
def list_cash_flows(
    year: Optional[int] = Query(None, description="Filter by year"),
    line_item: Optional[str] = Query(None, description="Filter by line item"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
):
    """
    List cash flow statement records across all companies.
    """
    query = db.query(CashFlowStatement)

    if year:
        query = query.filter(CashFlowStatement.year == year)
    if line_item:
        query = query.filter(CashFlowStatement.line_item.ilike(f"%{line_item}%"))

    total = query.count()
    records = query.offset(offset).limit(limit).all()

    return CashFlowListResponse(
        total=total,
        year=year,
        records=[CashFlowResponse.model_validate(r) for r in records]
    )


@router.get("/cash-flows/line-items", response_model=LineItemListResponse, summary="List unique cash flow line items")
def list_cash_flow_line_items(db: Session = Depends(get_db)):
    """
    Get a list of all unique line items in cash flow data with record counts.
    """
    results = db.query(
        CashFlowStatement.line_item,
        func.count(CashFlowStatement.id).label('count')
    ).group_by(CashFlowStatement.line_item).order_by(CashFlowStatement.line_item).all()

    return LineItemListResponse(
        total=len(results),
        line_items=[LineItemResponse(line_item=r[0], record_count=r[1]) for r in results]
    )


@router.get("/cash-flows/years", response_model=YearListResponse, summary="List available years for cash flows")
def list_cash_flow_years(db: Session = Depends(get_db)):
    """
    Get all available years in cash flow data.
    """
    years = db.query(distinct(CashFlowStatement.year)).order_by(CashFlowStatement.year.desc()).all()
    return YearListResponse(years=[y[0] for y in years])


@router.get("/companies/{duns}/cash-flow", response_model=CashFlowListResponse, summary="Get company cash flow")
def get_company_cash_flow(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    line_item: Optional[str] = Query(None, description="Filter by line item"),
    db: Session = Depends(get_db)
):
    """
    Get cash flow statement data for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    query = db.query(CashFlowStatement).filter(CashFlowStatement.duns == duns)

    if year:
        query = query.filter(CashFlowStatement.year == year)
    if line_item:
        query = query.filter(CashFlowStatement.line_item.ilike(f"%{line_item}%"))

    records = query.order_by(CashFlowStatement.year.desc(), CashFlowStatement.line_item).all()

    return CashFlowListResponse(
        total=len(records),
        duns=duns,
        year=year,
        records=[CashFlowResponse.model_validate(r) for r in records]
    )


# ============ INCOME STATEMENT ENDPOINTS ============

@router.get("/income-statements", response_model=IncomeStatementListResponse, summary="List all income statement records")
def list_income_statements(
    year: Optional[int] = Query(None, description="Filter by year"),
    line_item: Optional[str] = Query(None, description="Filter by line item"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: Session = Depends(get_db)
):
    """
    List income statement records across all companies.
    """
    query = db.query(IncomeStatement)

    if year:
        query = query.filter(IncomeStatement.year == year)
    if line_item:
        query = query.filter(IncomeStatement.line_item.ilike(f"%{line_item}%"))

    total = query.count()
    records = query.offset(offset).limit(limit).all()

    return IncomeStatementListResponse(
        total=total,
        year=year,
        records=[IncomeStatementResponse.model_validate(r) for r in records]
    )


@router.get("/income-statements/line-items", response_model=LineItemListResponse, summary="List unique income statement line items")
def list_income_statement_line_items(db: Session = Depends(get_db)):
    """
    Get a list of all unique line items in income statement data with record counts.
    """
    results = db.query(
        IncomeStatement.line_item,
        func.count(IncomeStatement.id).label('count')
    ).group_by(IncomeStatement.line_item).order_by(IncomeStatement.line_item).all()

    return LineItemListResponse(
        total=len(results),
        line_items=[LineItemResponse(line_item=r[0], record_count=r[1]) for r in results]
    )


@router.get("/income-statements/years", response_model=YearListResponse, summary="List available years for income statements")
def list_income_statement_years(db: Session = Depends(get_db)):
    """
    Get all available years in income statement data.
    """
    years = db.query(distinct(IncomeStatement.year)).order_by(IncomeStatement.year.desc()).all()
    return YearListResponse(years=[y[0] for y in years])


@router.get("/companies/{duns}/income-statement", response_model=IncomeStatementListResponse, summary="Get company income statement")
def get_company_income_statement(
    duns: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    line_item: Optional[str] = Query(None, description="Filter by line item"),
    db: Session = Depends(get_db)
):
    """
    Get income statement data for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    query = db.query(IncomeStatement).filter(IncomeStatement.duns == duns)

    if year:
        query = query.filter(IncomeStatement.year == year)
    if line_item:
        query = query.filter(IncomeStatement.line_item.ilike(f"%{line_item}%"))

    records = query.order_by(IncomeStatement.year.desc(), IncomeStatement.line_item).all()

    return IncomeStatementListResponse(
        total=len(records),
        duns=duns,
        year=year,
        records=[IncomeStatementResponse.model_validate(r) for r in records]
    )
