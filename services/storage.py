"""
Storage layer.

This file is responsible for saving and loading the application's data.
Instead of using a database, the application stores data in JSON files.

It manages three types of data:
- Items (scraped products)
- Websites (registered websites to scrape)
- History (records of previous scraping sessions)
"""

# Import the json module to read and write JSON files
import json

# Import os to work with folders and file paths
import os
from pathlib import Path

# Make storage paths relative to the repository root rather than the current
# working directory, so scraper runs from any folder still write to the same
# data files.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"

# File paths for each type of stored data
ITEMS_FILE = DATA_FOLDER / "items.json"
WEBSITES_FILE = DATA_FOLDER / "websites.json"
HISTORY_FILE = DATA_FOLDER / "history.json"
STATISTICS_FILE = DATA_FOLDER / "statistics.json"

def ensure_data_folder():
    """
    Create the data folder if it does not already exist.

    This prevents file errors when attempting to save data.
    """
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================
# ITEM STORAGE
# ==========================

def load_items():

    ensure_data_folder()

    if not ITEMS_FILE.exists():
        return []

    if ITEMS_FILE.stat().st_size == 0:
        return []

    with ITEMS_FILE.open("r") as file:
        return json.load(file)


def save_items(items):
    """
    Save a list of scraped items to items.json.

    Parameters:
        items (list): A list containing scraped products.
    """

    # Ensure the data folder exists
    ensure_data_folder()

    # Save the items as formatted JSON
    with ITEMS_FILE.open("w") as file:
        json.dump(items, file, indent=4)


# ==========================
# WEBSITE STORAGE
# ==========================

def load_websites():
    ensure_data_folder()

    default_websites = [
    {
        "name": "WebScraper E-Commerce Sandbox",
        "url": "https://webscraper.io/test-sites/e-commerce/allinone",
        "market": "E-Commerce"
    },
    {
        "name": "CoinGecko",
        "url": "https://www.coingecko.com/",
        "market": "Cryptocurrency"
    }
]

    if not WEBSITES_FILE.exists() or WEBSITES_FILE.stat().st_size == 0:
        save_websites(default_websites)
        return default_websites

    with WEBSITES_FILE.open("r") as file:
        return json.load(file)


def save_websites(websites):
    """
    Save all registered websites to websites.json.

    Parameters:
        websites (list): A list of registered websites.
    """

    # Ensure the data folder exists
    ensure_data_folder()

    # Save the website list as formatted JSON
    with WEBSITES_FILE.open("w") as file:
        json.dump(websites, file, indent=4)


# ==========================
# HISTORY STORAGE
# ==========================

def load_history():
    """
    Load the scraping history.
    """

    ensure_data_folder()

    if not HISTORY_FILE.exists():
        return []

    # If the file exists but is empty, return an empty list
    if HISTORY_FILE.stat().st_size == 0:
        return []

    with HISTORY_FILE.open("r") as file:
        return json.load(file)


def save_history(history):
    """
    Save the complete scraping history.

    Parameters:
        history (list): A list of scrape history records.
    """

    # Ensure the data folder exists
    ensure_data_folder()

    # Save the history records as formatted JSON
    with HISTORY_FILE.open("w") as file:
        json.dump(history, file, indent=4)


def add_history(record):
    """
    Add a single scraping record to the history.

    Parameters:
        record (dict): Information about one scraping session,
        such as timestamp, target website, number of items found,
        and whether the scrape was successful.
    """

    # Load the existing history records
    history = load_history()

    # Add the new record to the history list
    history.append(record)

    # Save the updated history back to the JSON file
    save_history(history)


def load_statistics():
    ensure_data_folder()

    if not STATISTICS_FILE.exists():
        return {}

    if STATISTICS_FILE.stat().st_size == 0:
        return {}

    with STATISTICS_FILE.open("r") as file:
        return json.load(file)


def save_statistics(statistics):
    ensure_data_folder()

    with STATISTICS_FILE.open("w") as file:
        json.dump(statistics, file, indent=4)