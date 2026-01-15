from datetime import datetime
from images.images import get_hold_image, svg_to_png
from routes import get_routes_at_date, update_routes_record
from mail.send_email import send_email
from map import highlight_map, get_map, set_map_size
from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd
from util.logging import get_logger
from util.config import get_section
from lm import send_campaign

logger = get_logger("main")
LOCATION = get_section("GYM")['LOCATION']
TEMPLATE = get_section("TEMPLATES")["EMAIL_TEMPLATE_PATH"]
DEFAULT_GRADE_ORDER = ["bleu", "vert", "jaune", "orange", "rouge", "noir", "unknown"]

logger.info("Starting update process")

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(TEMPLATE)

# Update the routes record and load today's new routes
update_routes_record()
#today = datetime.today().strftime("%Y-%m-%d")
today = "2025-12-18"
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

# Get the images for holds
holds_colors = new_routes['holdsColors'].unique()
for hold_color in holds_colors:
    image_path = get_hold_image(hold_color)
    if image_path:
        images_attachements.append(image_path)

# Render the template with the routes data
html_content = template.render(routes=new_routes.to_dict(orient='records'), date=today, nb=len(new_routes), stats=stat_grades)

# Verify recipients file exists
if not os.path.exists("recipients.txt"):
    raise FileNotFoundError("Recipients file 'recipients.txt' not found.")
# Read recipients from a file
with open("recipients.txt", "r") as f:
    recipients = [line.strip() for line in f if line.strip()]


# Send the email
subject = f"Nouveaux blocs à {LOCATION} le {today} !!"
send_campaign(html_content, subject)

'''
send_email(html_content, 
    subject=f"Nouveaux blocs à {LOCATION} le {today} !!", 
    recipients=recipients,
    images=images_attachements)
'''

logger.info("Email sent!")
