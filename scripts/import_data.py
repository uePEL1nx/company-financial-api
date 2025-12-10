# -*- coding: utf-8 -*-
import sys
import os
import csv
import re
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine, SessionLocal, Base
from app.models import Company, BalanceSheet, CashFlowStatement, IncomeStatement, Industry, Operation, Person


def parse_numeric_value(value_str):
    """Parse currency/percentage strings to numeric values."""
    if not value_str or value_str == '-' or value_str.strip() == '':
        return None

    # Remove quotes if present
    value_str = value_str.strip().strip('"').strip("'")

    if not value_str or value_str == '-':
        return None

    # Check if percentage
    if '%' in value_str:
        try:
            return float(value_str.replace('%', '').replace(',', '').strip())
        except ValueError:
            return None

    # Handle currency values like "$43,079" or "($34,984)"
    try:
        # Check for negative (parentheses)
        is_negative = '(' in value_str and ')' in value_str

        # Remove $, commas, parentheses
        cleaned = re.sub(r'[$,()"]', '', value_str).strip()

        if not cleaned or cleaned == '-':
            return None

        result = float(cleaned)
        return -result if is_negative else result
    except ValueError:
        return None


def import_company_info(session, data_dir):
    """Import company info from CSV files."""
    company_info_dir = data_dir / "company_info"
    companies = {}

    for csv_file in company_info_dir.glob("*.csv"):
        duns = csv_file.stem
        companies[duns] = {
            'duns': duns,
            'physical_address': None,
            'telephone_number': None,
            'acn': None,
            'company_type': None,
            'primary_sic': None
        }

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                field = row.get('field', '').strip()
                value = row.get('value', '').strip()

                if field == 'Physical Address':
                    companies[duns]['physical_address'] = value
                elif field == 'Telephone Number':
                    companies[duns]['telephone_number'] = value
                elif field == 'ACN':
                    companies[duns]['acn'] = value
                elif field == 'Company Type':
                    companies[duns]['company_type'] = value
                elif field == 'Primary SIC':
                    companies[duns]['primary_sic'] = value

    # Bulk insert companies
    for duns, info in companies.items():
        company = Company(**info)
        session.merge(company)

    session.commit()
    print(f"Imported {len(companies)} companies")
    return set(companies.keys())


def import_balance_sheets(session, data_dir, valid_duns):
    """Import balance sheet data."""
    balance_sheet_dir = data_dir / "balance_sheet"
    count = 0

    for csv_file in balance_sheet_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                try:
                    year = int(row.get('year', 0))
                except (ValueError, TypeError):
                    continue

                value = row.get('value', '')
                batch.append(BalanceSheet(
                    duns=duns,
                    line_item=row.get('line_item', ''),
                    year=year,
                    value=value,
                    numeric_value=parse_numeric_value(value)
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} balance sheet records")


def import_cash_flows(session, data_dir, valid_duns):
    """Import cash flow statement data."""
    cash_flow_dir = data_dir / "cash_flow_statement"
    count = 0

    for csv_file in cash_flow_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                try:
                    year = int(row.get('year', 0))
                except (ValueError, TypeError):
                    continue

                value = row.get('value', '')
                batch.append(CashFlowStatement(
                    duns=duns,
                    line_item=row.get('line_item', ''),
                    year=year,
                    value=value,
                    numeric_value=parse_numeric_value(value)
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} cash flow records")


def import_income_statements(session, data_dir, valid_duns):
    """Import income statement data."""
    income_dir = data_dir / "income_statement"
    count = 0

    for csv_file in income_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                try:
                    year = int(row.get('year', 0))
                except (ValueError, TypeError):
                    continue

                value = row.get('value', '')
                batch.append(IncomeStatement(
                    duns=duns,
                    line_item=row.get('line_item', ''),
                    year=year,
                    value=value,
                    numeric_value=parse_numeric_value(value)
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} income statement records")


def import_industries(session, data_dir, valid_duns):
    """Import industry classifications."""
    industries_dir = data_dir / "industries"
    count = 0

    for csv_file in industries_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                is_primary_val = row.get('is_primary', '0')
                try:
                    is_primary = bool(int(is_primary_val))
                except (ValueError, TypeError):
                    is_primary = False

                batch.append(Industry(
                    duns=duns,
                    industry_code=row.get('industry_code', ''),
                    industry_description=row.get('industry_description', ''),
                    is_primary=is_primary
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} industry records")


def import_operations(session, data_dir, valid_duns):
    """Import operations data."""
    operations_dir = data_dir / "operations"
    count = 0

    for csv_file in operations_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                batch.append(Operation(
                    duns=duns,
                    field_name=row.get('field_name', ''),
                    field_value=row.get('field_value', '')
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} operations records")


def import_people(session, data_dir, valid_duns):
    """Import people data."""
    people_dir = data_dir / "people"
    count = 0

    for csv_file in people_dir.glob("*.csv"):
        duns = csv_file.stem
        if duns not in valid_duns:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            batch = []
            for row in reader:
                batch.append(Person(
                    duns=duns,
                    person_name=row.get('person_name', ''),
                    title=row.get('title', ''),
                    responsibilities=row.get('responsibilities', '')
                ))
                count += 1

            session.bulk_save_objects(batch)

    session.commit()
    print(f"Imported {count} people records")


def main():
    # Setup paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    data_dir = project_dir / "CompanyData"

    print(f"Data directory: {data_dir}")
    print(f"Database will be created at: {project_dir / 'company_data.db'}")

    # Create tables
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)

    # Create session
    session = SessionLocal()

    try:
        # Import data in order (companies first due to foreign keys)
        print("\n--- Importing Company Info ---")
        valid_duns = import_company_info(session, data_dir)

        print("\n--- Importing Balance Sheets ---")
        import_balance_sheets(session, data_dir, valid_duns)

        print("\n--- Importing Cash Flow Statements ---")
        import_cash_flows(session, data_dir, valid_duns)

        print("\n--- Importing Income Statements ---")
        import_income_statements(session, data_dir, valid_duns)

        print("\n--- Importing Industries ---")
        import_industries(session, data_dir, valid_duns)

        print("\n--- Importing Operations ---")
        import_operations(session, data_dir, valid_duns)

        print("\n--- Importing People ---")
        import_people(session, data_dir, valid_duns)

        print("\n=== Import Complete ===")

        # Print summary
        print(f"\nDatabase Summary:")
        print(f"  Companies: {session.query(Company).count()}")
        print(f"  Balance Sheet Records: {session.query(BalanceSheet).count()}")
        print(f"  Cash Flow Records: {session.query(CashFlowStatement).count()}")
        print(f"  Income Statement Records: {session.query(IncomeStatement).count()}")
        print(f"  Industry Records: {session.query(Industry).count()}")
        print(f"  Operations Records: {session.query(Operation).count()}")
        print(f"  People Records: {session.query(Person).count()}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
