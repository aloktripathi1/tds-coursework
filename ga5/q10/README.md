# Q10: Geospatial Analysis — Nearest Warehouse Assignment

## Task
Given 50 delivery locations across India (`Delivery_ID`, `Latitude`, `Longitude`, `Weight_Kg`), assign each delivery to its **nearest warehouse** using Haversine distance, then identify the **warehouse that handles the most deliveries**.

---

## Requirements
* Use Haversine formula with Earth radius = **6371 km**
* Three warehouses: Delhi (28.6139, 77.209), Mumbai (19.076, 72.8777), Chennai (13.0827, 80.2707)
* Assign each delivery to the single closest warehouse
* Submit warehouse name (case-insensitive) and exact delivery count

---

## Approach

### 1. Load Data
Read `deliveries.csv` — columns: `Delivery_ID`, `Latitude`, `Longitude`, `Weight_Kg`.

### 2. Compute Distance to All 3 Warehouses
For each delivery, compute the Haversine distance to every warehouse. This gives 3 distances per delivery row.

### 3. Nearest-Neighbour Assignment
Use `min()` with a key function to select the warehouse name corresponding to the smallest distance — no need to store all 3 distances explicitly.

### 4. Count Assignments
Tally how many deliveries were assigned to each warehouse. The highest count is the answer.

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

WAREHOUSES = {
    'Delhi':   (28.6139, 77.2090),
    'Mumbai':  (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707),
}

counts = {w: 0 for w in WAREHOUSES}

with open('deliveries.csv') as f:
    for row in csv.DictReader(f):
        lat, lon = float(row['Latitude']), float(row['Longitude'])
        nearest = min(WAREHOUSES, key=lambda w: haversine(lat, lon, *WAREHOUSES[w]))
        counts[nearest] += 1

winner = max(counts, key=counts.get)
print(f"{winner}, {counts[winner]}")
```

---

## Verification

```bash
python solve.py
```

| Warehouse | Deliveries Assigned |
|-----------|-------------------|
| Delhi | 19 |
| Mumbai | 5 |
| **Chennai** | **26** ← busiest |

| Metric | Value |
|--------|-------|
| Total deliveries | 50 |
| Assignment method | Haversine nearest-neighbour |
| Busiest warehouse | Chennai |
| Delivery count | 26 |

---

## Submission

**Your Answer:**
```
Chennai, 26
```
