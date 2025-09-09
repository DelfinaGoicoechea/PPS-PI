import os
from PIL import Image, ImageDraw


def compose_grid(image_paths, output_path, rows=3, cols=2, padding=20, background_color=(255, 255, 255)):
    """Compose images into a rows x cols grid and save as a single PNG.

    - image_paths: list of absolute file paths in reading order (row-major)
    - output_path: absolute path to save the composed PNG
    - padding: pixels between tiles and around the border
    - background_color: RGB background color
    """
    if len(image_paths) != rows * cols:
        raise ValueError(f"Expected {rows*cols} images, got {len(image_paths)}")

    images = [Image.open(p).convert("RGB") for p in image_paths]

    # Choose a common tile size. To avoid upscaling (which reduces quality),
    # use the minimum width/height across images.
    min_width = min(img.width for img in images)
    min_height = min(img.height for img in images)
    tile_size = (min_width, min_height)

    resized = [img.resize(tile_size, Image.LANCZOS) for img in images]

    # Compute canvas size: include outer padding and inner paddings between tiles
    canvas_width = padding + cols * tile_size[0] + (cols - 1) * padding + padding
    canvas_height = padding + rows * tile_size[1] + (rows - 1) * padding + padding

    canvas = Image.new("RGB", (canvas_width, canvas_height), color=background_color)

    # Paste images row-major
    idx = 0
    for r in range(rows):
        for c in range(cols):
            x = padding + c * (tile_size[0] + padding)
            y = padding + r * (tile_size[1] + padding)
            canvas.paste(resized[idx], (x, y))
            idx += 1

    # Draw divider lines centered in the gaps between tiles
    draw = ImageDraw.Draw(canvas)
    line_color = (200, 200, 200)
    line_width = 4

    # Vertical separators (between columns)
    for c in range(1, cols):
        x_sep = padding + c * tile_size[0] + (c * padding) - padding // 2
        draw.line([(x_sep, padding), (x_sep, canvas_height - padding)], fill=line_color, width=line_width)

    # Horizontal separators (between rows)
    for r in range(1, rows):
        y_sep = padding + r * tile_size[1] + (r * padding) - padding // 2
        draw.line([(padding, y_sep), (canvas_width - padding, y_sep)], fill=line_color, width=line_width)

    # Overwrite if exists; PNG doesn't meaningfully use DPI, but the pixel size stays high.
    canvas.save(output_path, format="PNG", optimize=True)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Explicit list (avoids picking up all_together.png on subsequent runs)
    ordered_files = [
        "flower_openings_grupo.png",
        "time_flower_open_grupo.png",
        "collider_entries_grupo.png",
        "time_in_collider_grupo.png",
        "sound_decrements_grupo.png",
        "time_stationary_grupo.png",
    ]

    image_paths = [os.path.join(script_dir, name) for name in ordered_files]
    missing = [p for p in image_paths if not os.path.isfile(p)]
    if missing:
        missing_names = ", ".join(os.path.basename(p) for p in missing)
        raise FileNotFoundError(f"Missing input images: {missing_names}")

    output_path = os.path.join(script_dir, "all_together.png")

    compose_grid(image_paths, output_path, rows=3, cols=2, padding=30, background_color=(255, 255, 255))
    print(f"Imagen combinada guardada en: {output_path}")


if __name__ == "__main__":
    main()


