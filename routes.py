import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re
from util.config import get_section
from util.logging import get_logger
from pathlib import Path

logger = get_logger("routesLoader")
TARGET = get_section("URLS")['LIST_TARGET']
ROUTES_CSV_PATH = get_section("ROUTES")['CSV_PATH']

class Route:
    COLUMNS = ["liked", "topped", "commented", "grade", "color", "sector", "island", "section", "setterName", "holdsColors", "setterCode", "date"]
    
    def from_route_item(route_item):
        # Extract the data attributes
        r = {
            "liked": route_item.get("data-liked"),
            "topped": route_item.get("data-topped"),
            "commented": route_item.get("data-commented"),
            "grade": route_item.get("data-grade"),
            "color": route_item.get("data-color"),
            "sector": route_item.get("data-sector"),
            "island": 0,
            "section": 0,
            "setterCode": route_item.get("data-route-setter"),
            "date": route_item.get("data-date"),
        }

        if not r["grade"]:
            r["grade"] = "unknown"

        # Extract the setter name manually
        route_details = route_item.select_one(".route-details")
        r["setterName"] = route_details.contents[0].strip()
        match = re.search(r"(\d+)\s*-\s*(\d+)", route_details.text)
        if match:
            r['island'] = match.group(1)
            r['section'] = match.group(2)

        # Extract the holds colours manually
        holds_image = route_item.select_one(".me-1 img")
        if holds_image:
            holds_src = holds_image.get("src")
            holds_colors = holds_src.split("/")[-1]
            r["holdsColors"] = holds_colors

        return r


# Download and parse routes from the climbing route website and 
# return whether the update was successful
def update_routes_record():
    # Send a GET request to the target URL
    liste_html = req.get(TARGET)
    if liste_html.status_code != 200:
        logger.error(f"Failed to download routes, status code: {liste_html.status_code}")
        return False
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(liste_html.text, 'html.parser')

    # Extract route information
    routes = []
    for item in soup.select(".route-item"):
        r = Route.from_route_item(item)
        routes.append(r)

    # Save the new state
    df_new = pd.DataFrame(routes, columns=Route.COLUMNS)
    df_new.to_csv(ROUTES_CSV_PATH, index=False)

    logger.info(f"Routes data updated and saved to {ROUTES_CSV_PATH}")
    return True

# Get routes added at a specific date
def get_routes_at_date(date_str):
    df = get_routes()
    # Filter routes by the specified date
    new = df[df['date'] == date_str]
    return new

def get_routes():
    # Check if the file exists
    file = Path(ROUTES_CSV_PATH)
    if not file.exists():
        open(ROUTES_CSV_PATH, 'a').close()
    # Get all routes
    df = pd.read_csv(ROUTES_CSV_PATH, names=Route.COLUMNS)
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format="%Y-%m-%d")
    return df