# -*- coding: utf-8 -*-
"""
Data Validation Tests

Verifies that the API returns correct data by comparing against known source values.
Run with: python test_data_validation.py <candidate_api_url>
"""

import sys
import json
import requests
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class ValidationResult:
    test_name: str
    passed: bool
    expected: Any
    actual: Any
    message: str


class DataValidator:
    """Validates API data against known source values."""

    # Known correct values from source CSV files (DUNS: 740039581)
    SAMPLE_DUNS = "740039581"

    EXPECTED_COMPANY = {
        "acn": "082169060",
        "telephone_number": "02 89087900",
        "company_type": "Publicly Unlisted",
        "primary_sic_contains": "7389",
        "address_contains": "BARANGAROO"
    }

    EXPECTED_BALANCE_SHEET_2024 = {
        "Cash and cash equivalents ($000s)": "$43,079",
        "cash_numeric": 43079.0
    }

    EXPECTED_PEOPLE = [
        {"name_contains": "Rutherglen", "title": "Director"},
        {"name_contains": "Anderson", "title": "Director and Company Secretary"},
        {"name_contains": "Tromeur", "title": "Director of Finance"},
    ]

    EXPECTED_PEOPLE_COUNT = 10

    EXPECTED_INDUSTRIES = [
        {"code": "7389", "description_contains": "Business Services"},
        {"code": "6719", "description_contains": "Holding Companies"},
    ]

    EXPECTED_TOTAL_COMPANIES = 222

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results: List[ValidationResult] = []

    def make_request(self, endpoint: str, params: dict = None):
        """Make HTTP request and return JSON response."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json(), None
            return None, f"HTTP {response.status_code}"
        except Exception as e:
            return None, str(e)

    def add_result(self, result: ValidationResult):
        self.results.append(result)
        status = "PASS" if result.passed else "FAIL"
        print(f"  [{status}] {result.test_name}")
        if not result.passed:
            print(f"       Expected: {result.expected}")
            print(f"       Actual:   {result.actual}")

    def run_all_validations(self):
        """Run all data validation tests."""
        print(f"\n{'='*60}")
        print("DATA VALIDATION TESTS")
        print(f"{'='*60}")
        print(f"API URL: {self.base_url}")
        print(f"Sample DUNS: {self.SAMPLE_DUNS}")
        print(f"{'='*60}\n")

        self.validate_company_count()
        self.validate_company_info()
        self.validate_balance_sheet_data()
        self.validate_people_data()
        self.validate_industry_data()

        self.print_summary()

    def validate_company_count(self):
        """Validate total company count."""
        print("Validating: Company Count...")

        data, error = self.make_request("/companies")
        if error:
            self.add_result(ValidationResult(
                test_name="Total Company Count",
                passed=False,
                expected=self.EXPECTED_TOTAL_COMPANIES,
                actual=f"Error: {error}",
                message="Could not retrieve companies"
            ))
            return

        # Try different response structures
        total = data.get('total') or len(data.get('companies', data.get('data', data if isinstance(data, list) else [])))

        self.add_result(ValidationResult(
            test_name="Total Company Count",
            passed=abs(total - self.EXPECTED_TOTAL_COMPANIES) <= 2,
            expected=self.EXPECTED_TOTAL_COMPANIES,
            actual=total,
            message=f"Found {total} companies"
        ))

    def validate_company_info(self):
        """Validate company info fields match source."""
        print("\nValidating: Company Info...")

        data, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if error:
            self.add_result(ValidationResult(
                test_name="Company Info Retrieval",
                passed=False,
                expected="Company data",
                actual=f"Error: {error}",
                message="Could not retrieve company"
            ))
            return

        # ACN
        acn = data.get('acn') or data.get('ACN') or data.get('company_number')
        self.add_result(ValidationResult(
            test_name="Company ACN",
            passed=str(acn) == self.EXPECTED_COMPANY["acn"],
            expected=self.EXPECTED_COMPANY["acn"],
            actual=acn,
            message="ACN matches source"
        ))

        # Phone
        phone = data.get('telephone_number') or data.get('phone') or data.get('telephone')
        self.add_result(ValidationResult(
            test_name="Company Phone",
            passed=str(phone) == self.EXPECTED_COMPANY["telephone_number"],
            expected=self.EXPECTED_COMPANY["telephone_number"],
            actual=phone,
            message="Phone matches source"
        ))

        # Company Type
        comp_type = data.get('company_type') or data.get('type') or data.get('companyType')
        self.add_result(ValidationResult(
            test_name="Company Type",
            passed=comp_type == self.EXPECTED_COMPANY["company_type"],
            expected=self.EXPECTED_COMPANY["company_type"],
            actual=comp_type,
            message="Company type matches source"
        ))

        # Address contains expected value
        address = data.get('physical_address') or data.get('address') or data.get('physicalAddress') or ""
        self.add_result(ValidationResult(
            test_name="Company Address",
            passed=self.EXPECTED_COMPANY["address_contains"] in str(address).upper(),
            expected=f"Contains '{self.EXPECTED_COMPANY['address_contains']}'",
            actual=address[:80] + "..." if len(str(address)) > 80 else address,
            message="Address contains expected location"
        ))

        # Primary SIC contains expected code
        sic = data.get('primary_sic') or data.get('sic') or data.get('primarySic') or ""
        self.add_result(ValidationResult(
            test_name="Primary SIC Code",
            passed=self.EXPECTED_COMPANY["primary_sic_contains"] in str(sic),
            expected=f"Contains '{self.EXPECTED_COMPANY['primary_sic_contains']}'",
            actual=sic[:60] + "..." if len(str(sic)) > 60 else sic,
            message="SIC contains expected code"
        ))

    def validate_balance_sheet_data(self):
        """Validate balance sheet data matches source."""
        print("\nValidating: Balance Sheet Data...")

        # Try different endpoint patterns
        data = None
        for endpoint in [
            f"/companies/{self.SAMPLE_DUNS}/balance-sheet",
            f"/companies/{self.SAMPLE_DUNS}/balance_sheet",
            f"/companies/{self.SAMPLE_DUNS}/balancesheet"
        ]:
            data, error = self.make_request(endpoint, {"year": 2024})
            if data:
                break

        if not data:
            self.add_result(ValidationResult(
                test_name="Balance Sheet Retrieval",
                passed=False,
                expected="Balance sheet data",
                actual=f"Error: {error}",
                message="Could not retrieve balance sheet"
            ))
            return

        records = data.get('records') or data.get('data') or (data if isinstance(data, list) else [])

        # Find cash and cash equivalents
        cash_record = None
        for r in records:
            line_item = r.get('line_item') or r.get('lineItem') or r.get('name') or ""
            if "Cash and cash equivalents" in line_item:
                cash_record = r
                break

        if cash_record:
            value = cash_record.get('value') or cash_record.get('formatted_value')
            numeric = cash_record.get('numeric_value') or cash_record.get('numericValue') or cash_record.get('amount')

            self.add_result(ValidationResult(
                test_name="Cash Value (Formatted)",
                passed=str(value) == self.EXPECTED_BALANCE_SHEET_2024["Cash and cash equivalents ($000s)"],
                expected=self.EXPECTED_BALANCE_SHEET_2024["Cash and cash equivalents ($000s)"],
                actual=value,
                message="Formatted cash value matches"
            ))

            # Check numeric value (allow small float tolerance)
            if numeric is not None:
                expected_numeric = self.EXPECTED_BALANCE_SHEET_2024["cash_numeric"]
                self.add_result(ValidationResult(
                    test_name="Cash Value (Numeric)",
                    passed=abs(float(numeric) - expected_numeric) < 1,
                    expected=expected_numeric,
                    actual=numeric,
                    message="Numeric cash value matches"
                ))
        else:
            self.add_result(ValidationResult(
                test_name="Cash Line Item",
                passed=False,
                expected="Cash and cash equivalents record",
                actual="Not found in response",
                message="Could not find cash line item"
            ))

    def validate_people_data(self):
        """Validate people data matches source."""
        print("\nValidating: People Data...")

        # Try different endpoint patterns
        data = None
        for endpoint in [
            f"/companies/{self.SAMPLE_DUNS}/people",
            f"/companies/{self.SAMPLE_DUNS}/personnel"
        ]:
            data, error = self.make_request(endpoint)
            if data:
                break

        if not data:
            # Try getting from company detail
            data, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
            if data:
                data = {"people": data.get('people', [])}

        if not data:
            self.add_result(ValidationResult(
                test_name="People Data Retrieval",
                passed=False,
                expected="People data",
                actual=f"Error: {error}",
                message="Could not retrieve people"
            ))
            return

        people = data.get('people') or data.get('data') or (data if isinstance(data, list) else [])

        # Check count
        self.add_result(ValidationResult(
            test_name="People Count",
            passed=len(people) == self.EXPECTED_PEOPLE_COUNT,
            expected=self.EXPECTED_PEOPLE_COUNT,
            actual=len(people),
            message=f"Found {len(people)} people"
        ))

        # Check specific people exist
        for expected_person in self.EXPECTED_PEOPLE:
            found = False
            for p in people:
                name = p.get('person_name') or p.get('name') or p.get('personName') or ""
                title = p.get('title') or ""
                if expected_person["name_contains"] in name:
                    found = True
                    self.add_result(ValidationResult(
                        test_name=f"Person: {expected_person['name_contains']}",
                        passed=expected_person["title"].lower() in title.lower(),
                        expected=expected_person["title"],
                        actual=title,
                        message=f"Title matches for {expected_person['name_contains']}"
                    ))
                    break

            if not found:
                self.add_result(ValidationResult(
                    test_name=f"Person: {expected_person['name_contains']}",
                    passed=False,
                    expected=f"Person containing '{expected_person['name_contains']}'",
                    actual="Not found",
                    message="Person not found in data"
                ))

    def validate_industry_data(self):
        """Validate industry data matches source."""
        print("\nValidating: Industry Data...")

        # Try different endpoint patterns
        data = None
        for endpoint in [
            f"/companies/{self.SAMPLE_DUNS}/industries",
            f"/companies/{self.SAMPLE_DUNS}/industry"
        ]:
            data, error = self.make_request(endpoint)
            if data:
                break

        if not data:
            # Try getting from company detail
            company_data, _ = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
            if company_data:
                data = {"industries": company_data.get('industries', [])}

        if not data:
            self.add_result(ValidationResult(
                test_name="Industry Data Retrieval",
                passed=False,
                expected="Industry data",
                actual=f"Error: {error}",
                message="Could not retrieve industries"
            ))
            return

        industries = data.get('industries') or data.get('data') or (data if isinstance(data, list) else [])

        # Check specific industries exist
        for expected_ind in self.EXPECTED_INDUSTRIES:
            found = False
            for ind in industries:
                code = str(ind.get('industry_code') or ind.get('code') or ind.get('industryCode') or "")
                desc = ind.get('industry_description') or ind.get('description') or ind.get('industryDescription') or ""

                if code == expected_ind["code"]:
                    found = True
                    self.add_result(ValidationResult(
                        test_name=f"Industry Code: {expected_ind['code']}",
                        passed=expected_ind["description_contains"] in desc,
                        expected=f"Description contains '{expected_ind['description_contains']}'",
                        actual=desc[:50] + "..." if len(desc) > 50 else desc,
                        message=f"Industry {expected_ind['code']} description matches"
                    ))
                    break

            if not found:
                self.add_result(ValidationResult(
                    test_name=f"Industry Code: {expected_ind['code']}",
                    passed=False,
                    expected=f"Industry with code {expected_ind['code']}",
                    actual="Not found",
                    message="Industry code not found"
                ))

    def print_summary(self):
        """Print validation summary."""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        print(f"\n{'='*60}")
        print("VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"\nPassed: {passed}/{total} ({100*passed/total:.1f}%)")

        if passed == total:
            print("\nAll data validation tests PASSED")
            print("API data matches source CSV files correctly.")
        else:
            print(f"\nFailed tests: {total - passed}")
            print("\nFailed validations:")
            for r in self.results:
                if not r.passed:
                    print(f"  - {r.test_name}")

        print(f"\n{'='*60}")

        return passed, total

    def export_results(self, filepath: str):
        """Export validation results to JSON."""
        results_data = {
            "api_url": self.base_url,
            "sample_duns": self.SAMPLE_DUNS,
            "passed": sum(1 for r in self.results if r.passed),
            "total": len(self.results),
            "validations": [
                {
                    "test_name": r.test_name,
                    "passed": r.passed,
                    "expected": str(r.expected),
                    "actual": str(r.actual),
                    "message": r.message
                }
                for r in self.results
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)

        print(f"\nResults exported to: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_data_validation.py <candidate_api_url>")
        print("Example: python test_data_validation.py https://candidate-api.railway.app")
        sys.exit(1)

    api_url = sys.argv[1]

    validator = DataValidator(api_url)
    validator.run_all_validations()

    # Export results
    if len(sys.argv) > 2:
        validator.export_results(sys.argv[2])


if __name__ == "__main__":
    main()
