# config.py
import json
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.path.expanduser('~'), 'extractimail.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Store config.json in the user's home directory
CONFIG_FILE = os.path.join(os.path.expanduser('~'), 'extractimail_config.json')

DEFAULT_CONFIG = {
    "FOLDER_NAME": "Inbox",
    "SAVE_PATH": os.path.join(os.path.expanduser('~'), 'ExtractedAttachments'),
    "DAYS_BACK": 6,
    "SCHEDULE_DAY": "FRI",
    "SCHEDULE_TIME": "11:00"
}

def load_config():
    logging.debug("Loading configuration.")
    if not os.path.exists(CONFIG_FILE):
        logging.info("Configuration file not found. Creating default configuration.")
        save_config(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            logging.debug(f"Configuration loaded: {config}")
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise

def save_config(config_data):
    logging.debug(f"Saving configuration: {config_data}")
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        logging.info("Configuration saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save configuration: {e}")
        raise
