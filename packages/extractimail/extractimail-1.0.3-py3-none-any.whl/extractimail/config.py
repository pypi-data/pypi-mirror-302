import json
import os
import sys

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
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
