# Data Dictionary - Company Financial Data

## Overview

This document describes all data fields in the Company Financial Data API.

---

## Company Information

### companies table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| duns | string | D-U-N-S Number - unique business identifier | "740039581" |
| physical_address | string | Full street address | "LEVEL 24, 300 BARANGAROO AVENUE, BARANGAROO, 2000, NSW, Australia" |
| telephone_number | string | Contact phone number | "02 89087900" |
| acn | string | Australian Company Number | "082169060" |
| company_type | string | Legal structure classification | "Publicly Unlisted", "Private" |
| primary_sic | string | Primary Standard Industry Classification | "7389 - Business Services, Not Elsewhere Classified" |

---

## Financial Statements

### Common Fields

All financial statement tables share these fields:

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique record identifier |
| duns | string | Company DUNS number (foreign key) |
| line_item | string | Name of the financial metric |
| year | integer | Fiscal year (2015-2024) |
| value | string | Original formatted value (e.g., "$43,079") |
| numeric_value | float | Parsed numeric value (e.g., 43079.0) |

### Value Formatting

| Original Format | Numeric Value | Description |
|-----------------|---------------|-------------|
| "$43,079" | 43079.0 | Positive currency |
| "($34,984)" | -34984.0 | Negative currency (parentheses) |
| "16.47%" | 16.47 | Percentage |
| "-" | null | Not available |
| "" (blank) | null | Not reported |

**Note**: All monetary values are in thousands (000s) unless otherwise specified in the line_item name.

---

## Balance Sheet Line Items

### Current Assets
| Line Item | Description |
|-----------|-------------|
| Cash and cash equivalents ($000s) | Liquid cash holdings |
| Trade receivables ($000s) | Money owed by customers |
| Other receivables ($000s) | Other amounts due to company |
| Prepayments ($000s) | Advance payments made |
| Inventories - raw materials ($000s) | Raw material inventory |
| Inventories - work in progress ($000s) | Partially completed goods |
| Inventories - finished goods ($000s) | Completed inventory ready for sale |
| Total current assets ($000s) | Sum of all current assets |

### Non-Current Assets
| Line Item | Description |
|-----------|-------------|
| Property, plant and equipment ($000s) | Physical assets |
| Intangible assets ($000s) | Patents, goodwill, etc. |
| Deferred tax assets ($000s) | Future tax benefits |
| Investments ($000s) | Long-term investments |
| TOTAL ASSETS ($000s) | Total of all assets |

### Current Liabilities
| Line Item | Description |
|-----------|-------------|
| Trade payables ($000s) | Money owed to suppliers |
| Other payables ($000s) | Other amounts owed |
| Short-term loans ($000s) | Loans due within 1 year |
| Finance lease obligations ($000s) | Lease payments due |
| Tax payables ($000s) | Taxes owed |
| Provisions ($000s) | Reserved for future obligations |
| Total current liabilities ($000s) | Sum of current liabilities |

### Non-Current Liabilities
| Line Item | Description |
|-----------|-------------|
| Long-term loans ($000s) | Loans due after 1 year |
| Deferred tax liabilities ($000s) | Future tax obligations |
| Convertible preference shares ($000s) | Convertible equity instruments |
| Total non-current liabilities ($000s) | Sum of long-term liabilities |
| TOTAL LIABILITIES ($000s) | Total of all liabilities |

### Equity
| Line Item | Description |
|-----------|-------------|
| Contributed equity ($000s) | Capital from shareholders |
| Retained earnings ($000s) | Accumulated profits |
| Reserves ($000s) | Various equity reserves |
| Minority interests ($000s) | Non-controlling interests |
| NET ASSETS ($000s) | Total Assets - Total Liabilities |

---

## Cash Flow Statement Line Items

### Operating Activities
| Line Item | Description |
|-----------|-------------|
| Receipts from customers ($000s) | Cash received from sales |
| Payments to suppliers and employees ($000s) | Cash paid for operations |
| Interest paid ($000s) | Interest expense paid |
| Tax paid ($000s) | Income tax paid |
| Net cashflow from/(used in) operating activities ($000s) | Net operating cash |

### Investing Activities
| Line Item | Description |
|-----------|-------------|
| Purchases of property, plant and equipment ($000s) | Capital expenditures |
| Proceeds from sale of property, plant and equipment ($000s) | Asset sale proceeds |
| Purchases of intangible assets ($000s) | IP, software purchases |
| Investment disposals ($000s) | Sale of investments |
| Interest received ($000s) | Interest income received |
| Dividends received ($000s) | Dividend income received |
| Net cashflow from/(used in) investing activities ($000s) | Net investing cash |

### Financing Activities
| Line Item | Description |
|-----------|-------------|
| Proceeds from share issuances ($000s) | New equity raised |
| Proceeds from borrowings ($000s) | New debt raised |
| Dividends paid ($000s) | Cash dividends to shareholders |
| Finance lease repayments ($000s) | Lease principal payments |
| Net cashflow from/(used in) financing activities ($000s) | Net financing cash |

### Cash Summary
| Line Item | Description |
|-----------|-------------|
| Net increase/(decrease) in cash ($000s) | Total cash change |
| Cash at beginning of period ($000s) | Opening cash balance |
| Cash at end of period ($000s) | Closing cash balance |
| Foreign exchange effect on cash ($000s) | FX translation impact |

