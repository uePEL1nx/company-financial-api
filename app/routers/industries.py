# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Industry
from app.schemas import IndustryResponse, IndustryListResponse

router = APIRouter(prefix="/industries", tags=["Industries"])


@router.get("", response_model=IndustryListResponse, summary="List all industry classifications")
def list_industries(
    code: Optional[str] = Query(None, description="Filter by industry code"),
    description: Optional[str] = Query(None, description="Filter by description (partial match)"),
    primary_only: bool = Query(False, description="Only show primary industry classifications"),
    db: Session = Depends(get_db)
):
    """
    List all industry classifications across all companies.

    - **code**: Filter by exact SIC code
    - **description**: Partial match filter for industry description
    - **primary_only**: Only return primary industry assignments
    """
    query = db.query(Industry)

    if code:
        query = query.filter(Industry.industry_code == code)
    if description:
        query = query.filter(Industry.industry_description.ilike(f"%{description}%"))
    if primary_only:
        query = query.filter(Industry.is_primary == True)

    industries = query.all()

    return IndustryListResponse(
        total=len(industries),
        industries=[IndustryResponse.model_validate(i) for i in industries]
    )


@router.get("/codes", summary="List unique industry codes")
def list_industry_codes(db: Session = Depends(get_db)):
    """
    Get a list of all unique industry codes with descriptions and company counts.
    """
    results = db.query(
        Industry.industry_code,
        Industry.industry_description,
        func.count(Industry.duns.distinct()).label('company_count')
    ).filter(
        Industry.industry_code.isnot(None),
        Industry.industry_code != ''
    ).group_by(
        Industry.industry_code,
        Industry.industry_description
    ).order_by(func.count(Industry.duns.distinct()).desc()).all()

    return {
        "total": len(results),
        "codes": [
            {
                "code": r[0],
                "description": r[1],
                "company_count": r[2]
            }
            for r in results
        ]
    }
