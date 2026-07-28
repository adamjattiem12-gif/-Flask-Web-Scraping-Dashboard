"""
Item model.

Represents a single scraped product before it is stored.
This model defines the structure that every scraped item
should follow throughout the application.
"""

from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any


@dataclass
class Item:
    id: Optional[Any]           # string for crypto, int for ecommerce
    name: str
    price: float
    price_display: str
    currency: str
    source: str
    market: str
    scraped_at: str
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert the Item object into a dictionary."""
        return asdict(self)