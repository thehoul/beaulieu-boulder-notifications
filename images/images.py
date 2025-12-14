import requests as req
from cairosvg import svg2png
from util.config import get_section
from util.logging import get_logger
from pathlib import Path

logger = get_logger("imageLoader")
urls_config = get_section("URLS")

# Return the path of the hold image based on the hold color
# download the image if it does not exit locally
def get_hold_image(color):
    image_path = f"images/color_{color}.png"
    if Path(image_path).exists():
        return image_path

    logger.info(f"Image for holds {color} were downloaded")
    return download_color_image(color, image_path)

def download_color_image(color, dst_path):
    color_url = urls_config["COLOR_TARGET"]
    color_url = color_url.format(color=color)
    color_svg = req.get(color_url)
    if not color_svg.status_code == 200:
        logger.error(f"Could not load image for color {color}")
        return None

    svg_to_png(color_svg.content.decode('utf-8'), str(dst_path))
    return dst_path

def svg_to_png(svg_content, output_path):
    svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_path)