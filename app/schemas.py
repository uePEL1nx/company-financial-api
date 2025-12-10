# -*- coding: utf-8 -*-
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# Company schemas
class CompanyBase(BaseModel):
    duns: str
    physical_address: Optional[str] = None
    telephone_number: Optional[str] = None
    acn: Optional[str] = None
    company_type: Optional[str] = None
    primary_sic: Optional[str] = None


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    companies: List[CompanyResponse]


# Balance Sheet schemas
class BalanceSheetBase(BaseModel):
    id: int
    duns: str
    line_item: str
    year: int
    value: Optional[str] = None
    numeric_value: Optional[float] = None


class BalanceSheetResponse(BalanceSheetBase):
    model_config = ConfigDict(from_attributes=True)


class BalanceSheetListResponse(BaseModel):
    total: int
    duns: Optional[str] = None
    year: Optional[int] = None
    records: List[BalanceSheetResponse]


# Cash Flow schemas
class CashFlowBase(BaseModel):
    id: int
    duns: str
    line_item: str
    year: int
    value: Optional[str] = None
    numeric_value: Optional[float] = None


class CashFlowResponse(CashFlowBase):
    model_config = ConfigDict(from_attributes=True)


class CashFlowListResponse(BaseModel):
    total: int
    duns: Optional[str] = None
    year: Optional[int] = None
    records: List[CashFlowResponse]


# Income Statement schemas
class IncomeStatementBase(BaseModel):
    id: int
    duns: str
    line_item: str
    year: int
    value: Optional[str] = None
    numeric_value: Optional[float] = None


class IncomeStatementResponse(IncomeStatementBase):
    model_config = ConfigDict(from_attributes=True)


class IncomeStatementListResponse(BaseModel):
    total: int
    duns: Optional[str] = None
    year: Optional[int] = None
    records: List[IncomeStatementResponse]


# Industry schemas
class IndustryBase(BaseModel):
    id: int
    duns: str
    industry_code: Optional[str] = None
    industry_description: Optional[str] = None
    is_primary: bool


class IndustryResponse(IndustryBase):
    model_config = ConfigDict(from_attributes=True)


class IndustryListResponse(BaseModel):
    total: int
    industries: List[IndustryResponse]


# Operation schemas
class OperationBase(BaseModel):
    id: int
    duns: str
    field_name: Optional[str] = None
    field_value: Optional[str] = None


class OperationResponse(OperationBase):
    model_config = ConfigDict(from_attributes=True)


class OperationListResponse(BaseModel):
    total: int
    operations: List[OperationResponse]


# Person schemas
class PersonBase(BaseModel):
    id: int
    duns: str
    person_name: str
    title: Optional[str] = None
    responsibilities: Optional[str] = None


class PersonResponse(PersonBase):
    model_config = ConfigDict(from_attributes=True)


class PersonListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    people: List[PersonResponse]


# Company detail with all related data
class CompanyDetailResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    industries: List[IndustryResponse] = []
    operations: List[OperationResponse] = []
    people: List[PersonResponse] = []


# Line item schemas (for listing unique line items)
class LineItemResponse(BaseModel):
    line_item: str
    record_count: int


class LineItemListResponse(BaseModel):
    total: int
    line_items: List[LineItemResponse]


# Year list response
class YearListResponse(BaseModel):
    years: List[int]
