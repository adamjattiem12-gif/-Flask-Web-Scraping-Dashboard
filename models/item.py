"""
Item model.

Represents a single scraped product before it is stored.
This model defines the structure that every scraped item
should follow throughout the application.
"""

# Import dataclass to easily create a class for storing data
# Import asdict to convert an Item object into a dictionary
from dataclasses import dataclass, asdict


# The @dataclass decorator automatically generates
# the constructor (__init__) and other useful methods
@dataclass
class Item:

    # Name of the scraped product
    name: str

    # Price of the product
    price: float

    # Currency the price is displayed in (e.g., ZAR, USD)
    currency: str

    # Website where the product was scraped from
    source: str

    # Market or category the product belongs to
    # Example: South Africa, E-Commerce, Crypto
    market: str

    # Direct link to the product page
    url: str

    # Date and time the product was scraped
    timestamp: str

    # Convert the Item object into a dictionary
    # This makes it easy to save the item as JSON
    def to_dict(self):
        """Convert the Item object into a dictionary."""
        return asdict(self)