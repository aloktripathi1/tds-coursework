# Q1: Embeddings – K-Means Clustering on Product Descriptions

## Task

Embed 50 product descriptions using `text-embedding-3-small` and run K-Means clustering (k=5) to find the cluster label (0–4) with the most items.

---

## Requirements

* Model: `text-embedding-3-small` via OpenAI Python SDK
* All 50 descriptions embedded in a single batched API call
* `KMeans(n_clusters=5, random_state=42, n_init=10)` from scikit-learn
* Script must run with `uv run solution.py`

---

## Approach

### 1. Load Descriptions
Read `product_descriptions.txt`, stripping blank lines to get exactly 50 descriptions.

### 2. Batch Embeddings
All 50 descriptions are sent in a **single API call** to `text-embedding-3-small`, producing a `(50, 1536)` embedding matrix.

### 3. K-Means Clustering
Run KMeans with the required settings, find the cluster label with the maximum item count.

---

## Code

| File | Purpose |
|---|---|
| [`solution.py`](./solution.py) | Embeds descriptions, runs KMeans, prints answer |
| [`product_descriptions.txt`](./product_descriptions.txt) | 50 product descriptions (one per line) |

**Key logic:**
```python
response = client.embeddings.create(input=descriptions, model="text-embedding-3-small")
embeddings = np.array([item.embedding for item in response.data])

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(embeddings)

unique, counts = np.unique(labels, return_counts=True)
best_label = unique[np.argmax(counts)]
best_count = counts[np.argmax(counts)]
print(f"{best_label}, {best_count}")
```

---

## Execution

```bash
export OPENAI_API_KEY=...
export OPENAI_BASE_URL=https://aipipe.org/openai/v1

uv run solution.py
```

---

## Submission

**Your Answer:**
```
2, 14
```
