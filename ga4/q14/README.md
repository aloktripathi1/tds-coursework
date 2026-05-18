# Q14: Shell — Deduplicate and Aggregate Semi-Structured Address Data

## Task

Process a 1287-line text file of semi-structured address data, normalize formatting variations, deduplicate, and report the count of unique addresses.

---

## Requirements

* Extract the core address from each line (strip prefix/suffix noise)
* Normalize: remove commas, collapse extra whitespace, lowercase
* Deduplicate across all formatting variants
* Output format: `unique_addresses:count`

---

## Approach

### 1. Line Formats Identified
| Format | Example |
|---|---|
| Plain (no commas) | `333 Elm Rd Northtown OH 71900` |
| Comma-separated | `635 OAK AVE, springfield, CA 71278` |
| Extra spaces | `545  Magnolia Dr,  Pineville,  MI  42324` |
| Prefixed + suffixed | `Address: 755 Ash Pl, Westchester, OH 76546 (VALID)` |

### 2. Normalization Steps
1. Strip `Address:` prefix (case-insensitive)
2. Strip trailing `(VALID)` or any `(...)` suffix
3. Remove all commas
4. Collapse multiple spaces to a single space
5. Lowercase the entire string

### 3. Deduplication
Add each normalized address to a Python `set()` — duplicates are automatically discarded. The final count is `len(set)`.

---

## Code

```python
import re
from collections import Counter

with open('addresses_your-student-id.txt', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

unique = set()
for line in lines:
    addr = re.sub(r'^Address:\s*', '', line, flags=re.IGNORECASE)
    addr = re.sub(r'\s*\(.*?\)\s*$', '', addr)
    addr = addr.replace(',', '')
    addr = re.sub(r'\s+', ' ', addr).strip().lower()
    unique.add(addr)

print(f'unique_addresses:{len(unique)}')
```

---

## Verification

```bash
python deduplicate.py
```

- Total raw lines: **1287**
- After normalization: **1287 unique addresses** (no duplicates in this dataset)

---

## Submission

**Your Answer:**
```
unique_addresses:1287
```
