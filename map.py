from cairo import Path
import requests
from bs4 import BeautifulSoup
from images.images import svg_to_png
from listmonk.lm import delete_media, get_all_media, get_media, upload_media
from util.logging import get_logger
from util.config import get_section

logger = get_logger("mapLogger")
MAP_PATH = get_section("IMAGES")['MAP_PATH']

class GymMap:
    def __init__(self, sectors, png_width=1020, png_height=865):
        self.sectors = sectors
        self.blank_svg = get_blank_map_svg()
        self.png_width = png_width
        self.png_height = png_height

    def create_highlighted_map(self):
        svg = self.blank_svg
        for sector in self.sectors:
            svg = highlight_map(svg, sector[0], sector[1])
        return svg
    
    def upload_map(self, output_path="gym_map.png"):
        svg = self.create_highlighted_map()
        svg = set_map_size(svg, self.png_width, self.png_height)
        svg_to_png(svg, output_path)
        update_gym_map(output_path)
        # Delete the png file after upload
        Path(output_path).unlink()
    
    def get_map_url(self):
        media_id = get_map_media_id()
        if media_id is None:
            return None
        media = get_media(media_id)
        return media["url"]

def set_map_size(svg_content, width, height):
    soup = BeautifulSoup(svg_content, 'html.parser')
    svg_tag = soup.find("svg")
    svg_tag["width"] = str(width)
    svg_tag["height"] = str(height)
    return str(soup)

def highlight_sector(soup, sector_id):
    sectors = soup.find(id="sectors")
    if not sectors:
        logger.error("No sectors element found for highlighting")
        return soup

    sector = sectors.find(id=sector_id)
    if not sector:
        logger.warning(f"No sector {sector_id} found for highlighting")
        return soup
    sector["style"] = "fill:#ff0000;"
    return soup

def highlight_map(content, sector_id, section):
    soup = BeautifulSoup(content, 'html.parser')

    if not sector_id:
        logger.warning("No sector id provided for highlighting")
        return str(soup)
    
    # If section is 0, highlight the whole sector
    if section == 0:
        return str(highlight_sector(soup, sector_id))

    sections = soup.find(id="sections")
    if not sections:
        logger.error("No sections element found for highlighting")
        return str(highlight_sector(soup, sector_id))
    
    section = sections.find(id=section)
    if not section:
        logger.error(f"No section {section} found for highlighting")
        return str(highlight_sector(soup, sector_id))
    
    section["style"] = "fill:rgba(255,0,0,.5)"
    return str(soup)

def get_map():
    with open(MAP_PATH, "rb") as f:
        return f.read()
    
def get_map_media_id():
    all_media = get_all_media()
    for media in all_media:
        if media["filename"] == "gym_map.png":
            return media["id"]
    return None

def get_default_map_id():
    all_media = get_all_media()
    for media in all_media:
        if media["filename"] == "default_map.svg":
            return media["id"]
    return None

def get_blank_map_svg():
    id = get_default_map_id()
    if id is None:
        # TODO: download default map SVG from a URL and upload it
        logger.error("No default map SVG found in media")
        return None
    media = get_media(id)
    url = media["url"]
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content

def update_gym_map(gym_map_path):
    # Delete existing gym map media
    gym_map_id = get_map_media_id()
    if gym_map_id is not None:
        delete_media(gym_map_id)

    # Upload new gym map
    data = upload_media(gym_map_path)
    logger.info(f"Uploaded new gym map with media ID {data['id']} and name {data['filename']}")
