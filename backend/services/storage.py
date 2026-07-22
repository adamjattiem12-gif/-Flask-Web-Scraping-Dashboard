"""
Storage layer.

Responsible for saving and loading:
- Items
- Websites
- History
"""

import json
import os

DATA_FOLDER = "data"

ITEMS_FILE = os.path.join(DATA_FOLDER, "items.json")
WEBSITES_FILE = os.path.join(DATA_FOLDER, "websites.json")
HISTORY_FILE = os.path.join(DATA_FOLDER, "history.json")


def ensure_data_folder():
    """Create the data folder if it does not exist."""
    os.makedirs(DATA_FOLDER, exist_ok=True)


# ==========================
# ITEM STORAGE
# ==========================

def load_items():
    ensure_data_folder()

    if not os.path.exists(ITEMS_FILE):
        return []

    with open(ITEMS_FILE, "r") as file:
        return json.load(file)


def save_items(items):
    ensure_data_folder()

    with open(ITEMS_FILE, "w") as file:
        json.dump(items, file, indent=4)


# ==========================
# WEBSITE STORAGE
# ==========================

def load_websites():
    ensure_data_folder()

    if not os.path.exists(WEBSITES_FILE):

        # Default registered websites
        websites = [
            {
                "name": "Takealot",
                "url": "https://www.takealot.com",
                "market": "South Africa"
            },
            {
                "name": "Blueprint",
                "url": "https://www.blueprint.co.za",
                "market": "South Africa"
            }
        ]

        save_websites(websites)

        return websites

    with open(WEBSITES_FILE, "r") as file:
        return json.load(file)


def save_websites(websites):
    ensure_data_folder()

    with open(WEBSITES_FILE, "w") as file:
        json.dump(websites, file, indent=4)


# ==========================
# HISTORY STORAGE
# ==========================

def load_history():
    ensure_data_folder()

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    ensure_data_folder()

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def add_history(record):
    history = load_history()
    history.append(record)
    save_history(history)