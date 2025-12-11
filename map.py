from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("mapLogger")


MAP_PATH = "default_map.svg"

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