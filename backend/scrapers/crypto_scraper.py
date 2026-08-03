import logging
import sys
import os
import time
import requests
from datetime import datetime

# Allow running this file directly from any working directory
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from services.storage import (
    save_items,
    load_items,
    add_history,
    load_websites,
    load_statistics,
    save_statistics
)
from routes.display import set_current_items
from utils.cleaners import clean_items, clean_price, clean_rating
from utils.exceptions import ScraperError

logger = logging.getLogger(__name__)


def scrape_crypto(url="https://api.coinpaprika.com/v1/tickers"):
    """Scrape cryptocurrencies from the CoinPaprika API."""

    data = None

    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 429:
                response.raise_for_status()

            if response.status_code >= 500:
                response.raise_for_status()

            if response.status_code >= 400:
                raise ScraperError(
                    "Digital Assets",
                    url,
                    f"HTTP_ERROR_{response.status_code}",
                    status_code=response.status_code
                )

            data = response.json()
            break

        except (requests.Timeout, requests.ConnectionError) as exc:
            logger.warning(
                "Crypto scrape attempt %s failed with connection error: %s",
                attempt,
                exc
            )

            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Digital Assets", url, "CONNECTION_ERROR")

        except requests.RequestException as exc:
            logger.warning(
                "Crypto scrape attempt %s failed with HTTP error: %s",
                attempt,
                exc
            )

            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Digital Assets", url, "HTTP_SERVER_ERROR")

        except ValueError:
            raise ScraperError("Digital Assets", url, "INVALID_JSON")

    if data is None:
        raise ScraperError("Digital Assets", url, "MAX_RETRIES_EXCEEDED")

    if not isinstance(data, list):
        raise ScraperError("Digital Assets", url, "INVALID_RESPONSE_FORMAT")

    items = []

    for i, crypto in enumerate(data[:10]):

        try:
            usd = crypto.get("quotes", {}).get("USD", {})
            current_price = usd.get("price", 0)

            price_value = float(current_price) if current_price is not None else 0.0
            price_display = f"${price_value:.2f}"

            item = {
                "id": crypto.get("id"),
                "name": crypto.get("name"),
                "price": clean_price(price_display),
                "price_display": price_display,
                "currency": "USD",
                "source": "CoinPaprika API",
                "market": "Digital Assets",
                "scraped_at": datetime.now().isoformat(),
                "extra": {
                    "rating": clean_rating(i + 1),
                    "review_count": 0,
                    "change_24h": usd.get("percent_change_24h", 0),
                    "volume_24h": usd.get("volume_24h", 0)
                }
            }

            items.append(item)

        except (TypeError, ValueError, AttributeError) as exc:
            logger.warning(
                "Skipping malformed crypto record at index %s: %s",
                i,
                exc
            )

    return clean_items(items)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    print("Scraping crypto prices from CoinPaprika...")

    cryptos = scrape_crypto()

    if cryptos:

        # Load existing items
        existing_items = load_items()

        # Append new crypto items
        all_items = existing_items + cryptos

        # Save everything
        save_items(all_items)
        set_current_items(all_items)
        # Load statistics
        statistics = load_statistics()

        if not statistics:
            statistics = {}

        # Keep your existing JSON format
        statistics["total_items"] = len(all_items)
        statistics["total_websites"] = len(load_websites())
        statistics["successful_scrapes"] = statistics.get("successful_scrapes", 0) + 1
        statistics["last_scrape"] = datetime.now().isoformat()

        # Keep compatibility with your dashboard
        statistics["active_sites"] = statistics["total_websites"]

        total = statistics["successful_scrapes"] + statistics.get("failed_scrapes", 0)

        if total > 0:
            statistics["success_rate"] = round(
                (statistics["successful_scrapes"] / total) * 100,
                2
            )

        # Preserve existing markets
        if "markets" not in statistics:
            statistics["markets"] = {}

        statistics["markets"]["Digital Assets"] = {
            "item_count": len(cryptos),
            "avg_price": sum(item["price"] for item in cryptos) / len(cryptos),
            "last_updated": datetime.now().isoformat()
        }

        save_statistics(statistics)

        add_history({
            "timestamp": datetime.now().isoformat(),
            "target": "https://api.coinpaprika.com/v1/tickers",
            "market": "Digital Assets",
            "items_found": len(cryptos),
            "status": "Success"
        })

        print(f"\nSaved {len(cryptos)} cryptocurrencies to items.json")
        print(f"Total items in storage: {len(all_items)}")

    else:
        print("No cryptocurrencies found.")