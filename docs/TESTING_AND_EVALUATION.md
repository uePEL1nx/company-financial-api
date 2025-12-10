# Testing and Evaluation System

## Overview

This document describes the automated testing and evaluation system for assessing candidate API submissions in the developer skills assessment.

---

## Assessment Workflow

### 1. Candidate Receives Materials
- `CompanyData/` folder containing all CSV files
- `CANDIDATE_BRIEF.md` with requirements and instructions
- Time limit: 4-6 hours (estimate)

### 2. Candidate Submits
- Live API URL (e.g., `https://their-api.railway.app`)
- GitHub repository URL
- API documentation URL (typically `/docs`)

### 3. Evaluator Runs Tests
```bash
cd C:\Users\jd\APItest
python testing/test_submission.py https://candidate-api-url.com
```

### 4. Review Results
- Console output shows immediate pass/fail
- JSON file saved for records and comparison
- Manual code review of repository

---

## Automated Test Suite

### Location
```
C:\Users\jd\APItest\testing\
├── test_submission.py    # Main test script
├── README.md             # Quick reference
└── [results files]       # Generated JSON outputs
```

### Running Tests

```bash
# Basic usage
python testing/test_submission.py <candidate_api_url>

# Example
python testing/test_submission.py https://candidate-api.railway.app

# With custom output file
python testing/test_submission.py https://candidate-api.railway.app custom_results.json
```

### Test Categories

#### 1. Documentation (10 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| Swagger UI (`/docs`) | 5 | Returns HTML with "swagger" or "openapi" |
| OpenAPI Schema (`/openapi.json`) | 5 | Valid JSON with `paths` and `info` keys |

#### 2. Root Endpoints (5 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| Root (`/`) | 3 | Returns valid JSON |
| Health (`/health`) | 2 | Returns HTTP 200 (bonus) |

#### 3. Company Endpoints (18 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| List Companies (`/companies`) | 5 | Returns ~222 companies |
| Get Company (`/companies/{duns}`) | 5 | Returns company with identifier |
| Company People | 4 | Returns people records |
| Company Industries | 4 | Returns industry records |

#### 4. Financial Endpoints (21 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| Balance Sheet (`/companies/{duns}/balance-sheet`) | 5 | Returns financial records |
| Cash Flow (`/companies/{duns}/cash-flow`) | 5 | Returns financial records |
| Income Statement (`/companies/{duns}/income-statement`) | 5 | Returns financial records |
| Aggregate Balance Sheets (`/balance-sheets`) | 2 | Endpoint available (bonus) |
| Aggregate Cash Flows (`/cash-flows`) | 2 | Endpoint available (bonus) |
| Aggregate Income Statements (`/income-statements`) | 2 | Endpoint available (bonus) |

#### 5. People Endpoints (4 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| List People (`/people`) | 4 | Returns people records |

#### 6. Industry Endpoints (4 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| List Industries (`/industries`) | 4 | Returns industry records |

#### 7. Filtering & Pagination (8 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| Pagination | 4 | Respects `page_size` parameter |
| Year Filtering | 4 | Filters financial data by year |

#### 8. Error Handling (5 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| Invalid Company | 3 | Returns 404 for non-existent DUNS |
| Invalid Endpoint | 2 | Returns 404 for unknown routes |

#### 9. Performance (10 points)
| Test | Points | Pass Criteria |
|------|--------|---------------|
| List Companies Response | 5 | <1s excellent (5pt), <3s acceptable (3pt) |
| Single Company Response | 5 | <500ms excellent (5pt), <2s acceptable (3pt) |

### Total Points: 85

---

## Grading Scale

| Grade | Percentage | Interpretation |
|-------|------------|----------------|
| **A - Excellent** | 90%+ | Production-ready, exceeds expectations |
| **B - Good** | 80-89% | Solid implementation, minor gaps |
| **C - Satisfactory** | 70-79% | Meets basic requirements |
| **D - Needs Improvement** | 60-69% | Significant gaps or issues |
| **F - Unsatisfactory** | <60% | Does not meet requirements |

---

## Test Output Format

### Console Output
```
============================================================
API SUBMISSION TESTER
============================================================
Candidate URL: https://candidate-api.railway.app
Test Started: 2024-12-10 10:15:05
============================================================

Testing: Documentation...
Testing: Root Endpoints...
[... test progress ...]

============================================================
TEST RESULTS
============================================================

Documentation (10.0/10.0 - 100%)
--------------------------------------------------
  [+] Swagger UI (/docs): Swagger UI available [283ms]
      Points: 5.0/5.0
  [+] OpenAPI Schema (/openapi.json): Valid OpenAPI schema with 25 endpoints [156ms]
      Points: 5.0/5.0

[... category results ...]

============================================================
SUMMARY
============================================================

Total Score: 81.0 / 85.0 (95.3%)
Grade: A - Excellent

Category Breakdown:
  Documentation: 10.0/10.0 (100%)
  [... breakdown ...]
============================================================
```

