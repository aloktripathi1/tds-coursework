"""
solve_q5.py — ga4/q5: OpenRefine supplier spend consolidation
Simulates the OpenRefine cleanup steps in Pandas to find the final numeric answer.
"""
import pandas as pd
import re

# 1. Load CSV and trim whitespace on string columns
df = pd.read_csv("q-openrefine-supplier-spend.csv")
for col in df.select_dtypes(['object']).columns:
    df[col] = df[col].str.strip()

# 2. Cluster supplier names (specifically targeting Helios Robotics variants)
# OpenRefine nearest-neighbor would catch things like "Helios Robotix", "Helios-Robotics", "HELIOS ROBOTICS"
def normalize_supplier(name):
    name = str(name).upper()
    name = re.sub(r'[^A-Z]', '', name) # remove spaces and punctuation
    if 'HELIOS' in name and 'ROBOT' in name:
        return 'Helios Robotics'
    return name

df['supplier_name_clean'] = df['supplier_name'].apply(normalize_supplier)

# 3. Remove duplicate invoices (keep first)
df = df.drop_duplicates(subset=['invoice_id'], keep='first')

# 4. Clean amount_usd
def clean_money(val):
    # value.replace(/[^0-9.]/, "")
    cleaned = re.sub(r'[^0-9.]', '', str(val))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

df['amount_num'] = df['amount_usd'].apply(clean_money)

# 5. Filter: Helios Robotics, Software, Approved
mask = (
    (df['supplier_name_clean'] == 'Helios Robotics') & 
    (df['category'].str.lower() == 'software') & 
    (df['status'].str.lower() == 'approved')
)
filtered_df = df[mask]

# 6. Sum
total = filtered_df['amount_num'].sum()

print("Matching Rows:")
print(filtered_df[['invoice_id', 'supplier_name', 'category', 'status', 'amount_usd', 'amount_num']])
print(f"\nTotal Approved Software Spend for Helios Robotics: ${total:,.2f}")
