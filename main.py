import io
import requests
import polars as pl
from PIL import Image
import matplotlib.pyplot as plt

def download_image(url: str) -> Image.Image:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    print("Downloading Mona Lisa image...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Download failed! HTTP {response.status_code}")
    img = Image.open(io.BytesIO(response.content)).convert("RGB")
    print(f"Original image size: {img.size}")
    return img

def create_pixel_dataset(img: Image.Image, width: int, height: int) -> pl.DataFrame:
    img = img.resize((width, height))
    print(f"Resized image to: {img.size}")
    pixels = [(x, y, *img.getpixel((x, y))) for y in range(height) for x in range(width)]
    df = pl.DataFrame(pixels, schema=["x", "y", "r", "g", "b"])
    print(f"Created dataset with shape: {df.shape}")
    return df

def render_canvas(df: pl.DataFrame):
    width = df["x"].max() + 1
    height = df["y"].max() + 1
    canvas = [[(0, 0, 0)] * width for _ in range(height)]
    for x, y, r, g, b in df.iter_rows():
        canvas[y][x] = (r / 255, g / 255, b / 255)

    plt.figure(figsize=(8, 12))
    plt.imshow(canvas)
    plt.axis("off")
    plt.title("Mona Lisa (High-Resolution)")
    plt.show()

def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/6/6a/Mona_Lisa.jpg"
    img = download_image(url)
    df = create_pixel_dataset(img, width=500, height=750)
    render_canvas(df)

if __name__ == "__main__":
    main()
