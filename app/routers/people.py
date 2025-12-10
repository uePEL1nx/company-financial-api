# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.database import get_db
from app.models import Person
from app.schemas import PersonResponse, PersonListResponse

router = APIRouter(prefix="/people", tags=["People"])


@router.get("", response_model=PersonListResponse, summary="List all people")
def list_people(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),
    responsibilities: Optional[str] = Query(None, description="Filter by responsibilities"),
    db: Session = Depends(get_db)
):
    """
    List all personnel across all companies with filtering options.

    - **title**: Filter by job title (e.g., "Director", "CEO")
    - **name**: Filter by person name
    - **responsibilities**: Filter by responsibility type
    """
    query = db.query(Person)

    if title:
        query = query.filter(Person.title.ilike(f"%{title}%"))
    if name:
        query = query.filter(Person.person_name.ilike(f"%{name}%"))
    if responsibilities:
        query = query.filter(Person.responsibilities.ilike(f"%{responsibilities}%"))

    total = query.count()

    offset = (page - 1) * page_size
    people = query.offset(offset).limit(page_size).all()

    return PersonListResponse(
        total=total,
        page=page,
        page_size=page_size,
        people=[PersonResponse.model_validate(p) for p in people]
    )


@router.get("/titles", summary="List unique job titles")
def list_titles(db: Session = Depends(get_db)):
    """
    Get a list of all unique job titles with counts.
    """
    results = db.query(
        Person.title,
        func.count(Person.id).label('count')
    ).group_by(Person.title).order_by(func.count(Person.id).desc()).all()

    return {
        "total": len(results),
        "titles": [{"title": r[0], "count": r[1]} for r in results if r[0]]
    }


@router.get("/responsibilities", summary="List unique responsibilities")
def list_responsibilities(db: Session = Depends(get_db)):
    """
    Get a list of all unique responsibility types.
    """
    results = db.query(distinct(Person.responsibilities)).filter(
        Person.responsibilities.isnot(None),
        Person.responsibilities != ''
    ).all()

    # Parse and count unique responsibilities (they can be comma-separated)
    resp_counts = {}
    all_people = db.query(Person.responsibilities).filter(
        Person.responsibilities.isnot(None)
    ).all()

    for (resp_str,) in all_people:
        if resp_str:
            for resp in resp_str.split(','):
                resp = resp.strip()
                if resp:
                    resp_counts[resp] = resp_counts.get(resp, 0) + 1

    sorted_resp = sorted(resp_counts.items(), key=lambda x: x[1], reverse=True)

    return {
        "total": len(sorted_resp),
        "responsibilities": [{"responsibility": r[0], "count": r[1]} for r in sorted_resp]
    }
