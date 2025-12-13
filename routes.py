import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re
from util.config import get_section
from util.logging import get_logger

logger = get_logger("imageLoader")
target = get_section("URLS")['LIST_TARGET']

def download_routes():
    # Send a GET request to the target URL
    liste_html = req.get(target)
    assert liste_html.status_code == 200

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(liste_html.text, 'html.parser')

    # Extract route information
    routes = []
    for item in soup.select(".route-item"):

        # Extract the data attributes
        r = {
            "liked": item.get("data-liked"),
            "topped": item.get("data-topped"),
            "commented": item.get("data-commented"),
            "grade": item.get("data-grade"),
            "color": item.get("data-color"),
            "sector": item.get("data-sector"),
            "island": 0,
            "section": 0,
            "setterCode": item.get("data-route-setter"),
            "date": item.get("data-date"),
        }

        if not r["grade"]:
            r["grade"] = "unknown"

        # Extract the setter name manually
        route_details = item.select_one(".route-details")
        r["setterName"] = route_details.contents[0].strip()
        match = re.search(r"(\d+)\s*-\s*(\d+)", route_details.text)
        if match:
            r['island'] = match.group(1)
            r['section'] = match.group(2)

        # Extract the holds colours manually
        holds_image = item.select_one(".me-1 img")
        if holds_image:
            holds_src = holds_image.get("src")
            holds_colors = holds_src.split("/")[-1]
            r["holdsColors"] = holds_colors

        routes.append(r)

    return routes

def get_routes_at_date(date_str):
    # Get all routes
    routes = download_routes()
    df = pd.DataFrame(routes)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Filter routes by the specified date
    new = df[df['date'] == date_str]

    return new