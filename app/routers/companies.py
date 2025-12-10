# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Company, Industry, Operation, Person
from app.schemas import (
    CompanyResponse, CompanyListResponse, CompanyDetailResponse,
    IndustryResponse, IndustryListResponse,
    OperationResponse, OperationListResponse,
    PersonResponse, PersonListResponse
)

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("", response_model=CompanyListResponse, summary="List all companies")
def list_companies(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    industry_code: Optional[str] = Query(None, description="Filter by industry code"),
    company_type: Optional[str] = Query(None, description="Filter by company type"),
    search: Optional[str] = Query(None, description="Search in address or primary SIC"),
    db: Session = Depends(get_db)
):
    """
    List all companies with pagination and filtering options.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 50, max: 100)
    - **industry_code**: Filter by SIC industry code
    - **company_type**: Filter by company type
    - **search**: Search term for address or primary SIC
    """
    query = db.query(Company)

    # Apply filters
    if industry_code:
        query = query.join(Industry).filter(Industry.industry_code == industry_code)

    if company_type:
        query = query.filter(Company.company_type.ilike(f"%{company_type}%"))

    if search:
        query = query.filter(
            (Company.physical_address.ilike(f"%{search}%")) |
            (Company.primary_sic.ilike(f"%{search}%"))
        )

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * page_size
    companies = query.offset(offset).limit(page_size).all()

    return CompanyListResponse(
        total=total,
        page=page,
        page_size=page_size,
        companies=[CompanyResponse.model_validate(c) for c in companies]
    )


@router.get("/{duns}", response_model=CompanyDetailResponse, summary="Get company details")
def get_company(duns: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific company by DUNS number.

    Includes:
    - Company info (address, phone, ACN, type, primary SIC)
    - All industry classifications
    - Operations description
    - All personnel
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    return CompanyDetailResponse(
        duns=company.duns,
        physical_address=company.physical_address,
        telephone_number=company.telephone_number,
        acn=company.acn,
        company_type=company.company_type,
        primary_sic=company.primary_sic,
        industries=[IndustryResponse.model_validate(i) for i in company.industries],
        operations=[OperationResponse.model_validate(o) for o in company.operations],
        people=[PersonResponse.model_validate(p) for p in company.people]
    )


@router.get("/{duns}/industries", response_model=IndustryListResponse, summary="Get company industries")
def get_company_industries(duns: str, db: Session = Depends(get_db)):
    """
    Get all industry classifications for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    industries = db.query(Industry).filter(Industry.duns == duns).all()
    return IndustryListResponse(
        total=len(industries),
        industries=[IndustryResponse.model_validate(i) for i in industries]
    )


@router.get("/{duns}/operations", response_model=OperationListResponse, summary="Get company operations")
def get_company_operations(duns: str, db: Session = Depends(get_db)):
    """
    Get operations/business description for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    operations = db.query(Operation).filter(Operation.duns == duns).all()
    return OperationListResponse(
        total=len(operations),
        operations=[OperationResponse.model_validate(o) for o in operations]
    )


@router.get("/{duns}/people", response_model=PersonListResponse, summary="Get company personnel")
def get_company_people(
    duns: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all personnel (executives, directors) for a specific company.
    """
    company = db.query(Company).filter(Company.duns == duns).first()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with DUNS {duns} not found")

    query = db.query(Person).filter(Person.duns == duns)
    total = query.count()

    offset = (page - 1) * page_size
    people = query.offset(offset).limit(page_size).all()

    return PersonListResponse(
        total=total,
        page=page,
        page_size=page_size,
        people=[PersonResponse.model_validate(p) for p in people]
    )
