# -*- coding: utf-8 -*-
"""
Candidate API Submission Tester

This script tests a candidate's API submission against expected functionality.
Run with: python test_submission.py <candidate_api_url>

Example: python test_submission.py https://candidate-api.railway.app
"""

import sys
import json
import requests
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class TestResult:
    name: str
    category: str
    passed: bool
    message: str
    points: float = 0.0
    max_points: float = 0.0
    response_time_ms: Optional[float] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class TestSuite:
    candidate_url: str
    results: List[TestResult] = field(default_factory=list)

    def add_result(self, result: TestResult):
        self.results.append(result)

    def get_score(self) -> tuple:
        total_points = sum(r.points for r in self.results)
        max_points = sum(r.max_points for r in self.results)
        return total_points, max_points

    def get_category_scores(self) -> Dict[str, tuple]:
        categories = {}
        for r in self.results:
            if r.category not in categories:
                categories[r.category] = [0.0, 0.0]
            categories[r.category][0] += r.points
            categories[r.category][1] += r.max_points
        return {k: tuple(v) for k, v in categories.items()}


class APITester:
    """Tests candidate API submissions."""

    # Reference data for validation
    EXPECTED_COMPANY_COUNT = 222
    EXPECTED_YEARS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    SAMPLE_DUNS = "740039581"
    SAMPLE_DUNS_ACN = "082169060"

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.suite = TestSuite(candidate_url=base_url)

    def make_request(self, endpoint: str, params: dict = None) -> tuple:
        """Make HTTP request and return (response, elapsed_ms, error)."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            return response, elapsed_ms, None
        except requests.exceptions.Timeout:
            return None, None, "Request timed out"
        except requests.exceptions.ConnectionError:
            return None, None, "Connection failed"
        except Exception as e:
            return None, None, str(e)

    def run_all_tests(self):
        """Run all test categories."""
        print(f"\n{'='*60}")
        print(f"API SUBMISSION TESTER")
        print(f"{'='*60}")
        print(f"Candidate URL: {self.base_url}")
        print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # Run test categories
        self.test_documentation()
        self.test_root_endpoints()
        self.test_company_endpoints()
        self.test_financial_endpoints()
        self.test_people_endpoints()
        self.test_industry_endpoints()
        self.test_filtering_pagination()
        self.test_error_handling()
        self.test_performance()

        # Print results
        self.print_results()

    # ==================== DOCUMENTATION TESTS ====================

    def test_documentation(self):
        """Test API documentation availability."""
        print("Testing: Documentation...")

        # Test /docs endpoint (Swagger UI)
        response, elapsed, error = self.make_request("/docs")
        if error:
            self.suite.add_result(TestResult(
                name="Swagger UI (/docs)",
                category="Documentation",
                passed=False,
                message=f"Failed: {error}",
                max_points=5.0
            ))
        elif response.status_code == 200:
            has_swagger = "swagger" in response.text.lower() or "openapi" in response.text.lower()
            self.suite.add_result(TestResult(
                name="Swagger UI (/docs)",
                category="Documentation",
                passed=has_swagger,
                message="Swagger UI available" if has_swagger else "Page exists but no Swagger detected",
                points=5.0 if has_swagger else 2.0,
                max_points=5.0,
                response_time_ms=elapsed
            ))
        else:
            self.suite.add_result(TestResult(
                name="Swagger UI (/docs)",
                category="Documentation",
                passed=False,
                message=f"HTTP {response.status_code}",
                max_points=5.0
            ))

        # Test /openapi.json endpoint
        response, elapsed, error = self.make_request("/openapi.json")
        if error:
            self.suite.add_result(TestResult(
                name="OpenAPI Schema (/openapi.json)",
                category="Documentation",
                passed=False,
                message=f"Failed: {error}",
                max_points=5.0
            ))
        elif response.status_code == 200:
            try:
                schema = response.json()
                has_paths = "paths" in schema
                has_info = "info" in schema
                self.suite.add_result(TestResult(
                    name="OpenAPI Schema (/openapi.json)",
                    category="Documentation",
                    passed=has_paths and has_info,
                    message=f"Valid OpenAPI schema with {len(schema.get('paths', {}))} endpoints",
                    points=5.0 if (has_paths and has_info) else 2.0,
                    max_points=5.0,
                    response_time_ms=elapsed,
                    details={"endpoint_count": len(schema.get('paths', {}))}
                ))
            except json.JSONDecodeError:
                self.suite.add_result(TestResult(
                    name="OpenAPI Schema (/openapi.json)",
                    category="Documentation",
                    passed=False,
                    message="Invalid JSON response",
                    max_points=5.0
                ))
        else:
            self.suite.add_result(TestResult(
                name="OpenAPI Schema (/openapi.json)",
                category="Documentation",
                passed=False,
                message=f"HTTP {response.status_code}",
                max_points=5.0
            ))

    # ==================== ROOT ENDPOINT TESTS ====================

    def test_root_endpoints(self):
        """Test root and utility endpoints."""
        print("Testing: Root Endpoints...")

        # Test root endpoint
        response, elapsed, error = self.make_request("/")
        if error:
            self.suite.add_result(TestResult(
                name="Root Endpoint (/)",
                category="Root Endpoints",
                passed=False,
                message=f"Failed: {error}",
                max_points=3.0
            ))
        elif response.status_code == 200:
            try:
                data = response.json()
                self.suite.add_result(TestResult(
                    name="Root Endpoint (/)",
                    category="Root Endpoints",
                    passed=True,
                    message="Returns valid JSON",
                    points=3.0,
                    max_points=3.0,
                    response_time_ms=elapsed
                ))
            except json.JSONDecodeError:
                self.suite.add_result(TestResult(
                    name="Root Endpoint (/)",
                    category="Root Endpoints",
                    passed=False,
                    message="Does not return valid JSON",
                    max_points=3.0
                ))
        else:
            self.suite.add_result(TestResult(
                name="Root Endpoint (/)",
                category="Root Endpoints",
                passed=False,
                message=f"HTTP {response.status_code}",
                max_points=3.0
            ))

        # Test health endpoint (optional but good practice)
        response, elapsed, error = self.make_request("/health")
        if response and response.status_code == 200:
            self.suite.add_result(TestResult(
                name="Health Endpoint (/health)",
                category="Root Endpoints",
                passed=True,
                message="Health check available",
                points=2.0,
                max_points=2.0,
                response_time_ms=elapsed
            ))
        else:
            self.suite.add_result(TestResult(
                name="Health Endpoint (/health)",
                category="Root Endpoints",
                passed=False,
                message="Health endpoint not available (optional)",
                points=0.0,
                max_points=2.0
            ))

    # ==================== COMPANY ENDPOINT TESTS ====================

    def test_company_endpoints(self):
        """Test company-related endpoints."""
        print("Testing: Company Endpoints...")

        # Test list companies
        response, elapsed, error = self.make_request("/companies")
        if error:
            self.suite.add_result(TestResult(
                name="List Companies (GET /companies)",
                category="Company Endpoints",
                passed=False,
                message=f"Failed: {error}",
                max_points=5.0
            ))
        elif response.status_code == 200:
            try:
                data = response.json()
                # Check for company data (could be in 'companies', 'data', 'results', or root list)
                companies = data.get('companies') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])
                total = data.get('total') or len(companies)

                correct_count = abs(total - self.EXPECTED_COMPANY_COUNT) <= 5  # Allow small variance

                self.suite.add_result(TestResult(
                    name="List Companies (GET /companies)",
                    category="Company Endpoints",
                    passed=True,
                    message=f"Returns {total} companies (expected ~{self.EXPECTED_COMPANY_COUNT})",
                    points=5.0 if correct_count else 3.0,
                    max_points=5.0,
                    response_time_ms=elapsed,
                    details={"total_companies": total}
                ))
            except (json.JSONDecodeError, TypeError):
                self.suite.add_result(TestResult(
                    name="List Companies (GET /companies)",
                    category="Company Endpoints",
                    passed=False,
                    message="Invalid JSON response",
                    max_points=5.0
                ))
        else:
            self.suite.add_result(TestResult(
                name="List Companies (GET /companies)",
                category="Company Endpoints",
                passed=False,
                message=f"HTTP {response.status_code}",
                max_points=5.0
            ))

        # Test get single company
        response, elapsed, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if error:
            self.suite.add_result(TestResult(
                name=f"Get Company (GET /companies/{self.SAMPLE_DUNS})",
                category="Company Endpoints",
                passed=False,
                message=f"Failed: {error}",
                max_points=5.0
            ))
        elif response.status_code == 200:
            try:
                data = response.json()
                has_duns = 'duns' in data or 'DUNS' in data or 'id' in data
                has_address = any(k in data for k in ['physical_address', 'address', 'physicalAddress'])

                self.suite.add_result(TestResult(
                    name=f"Get Company (GET /companies/{self.SAMPLE_DUNS})",
                    category="Company Endpoints",
                    passed=has_duns,
                    message="Returns company details" if has_duns else "Missing company identifier",
                    points=5.0 if has_duns else 2.0,
                    max_points=5.0,
                    response_time_ms=elapsed,
                    details={"fields_returned": list(data.keys())[:10]}
                ))
            except json.JSONDecodeError:
                self.suite.add_result(TestResult(
                    name=f"Get Company (GET /companies/{self.SAMPLE_DUNS})",
                    category="Company Endpoints",
                    passed=False,
                    message="Invalid JSON response",
                    max_points=5.0
                ))
        elif response.status_code == 404:
            self.suite.add_result(TestResult(
                name=f"Get Company (GET /companies/{self.SAMPLE_DUNS})",
                category="Company Endpoints",
                passed=False,
                message="Company not found - data may not be imported correctly",
                max_points=5.0
            ))
        else:
            self.suite.add_result(TestResult(
                name=f"Get Company (GET /companies/{self.SAMPLE_DUNS})",
                category="Company Endpoints",
                passed=False,
                message=f"HTTP {response.status_code}",
                max_points=5.0
            ))

        # Test company people endpoint
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/people", f"/companies/{self.SAMPLE_DUNS}/personnel"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    people = data.get('people') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])
                    has_people = len(people) > 0
                    self.suite.add_result(TestResult(
                        name="Company People Endpoint",
                        category="Company Endpoints",
                        passed=has_people,
                        message=f"Returns {len(people)} people records",
                        points=4.0 if has_people else 2.0,
                        max_points=4.0,
                        response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.suite.add_result(TestResult(
                name="Company People Endpoint",
                category="Company Endpoints",
                passed=False,
                message="People endpoint not found or not working",
                max_points=4.0
            ))

        # Test company industries endpoint
        for endpoint in [f"/companies/{self.SAMPLE_DUNS}/industries", f"/companies/{self.SAMPLE_DUNS}/industry"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    industries = data.get('industries') or data.get('data') or (data if isinstance(data, list) else [])
                    has_industries = len(industries) > 0
                    self.suite.add_result(TestResult(
                        name="Company Industries Endpoint",
                        category="Company Endpoints",
                        passed=has_industries,
                        message=f"Returns {len(industries)} industry records",
                        points=4.0 if has_industries else 2.0,
                        max_points=4.0,
                        response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.suite.add_result(TestResult(
                name="Company Industries Endpoint",
                category="Company Endpoints",
                passed=False,
                message="Industries endpoint not found or not working",
                max_points=4.0
            ))

    # ==================== FINANCIAL ENDPOINT TESTS ====================

    def test_financial_endpoints(self):
        """Test financial data endpoints."""
        print("Testing: Financial Endpoints...")

        financial_tests = [
            ("Balance Sheet", [
                f"/companies/{self.SAMPLE_DUNS}/balance-sheet",
                f"/companies/{self.SAMPLE_DUNS}/balance_sheet",
                f"/companies/{self.SAMPLE_DUNS}/balancesheet"
            ]),
            ("Cash Flow", [
                f"/companies/{self.SAMPLE_DUNS}/cash-flow",
                f"/companies/{self.SAMPLE_DUNS}/cash_flow",
                f"/companies/{self.SAMPLE_DUNS}/cashflow"
            ]),
            ("Income Statement", [
                f"/companies/{self.SAMPLE_DUNS}/income-statement",
                f"/companies/{self.SAMPLE_DUNS}/income_statement",
                f"/companies/{self.SAMPLE_DUNS}/incomestatement"
            ])
        ]

        for name, endpoints in financial_tests:
            found = False
            for endpoint in endpoints:
                response, elapsed, error = self.make_request(endpoint)
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        records = data.get('records') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])
                        has_records = len(records) > 0

                        # Check for year field
                        has_year = any('year' in str(r).lower() for r in records[:5]) if records else False

                        self.suite.add_result(TestResult(
                            name=f"Company {name}",
                            category="Financial Endpoints",
                            passed=has_records,
                            message=f"Returns {len(records)} records",
                            points=5.0 if has_records else 2.0,
                            max_points=5.0,
                            response_time_ms=elapsed,
                            details={"record_count": len(records), "has_year_field": has_year}
                        ))
                        found = True
                        break
                    except:
                        pass

            if not found:
                self.suite.add_result(TestResult(
                    name=f"Company {name}",
                    category="Financial Endpoints",
                    passed=False,
                    message=f"{name} endpoint not found or not working",
                    max_points=5.0
                ))

        # Test aggregate financial endpoints (bonus)
        for name, endpoints in [
            ("Balance Sheets List", ["/balance-sheets", "/balance_sheets", "/balancesheets"]),
            ("Cash Flows List", ["/cash-flows", "/cash_flows", "/cashflows"]),
            ("Income Statements List", ["/income-statements", "/income_statements", "/incomestatements"])
        ]:
            for endpoint in endpoints:
                response, elapsed, error = self.make_request(endpoint, {"limit": 10})
                if response and response.status_code == 200:
                    self.suite.add_result(TestResult(
                        name=f"Aggregate {name}",
                        category="Financial Endpoints",
                        passed=True,
                        message="Aggregate endpoint available",
                        points=2.0,
                        max_points=2.0,
                        response_time_ms=elapsed
                    ))
                    break
            else:
                self.suite.add_result(TestResult(
                    name=f"Aggregate {name}",
                    category="Financial Endpoints",
                    passed=False,
                    message="Aggregate endpoint not available (bonus)",
                    points=0.0,
                    max_points=2.0
                ))

    # ==================== PEOPLE ENDPOINT TESTS ====================

    def test_people_endpoints(self):
        """Test people-related endpoints."""
        print("Testing: People Endpoints...")

        for endpoint in ["/people", "/personnel"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    people = data.get('people') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])

                    self.suite.add_result(TestResult(
                        name="List People (GET /people)",
                        category="People Endpoints",
                        passed=len(people) > 0,
                        message=f"Returns people records",
                        points=4.0 if len(people) > 0 else 0.0,
                        max_points=4.0,
                        response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.suite.add_result(TestResult(
                name="List People (GET /people)",
                category="People Endpoints",
                passed=False,
                message="People list endpoint not found",
                max_points=4.0
            ))

    # ==================== INDUSTRY ENDPOINT TESTS ====================

    def test_industry_endpoints(self):
        """Test industry-related endpoints."""
        print("Testing: Industry Endpoints...")

        for endpoint in ["/industries", "/industry"]:
            response, elapsed, error = self.make_request(endpoint)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    industries = data.get('industries') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])

                    self.suite.add_result(TestResult(
                        name="List Industries (GET /industries)",
                        category="Industry Endpoints",
                        passed=len(industries) > 0,
                        message=f"Returns industry records",
                        points=4.0 if len(industries) > 0 else 0.0,
                        max_points=4.0,
                        response_time_ms=elapsed
                    ))
                    break
                except:
                    pass
        else:
            self.suite.add_result(TestResult(
                name="List Industries (GET /industries)",
                category="Industry Endpoints",
                passed=False,
                message="Industries list endpoint not found",
                max_points=4.0
            ))

    # ==================== FILTERING & PAGINATION TESTS ====================

    def test_filtering_pagination(self):
        """Test filtering and pagination capabilities."""
        print("Testing: Filtering & Pagination...")

        # Test pagination
        response, elapsed, error = self.make_request("/companies", {"page": 1, "page_size": 5})
        if response and response.status_code == 200:
            try:
                data = response.json()
                companies = data.get('companies') or data.get('data') or data.get('results') or (data if isinstance(data, list) else [])

                # Check if pagination worked
                is_paginated = len(companies) <= 10  # Should respect page_size

                self.suite.add_result(TestResult(
                    name="Pagination Support",
                    category="Filtering & Pagination",
                    passed=is_paginated,
                    message=f"Returned {len(companies)} items with page_size=5",
                    points=4.0 if is_paginated else 2.0,
                    max_points=4.0,
                    response_time_ms=elapsed
                ))
            except:
                self.suite.add_result(TestResult(
                    name="Pagination Support",
                    category="Filtering & Pagination",
                    passed=False,
                    message="Could not parse pagination response",
                    max_points=4.0
                ))
        else:
            self.suite.add_result(TestResult(
                name="Pagination Support",
                category="Filtering & Pagination",
                passed=False,
                message="Pagination not working",
                max_points=4.0
            ))

        # Test year filtering on financial data
        response, elapsed, error = self.make_request(
            f"/companies/{self.SAMPLE_DUNS}/balance-sheet",
            {"year": 2024}
        )
        if response and response.status_code == 200:
            try:
                data = response.json()
                records = data.get('records') or data.get('data') or (data if isinstance(data, list) else [])

                # Check if filtering worked (all records should be 2024)
                if records:
                    years_in_response = set()
                    for r in records[:20]:
                        if isinstance(r, dict) and 'year' in r:
                            years_in_response.add(r['year'])

                    filtered_correctly = years_in_response == {2024} or len(years_in_response) == 0

                    self.suite.add_result(TestResult(
                        name="Year Filtering",
                        category="Filtering & Pagination",
                        passed=filtered_correctly,
                        message=f"Year filter working" if filtered_correctly else f"Found years: {years_in_response}",
                        points=4.0 if filtered_correctly else 2.0,
                        max_points=4.0,
                        response_time_ms=elapsed
                    ))
                else:
                    self.suite.add_result(TestResult(
                        name="Year Filtering",
                        category="Filtering & Pagination",
                        passed=True,
                        message="Year filtering accepted (no records to verify)",
                        points=3.0,
                        max_points=4.0
                    ))
            except:
                self.suite.add_result(TestResult(
                    name="Year Filtering",
                    category="Filtering & Pagination",
                    passed=False,
                    message="Could not parse filtered response",
                    max_points=4.0
                ))
        else:
            self.suite.add_result(TestResult(
                name="Year Filtering",
                category="Filtering & Pagination",
                passed=False,
                message="Year filtering not supported",
                max_points=4.0
            ))

    # ==================== ERROR HANDLING TESTS ====================

    def test_error_handling(self):
        """Test error handling."""
        print("Testing: Error Handling...")

        # Test 404 for non-existent company
        response, elapsed, error = self.make_request("/companies/INVALID_DUNS_12345")
        if error:
            self.suite.add_result(TestResult(
                name="404 for Invalid Company",
                category="Error Handling",
                passed=False,
                message=f"Request failed: {error}",
                max_points=3.0
            ))
        elif response is not None:
            if response.status_code == 404:
                self.suite.add_result(TestResult(
                    name="404 for Invalid Company",
                    category="Error Handling",
                    passed=True,
                    message="Correctly returns 404 for invalid DUNS",
                    points=3.0,
                    max_points=3.0,
                    response_time_ms=elapsed
                ))
            elif response.status_code == 200:
                self.suite.add_result(TestResult(
                    name="404 for Invalid Company",
                    category="Error Handling",
                    passed=False,
                    message="Returns 200 for invalid company (should be 404)",
                    max_points=3.0
                ))
            else:
                self.suite.add_result(TestResult(
                    name="404 for Invalid Company",
                    category="Error Handling",
                    passed=True,
                    message=f"Returns HTTP {response.status_code} for invalid DUNS",
                    points=2.0,
                    max_points=3.0,
                    response_time_ms=elapsed
                ))
        else:
            self.suite.add_result(TestResult(
                name="404 for Invalid Company",
                category="Error Handling",
                passed=False,
                message="No response received",
                max_points=3.0
            ))

        # Test invalid endpoint
        response, elapsed, error = self.make_request("/invalid_endpoint_xyz")
        if error:
            self.suite.add_result(TestResult(
                name="404 for Invalid Endpoint",
                category="Error Handling",
                passed=False,
                message=f"Request failed: {error}",
                max_points=2.0
            ))
        elif response is not None and response.status_code == 404:
            self.suite.add_result(TestResult(
                name="404 for Invalid Endpoint",
                category="Error Handling",
                passed=True,
                message="Correctly returns 404 for invalid endpoint",
                points=2.0,
                max_points=2.0,
                response_time_ms=elapsed
            ))
        else:
            status = response.status_code if response else "No response"
            self.suite.add_result(TestResult(
                name="404 for Invalid Endpoint",
                category="Error Handling",
                passed=False,
                message=f"Expected 404, got: {status}",
                max_points=2.0
            ))

    # ==================== PERFORMANCE TESTS ====================

    def test_performance(self):
        """Test API performance."""
        print("Testing: Performance...")

        # Test response time for list endpoint
        response, elapsed, error = self.make_request("/companies", {"page_size": 50})
        if elapsed:
            is_fast = elapsed < 1000  # Under 1 second
            is_acceptable = elapsed < 3000  # Under 3 seconds

            if is_fast:
                points = 5.0
                message = f"Excellent response time: {elapsed:.0f}ms"
            elif is_acceptable:
                points = 3.0
                message = f"Acceptable response time: {elapsed:.0f}ms"
            else:
                points = 1.0
                message = f"Slow response time: {elapsed:.0f}ms"

            self.suite.add_result(TestResult(
                name="Response Time (List Companies)",
                category="Performance",
                passed=is_acceptable,
                message=message,
                points=points,
                max_points=5.0,
                response_time_ms=elapsed
            ))

        # Test response time for single company with related data
        response, elapsed, error = self.make_request(f"/companies/{self.SAMPLE_DUNS}")
        if elapsed:
            is_fast = elapsed < 500
            is_acceptable = elapsed < 2000

            if is_fast:
                points = 5.0
                message = f"Excellent response time: {elapsed:.0f}ms"
            elif is_acceptable:
                points = 3.0
                message = f"Acceptable response time: {elapsed:.0f}ms"
            else:
                points = 1.0
                message = f"Slow response time: {elapsed:.0f}ms"

            self.suite.add_result(TestResult(
                name="Response Time (Single Company)",
                category="Performance",
                passed=is_acceptable,
                message=message,
                points=points,
                max_points=5.0,
                response_time_ms=elapsed
            ))

    # ==================== RESULTS OUTPUT ====================

    def print_results(self):
        """Print formatted test results."""
        print(f"\n{'='*60}")
        print("TEST RESULTS")
        print(f"{'='*60}\n")

        # Group by category
        categories = {}
        for result in self.suite.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(result)

        # Print each category
        for category, results in categories.items():
            cat_points = sum(r.points for r in results)
            cat_max = sum(r.max_points for r in results)
            cat_pct = (cat_points / cat_max * 100) if cat_max > 0 else 0

            print(f"\n{category} ({cat_points:.1f}/{cat_max:.1f} - {cat_pct:.0f}%)")
            print("-" * 50)

            for result in results:
                status = "PASS" if result.passed else "FAIL"
                status_icon = "+" if result.passed else "x"
                time_str = f" [{result.response_time_ms:.0f}ms]" if result.response_time_ms else ""
                print(f"  [{status_icon}] {result.name}: {result.message}{time_str}")
                print(f"      Points: {result.points:.1f}/{result.max_points:.1f}")

        # Print summary
        total_points, max_points = self.suite.get_score()
        percentage = (total_points / max_points * 100) if max_points > 0 else 0

        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"\nTotal Score: {total_points:.1f} / {max_points:.1f} ({percentage:.1f}%)")

        # Grade
        if percentage >= 90:
            grade = "A - Excellent"
        elif percentage >= 80:
            grade = "B - Good"
        elif percentage >= 70:
            grade = "C - Satisfactory"
        elif percentage >= 60:
            grade = "D - Needs Improvement"
        else:
            grade = "F - Unsatisfactory"

        print(f"Grade: {grade}")

        # Category breakdown
        print(f"\nCategory Breakdown:")
        cat_scores = self.suite.get_category_scores()
        for cat, (points, max_pts) in cat_scores.items():
            pct = (points / max_pts * 100) if max_pts > 0 else 0
            print(f"  {cat}: {points:.1f}/{max_pts:.1f} ({pct:.0f}%)")

        print(f"\n{'='*60}")

        return total_points, max_points, percentage

    def export_results_json(self, filepath: str):
        """Export results to JSON file."""
        results_data = {
            "candidate_url": self.suite.candidate_url,
            "test_date": datetime.now().isoformat(),
            "total_points": self.suite.get_score()[0],
            "max_points": self.suite.get_score()[1],
            "percentage": (self.suite.get_score()[0] / self.suite.get_score()[1] * 100) if self.suite.get_score()[1] > 0 else 0,
            "category_scores": {k: {"points": v[0], "max": v[1]} for k, v in self.suite.get_category_scores().items()},
            "tests": [
                {
                    "name": r.name,
                    "category": r.category,
                    "passed": r.passed,
                    "message": r.message,
                    "points": r.points,
                    "max_points": r.max_points,
                    "response_time_ms": r.response_time_ms,
                    "details": r.details
                }
                for r in self.suite.results
            ]
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2)

        print(f"\nResults exported to: {filepath}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_submission.py <candidate_api_url>")
        print("Example: python test_submission.py https://candidate-api.railway.app")
        sys.exit(1)

    candidate_url = sys.argv[1]

    # Run tests
    tester = APITester(candidate_url)
    tester.run_all_tests()

    # Export results
    if len(sys.argv) > 2:
        tester.export_results_json(sys.argv[2])
    else:
        # Default export
        safe_url = candidate_url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
        tester.export_results_json(f"test_results_{safe_url}.json")


if __name__ == "__main__":
    main()
