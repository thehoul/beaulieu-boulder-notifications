import configparser

CONFIG_FILE = "config.cfg"

# Verify the configuration exists
config = configparser.ConfigParser()
if not config.read(CONFIG_FILE):
    raise FileNotFoundError(f"Configuration file {CONFIG_FILE} not found.")
# Load the configuration
config.read(CONFIG_FILE)

def get_section(section_name):
    return config[section_name]


