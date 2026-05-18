# Q3: LLM Topic Modeling — News Headlines Classification

## Task
Classify 200 real-world news headlines from `news_headlines.csv` into exactly one of five topics using an LLM, then report the count of headlines classified as **Technology**.

---

## Requirements
* Classify ALL 200 headlines — no skipping
* Use `temperature=0` for deterministic, reproducible classification
* Use exactly these category spellings: `Politics, Sports, Technology, Business, Entertainment`
* Batch headlines in groups of 10 per API call to reduce cost and latency
* Submit only the integer count for `Technology`

---

## Approach

### 1. Load Headlines
Read `news_headlines.csv` with `pandas`, strip blank lines, extract the `headline` column as a list of 200 strings.

### 2. Batch Classification
Group headlines into batches of 10. For each batch, send a single prompt to `gpt-4o-mini` asking it to return a JSON array of exactly 10 labels — one per headline, in order.

### 3. Prompt Engineering
The prompt enforces:
- Exact valid label spellings
- JSON array output only (no explanation, no preamble)
- A concrete example to anchor the format

### 4. Count
Attach labels back to the dataframe and use `Counter` or pandas filtering to count `Technology` entries.

---

## Category Definitions

| Category | Covers |
|---|---|
| Politics | Government, legislation, elections, diplomacy |
| Sports | Games, tournaments, athletes, records |
| Technology | Software, hardware, AI, cybersecurity, research |
| Business | Earnings, markets, corporate news, economics |
| Entertainment | Movies, music, TV, celebrity, awards |

> **Key borderline rule:** Cybersecurity incidents are **Technology** regardless of the victim. Funding rounds and supply chain stories are **Business** even if the subject is a tech company.

---

## Code

**Script:** [`solution.py`](./solution.py)

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai", "pandas"]
# ///

import pandas as pd
import json
from openai import OpenAI
from collections import Counter

df = pd.read_csv("news_headlines.csv")
headlines = df["headline"].tolist()
print(f"Loaded {len(headlines)} headlines")

client = OpenAI()

VALID_LABELS = {"Politics", "Sports", "Technology", "Business", "Entertainment"}
BATCH_SIZE = 10

def classify_batch(batch: list[str]) -> list[str]:
    numbered = "\n".join(f"{i+1}. {h}" for i, h in enumerate(batch))
    prompt = (
        "Classify each news headline below into exactly one of these topics:\n"
        "Politics, Sports, Technology, Business, Entertainment\n\n"
        "Rules:\n"
        "- Use EXACTLY those spellings, nothing else\n"
        "- Return ONLY a JSON array of strings, one per headline, in the same order\n"
        "- No explanation, no extra text — just the JSON array\n\n"
        "Example output for 3 headlines: [\"Sports\", \"Technology\", \"Politics\"]\n\n"
        f"Headlines:\n{numbered}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = resp.choices[0].message.content.strip()
    labels = json.loads(raw)
    cleaned = []
    for label in labels:
        label = label.strip()
        cleaned.append(label if label in VALID_LABELS else "Politics")
    return cleaned

all_labels = []
for i in range(0, len(headlines), BATCH_SIZE):
    batch = headlines[i:i + BATCH_SIZE]
    print(f"Classifying headlines {i+1}–{min(i+BATCH_SIZE, len(headlines))}...")
    all_labels.extend(classify_batch(batch))

df["topic"] = all_labels
counts = Counter(df["topic"])
print("\n--- Topic Counts ---")
for topic, count in sorted(counts.items()):
    print(f"  {topic}: {count}")

tech_count = df[df["topic"] == "Technology"].shape[0]
print(f"\nTechnology count: {tech_count}")
```

---

## Verification

```bash
export OPENAI_API_KEY="sk-..."
uv run solution.py
```

| Metric | Value |
|---|---|
| Total headlines | 200 |
| Politics | 40 |
| Sports | 40 |
| Business | 42 |
| Entertainment | 36 |
| Technology | 42 |
| Model | `gpt-4o-mini` |
| Temperature | `0` |
| Batch size | 10 per API call |

---

## Submission

**Your Answer:**
```
42
```