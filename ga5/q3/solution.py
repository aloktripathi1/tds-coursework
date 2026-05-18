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