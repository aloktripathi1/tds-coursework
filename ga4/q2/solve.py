"""
solve.py — ga4/q2: Z-Score Outlier Surveillance
Reads q-excel-zscore-outlier.csv, computes z-scores, counts |z| >= 2.5
"""
import csv
import math

scores = []
with open("q-excel-zscore-outlier.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Try common column names
        for col in row:
            try:
                val = float(row[col])
                scores.append(val)
                break
            except (ValueError, TypeError):
                continue

n = len(scores)
mean = sum(scores) / n
stdev = math.sqrt(sum((x - mean) ** 2 for x in scores) / (n - 1))  # STDEV.S

print(f"Clinics found : {n}")
print(f"Mean          : {mean:.4f}")
print(f"StdDev (S)    : {stdev:.4f}")

outliers = [(s, abs((s - mean) / stdev)) for s in scores if abs((s - mean) / stdev) >= 2.5]
print(f"\nOutliers (|z| >= 2.5): {len(outliers)}")
for score, z in sorted(outliers, key=lambda x: -x[1]):
    print(f"  score={score:.2f}  z={z:.4f}")

print(f"\nAnswer: {len(outliers)}")
