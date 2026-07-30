import logging
import sys
import os
import time
import requests
from urllib.parse import urlparse
from datetime import datetime

# Allow running this file directly from any working directory
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from utils.cleaners import clean_items, clean_price, clean_rating
from utils.exceptions import ScraperError

logger = logging.getLogger(__name__)


def scrape_crypto(url="https://api.coinpaprika.com/v1/tickers"):
    """Scrape cryptocurrencies from a CoinPaprika-compatible API endpoint.

    Parameters:
        url (str): Target API endpoint. Defaults to the CoinPaprika tickers endpoint.
                   Pass a custom URL from the website registry to override.
    """

    data = None
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 429:
                response.raise_for_status() # Trigger retry
                
            if response.status_code >= 500:
                response.raise_for_status() # Trigger retry
                
            if response.status_code >= 400:
                raise ScraperError("Digital Assets", url, f"HTTP_ERROR_{response.status_code}", status_code=response.status_code)
                
            data = response.json()
            break
            
        except (requests.Timeout, requests.ConnectionError) as exc:
            logger.warning("Crypto scrape attempt %s failed with connection error: %s", attempt, exc)
            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Digital Assets", url, "CONNECTION_ERROR")
        except requests.RequestException as exc:
            # This catches the 5xx and 429 HTTP errors raised by raise_for_status()
            logger.warning("Crypto scrape attempt %s failed with HTTP error: %s", attempt, exc)
            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Digital Assets", url, "HTTP_SERVER_ERROR")
        except ValueError as exc:
            raise ScraperError("Digital Assets", url, "INVALID_JSON")

    if data is None:
        raise ScraperError("Digital Assets", url, "MAX_RETRIES_EXCEEDED")

    if not isinstance(data, list):
        raise ScraperError("Digital Assets", url, "INVALID_RESPONSE_FORMAT")

    items = []

    # Loop through each cryptocurrency
    for i, crypto in enumerate(data[:10]):
        try:
            usd = crypto.get("quotes", {}).get("USD", {})
            current_price = usd.get("price", 0)
            price_value = float(current_price) if current_price is not None else 0.0
            price_display = f"${price_value:.2f}"

            item = {
                "id": crypto.get('id'),
                "name": crypto.get('name'),
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
                    "volume_24h": usd.get("volume_24h", 0),
                }
            }
            items.append(item)
        except (TypeError, ValueError, AttributeError) as exc:
            logger.warning("Skipping malformed crypto record at index %s: %s", i, exc)
            continue

    return clean_items(items)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Scraping crypto prices from CoinPaprika...")
    cryptos = scrape_crypto()
    if cryptos:
        print(f"\nFetched {len(cryptos)} cryptocurrencies:")
        for crypto in cryptos:
            print(f"  {crypto['name']} - {crypto['price_display']} - Rank: {crypto['extra']['rating']}")
        print("\n[OK] Scraper test complete. Use POST /api/scrape to persist data.")
    else:
        print("No data returned — check your network connection.")
