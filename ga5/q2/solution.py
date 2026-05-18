# /// script
# requires-python = ">=3.11"
# dependencies = ["sentence-transformers", "Pillow", "numpy"]
# ///

import clip
import torch
from PIL import Image
import os
import numpy as np

TEXT_QUERY = "tall coastal lighthouse beacon on a rocky ocean cliff"

# Load CLIP model (ViT-B/32 = clip-ViT-B-32)
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load all 10 images
image_files = sorted([f for f in os.listdir(".") if f.startswith("img_") and f.endswith(".jpg")])
print(f"Found images: {image_files}")

# Encode text
text_tokens = clip.tokenize([TEXT_QUERY]).to(device)
with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

# Encode images and compute cosine similarity
print("\nSimilarity scores:")
scores = []
for fname in image_files:
    img = preprocess(Image.open(fname)).unsqueeze(0).to(device)
    with torch.no_grad():
        img_features = model.encode_image(img)
        img_features = img_features / img_features.norm(dim=-1, keepdim=True)
    score = (text_features @ img_features.T).item()
    scores.append(score)
    print(f"  {fname}: {score:.4f}")

best_idx = int(np.argmax(scores))
print(f"\nBest match: {image_files[best_idx]} (score: {scores[best_idx]:.4f})")
