# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai",
#   "scikit-learn",
#   "numpy",
# ]
# ///

import os
from openai import OpenAI
from sklearn.cluster import KMeans
import numpy as np

# Load descriptions
with open("product_descriptions.txt", "r", encoding="utf-8") as f:
    descriptions = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(descriptions)} descriptions")

# Generate embeddings in a single batched call
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)

response = client.embeddings.create(
    input=descriptions,
    model="text-embedding-3-small",
)

embeddings = np.array([item.embedding for item in response.data])
print(f"Embedding matrix shape: {embeddings.shape}")

# K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(embeddings)

# Find cluster with most items
unique, counts = np.unique(labels, return_counts=True)
max_idx = np.argmax(counts)
best_label = unique[max_idx]
best_count = counts[max_idx]

print(f"\nCluster counts: {dict(zip(unique, counts))}")
print(f"\nAnswer: {best_label}, {best_count}")
