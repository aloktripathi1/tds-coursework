# Q13: Shell — Extract and Flatten Nested JSON from Multiple Files

## Task

Extract a ZIP archive of 50+ JSON files from a simulated API, navigate the nested `metrics.level` field, and count how many records exist at each level (1–10).

---

## Requirements

* Extract all JSON files from the ZIP
* Read the nested `metrics.level` field from every record
* Count records per level
* Output: `level1:count|level2:count|...` (sorted by level number)

---

## Approach

### 1. ZIP Structure
The archive contains **76 JSON files** (`file_0.json` … `file_75.json`). Each file is a JSON **array** of user records.

### 2. Record Structure
```json
{
  "id": "...",
  "profile": { ... },
  "metrics": { "score": 34, "level": 5 }
}
```
Target field: `record["metrics"]["level"]` (integer 1–10)

### 3. Aggregation
- Open ZIP directly with `zipfile` (no disk extraction needed)
- Iterate all `.json` files, parse each, collect `metrics.level`
- Count with `defaultdict(int)`, sort by level key

---

## Code

**Script:** [`parse_json.py`](./parse_json.py)

```python
import zipfile, json
from collections import defaultdict

counts = defaultdict(int)
with zipfile.ZipFile("api_data_your-student-id.zip") as z:
    for name in z.namelist():
        if not name.endswith(".json"): continue
        for rec in json.loads(z.read(name)):
            level = rec.get("metrics", {}).get("level")
            if level is not None:
                counts[int(level)] += 1

print("|".join(f"level{k}:{counts[k]}" for k in sorted(counts)))
```

---

## Verification

```bash
python parse_json.py
```

Level distribution (across all 76 files):

| Level | Count |
|---|---|
| 1 | 54 |
| 2 | 74 |
| 3 | 64 |
| 4 | 63 |
| 5 | 73 |
| 6 | 67 |
| 7 | 54 |
| 8 | 64 |
| 9 | 69 |
| 10 | 59 |

---

## Submission

**Your Answer:**
```
level1:54|level2:74|level3:64|level4:63|level5:73|level6:67|level7:54|level8:64|level9:69|level10:59
```
