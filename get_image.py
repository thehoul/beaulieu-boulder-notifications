import requests as req
from cairosvg import svg2png
from util.config import get_section
from util.logging import get_logger

logger = get_logger("imageLoader")
urls_config = get_section("URLS")

def get_grade_image(grade):
    if grade == "unknown":
        with open("grade_unknown.svg", "rb") as f:
            return f.read()
        
    # Send a GET request to the target URL
    grade_url = urls_config["GRADE_TARGET"]
    grade_url = grade_url.format(grade=grade)
    grade_svg = req.get(grade_url)
    if not grade_svg.status_code == 200:
        logger.error(f"Could not load image for grade {grade}")
        return None

    return grade_svg.content

def get_color_image(color):
    color_url = urls_config["COLOR_TARGET"]
    color_url = color_url.format(color=color)
    color_svg = req.get(color_url)
    if not color_svg.status_code == 200:
        logger.error(f"Could not load image for color {color}")
        return None

    return color_svg.content

def svg_to_png(svg_content, output_path):
    svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_path)