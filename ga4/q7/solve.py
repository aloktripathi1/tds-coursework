"""
solve_q7.py — ga4/q7: JSON Flatten nested customer orders
Streams a JSONL file, flattening nested orders and items to sum the quantity matching specific criteria.
"""
import json
from datetime import datetime

# Target criteria:
# Region: North America
# Channel: Marketplace
# Category: Collaboration
# Date Range: 2024-03-12 to 2024-05-05 (inclusive)

start_date = "2024-03-12"
end_date = "2024-05-05"

total_quantity = 0
processed_customers = 0

with open("q-json-customer-flatten.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        customer = json.loads(line)
        processed_customers += 1
        
        # Filter by region
        if customer.get("region") != "North America":
            continue
            
        orders = customer.get("orders", [])
        for order in orders:
            # Filter by channel
            if order.get("channel") != "Marketplace":
                continue
                
            # Filter by order date (YYYY-MM-DD comparison works lexicographically)
            order_date = order.get("order_date", "")
            if not (start_date <= order_date <= end_date):
                continue
                
            items = order.get("items", [])
            for item in items:
                # Filter by category
                if item.get("category") == "Collaboration":
                    total_quantity += item.get("quantity", 0)

print(f"Processed customers: {processed_customers}")
print(f"Total matching quantity: {total_quantity}")
