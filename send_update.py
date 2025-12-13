from datetime import datetime
from get_image import *
from get_routes import get_routes_at_date
from mail.send_email import send_email
from map import highlight_map, get_map, set_map_size
from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
from util.logging import get_logger
from util.config import get_section

location = get_section("GYM")['LOCATION']

TEMPLATE = "email_template.html"

DEFAULT_GRADE_ORDER = ["bleu", "vert", "jaune", "orange", "rouge", "noir", "unknown"]

logger = get_logger("main")

logger.info("Starting update process")

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(TEMPLATE)

# Get routes
today = datetime.today().strftime("%Y-%m-%d")
new_routes = get_routes_at_date(today)

if new_routes.empty:
    logger.info("No new routes found for today")
    exit()

# Format and sort the routes
new_routes['grade'] = new_routes['grade'].str.lower()
new_routes['grade_order'] = pd.Categorical(new_routes['grade'], categories=DEFAULT_GRADE_ORDER, ordered=True)
new_routes = new_routes.sort_values('grade_order').drop(columns=['grade_order'])

# Get statistics per grade
per_grade = new_routes.groupby('grade').size().reset_index(name='count')
per_grade['grade'] = pd.Categorical(per_grade['grade'], categories=DEFAULT_GRADE_ORDER, ordered=True)
per_grade = per_grade.sort_values('grade')
stat_grades = per_grade.to_dict(orient='records')

# Get and modify the gym map SVG to highlight the sectors
images_attachements = []
new_routes['sector-section'] = new_routes.apply(lambda row: (row['sector'], int(row['section'])), axis=1)
sectors = new_routes['sector-section'].unique()
svg = get_map()

# Highlight the sectors/sections on the map
for sector in sectors:
    svg = highlight_map(svg, sector[0], sector[1])

# Set the width and height of the map for better visibility
svg = set_map_size(svg, 1020, 865)
gym_map_path = "gym_map.png"
svg_to_png(svg, gym_map_path)
images_attachements.append(gym_map_path)

# Get the images for grades and colors
grades = new_routes['grade'].unique()
colors = new_routes['holdsColors'].unique()
for grade in grades:
    if not grade:
        # Grade might be missing sometimes so skip if is the case
        continue
    img_name = f"grade_{grade}.png"
    images_attachements.append(img_name)
    img = get_grade_image(grade)
    svg_to_png(img.decode('utf-8'), img_name)

for color in colors:
    img_name = f"color_{color}.png"
    images_attachements.append(img_name)
    img = get_color_image(color)
    svg_to_png(img.decode('utf-8'), img_name)

# Render the template with the routes data
html_content = template.render(routes=new_routes.to_dict(orient='records'), date=today, nb=len(new_routes), stats=stat_grades)

# Verify recipients file exists
if not os.path.exists("recipients.txt"):
    raise FileNotFoundError("Recipients file 'recipients.txt' not found.")
# Read recipients from a file
with open("recipients.txt", "r") as f:
    recipients = [line.strip() for line in f if line.strip()]

# Send the email
send_email(html_content, 
    subject=f"Nouveaux blocs à {location} le {today} !!", 
    recipients=recipients,
    images=images_attachements)

logger.info("Email sent!")
# Cleanup the generated images
for img in images_attachements:
    os.remove(img)
