import logging
import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Allow running this file directly from any working directory
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from utils.cleaners import clean_items, clean_price, clean_rating

logger = logging.getLogger(__name__)


def scrape_ecommerce():
    """Scrape electronics from WebScraper.io E-Commerce Sandbox"""

    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("E-commerce scrape request failed: %s", exc)
        return []

    if response.status_code != 200:
        logger.warning("E-commerce scrape returned unexpected status: %s", response.status_code)
        return []

    try:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all products
        product_names = soup.select('.title')
        prices = soup.select('span[itemprop="price"]')
        ratings = soup.select('p[data-rating]')
        review_counts = soup.select('span[itemprop="reviewCount"]')

        items = []

        # Loop through and build item objects
        for i in range(len(product_names)):
            price_text = prices[i].get_text(strip=True) if i < len(prices) else "0"
            rating_text = ratings[i].get('data-rating') if i < len(ratings) else 0
            review_text = review_counts[i].get_text(strip=True) if i < len(review_counts) else "0"

            item = {
                "id": i + 1,
                "name": product_names[i].get_text(strip=True),
                "price": clean_price(price_text),
                "price_display": price_text,
                "currency": "USD",
                "source": "WebScraper.io E-Commerce",
                "market": "Retail Goods",
                "scraped_at": datetime.now().isoformat(),
                "extra": {
                    "rating": clean_rating(rating_text),
                    "review_count": clean_rating(review_text)
                }
            }
            items.append(item)
    except (AttributeError, IndexError, TypeError, ValueError) as exc:
        logger.exception("E-commerce scrape failed while parsing page content: %s", exc)
        return []

    return clean_items(items)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Import storage (backend dir already on sys.path from above)
    from services.storage import (
        save_items, add_history,
        load_statistics, save_statistics, load_websites
    )

    print("Scraping e-commerce products...")
    products = scrape_ecommerce()

    if products:
        print(f"\nFetched {len(products)} products:")
        for product in products:
            print(f"  {product['name']} - {product['price_display']} - Rating: {product['extra']['rating']}")

        # Save results to backend/data/items.json
        save_items(products)
        print(f"\n[OK] Saved {len(products)} items to backend/data/items.json")

        # Log to backend/data/history.json
        add_history({
            "timestamp": datetime.now().isoformat(),
            "scraper_type": "ecommerce",
            "items_found": len(products),
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
        stats["total_items"] = len(products)
        stats["total_websites"] = len(load_websites())
        stats["successful_scrapes"] = stats.get("successful_scrapes", 0) + 1
        stats["last_scrape"] = datetime.now().isoformat()
        stats["markets"]["Retail Goods"] = len(products)
        save_statistics(stats)
        print("[OK] Statistics updated in backend/data/statistics.json")

    else:
        print("No data returned — check your network connection.")

        # Log the failed scrape to statistics
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