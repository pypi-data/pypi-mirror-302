# config.py
import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "FOLDER_NAME": "Certificates_genAI_test",
    "SAVE_PATH": r"C:\github_repos\personal_repos\micellaneous",
    "DAYS_BACK": 6,
    "ALLOWED_EXTENSIONS": [".pdf", ".xlsx"]
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
