# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    duns = Column(String(20), primary_key=True, index=True)
    physical_address = Column(Text, nullable=True)
    telephone_number = Column(String(50), nullable=True)
    acn = Column(String(20), nullable=True)
    company_type = Column(String(100), nullable=True)
    primary_sic = Column(String(200), nullable=True)

    # Relationships
    balance_sheets = relationship("BalanceSheet", back_populates="company", cascade="all, delete-orphan")
    cash_flows = relationship("CashFlowStatement", back_populates="company", cascade="all, delete-orphan")
    income_statements = relationship("IncomeStatement", back_populates="company", cascade="all, delete-orphan")
    industries = relationship("Industry", back_populates="company", cascade="all, delete-orphan")
    operations = relationship("Operation", back_populates="company", cascade="all, delete-orphan")
    people = relationship("Person", back_populates="company", cascade="all, delete-orphan")


class BalanceSheet(Base):
    __tablename__ = "balance_sheets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    line_item = Column(String(200), index=True)
    year = Column(Integer, index=True)
    value = Column(String(100), nullable=True)  # Keep as string to preserve formatting
    numeric_value = Column(Float, nullable=True)  # Parsed numeric value

    company = relationship("Company", back_populates="balance_sheets")

    __table_args__ = (
        Index('ix_balance_sheet_duns_year', 'duns', 'year'),
    )


class CashFlowStatement(Base):
    __tablename__ = "cash_flow_statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    line_item = Column(String(200), index=True)
    year = Column(Integer, index=True)
    value = Column(String(100), nullable=True)
    numeric_value = Column(Float, nullable=True)

    company = relationship("Company", back_populates="cash_flows")

    __table_args__ = (
        Index('ix_cash_flow_duns_year', 'duns', 'year'),
    )


class IncomeStatement(Base):
    __tablename__ = "income_statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    line_item = Column(String(200), index=True)
    year = Column(Integer, index=True)
    value = Column(String(100), nullable=True)
    numeric_value = Column(Float, nullable=True)

    company = relationship("Company", back_populates="income_statements")

    __table_args__ = (
        Index('ix_income_statement_duns_year', 'duns', 'year'),
    )


class Industry(Base):
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    industry_code = Column(String(20), index=True, nullable=True)
    industry_description = Column(String(200), nullable=True)
    is_primary = Column(Boolean, default=False)

    company = relationship("Company", back_populates="industries")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    field_name = Column(String(100), nullable=True)
    field_value = Column(Text, nullable=True)

    company = relationship("Company", back_populates="operations")


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, autoincrement=True)
    duns = Column(String(20), ForeignKey("companies.duns"), index=True)
    person_name = Column(String(200), index=True)
    title = Column(String(200), nullable=True)
    responsibilities = Column(Text, nullable=True)

    company = relationship("Company", back_populates="people")
