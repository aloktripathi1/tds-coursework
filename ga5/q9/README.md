# Q9: Geospatial Analysis — Haversine Distance & Correlation

## Task
Given 30 store locations across India (`Store_ID`, `Latitude`, `Longitude`, `Monthly_Revenue`), compute the **Haversine distance** (km) from each store to the HQ in New Delhi (28.6139°N, 77.209°E), then find the **Pearson correlation** between `Distance_Km` and `Monthly_Revenue`.

---

## Requirements
* Use Haversine formula with Earth radius = **6371 km**
* Use **sample** Pearson correlation (matches Excel `CORREL`)
* Round result to 4 decimal places
* Accepted within ±5% of the correct value

---

## Approach

### 1. Load Data
Read `store_locations.csv` — columns: `Store_ID`, `Latitude`, `Longitude`, `Monthly_Revenue`.

### 2. Haversine Distance
For each store, compute great-circle distance to HQ using the Haversine formula. Converts lat/lon degrees to radians first, then applies spherical trigonometry to account for Earth's curvature.

```
a = sin²(Δlat/2) + cos(lat1)·cos(lat2)·sin²(Δlon/2)
distance = 2R · atan2(√a, √(1−a))
```

### 3. Pearson Correlation
Compute the Pearson correlation coefficient between the list of distances and the list of revenues using the standard formula:

```
r = Σ[(xᵢ − x̄)(yᵢ − ȳ)] / √[Σ(xᵢ − x̄)² · Σ(yᵢ − ȳ)²]
```

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import csv, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

HQ = (28.6139, 77.209)
distances, revenues = [], []

with open('store_locations.csv') as f:
    for row in csv.DictReader(f):
        distances.append(haversine(*HQ, float(row['Latitude']), float(row['Longitude'])))
        revenues.append(float(row['Monthly_Revenue']))

n    = len(distances)
md   = sum(distances) / n
mr   = sum(revenues)  / n
num  = sum((distances[i]-md) * (revenues[i]-mr) for i in range(n))
den  = math.sqrt(sum((d-md)**2 for d in distances) * sum((r-mr)**2 for r in revenues))
print(round(num / den, 4))
```

---

## Verification

```bash
python solve.py
```

| Metric | Value |
|--------|-------|
| Stores | 30 |
| HQ | New Delhi (28.6139, 77.209) |
| Correlation direction | Negative (stores farther from HQ → lower revenue) |
| Pearson r | **−0.3170** |

---

## Submission

**Your Answer:**
```
-0.3170
```
