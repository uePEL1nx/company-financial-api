# API Submission Testing System

Automated testing suite for evaluating candidate API submissions.

## Quick Start

```bash
# Install dependencies
pip install requests

# Run tests against a candidate's API
python test_submission.py https://candidate-api-url.com

# Run tests with custom output file
python test_submission.py https://candidate-api-url.com results.json
```

## What It Tests

### 1. Documentation (10 points)
- Swagger UI availability at `/docs`
- OpenAPI schema at `/openapi.json`

### 2. Root Endpoints (5 points)
- Root endpoint `/` returns valid JSON
- Health check endpoint `/health` (bonus)

### 3. Company Endpoints (18 points)
- List all companies `GET /companies`
- Get single company `GET /companies/{duns}`
- Company people `GET /companies/{duns}/people`
- Company industries `GET /companies/{duns}/industries`

### 4. Financial Endpoints (21 points)
- Balance sheet data `GET /companies/{duns}/balance-sheet`
- Cash flow data `GET /companies/{duns}/cash-flow`
- Income statement data `GET /companies/{duns}/income-statement`
- Aggregate endpoints (bonus): `/balance-sheets`, `/cash-flows`, `/income-statements`

### 5. People Endpoints (4 points)
- List all people `GET /people`

### 6. Industry Endpoints (4 points)
- List all industries `GET /industries`

### 7. Filtering & Pagination (8 points)
- Pagination support (`page`, `page_size` parameters)
- Year filtering on financial data

### 8. Error Handling (5 points)
- 404 response for invalid company DUNS
- 404 response for invalid endpoints

### 9. Performance (10 points)
- Response time for list endpoints (<1s excellent, <3s acceptable)
- Response time for single company (<500ms excellent, <2s acceptable)

## Total Points: 85

## Grading Scale

| Grade | Score |
|-------|-------|
| A - Excellent | 90%+ |
| B - Good | 80-89% |
| C - Satisfactory | 70-79% |
| D - Needs Improvement | 60-69% |
| F - Unsatisfactory | <60% |

## Output

The tester generates:
1. Console output with detailed results
2. JSON file with full test data

### JSON Output Structure

```json
{
  "candidate_url": "https://...",
  "test_date": "2024-12-10T...",
  "total_points": 76.0,
  "max_points": 82.0,
  "percentage": 92.7,
  "category_scores": {
    "Documentation": {"points": 10.0, "max": 10.0},
    ...
  },
  "tests": [
    {
      "name": "Swagger UI (/docs)",
      "category": "Documentation",
      "passed": true,
      "message": "Swagger UI available",
      "points": 5.0,
      "max_points": 5.0,
      "response_time_ms": 283.5,
      "details": null
    },
    ...
  ]
}
```

## Flexible Endpoint Detection

The tester tries multiple common endpoint formats:
- `/balance-sheet` or `/balance_sheet` or `/balancesheet`
- `/cash-flow` or `/cash_flow` or `/cashflow`
- `/income-statement` or `/income_statement` or `/incomestatement`

This ensures candidates aren't penalized for minor naming differences.

## Test Against Reference Implementation

```bash
# Test against the reference API
python test_submission.py https://company-financial-api-production.up.railway.app
```

## Notes

- Tests use a 30-second timeout per request
- Sample DUNS used for testing: `740039581`
- Expected company count: 222
- Response times may vary based on hosting platform cold starts
