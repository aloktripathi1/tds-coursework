# Q8: JSON — Parse partial or corrupted JSON data

## Task

Recover aggregating sales data from an OCR-digitized JSONL file (`q-parse-partial-json.jsonl`) containing 100 rows. The data is damaged (truncated at the end), meaning standard JSON parsers will fail. Extract the `sales` value from each row and compute the total sum.

---

## Requirements

* Read `q-parse-partial-json.jsonl` (100 rows)
* Handle truncated JSON strings where the `id` field or closing braces are missing
* Extract the numeric value for the `sales` key
* Sum the `sales` across all 100 rows

---

## Approach

### Regex-Based Extraction
Because the JSON strings end abruptly (e.g., `..., "sales": 123.45, "id`), calling `json.loads(line)` raises a `requests.exceptions.JSONDecodeError` or `ValueError`. 

Instead of trying to repair the JSON string structurally (which is fragile if strings end mid-word), we can bypass the JSON parser entirely and use Regular Expressions (regex) to extract the known field.

1. **Pattern Matching:** `r'"sales"\s*:\s*([0-9.]+)'`
   - `"sales"`: Matches the literal string key.
   - `\s*:\s*`: Matches the colon, ignoring any surrounding whitespace.
   - `([0-9.]+)`: Captures one or more digits and/or decimal points (the numeric value).
2. **Extraction & Aggregation:** Map the captured string to a `float` and add it to our running `total_sales`.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import re

total_sales = 0.0

with open("q-parse-partial-json.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
            
        # Extract the numeric value following the "sales" key
        match = re.search(r'"sales"\s*:\s*([0-9.]+)', line)
        if match:
            total_sales += float(match.group(1))

print(total_sales)
```

---

## Execution

```bash
python solve.py
```