---

## Income Statement Line Items

### Revenue
| Line Item | Description |
|-----------|-------------|
| Revenue from continuing operations ($000s) | Primary business revenue |
| Revenue from discontinued operations ($000s) | Revenue from divested units |
| Revenue growth (%) | Year-over-year revenue change |

### Costs & Expenses
| Line Item | Description |
|-----------|-------------|
| Cost of sales ($000s) | Direct costs of goods sold |
| Administrative expenses ($000s) | G&A overhead costs |
| Finance costs ($000s) | Interest and financing expenses |
| Research & development ($000s) | R&D expenditure |

### Profitability Metrics
| Line Item | Description |
|-----------|-------------|
| Gross profit ($000s) | Revenue - Cost of sales |
| EBIT ($000s) | Earnings Before Interest & Tax |
| EBITDA ($000s) | EBIT + Depreciation & Amortization |
| Profit before tax ($000s) | Pre-tax profit |
| Net profit for the period ($000s) | Bottom line profit |
| EBITDA margin (%) | EBITDA / Revenue |
| EBIT margin (%) | EBIT / Revenue |
| Net profit margin (%) | Net Profit / Revenue |

### Employee Metrics
| Line Item | Description |
|-----------|-------------|
| Salaries and wages ($000s) | Employee compensation |
| Superannuation - defined contribution ($000s) | Retirement contributions |
| Superannuation - defined benefit ($000s) | Pension obligations |
| Total employee benefits expense ($000s) | Total staff costs |
| Number of employees | Headcount |

### Depreciation & Amortization
| Line Item | Description |
|-----------|-------------|
| Depreciation - property, plant & equipment ($000s) | Physical asset depreciation |
| Amortization - intangible assets ($000s) | Intangible asset amortization |
| Total depreciation and amortization expense ($000s) | Total D&A |

### Earnings Per Share
| Line Item | Description |
|-----------|-------------|
| Basic EPS - continuing operations | Basic earnings per share |
| Diluted EPS - continuing operations | Diluted earnings per share |
| Basic EPS - total | Total basic EPS |
| Diluted EPS - total | Total diluted EPS |

---

## Industries

### industries table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| id | integer | Unique record identifier | 1 |
| duns | string | Company DUNS number | "740039581" |
| industry_code | string | 4-digit SIC code | "7389" |
| industry_description | string | Industry name | "Business Services, Not Elsewhere Classified" |
| is_primary | boolean | Primary classification flag | true/false |

### Common Industry Codes

| Code | Description | Company Count |
|------|-------------|---------------|
| 6719 | Offices of Holding Companies | 77 |
| 7389 | Business Services, NEC | 17 |
| 6726 | Unit Investment Trusts | 13 |
| 8741 | Management Services | 13 |
| 6282 | Investment Advice | 12 |
| 6799 | Investors, NEC | 11 |
| 7371 | Computer Programming Services | 10 |
| 6722 | Management Investment Offices | 8 |
| 7011 | Hotels and Motels | 8 |
| 7379 | Computer Related Services, NEC | 8 |

---

## Operations

### operations table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| id | integer | Unique record identifier | 1 |
| duns | string | Company DUNS number | "742298797" |
| field_name | string | Field identifier | "Operations" |
| field_value | text | Business description | "The Webb Project is in the north-east of Western Australia..." |

**Note**: Only 24 companies have operations data populated.

---

## People

### people table

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| id | integer | Unique record identifier | 1 |
| duns | string | Company DUNS number | "740039581" |
| person_name | string | Full name | "Mark Rutherglen" |
| title | string | Job title | "Director", "CEO", "CFO" |
| responsibilities | string | Decision-making areas (comma-separated) | "Financial Decision Maker, IT Decision Maker" |

### Common Titles

| Title | Count |
|-------|-------|
| Director | 500+ |
| Director and Company Secretary | 150+ |
| Company Secretary | 100+ |
| Non-Executive Director | 80+ |
| Managing Director | 50+ |
| CEO | 30+ |
| CFO | 25+ |

### Responsibility Types

| Responsibility | Description |
|----------------|-------------|
| Director | Board member |
| Company Secretary | Corporate governance officer |
| Financial Decision Maker | Finance authority |
| IT Decision Maker | Technology authority |
| Human Resources Decision Maker | HR authority |
| Marketing Decision Maker | Marketing authority |
| Operations Decision Maker | Operations authority |
| Sales Decision Maker | Sales authority |
| Purchasing | Procurement authority |

---

## Data Quality Notes

### Missing Values
- Dash (`-`) indicates "not available" or "not applicable"
- Blank values indicate "not reported"
- Both are stored as `null` in `numeric_value`

### Currency Formatting
- All monetary values in thousands unless specified
- Negatives shown in parentheses: `($1,234)`
- Dollar sign and commas in original `value` field
- Clean number in `numeric_value` field

### Time Coverage
- Financial statements: 2015-2024 (10 years)
- Not all companies have data for all years
- Growth percentages may be null if prior year is missing

### Data Completeness
- 222 companies total
- 218 companies have operations and people data
- All 222 have financial statement data
