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
    """
    Load all stored items from items.json.

    Returns:
        list: A list of stored items.
        Returns an empty list if the file does not exist.
    """

    # Make sure the data folder exists
    ensure_data_folder()

    # If no items have been saved yet, return an empty list
    if not os.path.exists(ITEMS_FILE):
        return []

    # Open the JSON file and return its contents
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
    """
    Load all registered websites.

    If the websites file does not exist, create it with
    the default registered websites.
    """

    # Ensure the data folder exists
    ensure_data_folder()

    # Create the websites file if it does not exist
    if not os.path.exists(WEBSITES_FILE):

        # Default websites available when the application starts
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

        # Save the default websites
        save_websites(websites)

        # Return the default website list
        return websites

    # Load and return the saved websites
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
    Load the scraping history from history.json.

    Returns:
        list: A list of previous scrape records.
        Returns an empty list if no history exists.
    """

    # Ensure the data folder exists
    ensure_data_folder()

    # Return an empty list if the history file does not exist
    if not os.path.exists(HISTORY_FILE):
        return []

    # Load and return the history records
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