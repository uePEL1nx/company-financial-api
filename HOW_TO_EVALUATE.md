# How to Evaluate Candidate API Submissions

## Quick Start

When a candidate submits their API URL, run:

```bash
cd C:\Users\jd\APItest
python testing/evaluate_submission.py <candidate_url> "<candidate_name>"
```

### Example

```bash
python testing/evaluate_submission.py https://candidate-api.railway.app "John Smith"
```

This will:
1. Run all functional tests (85 points)
2. Validate data accuracy (14 checks)
3. Calculate combined score (out of 100)
4. Assign grade (A-F) and recommendation
5. Export detailed JSON report

---

## What Candidates Submit

Candidates provide a **single URL** to their deployed API that includes:
- Working REST endpoints for company financial data
- Interactive documentation at `/docs`

Example: `https://their-api.railway.app`

---

## Scoring Breakdown

### Functional Tests (85% of final score)

| Category | Points | What's Tested |
|----------|--------|---------------|
| Documentation | 10 | `/docs` Swagger UI, `/openapi.json` schema |
| Root Endpoints | 5 | `/` returns JSON, `/health` available |
| Company Endpoints | 18 | List companies, single company, people, industries |
| Financial Endpoints | 21 | Balance sheet, cash flow, income statement |
| People & Industries | 8 | `/people`, `/industries` list endpoints |
| Filtering & Pagination | 8 | `page_size` param, `year` filter |
| Error Handling | 5 | 404 for invalid company/endpoint |
| Performance | 10 | Response times (<1s excellent, <3s acceptable) |
| **Total** | **85** | |

### Data Validation (15% of final score)

| Check | Expected Value |
|-------|----------------|
| Company Count | 222 |
| ACN | 082169060 |
| Phone | 02 89087900 |
| Company Type | Publicly Unlisted |
| Address | Contains "BARANGAROO" |
| Primary SIC | Contains "7389" |
| Cash 2024 (formatted) | $43,079 |
| Cash 2024 (numeric) | 43079.0 |
| People Count | 10 |
| Person: Rutherglen | Title: Director |
| Person: Anderson | Title: Director and Company Secretary |
| Person: Tromeur | Title: Director of Finance |
| Industry 7389 | Contains "Business Services" |
| Industry 6719 | Contains "Holding Companies" |

---

## Final Score Calculation

```
Final Score = (Functional % × 0.85) + (Validation % × 0.15)
```

Example:
- Functional: 81/85 (95.3%)
- Validation: 14/14 (100%)
- Final: (95.3 × 0.85) + (100 × 0.15) = **96.0/100**

---

## Grading Scale

| Grade | Score | Recommendation |
|-------|-------|----------------|
| **A - Excellent** | 90%+ | Strong Hire |
| **B - Good** | 80-89% | Hire |
| **C - Satisfactory** | 70-79% | Maybe |
| **D - Needs Improvement** | 60-69% | Likely No |
| **F - Unsatisfactory** | <60% | No Hire |

---

## Output Files

Each evaluation creates a JSON report:

```
evaluation_<candidate_name>_<timestamp>.json
```

Contains:
- All test results with pass/fail status
- Points breakdown by category
- Data validation results
- Final score and recommendation

---

## Reference Implementation Score

Our API: **96.0/100 (Grade A - Strong Hire)**

- Functional: 81/85 (95.3%)
- Validation: 14/14 (100%)
- Only deduction: Performance (Railway cold starts ~1 second)

---

## Troubleshooting

### Tests fail to connect
- Verify URL includes `https://`
- Check API is deployed and accessible
- Try accessing `/docs` in browser first

### Data validation fails
- Candidate may have imported data differently
- Check their `/docs` for actual endpoint structure
- Small variations in formatting are acceptable

### Performance tests fail
- Free tier hosting has cold starts
- Re-run tests after warming up the API
- Consider this in overall evaluation

---

## Files Reference

| File | Purpose |
|------|---------|
| `testing/evaluate_submission.py` | Main evaluation script |
| `testing/test_submission.py` | Functional tests only |
| `testing/test_data_validation.py` | Data validation only |
| `CANDIDATE_BRIEF_SIMPLE.md` | Instructions for candidates |
| `docs/TESTING_AND_EVALUATION.md` | Detailed evaluation methodology |

---

## Complete Evaluation Workflow

1. **Receive submission**: Candidate provides API URL
2. **Run evaluation**:
   ```bash
   python testing/evaluate_submission.py <url> "<name>"
   ```
3. **Review output**: Check console for summary
4. **Save report**: JSON file auto-generated
5. **Make decision**: Use grade/recommendation as guide

---

*Last updated: December 2024*
