# Q6: JSON — Sensor roll-up analytics

## Task

Stream a large JSONL telemetry file to clean and aggregate IoT sensor data. Find the average temperature (in Celsius) for `compressor` devices at `Lab-East` over a specific time window, excluding maintenance events.

---

## Requirements

* Stream the file (do not load fully into memory)
* Site: **Lab-East**
* Device ID: starts with **compressor**
* Time Window: **2024-07-29 22:46:40.406Z** to **2024-08-11 22:46:40.406Z** (UTC)
* Exclusion: `status` cannot be `maintenance` or `offline`
* Unit conversion: Convert to Celsius if recorded in Fahrenheit
* Output: Average temperature in °C rounded to 2 decimal places

---

## Approach

### 1. Streaming JSONL
Instead of `json.loads(f.read())`, iterate line by line `for line in f:` and `json.loads(line)`.

### 2. Time Filtering
Parsed the ISO timestamps using `datetime.fromisoformat` and compared against the defined boundaries in Python `datetime` objects.

### 3. Temperature Normalization
Checked the `unit` field inside the `metrics` object. If `F` or `Fahrenheit`, applied `(temp - 32) * 5/9` before adding it to the rolling sum.

### 4. Aggregation
Accumulated `total_temp_c` and `count`, dividing at the end to compute the average.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import json
from datetime import datetime

start_time = datetime.fromisoformat("2024-07-29T22:46:40.406+00:00")
end_time = datetime.fromisoformat("2024-08-11T22:46:40.406+00:00")

total_temp_c = 0.0
count = 0

with open("q-json-sensor-rollup.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        record = json.loads(line)
        
        if record.get("site") != "Lab-East": continue
        if not record.get("device_id", "").startswith("compressor"): continue
        if record.get("status") in ("maintenance", "offline"): continue
        
        ts_str = record.get("timestamp")
        if not ts_str: continue
        
        if ts_str.endswith('Z'): ts_str = ts_str[:-1] + '+00:00'
        ts = datetime.fromisoformat(ts_str)
        if not (start_time <= ts <= end_time): continue
            
        metrics = record.get("metrics", {})
        temp = metrics.get("temperature")
        unit = metrics.get("unit", "C")
        
        if temp is None: continue
        temp_c = (temp - 32) * 5/9 if unit in ("F", "Fahrenheit") else temp
            
        total_temp_c += temp_c
        count += 1

print(f"{total_temp_c / count:.2f}")
```

---

## Execution

```bash
python solve.py
```