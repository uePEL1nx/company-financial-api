# Software Developer Assessment

## The Task

Build a REST API that serves company financial data from the provided CSV files.

## What You Receive

A `CompanyData/` folder containing CSV files organized into 7 subdirectories:

| Directory | Content |
|-----------|---------|
| `balance_sheet/` | Balance sheet data |
| `cash_flow_statement/` | Cash flow statements |
| `income_statement/` | Income statements |
| `company_info/` | Company details |
| `industries/` | Industry classifications |
| `operations/` | Business descriptions |
| `people/` | Executive and director information |

Each file is named by DUNS number (e.g., `740039581.csv`), which is the unique identifier linking data across all categories.

## What You Submit

**A single URL** to your deployed API that includes:
- Working API endpoints
- Interactive documentation at `/docs`

Example submission: `https://your-api.railway.app`

We will access `https://your-api.railway.app/docs` to review your API documentation and test your endpoints.

## Requirements

Your API must:
1. Serve the provided company data through REST endpoints
2. Include auto-generated API documentation at `/docs`
3. Be publicly accessible

## Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Functionality | 30% |
| API Design | 25% |
| Documentation Quality | 25% |
| Code Quality (inferred from API behavior) | 20% |

## Time Limit

4-6 hours (estimate)

## Notes

- Choose any language, framework, and hosting platform
- The data is for assessment purposes only
- Focus on delivering working functionality

## Questions?

If you have questions about the requirements, please ask before starting.

Good luck!
