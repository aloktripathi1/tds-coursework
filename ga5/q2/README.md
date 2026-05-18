# Q2: Multimodal Embeddings – CLIP Image Search

## Task

Use CLIP (`clip-ViT-B-32`) to find the image most similar to a text query using cosine similarity.

**Text query:** `"tall coastal lighthouse beacon on a rocky ocean cliff"`

---

## Requirements

* Model: `clip-ViT-B-32` (OpenAI CLIP ViT-B/32)
* Cosine similarity between text and each of 10 images
* Submit the filename with the highest score

---

## Approach

### 1. Load Model
Used OpenAI's `clip` package with `ViT-B/32`. Text and image embeddings are L2-normalised before comparison.

### 2. Cosine Similarity
Cosine similarity = `text_features @ image_features.T` (after L2 normalisation).

**All scores:**
| Image | Score |
|-------|-------|
| img_01.jpg | 0.1767 |
| img_02.jpg | 0.1870 |
| img_03.jpg | 0.1463 |
| img_04.jpg | 0.1189 |
| img_05.jpg | 0.1917 |
| img_06.jpg | 0.1514 |
| **img_07.jpg** | **0.2966** ← highest |
| img_08.jpg | 0.1252 |
| img_09.jpg | 0.1736 |
| img_10.jpg | 0.1894 |

---

## Code

| File | Purpose |
|---|---|
| [`solution.py`](./solution.py) | Loads CLIP, computes cosine similarity, prints best match |
| `img_01.jpg` – `img_10.jpg` | 10 product images |

**Key logic:**
```python
model, preprocess = clip.load("ViT-B/32", device=device)

text_tokens = clip.tokenize([TEXT_QUERY]).to(device)
text_features = model.encode_text(text_tokens)
text_features = text_features / text_features.norm(dim=-1, keepdim=True)

img_features = model.encode_image(preprocess(img).unsqueeze(0))
img_features = img_features / img_features.norm(dim=-1, keepdim=True)

score = (text_features @ img_features.T).item()
```

---

## Execution

```bash
pip install git+https://github.com/openai/CLIP.git Pillow numpy torch

python solution.py
```

---

## Submission

**Your Answer:**
```
img_07.jpg
```
