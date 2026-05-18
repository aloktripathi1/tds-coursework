# Q19: Reconstruct and Desaturate a Scrambled Image

## Task

Download a scrambled 5×5 jigsaw image (`jigsaw.webp`), reassemble it using the provided tile mapping, then convert the result to grayscale using the ITU-R BT.709 luminance formula and export as a lossless PNG.

---

## Requirements

* Reassemble all 25 tiles (100×100 px each) from their scrambled positions to original positions
* Apply luminance formula: `L = 0.2126·R + 0.7152·G + 0.0722·B`
* Export the grayscale image as PNG (no resizing, no lossy compression)

---

## Approach

### 1. Tile Grid
The input `jigsaw.webp` is 500×500 px divided into a 5×5 grid of 100×100 px tiles.
Each tile at `(scrambled_row, scrambled_col)` must be placed at `(original_row, original_col)`.

### 2. Reassembly
Crop each tile from the scrambled image and paste it at the correct destination in a new RGB canvas using the 25-entry mapping table.

### 3. Grayscale Conversion
Iterate every pixel of the reconstructed image and apply floor truncation:

```python
L = int(0.2126 * R + 0.7152 * G + 0.0722 * B)
```

Using `int()` (floor truncation) matches the numpy `.astype(np.uint8)` convention.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
from PIL import Image

mapping = [
    (0,0,2,1),(0,1,1,1),(0,2,4,1),(0,3,0,3),(0,4,0,1),
    (1,0,1,4),(1,1,2,0),(1,2,2,4),(1,3,4,2),(1,4,2,2),
    (2,0,0,0),(2,1,3,2),(2,2,4,3),(2,3,3,0),(2,4,3,4),
    (3,0,1,0),(3,1,2,3),(3,2,3,3),(3,3,4,4),(3,4,0,2),
    (4,0,3,1),(4,1,1,2),(4,2,1,3),(4,3,0,4),(4,4,4,0),
]

img = Image.open("jigsaw.webp").convert("RGB")
w, h = img.size          # 500x500
tw, th = w // 5, h // 5  # 100x100 tiles

out = Image.new("RGB", (w, h))
for (sr, sc, or_, oc) in mapping:
    tile = img.crop((sc*tw, sr*th, sc*tw+tw, sr*th+th))
    out.paste(tile, (oc*tw, or_*th))

out_rgb = out.load()
gray_img = Image.new("L", out.size)
gray_pix = gray_img.load()
for y in range(h):
    for x in range(w):
        r, g, b = out_rgb[x, y]
        gray_pix[x, y] = int(0.2126*r + 0.7152*g + 0.0722*b)

gray_img.save("output.png")
```

---

## Verification

```bash
python solve.py
# Image size: 500x500
# Tile size: 100x100
# Saved output.png (floor truncation)
```

Output file: `output.png` (500×500, mode L, PNG lossless)

---

## Submission

Upload **`output.png`** — the luminance-based grayscale reconstruction of the original image.
