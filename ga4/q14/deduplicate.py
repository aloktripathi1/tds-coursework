"""
deduplicate.py
Normalizes and deduplicates semi-structured address lines.
Output: unique_addresses:count
"""
import re

with open("addresses_your-student-id.txt", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip()]

unique = set()
for line in lines:
    # Strip 'Address:' prefix
    addr = re.sub(r"^Address:\s*", "", line, flags=re.IGNORECASE)
    # Strip trailing '(VALID)' or any parenthesised suffix
    addr = re.sub(r"\s*\(.*?\)\s*$", "", addr)
    # Remove commas
    addr = addr.replace(",", "")
    # Collapse whitespace and lowercase
    addr = re.sub(r"\s+", " ", addr).strip().lower()
    if addr:
        unique.add(addr)

print(f"unique_addresses:{len(unique)}")
