import requests as req
from cairosvg import svg2png
from listmonk.lm import get_all_media, upload_media
from util.config import get_section
from util.logging import get_logger
from pathlib import Path

logger = get_logger("imageLoader")
urls_config = get_section("URLS")

def check_hold_image_uploaded(hold_color):
    image_name = f"color_{hold_color}.png"
    all_media = get_all_media()
    for media in all_media:
        if media["filename"] == image_name:
            return True
    return False

def check_or_upload_hold_image(hold_color):
    # If the image is already uploaded, do nothing
    if check_hold_image_uploaded(hold_color):
        return False
    
    # Download the image
    image_path = get_hold_image(hold_color)
    if image_path is None:
        logger.error(f"Could not download image for hold color {hold_color}")
        return False
    
    # Upload the image
    data = upload_media(image_path)
    logger.info(f"Uploaded image for hold color {hold_color} with media ID {data['id']} and name {data['filename']}")

    # Delete the local image file
    Path(image_path).unlink()
    return True

def get_hold_color_image_url(hold_color):
    return f"{urls_config["LM_BASE_URL"]}/uploads/color_{hold_color}.png"


# Return the path of the hold image based on the hold color
# download the image if it does not exist locally
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