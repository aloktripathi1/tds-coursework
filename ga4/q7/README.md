# Q7: JSON — Flatten nested customer orders

## Task

Stream a nested JSONL export of customer orders, flatten the `orders` and `items` arrays, and compute the total quantity of **Collaboration** items sold through **Marketplace** to customers in **North America** between **2024-03-12** and **2024-05-05**.

---

## Requirements

* Stream the file (`q-json-customer-flatten.jsonl`)
* Filter down to:
  - Region: **North America**
  - Channel: **Marketplace**
  - Category: **Collaboration**
  - Date range: **2024-03-12** through **2024-05-05**
* Sum the `quantity` of the matched line items

---

## Approach

### 1. Streaming JSONL
Used Python to stream the file line-by-line using `json.loads(line)`. This prevents out-of-memory errors for massive files.

### 2. Flattening the Hierarchy
Each `line` is a `customer`.
Inside the customer, we iterate `for order in customer.get("orders", [])`.
Inside the order, we iterate `for item in order.get("items", [])`.
This gives us "one row per item" conceptually.

### 3. Applying Filters
At each level of the hierarchy, we fail fast to save processing time:
- Customer level: skip if `region != "North America"`
- Order level: skip if `channel != "Marketplace"`
- Order level: skip if `order_date` isn't within `"2024-03-12"` and `"2024-05-05"` (lexicographical string comparison works perfectly for ISO dates)
- Item level: skip if `category != "Collaboration"`

### 4. Aggregation
If an item passes all filters, add its `quantity` to `total_quantity`.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import json

start_date = "2024-03-12"
end_date = "2024-05-05"

total_quantity = 0

with open("q-json-customer-flatten.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
            
        customer = json.loads(line)
        if customer.get("region") != "North America": continue
            
        for order in customer.get("orders", []):
            if order.get("channel") != "Marketplace": continue
            if not (start_date <= order.get("order_date", "") <= end_date): continue
                
            for item in order.get("items", []):
                if item.get("category") == "Collaboration":
                    total_quantity += item.get("quantity", 0)

print(total_quantity)
```

---

## Execution

```bash
python solve.py
```
