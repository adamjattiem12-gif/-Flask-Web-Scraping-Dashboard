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

# Folder where all application data will be stored
DATA_FOLDER = "data"

# File paths for each type of stored data
ITEMS_FILE = os.path.join(DATA_FOLDER, "items.json")
WEBSITES_FILE = os.path.join(DATA_FOLDER, "websites.json")
HISTORY_FILE = os.path.join(DATA_FOLDER, "history.json")
STATISTICS_FILE = os.path.join(DATA_FOLDER, "statistics.json")

def ensure_data_folder():
    """
    Create the data folder if it does not already exist.

    This prevents file errors when attempting to save data.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)


# ==========================
# ITEM STORAGE
# ==========================

def load_items():

    ensure_data_folder()

    if not os.path.exists(ITEMS_FILE):
        return []

    if os.path.getsize(ITEMS_FILE) == 0:
        return []

    with open(ITEMS_FILE, "r") as file:
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
    with open(ITEMS_FILE, "w") as file:
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

    if not os.path.exists(WEBSITES_FILE) or os.path.getsize(WEBSITES_FILE) == 0:
        save_websites(default_websites)
        return default_websites

    with open(WEBSITES_FILE, "r") as file:
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
    with open(WEBSITES_FILE, "w") as file:
        json.dump(websites, file, indent=4)


# ==========================
# HISTORY STORAGE
# ==========================

def load_history():
    """
    Load the scraping history.
    """

    ensure_data_folder()

    if not os.path.exists(HISTORY_FILE):
        return []

    # If the file exists but is empty, return an empty list
    if os.path.getsize(HISTORY_FILE) == 0:
        return []

    with open(HISTORY_FILE, "r") as file:
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
    with open(HISTORY_FILE, "w") as file:
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


    STATISTICS_FILE = os.path.join(DATA_FOLDER, "statistics.json")


def load_statistics():
    ensure_data_folder()

    if not os.path.exists(STATISTICS_FILE):
        return {}

    if os.path.getsize(STATISTICS_FILE) == 0:
        return {}

    with open(STATISTICS_FILE, "r") as file:
        return json.load(file)


def save_statistics(statistics):
    ensure_data_folder()

    with open(STATISTICS_FILE, "w") as file:
        json.dump(statistics, file, indent=4)