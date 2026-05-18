# Q2: Excel – Z-Score Outlier Surveillance

## Task

Given weekly patient satisfaction scores across PulseCare clinics, compute the **z-score** for each clinic and count how many have `|z-score| ≥ 2.5`.

---

## Requirements

* Use `AVERAGE` and `STDEV.S` to compute mean and standard deviation
* Use `=STANDARDIZE(score, mean, stdev)` for each clinic's z-score
* Count clinics where `ABS(z-score) ≥ 2.5` using `COUNTIFS` or a helper column

---

## Approach

### 1. Import Data
Load `q-excel-zscore-outlier.csv` into Excel.

### 2. Compute Statistics
In a spare cell, calculate:
- Mean: `=AVERAGE(score_range)`
- Std Dev: `=STDEV.S(score_range)`

### 3. Compute Z-Scores
Add a helper column with `=STANDARDIZE(B2, $mean_cell, $stdev_cell)` for each clinic. Drag down.

### 4. Count Outliers
Use: `=COUNTIF(zscore_range, ">="&2.5) + COUNTIF(zscore_range, "<="&-2.5)`
or equivalently: `=COUNTIFS(ABS_col, ">="&2.5)`

---

## Code

| File | Purpose |
|---|---|
| `q-excel-zscore-outlier.csv` | Clinic satisfaction scores |

**Key Excel formulas:**
```excel
Mean:    =AVERAGE(B2:B101)
StdDev:  =STDEV.S(B2:B101)
Z-score: =STANDARDIZE(B2, $D$1, $D$2)
Count:   =COUNTIF(C2:C101,">="&2.5)+COUNTIF(C2:C101,"<="&-2.5)
```

---

## Execution

1. Open `q-excel-zscore-outlier.csv` in Excel
2. Compute `AVERAGE` and `STDEV.S` in helper cells
3. Add a z-score column using `STANDARDIZE`
4. Use `COUNTIF` to count clinics with `|z-score| ≥ 2.5`

---

## Submission

**Your Answer:**
```
<paste answer here>
```
