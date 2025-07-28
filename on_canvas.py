import polars as pl
import matplotlib.pyplot as plt

# Load the parquet dataset
df = pl.read_parquet("monalisa_pixels_highres.parquet")

# Determine image dimensions
width = df["x"].max() + 1
height = df["y"].max() + 1

# Build canvas (height x width)
canvas = [[(0, 0, 0)] * width for _ in range(height)]

for x, y, r, g, b in df.iter_rows():
    canvas[y][x] = (r/255, g/255, b/255)

# Plot using matplotlib
plt.figure(figsize=(8, 12))
plt.imshow(canvas)
plt.axis("off")
plt.title("Mona Lisa from Polars Dataset")
plt.show()
