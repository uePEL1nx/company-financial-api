# -*- coding: utf-8 -*-
"""
Candidate API Submission Evaluator

Single script to run complete evaluation of a candidate's API submission.
Combines functional tests and data validation into one unified score.

Usage:
    python evaluate_submission.py <candidate_api_url> [candidate_name]

Example:
    python evaluate_submission.py https://candidate-api.railway.app "John Smith"
"""

import sys
import json
import requests
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TestResult:
    name: str
    category: str
    passed: bool
    message: str
    points: float = 0.0
    max_points: float = 0.0
    response_time_ms: Optional[float] = None


@dataclass
class EvaluationReport:
    candidate_url: str
    candidate_name: str
    evaluation_date: str
    functional_score: float
    functional_max: float
    validation_passed: int
    validation_total: int
    final_score: float
    final_max: float
    grade: str
    recommendation: str
    category_scores: Dict[str, Dict[str, float]]
    test_results: List[Dict]
    validation_results: List[Dict]


# =============================================================================
# EVALUATOR CLASS
# =============================================================================

class SubmissionEvaluator:
    """Complete evaluation of candidate API submissions."""

    # Test configuration
    TIMEOUT = 30
    SAMPLE_DUNS = "740039581"
    EXPECTED_COMPANY_COUNT = 222

    # Known correct values from source CSV files
    EXPECTED_DATA = {
        "company": {
            "acn": "082169060",
            "telephone_number": "02 89087900",
            "company_type": "Publicly Unlisted",
            "address_contains": "BARANGAROO",
            "primary_sic_contains": "7389"
        },
        "balance_sheet_2024": {
            "cash_formatted": "$43,079",
            "cash_numeric": 43079.0
        },
        "people": {
            "count": 10,
            "expected": [
                {"name_contains": "Rutherglen", "title": "Director"},
                {"name_contains": "Anderson", "title": "Director and Company Secretary"},
                {"name_contains": "Tromeur", "title": "Director of Finance"},
            ]
        },
        "industries": [
            {"code": "7389", "description_contains": "Business Services"},
            {"code": "6719", "description_contains": "Holding Companies"},
        ]
    }

    def __init__(self, base_url: str, candidate_name: str = "Unknown"):
        self.base_url = base_url.rstrip('/')
        self.candidate_name = candidate_name
        self.functional_results: List[TestResult] = []
        self.validation_results: List[Dict] = []

    def make_request(self, endpoint: str, params: dict = None) -> tuple:
        """Make HTTP request and return (response, elapsed_ms, error)."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            return response, elapsed_ms, None
        except requests.exceptions.Timeout:
            return None, None, "Request timed out"
        except requests.exceptions.ConnectionError:
            return None, None, "Connection failed"
        except Exception as e:
            return None, None, str(e)

    def add_functional_result(self, result: TestResult):
        self.functional_results.append(result)

    def add_validation_result(self, name: str, passed: bool, expected: Any, actual: Any):
        self.validation_results.append({
            "name": name,
            "passed": passed,
            "expected": str(expected),
            "actual": str(actual)
        })

    # =========================================================================
    # FUNCTIONAL TESTS
    # =========================================================================

    def run_functional_tests(self):
        """Run all functional tests."""
        self._test_documentation()
        self._test_root_endpoints()
        self._test_company_endpoints()
        self._test_financial_endpoints()
        self._test_people_industries()
        self._test_filtering_pagination()
        self._test_error_handling()
        self._test_performance()

    def _test_documentation(self):
        """Test API documentation."""
        # Swagger UI
        response, elapsed, error = self.make_request("/docs")
        if response and response.status_code == 200:
            has_swagger = "swagger" in response.text.lower() or "openapi" in response.text.lower()
            self.add_functional_result(TestResult(
                name="Swagger UI (/docs)", category="Documentation",
                passed=has_swagger, message="Available" if has_swagger else "Page exists but no Swagger",
                points=5.0 if has_swagger else 2.0, max_points=5.0, response_time_ms=elapsed
            ))
        else:
            self.add_functional_result(TestResult(
                name="Swagger UI (/docs)", category="Documentation",
                passed=False, message=error or f"HTTP {response.status_code if response else 'No response'}",
                max_points=5.0
            ))

        # OpenAPI schema
        response, elapsed, error = self.make_request("/openapi.json")
        if response and response.status_code == 200:
            try:
                schema = response.json()
                valid = "paths" in schema and "info" in schema
                self.add_functional_result(TestResult(
                    name="OpenAPI Schema", category="Documentation",
                    passed=valid, message=f"Valid schema with {len(schema.get('paths', {}))} endpoints",
                    points=5.0 if valid else 2.0, max_points=5.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="OpenAPI Schema", category="Documentation",
                    passed=False, message="Invalid JSON", max_points=5.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="OpenAPI Schema", category="Documentation",
                passed=False, message=error or "Not available", max_points=5.0
            ))

    def _test_root_endpoints(self):
        """Test root endpoints."""
        # Root
        response, elapsed, error = self.make_request("/")
        if response and response.status_code == 200:
            try:
                response.json()
                self.add_functional_result(TestResult(
                    name="Root Endpoint (/)", category="Root Endpoints",
                    passed=True, message="Returns valid JSON",
                    points=3.0, max_points=3.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="Root Endpoint (/)", category="Root Endpoints",
                    passed=False, message="Does not return JSON", max_points=3.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="Root Endpoint (/)", category="Root Endpoints",
                passed=False, message=error or "Not available", max_points=3.0
            ))

        # Health
        response, elapsed, error = self.make_request("/health")
        passed = response and response.status_code == 200
        self.add_functional_result(TestResult(
            name="Health Endpoint", category="Root Endpoints",
            passed=passed, message="Available" if passed else "Not available (optional)",
            points=2.0 if passed else 0.0, max_points=2.0, response_time_ms=elapsed
        ))

    def _test_company_endpoints(self):
        """Test company endpoints."""
        # List companies
        response, elapsed, error = self.make_request("/companies")
        if response and response.status_code == 200:
            try:
                data = response.json()
                companies = data.get('companies') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])
                total = data.get('total') or len(companies)
                correct = abs(total - self.EXPECTED_COMPANY_COUNT) <= 5
                self.add_functional_result(TestResult(
                    name="List Companies", category="Company Endpoints",
                    passed=True, message=f"Returns {total} companies",
                    points=5.0 if correct else 3.0, max_points=5.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="List Companies", category="Company Endpoints",
                    passed=False, message="Invalid response", max_points=5.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="List Companies", category="Company Endpoints",
                passed=False, message=error or "Not available", max_points=5.0
            ))

        # Single company
        response, elapsed, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if response and response.status_code == 200:
            try:
                data = response.json()
                has_id = 'duns' in data or 'id' in data
                self.add_functional_result(TestResult(
                    name="Get Single Company", category="Company Endpoints",
                    passed=has_id, message="Returns company details",
                    points=5.0 if has_id else 2.0, max_points=5.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="Get Single Company", category="Company Endpoints",
                    passed=False, message="Invalid response", max_points=5.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="Get Single Company", category="Company Endpoints",
                passed=False, message=error or "Not available", max_points=5.0
            ))

        # Company people
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/people", f"/companies/{self.SAMPLE_DUNS}/personnel"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    people = data.get('people') or data.get('data') or (data if isinstance(data, list) else [])
                    self.add_functional_result(TestResult(
                        name="Company People", category="Company Endpoints",
                        passed=len(people) > 0, message=f"Returns {len(people)} people",
                        points=4.0, max_points=4.0, response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.add_functional_result(TestResult(
                name="Company People", category="Company Endpoints",
                passed=False, message="Not available", max_points=4.0
            ))

        # Company industries
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/industries", f"/companies/{self.SAMPLE_DUNS}/industry"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    industries = data.get('industries') or data.get('data') or (data if isinstance(data, list) else [])
                    self.add_functional_result(TestResult(
                        name="Company Industries", category="Company Endpoints",
                        passed=len(industries) > 0, message=f"Returns {len(industries)} industries",
                        points=4.0, max_points=4.0, response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.add_functional_result(TestResult(
                name="Company Industries", category="Company Endpoints",
                passed=False, message="Not available", max_points=4.0
            ))

    def _test_financial_endpoints(self):
        """Test financial endpoints."""
        financial_tests = [
            ("Balance Sheet", [f"/companies/{self.SAMPLE_DUNS}/balance-sheet", f"/companies/{self.SAMPLE_DUNS}/balance_sheet"]),
            ("Cash Flow", [f"/companies/{self.SAMPLE_DUNS}/cash-flow", f"/companies/{self.SAMPLE_DUNS}/cash_flow"]),
            ("Income Statement", [f"/companies/{self.SAMPLE_DUNS}/income-statement", f"/companies/{self.SAMPLE_DUNS}/income_statement"])
        ]

        for name, endpoints in financial_tests:
            found = False
            for endpoint in endpoints:
                response, elapsed, error = self.make_request(endpoint)
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        records = data.get('records') or data.get('data') or (data if isinstance(data, list) else [])
                        self.add_functional_result(TestResult(
                            name=name, category="Financial Endpoints",
                            passed=len(records) > 0, message=f"Returns {len(records)} records",
                            points=5.0, max_points=5.0, response_time_ms=elapsed
                        ))
                        found = True
                        break
                    except:
                        pass
            if not found:
                self.add_functional_result(TestResult(
                    name=name, category="Financial Endpoints",
                    passed=False, message="Not available", max_points=5.0
                ))

        # Aggregate endpoints (bonus)
        for name, endpoints in [
            ("Aggregate Balance Sheets", ["/balance-sheets", "/balance_sheets"]),
            ("Aggregate Cash Flows", ["/cash-flows", "/cash_flows"]),
            ("Aggregate Income Statements", ["/income-statements", "/income_statements"])
        ]:
            for endpoint in endpoints:
                response, elapsed, error = self.make_request(endpoint, {"limit": 10})
                if response and response.status_code == 200:
                    self.add_functional_result(TestResult(
                        name=name, category="Financial Endpoints",
                        passed=True, message="Available",
                        points=2.0, max_points=2.0, response_time_ms=elapsed
                    ))
                    break
            else:
                self.add_functional_result(TestResult(
                    name=name, category="Financial Endpoints",
                    passed=False, message="Not available (bonus)", max_points=2.0
                ))

    def _test_people_industries(self):
        """Test people and industries list endpoints."""
        # People
        for endpoint in ["/people", "/personnel"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                self.add_functional_result(TestResult(
                    name="List People", category="People & Industries",
                    passed=True, message="Available",
                    points=4.0, max_points=4.0, response_time_ms=elapsed
                ))
                break
        else:
            self.add_functional_result(TestResult(
                name="List People", category="People & Industries",
                passed=False, message="Not available", max_points=4.0
            ))

        # Industries
        for endpoint in ["/industries", "/industry"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                self.add_functional_result(TestResult(
                    name="List Industries", category="People & Industries",
                    passed=True, message="Available",
                    points=4.0, max_points=4.0, response_time_ms=elapsed
                ))
                break
        else:
            self.add_functional_result(TestResult(
                name="List Industries", category="People & Industries",
                passed=False, message="Not available", max_points=4.0
            ))

    def _test_filtering_pagination(self):
        """Test filtering and pagination."""
        # Pagination
        response, elapsed, error = self.make_request("/companies", {"page": 1, "page_size": 5})
        if response and response.status_code == 200:
            try:
                data = response.json()
                companies = data.get('companies') or data.get('data') or (data if isinstance(data, list) else [])
                paginated = len(companies) <= 10
                self.add_functional_result(TestResult(
                    name="Pagination", category="Filtering & Pagination",
                    passed=paginated, message=f"Returns {len(companies)} items with page_size=5",
                    points=4.0 if paginated else 2.0, max_points=4.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="Pagination", category="Filtering & Pagination",
                    passed=False, message="Invalid response", max_points=4.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="Pagination", category="Filtering & Pagination",
                passed=False, message="Not working", max_points=4.0
            ))

        # Year filter
        response, elapsed, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}/balance-sheet", {"year": 2024})
        if response and response.status_code == 200:
            try:
                data = response.json()
                records = data.get('records') or data.get('data') or (data if isinstance(data, list) else [])
                years = set(r.get('year') for r in records[:20] if isinstance(r, dict) and 'year' in r)
                filtered = years == {2024} or len(years) == 0
                self.add_functional_result(TestResult(
                    name="Year Filtering", category="Filtering & Pagination",
                    passed=filtered, message="Working" if filtered else f"Found years: {years}",
                    points=4.0 if filtered else 2.0, max_points=4.0, response_time_ms=elapsed
                ))
            except:
                self.add_functional_result(TestResult(
                    name="Year Filtering", category="Filtering & Pagination",
                    passed=False, message="Invalid response", max_points=4.0
                ))
        else:
            self.add_functional_result(TestResult(
                name="Year Filtering", category="Filtering & Pagination",
                passed=False, message="Not supported", max_points=4.0
            ))

    def _test_error_handling(self):
        """Test error handling."""
        # Invalid company
        response, elapsed, error = self.make_request("/companies/INVALID_DUNS_12345")
        if error:
            self.add_functional_result(TestResult(
                name="404 Invalid Company", category="Error Handling",
                passed=False, message=f"Error: {error}", max_points=3.0
            ))
        elif response is not None:
            passed = response.status_code == 404
            self.add_functional_result(TestResult(
                name="404 Invalid Company", category="Error Handling",
                passed=passed,
                message=f"Returns {response.status_code}" + (" (correct)" if passed else " (should be 404)"),
                points=3.0 if passed else 0.0, max_points=3.0, response_time_ms=elapsed
            ))
        else:
            self.add_functional_result(TestResult(
                name="404 Invalid Company", category="Error Handling",
                passed=False, message="No response", max_points=3.0
            ))

        # Invalid endpoint
        response, elapsed, error = self.make_request("/invalid_endpoint_xyz")
        if error:
            self.add_functional_result(TestResult(
                name="404 Invalid Endpoint", category="Error Handling",
                passed=False, message=f"Error: {error}", max_points=2.0
            ))
        elif response is not None:
            passed = response.status_code == 404
            self.add_functional_result(TestResult(
                name="404 Invalid Endpoint", category="Error Handling",
                passed=passed,
                message=f"Returns {response.status_code}" + (" (correct)" if passed else ""),
                points=2.0 if passed else 0.0, max_points=2.0, response_time_ms=elapsed
            ))
        else:
            self.add_functional_result(TestResult(
                name="404 Invalid Endpoint", category="Error Handling",
                passed=False, message="No response", max_points=2.0
            ))

    def _test_performance(self):
        """Test performance."""
        # List companies
        response, elapsed, error = self.make_request("/companies", {"page_size": 50})
        if elapsed:
            if elapsed < 1000:
                points, msg = 5.0, f"Excellent: {elapsed:.0f}ms"
            elif elapsed < 3000:
                points, msg = 3.0, f"Acceptable: {elapsed:.0f}ms"
            else:
                points, msg = 1.0, f"Slow: {elapsed:.0f}ms"
            self.add_functional_result(TestResult(
                name="List Response Time", category="Performance",
                passed=elapsed < 3000, message=msg,
                points=points, max_points=5.0, response_time_ms=elapsed
            ))

        # Single company
        response, elapsed, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if elapsed:
            if elapsed < 500:
                points, msg = 5.0, f"Excellent: {elapsed:.0f}ms"
            elif elapsed < 2000:
                points, msg = 3.0, f"Acceptable: {elapsed:.0f}ms"
            else:
                points, msg = 1.0, f"Slow: {elapsed:.0f}ms"
            self.add_functional_result(TestResult(
                name="Detail Response Time", category="Performance",
                passed=elapsed < 2000, message=msg,
                points=points, max_points=5.0, response_time_ms=elapsed
            ))

    # =========================================================================
    # DATA VALIDATION
    # =========================================================================

    def run_data_validation(self):
        """Run all data validation tests."""
        self._validate_company_count()
        self._validate_company_info()
        self._validate_balance_sheet()
        self._validate_people()
        self._validate_industries()

    def _validate_company_count(self):
        """Validate company count."""
        response, _, _ = self.make_request("/companies")
        if response and response.status_code == 200:
            data = response.json()
            total = data.get('total') or len(data.get('companies', data.get('data', [])))
            self.add_validation_result(
                "Company Count",
                abs(total - self.EXPECTED_COMPANY_COUNT) <= 2,
                self.EXPECTED_COMPANY_COUNT,
                total
            )
        else:
            self.add_validation_result("Company Count", False, self.EXPECTED_COMPANY_COUNT, "Error")

    def _validate_company_info(self):
        """Validate company info fields."""
        response, _, _ = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if not response or response.status_code != 200:
            for field in ["ACN", "Phone", "Type", "Address", "SIC"]:
                self.add_validation_result(f"Company {field}", False, "Expected value", "Could not retrieve")
            return

        data = response.json()
        exp = self.EXPECTED_DATA["company"]

        # ACN
        acn = data.get('acn') or data.get('ACN') or ""
        self.add_validation_result("Company ACN", str(acn) == exp["acn"], exp["acn"], acn)

        # Phone
        phone = data.get('telephone_number') or data.get('phone') or ""
        self.add_validation_result("Company Phone", str(phone) == exp["telephone_number"], exp["telephone_number"], phone)

        # Type
        ctype = data.get('company_type') or data.get('type') or ""
        self.add_validation_result("Company Type", ctype == exp["company_type"], exp["company_type"], ctype)

        # Address
        addr = data.get('physical_address') or data.get('address') or ""
        self.add_validation_result("Company Address", exp["address_contains"] in str(addr).upper(), f"Contains '{exp['address_contains']}'", addr[:50])

        # SIC
        sic = data.get('primary_sic') or data.get('sic') or ""
        self.add_validation_result("Primary SIC", exp["primary_sic_contains"] in str(sic), f"Contains '{exp['primary_sic_contains']}'", sic[:50])

    def _validate_balance_sheet(self):
        """Validate balance sheet data."""
        data = None
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/balance-sheet", f"/companies/{self.SAMPLE_DUNS}/balance_sheet"]:
            response, _, _ = self.make_request(endpoint, {"year": 2024})
            if response and response.status_code == 200:
                data = response.json()
                break

        if not data:
            self.add_validation_result("Cash Value (Formatted)", False, "$43,079", "Could not retrieve")
            self.add_validation_result("Cash Value (Numeric)", False, "43079.0", "Could not retrieve")
            return

        records = data.get('records') or data.get('data') or (data if isinstance(data, list) else [])
        exp = self.EXPECTED_DATA["balance_sheet_2024"]

        cash_record = None
        for r in records:
            if "Cash and cash equivalents" in (r.get('line_item') or r.get('name') or ""):
                cash_record = r
                break

        if cash_record:
            value = cash_record.get('value') or ""
            numeric = cash_record.get('numeric_value')
            self.add_validation_result("Cash Value (Formatted)", str(value) == exp["cash_formatted"], exp["cash_formatted"], value)
            if numeric is not None:
                self.add_validation_result("Cash Value (Numeric)", abs(float(numeric) - exp["cash_numeric"]) < 1, exp["cash_numeric"], numeric)
            else:
                self.add_validation_result("Cash Value (Numeric)", False, exp["cash_numeric"], "Not provided")
        else:
            self.add_validation_result("Cash Value (Formatted)", False, exp["cash_formatted"], "Not found")
            self.add_validation_result("Cash Value (Numeric)", False, exp["cash_numeric"], "Not found")

    def _validate_people(self):
        """Validate people data."""
        data = None
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/people", f"/companies/{self.SAMPLE_DUNS}"]:
            response, _, _ = self.make_request(endpoint)
            if response and response.status_code == 200:
                data = response.json()
                if 'people' in data or isinstance(data.get('data'), list):
                    break

        if not data:
            self.add_validation_result("People Count", False, 10, "Could not retrieve")
            return

        people = data.get('people') or data.get('data') or (data if isinstance(data, list) else [])
        exp = self.EXPECTED_DATA["people"]

        self.add_validation_result("People Count", len(people) == exp["count"], exp["count"], len(people))

        for expected in exp["expected"]:
            found = False
            for p in people:
                name = p.get('person_name') or p.get('name') or ""
                title = p.get('title') or ""
                if expected["name_contains"] in name:
                    found = expected["title"].lower() in title.lower()
                    self.add_validation_result(
                        f"Person: {expected['name_contains']}",
                        found,
                        expected["title"],
                        title
                    )
                    break
            if not found:
                self.add_validation_result(f"Person: {expected['name_contains']}", False, expected["title"], "Not found")

    def _validate_industries(self):
        """Validate industry data."""
        data = None
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/industries", f"/companies/{self.SAMPLE_DUNS}"]:
            response, _, _ = self.make_request(endpoint)
            if response and response.status_code == 200:
                data = response.json()
                if 'industries' in data or isinstance(data.get('data'), list):
                    break

        if not data:
            for exp in self.EXPECTED_DATA["industries"]:
                self.add_validation_result(f"Industry: {exp['code']}", False, exp["description_contains"], "Could not retrieve")
            return

        industries = data.get('industries') or data.get('data') or (data if isinstance(data, list) else [])

        for expected in self.EXPECTED_DATA["industries"]:
            found = False
            for ind in industries:
                code = str(ind.get('industry_code') or ind.get('code') or "")
                desc = ind.get('industry_description') or ind.get('description') or ""
                if code == expected["code"]:
                    found = expected["description_contains"] in desc
                    self.add_validation_result(
                        f"Industry: {expected['code']}",
                        found,
                        f"Contains '{expected['description_contains']}'",
                        desc[:40]
                    )
                    break
            if not found:
                self.add_validation_result(f"Industry: {expected['code']}", False, expected["description_contains"], "Not found")

    # =========================================================================
    # EVALUATION & REPORTING
    # =========================================================================

    def evaluate(self) -> EvaluationReport:
        """Run full evaluation and generate report."""
        print(f"\n{'='*70}")
        print("CANDIDATE API EVALUATION")
        print(f"{'='*70}")
        print(f"Candidate: {self.candidate_name}")
        print(f"API URL: {self.base_url}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        # Run tests
        print("Running Functional Tests...")
        print("-" * 40)
        self.run_functional_tests()

        print("\nRunning Data Validation...")
        print("-" * 40)
        self.run_data_validation()

        # Calculate scores
        functional_score = sum(r.points for r in self.functional_results)
        functional_max = sum(r.max_points for r in self.functional_results)
        validation_passed = sum(1 for r in self.validation_results if r["passed"])
        validation_total = len(self.validation_results)

        # Combined score: Functional (85%) + Data Validation (15%)
        functional_pct = (functional_score / functional_max * 100) if functional_max > 0 else 0
        validation_pct = (validation_passed / validation_total * 100) if validation_total > 0 else 0
        final_score = (functional_pct * 0.85) + (validation_pct * 0.15)

        # Grade
        if final_score >= 90:
            grade = "A - Excellent"
            recommendation = "Strong Hire"
        elif final_score >= 80:
            grade = "B - Good"
            recommendation = "Hire"
        elif final_score >= 70:
            grade = "C - Satisfactory"
            recommendation = "Maybe"
        elif final_score >= 60:
            grade = "D - Needs Improvement"
            recommendation = "Likely No"
        else:
            grade = "F - Unsatisfactory"
            recommendation = "No Hire"

        # Category scores
        categories = {}
        for r in self.functional_results:
            if r.category not in categories:
                categories[r.category] = {"points": 0.0, "max": 0.0}
            categories[r.category]["points"] += r.points
            categories[r.category]["max"] += r.max_points

        # Create report
        report = EvaluationReport(
            candidate_url=self.base_url,
            candidate_name=self.candidate_name,
            evaluation_date=datetime.now().isoformat(),
            functional_score=functional_score,
            functional_max=functional_max,
            validation_passed=validation_passed,
            validation_total=validation_total,
            final_score=final_score,
            final_max=100.0,
            grade=grade,
            recommendation=recommendation,
            category_scores=categories,
            test_results=[{
                "name": r.name, "category": r.category, "passed": r.passed,
                "message": r.message, "points": r.points, "max_points": r.max_points
            } for r in self.functional_results],
            validation_results=self.validation_results
        )

        self._print_report(report)
        return report

    def _print_report(self, report: EvaluationReport):
        """Print formatted report."""
        print(f"\n{'='*70}")
        print("EVALUATION RESULTS")
        print(f"{'='*70}\n")

        # Functional tests by category
        print("FUNCTIONAL TESTS")
        print("-" * 50)
        for category, scores in report.category_scores.items():
            pct = (scores["points"] / scores["max"] * 100) if scores["max"] > 0 else 0
            print(f"  {category}: {scores['points']:.1f}/{scores['max']:.1f} ({pct:.0f}%)")

        print(f"\n  FUNCTIONAL TOTAL: {report.functional_score:.1f}/{report.functional_max:.1f} ({report.functional_score/report.functional_max*100:.1f}%)")

        # Data validation
        print(f"\nDATA VALIDATION")
        print("-" * 50)
        for v in report.validation_results:
            status = "PASS" if v["passed"] else "FAIL"
            print(f"  [{status}] {v['name']}")
            if not v["passed"]:
                print(f"        Expected: {v['expected']}")
                print(f"        Actual: {v['actual']}")

        print(f"\n  VALIDATION TOTAL: {report.validation_passed}/{report.validation_total} ({report.validation_passed/report.validation_total*100:.1f}%)")

        # Final score
        print(f"\n{'='*70}")
        print("FINAL SCORE")
        print(f"{'='*70}")
        print(f"""
  Functional Tests (85%):  {report.functional_score:.1f}/{report.functional_max:.1f}
  Data Validation (15%):   {report.validation_passed}/{report.validation_total}

  COMBINED SCORE: {report.final_score:.1f}/100

  GRADE: {report.grade}
  RECOMMENDATION: {report.recommendation}
