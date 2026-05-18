# Q7: Outlier Detection with Z-Score Method

## Task
Given 200 delivery time records (single column `Delivery_Minutes`), compute a Z-score for each record and count how many have an **absolute Z-score greater than 2** (i.e., |Z| > 2).

---

## Requirements
* Use **sample standard deviation** (divides by n−1) — matches Excel's `STDEV`, Python's `statistics.stdev()`
* Z-score formula: `Z = (value − mean) / stdev`
* Flag condition: `|Z| > 2` (strictly greater than, not ≥)
* Submit a single integer count

---

## Approach

### 1. Load Data
Read `delivery_times.csv` and extract the `Delivery_Minutes` column as a list of floats.

### 2. Compute Mean and Sample StDev
Use sample standard deviation (n−1) — not population (n). This gives a slightly larger, more conservative spread estimate appropriate for a data sample.

### 3. Z-Score Each Value
For every delivery time, apply: `Z = (value − mean) / stdev`

### 4. Count Outliers
Count values where `abs(Z) > 2`. The absolute value catches both unusually fast **and** unusually slow deliveries.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import csv, statistics

vals = []
with open('delivery_times.csv') as f:
    for row in csv.DictReader(f):
        vals.append(float(row['Delivery_Minutes']))

mean  = statistics.mean(vals)
stdev = statistics.stdev(vals)   # sample stdev (n-1) — matches Excel STDEV

outliers = sum(1 for v in vals if abs((v - mean) / stdev) > 2)
print(outliers)
```

---

## Verification

```bash
python solve.py
```

| Metric | Value |
|--------|-------|
| Total records | 200 |
| Mean delivery time | 49.25 min |
| Sample StDev | 8.78 min |
| Outliers (\|Z\| > 2) | **9** |

---

## Submission

**Your Answer:**
```
9
```
