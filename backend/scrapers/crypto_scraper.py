import logging
import sys
import os
import requests
from datetime import datetime

# Allow running this file directly from any working directory
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from utils.cleaners import clean_items, clean_price, clean_rating

logger = logging.getLogger(__name__)


def scrape_crypto(url="https://api.coingecko.com/api/v3/coins/markets"):
    """Scrape cryptocurrencies from a CoinGecko-compatible API endpoint.

    Parameters:
        url (str): Target API endpoint. Defaults to the CoinGecko markets endpoint.
                   Pass a custom URL from the website registry to override.
    """

    # Parameters (filters for the API)
    params = {
        "vs_currency": "usd",           # Show prices in USD
        "order": "market_cap_desc",     # Sort by market cap (largest first)
        "per_page": 10                  # Get top 10 cryptos
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        logger.warning("Crypto scrape request failed: %s", exc)
        return []
    except ValueError as exc:
        logger.warning("Crypto scrape returned invalid JSON: %s", exc)
        return []

    if response.status_code != 200:
        logger.warning("Crypto scrape returned unexpected status: %s", response.status_code)
        return []

    if not isinstance(data, list):
        logger.warning("Crypto scrape response was not a list: %s", type(data).__name__)
        return []

    items = []

    # Loop through each cryptocurrency
    for i, crypto in enumerate(data):
        try:
            current_price = crypto.get('current_price', 0)
            price_value = float(current_price) if current_price is not None else 0.0
            price_display = f"${price_value:.2f}"

            item = {
                "id": crypto.get('id'),
                "name": crypto.get('name'),
                "price": clean_price(price_display),
                "price_display": price_display,
                "currency": "USD",
                "source": "CoinGecko API",
                "market": "Digital Assets",
                "scraped_at": datetime.now().isoformat(),
                "extra": {
                    "rating": clean_rating(i + 1),
                    "review_count": 0
                }
            }
            items.append(item)
        except (TypeError, ValueError, AttributeError) as exc:
            logger.warning("Skipping malformed crypto record at index %s: %s", i, exc)
            continue

    return clean_items(items)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Import storage (backend dir already on sys.path from above)
    from services.storage import (
        save_items, add_history,
        load_statistics, save_statistics, load_websites
    )

    print("Scraping crypto prices from CoinGecko...")
    cryptos = scrape_crypto()  # Uses default URL when run directly

    if cryptos:
        print(f"\nFetched {len(cryptos)} cryptocurrencies:")
        for crypto in cryptos:
            print(f"  {crypto['name']} - {crypto['price_display']} - Rank: {crypto['extra']['rating']}")

        # Save results to backend/data/items.json
        save_items(cryptos)
        print(f"\n[OK] Saved {len(cryptos)} items to backend/data/items.json")

        # Log to backend/data/history.json
        add_history({
            "timestamp": datetime.now().isoformat(),
            "scraper_type": "crypto",
            "items_found": len(cryptos),
            "success": True
        })
        print("[OK] History logged to backend/data/history.json")

        # Update backend/data/statistics.json
        stats = load_statistics()
        if not stats:
            stats = {
                "total_items": 0,
                "total_websites": 0,
                "successful_scrapes": 0,
                "failed_scrapes": 0,
                "last_scrape": "",
                "markets": {}
            }
        stats["total_items"] = len(cryptos)
        stats["total_websites"] = len(load_websites())
        stats["successful_scrapes"] = stats.get("successful_scrapes", 0) + 1
        stats["last_scrape"] = datetime.now().isoformat()
        stats["markets"]["Digital Assets"] = len(cryptos)
        save_statistics(stats)
        print("[OK] Statistics updated in backend/data/statistics.json")

    else:
        print("No data returned — check your network connection.")

        # Log the failed scrape to statistics
        from services.storage import load_statistics, save_statistics
        stats = load_statistics()
        if not stats:
            stats = {
                "total_items": 0,
                "total_websites": 0,
                "successful_scrapes": 0,
                "failed_scrapes": 0,
                "last_scrape": "",
                "markets": {}
            }
        stats["failed_scrapes"] = stats.get("failed_scrapes", 0) + 1
        save_statistics(stats)