import polars as pl

# ANSI color helper
def ansi_color(r, g, b, bg=False):
    return f"\033[{'48' if bg else '38'};2;{r};{g};{b}m"

# Load dataset
df = pl.read_parquet("monalisa_pixels_highres.parquet")

width = df["x"].max() + 1
height = df["y"].max() + 1

# Build 2D pixel grid
pixels = [[(0, 0, 0)] * width for _ in range(height)]
for x, y, r, g, b in df.iter_rows():
    pixels[y][x] = (r, g, b)

# Scale down factor (bigger = smaller in terminal)
scale = 5   # adjust to 4, 6, or 8 depending on your terminal width

for y in range(0, height, 2 * scale):
    line = ""
    for x in range(0, width, scale):
        top = pixels[y][x]
        bottom = pixels[y + scale][x] if y + scale < height else (0, 0, 0)
        line += ansi_color(*top, bg=False) + ansi_color(*bottom, bg=True) + "▀"
    print(line + "\033[0m")
