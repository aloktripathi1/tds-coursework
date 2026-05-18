"""
solve_q8.py — ga4/q8: Parse partial JSON
Reads a JSONL file with truncated/damaged lines and extracts the "sales" value using regex.
"""
import re

total_sales = 0.0
count = 0

with open("q-parse-partial-json.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        # The line looks like: {"city": "...", "product": "...", "sales": 123.45, "id": ... (truncated)
        # Or {"city": "...", "product": "...", "sales": 123
        
        # Regular expression to find the "sales" key and its numeric value
        # Matches "sales": optionally followed by spaces, then digits optionally with a decimal
        match = re.search(r'"sales"\s*:\s*([0-9.]+)', line)
        if match:
            sales_val = float(match.group(1))
            total_sales += sales_val
            count += 1
        else:
            print(f"Warning: Could not find 'sales' in line: {line}")

print(f"Total rows parsed: {count}")
print(f"Total sales      : {total_sales}")
