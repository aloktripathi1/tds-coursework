from PIL import Image

# Mapping: (scrambled_row, scrambled_col) -> (original_row, original_col)
mapping = [
    (0,0, 2,1), (0,1, 1,1), (0,2, 4,1), (0,3, 0,3), (0,4, 0,1),
    (1,0, 1,4), (1,1, 2,0), (1,2, 2,4), (1,3, 4,2), (1,4, 2,2),
    (2,0, 0,0), (2,1, 3,2), (2,2, 4,3), (2,3, 3,0), (2,4, 3,4),
    (3,0, 1,0), (3,1, 2,3), (3,2, 3,3), (3,3, 4,4), (3,4, 0,2),
    (4,0, 3,1), (4,1, 1,2), (4,2, 1,3), (4,3, 0,4), (4,4, 4,0),
]

# Load scrambled image
img = Image.open("jigsaw.webp").convert("RGB")
w, h = img.size
print(f"Image size: {w}x{h}")

# Grid is 5x5, compute tile size
tile_w = w // 5
tile_h = h // 5
print(f"Tile size: {tile_w}x{tile_h}")

# Create output image
out = Image.new("RGB", (w, h))

for (scr_r, scr_c, orig_r, orig_c) in mapping:
    # Crop tile from scrambled image at (scr_r, scr_c)
    left   = scr_c * tile_w
    upper  = scr_r * tile_h
    right  = left + tile_w
    lower  = upper + tile_h
    tile = img.crop((left, upper, right, lower))

    # Paste into reconstructed image at (orig_r, orig_c)
    dest_left  = orig_c * tile_w
    dest_upper = orig_r * tile_h
    out.paste(tile, (dest_left, dest_upper))

# Convert to grayscale using ITU-R BT.709 luminance: 0.2126R + 0.7152G + 0.0722B
# Use standard floor truncation (int) as many implementations do
out_rgb = out.load()
gray_img = Image.new("L", out.size)
gray_pix = gray_img.load()
for y in range(out.size[1]):
    for x in range(out.size[0]):
        r, g, b = out_rgb[x, y]
        val = 0.2126 * r + 0.7152 * g + 0.0722 * b
        gray_pix[x, y] = int(val)   # floor/truncation

gray_img.save("output.png")
print("Saved output.png (floor truncation)")
