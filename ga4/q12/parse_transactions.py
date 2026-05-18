"""
parse_transactions.py
Cleans and aggregates the messy transaction CSV for ga4/q12.

Row formats present in the file:
1. Pure pipe:    TXN|Date|Amount|Category|Merchant|City[|EXTRA|JUNK]
2. Hybrid pipe:  TXN|Date,Amount|Category,Merchant|City  (4 pipe-fields)
3. Pure comma:   TXN , Date , Amount , Category , Merchant , City   (spaces OK)

Rules:
- Strip extra whitespace from every field
- Skip rows where category is empty or missing
- Ignore extra trailing fields (EXTRA, JUNK, etc.)
- Sum amounts per category; output sorted alphabetically:
  Category:Amount|Category:Amount|...
"""

from collections import defaultdict

CSV_FILE = r"transactions_your-student-id.csv"

totals = defaultdict(float)

with open(CSV_FILE, encoding="utf-8") as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue

        pipe_fields = [p.strip() for p in line.split("|")]

        # Require >= 4 pipe fields to treat as pipe-based
        if len(pipe_fields) >= 4 and pipe_fields[0].startswith("TXN"):
            if len(pipe_fields) >= 5:
                # Pure pipe: ID|Date|Amount|Category|Merchant|City|[EXTRA...]
                try:
                    amount = float(pipe_fields[2])
                    cat    = pipe_fields[3]
                except ValueError:
                    continue
            else:
                # Hybrid (4 pipe fields): ID|Date,Amount|Category,Merchant|City
                try:
                    _, amount_str = pipe_fields[1].split(",", 1)
                    cat    = pipe_fields[2].split(",", 1)[0].strip()
                    amount = float(amount_str.strip())
                except (ValueError, IndexError):
                    continue
        else:
            # Pure comma row: ID , Date , Amount , Category , Merchant , City
            comma_fields = [p.strip() for p in line.split(",")]
            if len(comma_fields) < 4:
                continue
            if comma_fields[0].lower() == "transactionid":
                continue
            try:
                amount = float(comma_fields[2])
                cat    = comma_fields[3]
            except ValueError:
                continue

        # Skip header or missing category
        if not cat or cat.lower() == "category":
            continue

        totals[cat] += amount

# Build output
result = "|".join(
    f"{cat}:{totals[cat]:.2f}"
    for cat in sorted(totals.keys())
)
print(result)
