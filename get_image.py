import requests as req
from cairosvg import svg2png

target = "https://climbingroute.app/en/salles/lausanne-beaulieu/blocs/liste"
grade_target = "https://climbingroute.app/_assets/f3ae42a2c816b314c3ef59fb4d10d249/Icons/Grades/grimper-b-{grade}.svg"
color_target = "https://climbingroute.app/svg/1/{color}"

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

    
