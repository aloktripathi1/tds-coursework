"""
solve_q6.py — ga4/q6: JSON Sensor roll-up analytics
Streams a JSONL file to compute the average Celsius temperature for a specific device, site, and time window.
"""
import json
from datetime import datetime, timezone

def parse_iso(ts_str):
    # e.g., "2024-07-29T22:46:40.406Z"
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    return datetime.fromisoformat(ts_str)

start_time = parse_iso("2024-07-29T22:46:40.406Z")
end_time = parse_iso("2024-08-11T22:46:40.406Z")

total_temp_c = 0.0
count = 0

with open("q-json-sensor-rollup.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        record = json.loads(line)
        
        # 1. Filter to site Lab-East
        if record.get("site") != "Lab-East":
            continue
            
        # 2. Filter to device starting with 'compressor'
        if not record.get("device_id", "").startswith("compressor"):
            continue
            
        # 3. Exclude status 'maintenance' or 'offline'
        status = record.get("status", "")
        if status in ("maintenance", "offline"):
            continue
            
        # 4. Restrict time window
        ts_str = record.get("timestamp")
        if not ts_str:
            continue
        try:
            ts = parse_iso(ts_str)
        except ValueError:
            continue
            
        if not (start_time <= ts <= end_time):
            continue
            
        # 5. Get temperature and convert if Fahrenheit
        metrics = record.get("metrics", {})
        temp = metrics.get("temperature")
        unit = metrics.get("unit", "C")
        
        if temp is None:
            continue
            
        if unit == "F" or unit == "Fahrenheit":
            temp_c = (temp - 32) * 5.0 / 9.0
        else:
            temp_c = temp
            
        total_temp_c += temp_c
        count += 1

if count > 0:
    avg = total_temp_c / count
    print(f"Records matched: {count}")
    print(f"Average temp   : {avg:.2f}°C")
else:
    print("No records matched the criteria.")
