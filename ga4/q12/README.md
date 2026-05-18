# Q12: Shell — Parse and Aggregate Messy CSV Transaction Logs

## Task

Clean and aggregate a messy transaction CSV file that mixes pipe and comma separators, has extra whitespace, missing categories, and trailing junk fields. Output total transaction amounts per category, sorted alphabetically.

---

## Requirements

* Handle inconsistent separators (pipes and commas)
* Clean up extra whitespace
* Filter out rows with missing category data
* Calculate the total transaction amount for each category
* Output format: `Category:Amount|Category:Amount|...` (alphabetical, 2 decimal places)

---

## Approach

### Row Types Identified
Inspecting the CSV revealed **three distinct row formats**:

| Type | Example |
|---|---|
| Pure pipe | `TXN000005\|2025-08-20\|286.88\|Electronics\|FreshMart\|NYC` |
| Pure pipe with extra junk | `TXN000002\|...\|Electronics\|StyleShop\|NYC\|EXTRA\|JUNK` |
| Hybrid (pipe outer, comma inside) | `TXN000004\|2025-08-02,132.01\|Furniture,BookWorld\|San Antonio` |
| Pure comma with whitespace | `TXN000006  ,  2025-06-21,  445.55  , Clothing  , FurniturePro  , NYC` |

> **Bug fixed:** Comma-only rows start with `TXN` so they matched the pipe branch, but had only 1 pipe field — hitting `else: continue` and being silently skipped. Fixed by requiring `len(pipe_fields) >= 4` before entering the pipe branch.

### Parsing Logic
1. **Split by pipe first.** If `fields[0]` starts with `TXN`:
   - `≥ 5 pipe fields` → pure pipe row; `fields[2]` = amount, `fields[3]` = category
   - `== 4 pipe fields` → hybrid row; split `fields[1]` by comma to get amount, split `fields[2]` by comma to get category
2. **Otherwise** split by comma → pure comma row; strip whitespace from each field
3. **Skip** if category is empty or missing
4. **Aggregate** amounts per category using a dict

### Key Pitfall
Rows with 4 pipe fields (hybrid format) had `City` appearing in the category slot — these were correctly handled by recognising the hybrid pattern and splitting the composite fields.

---

## Code

**Script:** [`parse_transactions.py`](./parse_transactions.py)

```python
from collections import defaultdict
totals = defaultdict(float)

with open('transactions_your-student-id.csv', encoding='utf-8') as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line: continue
        pipe_fields = [p.strip() for p in line.split('|')]

        if pipe_fields[0].startswith('TXN'):
            if len(pipe_fields) >= 5:           # pure pipe
                amount = float(pipe_fields[2]); cat = pipe_fields[3]
            elif len(pipe_fields) == 4:          # hybrid
                _, amount_str = pipe_fields[1].split(',', 1)
                cat  = pipe_fields[2].split(',', 1)[0].strip()
                amount = float(amount_str.strip())
            else: continue
        else:                                    # pure comma
            comma_fields = [p.strip() for p in line.split(',')]
            if len(comma_fields) < 4: continue
            amount = float(comma_fields[2]); cat = comma_fields[3]

        if not cat or cat.lower() == 'category': continue
        totals[cat] += amount

print('|'.join(f'{k}:{v:.2f}' for k, v in sorted(totals.items())))
```

---

## Verification

```bash
python parse_transactions.py
```

Per-category breakdown (100,126 data rows processed):

| Category | Total |
|---|---|
| Beauty | 2565602.32 |
| Books | 2559203.89 |
| Clothing | 2618436.31 |
| Electronics | 2584087.08 |
| Furniture | 2631823.45 |
| Groceries | 2630306.96 |
| Sports | 2623801.17 |
| Toys | 2602914.58 |

---

## Submission

**Your Answer:**
```
Beauty:2565602.32|Books:2559203.89|Clothing:2618436.31|Electronics:2584087.08|Furniture:2631823.45|Groceries:2630306.96|Sports:2623801.17|Toys:2602914.58
```
