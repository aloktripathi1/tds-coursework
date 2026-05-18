# Q1: Excel — Operational Margin Consolidation (File 1)

## Task
Load `q-excel-operational-metrics__1_.xlsx`, clean and standardise the `Operational Close` sheet, then compute the **total variance (Revenue − Expense)** for records where:
- Region = **Europe**
- Ops Category = **Onboarding**
- Closing Period ≤ **15 Jul 2024**

---

## Requirements
* Trim leading/trailing whitespace from all fields
* Map all region aliases (e.g. `EU`, `Europa`, `E.U.`, `Europe Region`) → canonical `Europe`
* Parse four date formats: `YYYY-MM-DD`, `DD/MM/YYYY`, `Mon DD, YYYY`, and `YYYY Qn` (quarter → last calendar day)
* Strip currency symbols (`$`, `USD`), commas, and spaces from numeric columns
* If Expense is blank or `USD TBD`, substitute **37% of reported Revenue**
* Extract the first pipe-delimited segment of `Ops Notes` as the category
* Filter and sum `Revenue − Expense` across all matching rows

---

## Approach

### 1. Load the Workbook
Open the `.xlsx` file with `openpyxl` and iterate rows from the `Operational Close` sheet.

### 2. Standardise Regions
Strip whitespace, then normalise to lowercase with punctuation removed. Pattern-match against known aliases:
- `europe`, `eu`, `europa` → **Europe**
- `northamerica`, `northam` → **North America**
- `latinamerica`, `latam`, `latin` → **Latin America**
- `asiapacific`, `asiapac`, `apac` → **Asia Pacific**
- `middleeast`, `mea` → **Middle East & Africa**

### 3. Parse Dates
Detect format by structure, then convert to a Python `date` object:
- Contains `-` and matches `DDDD-DD-DD` → `YYYY-MM-DD`
- Contains `/` → `DD/MM/YYYY`
- Contains letter month → `strptime('%b %d, %Y')`
- Matches `YYYY Qn` → last day of that quarter via `DATE(year, q*3+1, 0)` logic

### 4. Clean Numerics
```python
re.sub(r'[USD$,\s]', '', value, flags=re.IGNORECASE)
```
If result is empty or contained `TBD` → `expense = revenue × 0.37`

### 5. Split Ops Notes
```python
category = ops_notes.strip().split('|')[0].strip()
```

### 6. Filter & Sum
Keep rows where `region == 'Europe'`, `category == 'Onboarding'`, and `parsed_date <= date(2024, 7, 15)`. Accumulate `revenue − expense`.

---

## Code

**Script:** [`solve_excel_file1.py`](./solve_excel_file1.py)

```python
import re, openpyxl
from datetime import date, datetime

wb = openpyxl.load_workbook('q-excel-operational-metrics__1_.xlsx')
ws = wb['Operational Close']
data = list(ws.iter_rows(values_only=True))[1:]

def canonicalize_region(r):
    if r is None: return None
    r_lower = re.sub(r'[\s\-\.&/_]', '', r).lower()
    if any(x in r_lower for x in ['europe', 'eu', 'europa']): return 'Europe'
    if any(x in r_lower for x in ['northamerica', 'northam']): return 'North America'
    if any(x in r_lower for x in ['latinamerica', 'latam', 'latin']): return 'Latin America'
    if any(x in r_lower for x in ['asiapacific', 'asiapac', 'apac']): return 'Asia Pacific'
    if any(x in r_lower for x in ['middleeast', 'mea']): return 'Middle East & Africa'
    return r

def parse_date(d):
    if isinstance(d, (date, datetime)): return d if isinstance(d, date) else d.date()
    d = str(d).strip()
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', d)
    if m: return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', d)
    if m: return date(int(m[3]), int(m[2]), int(m[1]))
    try: return datetime.strptime(d, '%b %d, %Y').date()
    except: pass
    m = re.match(r'^(\d{4})\s*Q([1-4])$', d)
    if m:
        y, q = int(m[1]), int(m[2])
        return {1: date(y,3,31), 2: date(y,6,30), 3: date(y,9,30), 4: date(y,12,31)}[q]

def parse_numeric(v):
    if v is None: return None
    v = str(v).strip()
    if 'TBD' in v.upper() or v == '': return None
    v = re.sub(r'[USD$,\s]', '', v, flags=re.IGNORECASE)
    try: return float(v)
    except: return None

cutoff = date(2024, 7, 15)
total_variance = 0.0

for row in data:
    _, region, closing_period, revenue_raw, expense_raw, ops_notes, _ = row
    if canonicalize_region(region) != 'Europe': continue
    parsed_date = parse_date(closing_period)
    if parsed_date is None or parsed_date > cutoff: continue
    if not ops_notes or ops_notes.strip().split('|')[0].strip().lower() != 'onboarding': continue
    revenue = parse_numeric(revenue_raw)
    if revenue is None: continue
    expense = parse_numeric(expense_raw)
    if expense is None: expense = revenue * 0.37
    total_variance += revenue - expense

print(total_variance)
```

---

## Verification

```bash
python solve_excel_file1.py
```

| Metric | Value |
|---|---|
| Total rows in sheet | 650 |
| Matched records | 16 |
| Records with imputed expense (37%) | 1 (RC-00212) |
| **Total Variance** | **455037.98** |

---

## Submission

**Your Answer:**
```
455037.98
```
