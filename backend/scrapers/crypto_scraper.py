import logging
import requests
from datetime import datetime
from utils.cleaners import clean_items, clean_price, clean_rating

logger = logging.getLogger(__name__)


def scrape_crypto():
    """Scrape cryptocurrencies from CoinGecko API"""

    # API endpoint (like a URL, but returns JSON instead of HTML)
    url = "https://api.coingecko.com/api/v3/coins/markets"

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
    # Test it
    cryptos = scrape_crypto()
    for crypto in cryptos:
        print(f"{crypto['name']} - {crypto['price_display']} - Rank: {crypto['extra']['rating']}")