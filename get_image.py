from bs4 import BeautifulSoup
import requests as req
from cairosvg import svg2png

target = "https://climbingroute.app/en/salles/lausanne-beaulieu/blocs/liste"
grade_target = "https://climbingroute.app/_assets/f3ae42a2c816b314c3ef59fb4d10d249/Icons/Grades/grimper-b-{grade}.svg"
color_target = "https://climbingroute.app/svg/1/{color}"

def get_map_svg():
    # Send a GET request to the target URL
    blocs_liste = req.get(target)
    assert blocs_liste.status_code == 200

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(blocs_liste.text, 'html.parser')

    svg = soup.find("svg", {"id": "Calque_1"})

    return str(svg)

def modify_svg_for_sector(svg_content, sector_id):
    soup = BeautifulSoup(svg_content, 'html.parser')

    sector = soup.find(id=sector_id)
    sector["style"] = "fill:#FF0000;"

    return str(soup)

def set_svg_size(svg_content, width, height):
    soup = BeautifulSoup(svg_content, 'html.parser')
    svg_tag = soup.find("svg")
    svg_tag["width"] = str(width)
    svg_tag["height"] = str(height)
    return str(soup)

def get_grade_image(grade):
    if grade == "unknown":
        with open("grade_unknown.svg", "rb") as f:
            return f.read()
    # Send a GET request to the target URL
    grade_url = grade_target.format(grade=grade)
    grade_svg = req.get(grade_url)
    assert grade_svg.status_code == 200

    return grade_svg.content

def get_color_image(color):
    color_url = color_target.format(color=color)
    color_svg = req.get(color_url)
    assert color_svg.status_code == 200

    return color_svg.content

def svg_to_png(svg_content, output_path):
    svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_path)

    
