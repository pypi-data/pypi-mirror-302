from typing import List, Optional
from math import ceil

from PIL import Image, ImageDraw

from .text_utils import *


def draw_image_grid(images: List[Image.Image],
                    cols: int,
                    captions: Optional[List[str]] = None,
                    fontsize: int = 16,
                    cell_width: Optional[int] = None,
                    border_width: int = 0):
    if captions is not None and len(captions) != len(images):
        raise ValueError(f'Number of captions ({len(captions)}) does not match number of images ({len(images)})')

    rows = int(ceil(len(images) / cols))

    width, height = images[0].size

    # Resize images, if cell width is specified
    if cell_width is not None:
        height = int(height * cell_width / width)
        width = cell_width
        images = [img.resize((width, height)) for img in images]

    width += border_width
    height += border_width

    grid = Image.new('RGB', size=(cols * width, rows * height))

    for i, img in enumerate(images):
        grid.paste(img, box=(i % cols * width, i // cols * height))

    if captions is not None:
        font = load_font(fontsize)
        captions = wrap_texts(captions, font, line_length=int(width * 0.95))
        caption_sizes = compute_texts_sizes(captions, font)

        drawing = ImageDraw.Draw(grid)

        for i, (caption, caption_size) in enumerate(zip(captions, caption_sizes)):
            row = i // cols
            col = i % cols

            x0 = width * col
            y0 = height * row
            x1 = x0 + width
            y1 = y0 + caption_size[1]
            drawing.rectangle((x0, y0, x1, y1), fill=(255, 255, 255))

            x = width * col + width / 2
            y = height * row + caption_size[1] / 2
            draw_text(caption, x, y, font, drawing)

    return grid
