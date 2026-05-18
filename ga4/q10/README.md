# Q10: Google Sheets — AI Formula Extract Zip Codes

## Task

Process a personalized CSV of 100 messy addresses (`addresses_23f3003225@ds.study.iitm.ac.in.csv`) and extract the zip code for each row using an AI formula, returning "N/A" if none exists. Supply the concatenated output of all 100 rows.

---

## Requirements

* Download `addresses_23f3003225@ds.study.iitm.ac.in.csv`
* Extract the zip/postal code from each address
* If there is no zip code, output `N/A`
* Concatenate all 100 rows into a single string (using `,`)

---

## Approach

### Google Sheets Approach
If doing this natively in Google Sheets (using the TDS `workspace` `=AI()` custom function):
1. In cell `B2`: `=AI("Extract the zip code (or postal code) from this address. If none exists, return N/A: " & A2)`
2. Double click the bottom right of `B2` to fill down to `B101`
3. In cell `C2`: `=TEXTJOIN(",", TRUE, B2:B101)` 
4. Copy `C2` text.

### Programmatic Approach (Python + Gemini)
To automate this, the Python script reads the CSV, concatenates everything into a single bulk prompt, and asks the Gemini API to extract the zip codes for all 100 lines at once, returning the perfectly formatted comma-separated list.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import os, csv
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

addresses = []
with open("addresses_23f3003225@ds.study.iitm.ac.in.csv", "r") as f:
    next(csv.reader(f)) # skip header
    for row in csv.reader(f):
        if row: addresses.append(row[0])

prompt = "Extract the zip code (or postal code) from each. If none exists, return exactly 'N/A'. Return as a clean comma-separated list of exactly 100 items.\n\n"
for i, addr in enumerate(addresses):
    prompt += f"{i+1}. {addr}\n"

response = model.generate_content(prompt)
print(response.text.strip().replace('\n', ''))
```

---

## Execution

```bash
export GEMINI_API_KEY="AIzaSy..."
python solve.py
```