### JSON Output
```json
{
  "candidate_url": "https://candidate-api.railway.app",
  "test_date": "2024-12-10T10:15:05.123456",
  "total_points": 81.0,
  "max_points": 85.0,
  "percentage": 95.3,
  "category_scores": {
    "Documentation": {"points": 10.0, "max": 10.0},
    "Root Endpoints": {"points": 5.0, "max": 5.0},
    "Company Endpoints": {"points": 18.0, "max": 18.0},
    "Financial Endpoints": {"points": 21.0, "max": 21.0},
    "People Endpoints": {"points": 4.0, "max": 4.0},
    "Industry Endpoints": {"points": 4.0, "max": 4.0},
    "Filtering & Pagination": {"points": 8.0, "max": 8.0},
    "Error Handling": {"points": 5.0, "max": 5.0},
    "Performance": {"points": 6.0, "max": 10.0}
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
    }
    // ... all test results
  ]
}
```

---

## Flexible Endpoint Detection

The test suite accommodates common naming variations:

| Canonical | Also Accepts |
|-----------|--------------|
| `/balance-sheet` | `/balance_sheet`, `/balancesheet` |
| `/cash-flow` | `/cash_flow`, `/cashflow` |
| `/income-statement` | `/income_statement`, `/incomestatement` |
| `/people` | `/personnel` |
| `/industries` | `/industry` |

This prevents penalizing candidates for minor naming convention differences.

---

## Reference Implementation Benchmark

### Our API Score
- **URL**: https://company-financial-api-production.up.railway.app
- **Score**: 81/85 (95.3%)
- **Grade**: A - Excellent

### Deductions
- Performance: 4 points lost due to Railway cold start times (~1 second)
- All functional tests pass 100%

### Expected Candidate Range
| Level | Expected Score | Notes |
|-------|----------------|-------|
| Senior | 75-85 (88-100%) | Full implementation, good performance |
| Mid-level | 60-75 (70-88%) | Core features, may miss bonus endpoints |
| Junior | 45-60 (53-70%) | Basic functionality, gaps in filtering/docs |

---

## Manual Code Review Checklist

In addition to automated tests, review the candidate's code for:

### Code Quality (20% of overall evaluation)
- [ ] Clean, readable code structure
- [ ] Consistent naming conventions
- [ ] Appropriate error handling
- [ ] No hardcoded values or secrets
- [ ] Proper separation of concerns

### Database Design (20% of overall evaluation)
- [ ] Appropriate schema design
- [ ] Proper use of foreign keys
- [ ] Efficient indexing for common queries
- [ ] Data types match the data
- [ ] Handles null/missing values appropriately

### API Design (15% of overall evaluation)
- [ ] RESTful conventions followed
- [ ] Consistent response formats
- [ ] Appropriate HTTP status codes
- [ ] Query parameters well-designed
- [ ] Pagination implemented correctly

### Documentation (15% of overall evaluation)
- [ ] README with setup instructions
- [ ] API endpoints documented
- [ ] Clear parameter descriptions
- [ ] Example requests/responses

### Deployment (15% of overall evaluation)
- [ ] Successfully deployed and accessible
- [ ] Reasonable response times
- [ ] Handles concurrent requests
- [ ] No obvious security issues

---

## Evaluation Scoring Sheet

### Candidate Information
- **Name**: _______________
- **Date**: _______________
- **API URL**: _______________
- **GitHub URL**: _______________

### Automated Test Score
- **Points**: _____ / 85
- **Percentage**: _____%
- **Grade**: _____

### Manual Review Scores (1-5 scale)

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Code Quality | /5 | 20% | |
| Database Design | /5 | 20% | |
| API Design | /5 | 15% | |
| Documentation | /5 | 15% | |
| Deployment | /5 | 15% | |
| **Automated Tests** | (from above) | 15% | |

### Final Score Calculation
```
Final = (Automated % × 0.15) + (Code × 0.20) + (DB × 0.20) + (API × 0.15) + (Docs × 0.15) + (Deploy × 0.15)
```

### Overall Recommendation
- [ ] Strong Hire
- [ ] Hire
- [ ] Maybe
- [ ] No Hire

### Notes
```
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## Troubleshooting

### Common Issues

**Test fails to connect**
- Check URL is correct and includes `https://`
- Verify API is deployed and accessible
- Check for firewall/CORS issues

**All financial tests fail**
- Candidate may have different endpoint naming
- Check their `/docs` for actual endpoint paths
- May need to manually verify

**Performance tests fail**
- Railway/Render free tiers have cold starts
- Re-run tests after warming up the API
- Consider platform limitations in evaluation

**Data count mismatch**
- Candidate may have imported data differently
- Check if they have 222 companies
- Small variance (±5) is acceptable

### Manual Testing

If automated tests are inconclusive:
```bash
# Test root
curl https://candidate-api.com/

# Test companies
curl https://candidate-api.com/companies

# Test single company
curl https://candidate-api.com/companies/740039581

# Test financial data
curl "https://candidate-api.com/companies/740039581/balance-sheet?year=2024"
```

---

## File Locations Summary

| File | Purpose |
|------|---------|
| `testing/test_submission.py` | Main test script |
| `testing/README.md` | Quick reference |
| `CANDIDATE_BRIEF.md` | Instructions for candidates |
| `docs/PROJECT_DOCUMENTATION.md` | Full technical docs |
| `docs/DATA_DICTIONARY.md` | Field definitions |
| `docs/TESTING_AND_EVALUATION.md` | This document |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2024-12-10 | 1.0 | Initial release |

---

*Last updated: December 2024*