""")
        print(f"{'='*70}\n")

    def export_report(self, report: EvaluationReport, filepath: str):
        """Export report to JSON."""
        data = {
            "candidate_name": report.candidate_name,
            "candidate_url": report.candidate_url,
            "evaluation_date": report.evaluation_date,
            "scores": {
                "functional": {"score": report.functional_score, "max": report.functional_max},
                "validation": {"passed": report.validation_passed, "total": report.validation_total},
                "final": {"score": report.final_score, "max": 100}
            },
            "grade": report.grade,
            "recommendation": report.recommendation,
            "category_breakdown": report.category_scores,
            "functional_tests": report.test_results,
            "data_validations": report.validation_results
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Report exported to: {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("CANDIDATE API SUBMISSION EVALUATOR")
        print("=" * 60)
        print("\nUsage:")
        print("  python evaluate_submission.py <api_url> [candidate_name]")
        print("\nExamples:")
        print('  python evaluate_submission.py https://api.railway.app "John Smith"')
        print("  python evaluate_submission.py https://api.railway.app")
        print("\nThe script will:")
        print("  1. Run functional tests (85 points)")
        print("  2. Validate data accuracy (14 checks)")
        print("  3. Generate combined score and grade")
        print("  4. Export results to JSON file")
        sys.exit(1)

    api_url = sys.argv[1]
    candidate_name = sys.argv[2] if len(sys.argv) > 2 else "Unknown Candidate"

    evaluator = SubmissionEvaluator(api_url, candidate_name)
    report = evaluator.evaluate()

    # Export report
    safe_name = candidate_name.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"evaluation_{safe_name}_{timestamp}.json"
    evaluator.export_report(report, filepath)


if __name__ == "__main__":
    main()
