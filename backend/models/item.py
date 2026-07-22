"""
Item model.

Represents a single scraped product waiting to be stored.
""" 

from dataclasses import dataclass, asdict


@dataclass
class Item:
    name: str
    price: float
    currency: str
    source: str
    market: str
    url: str
    timestamp: str

    def to_dict(self):
        """Convert the Item object into a dictionary."""
        return asdict(self)