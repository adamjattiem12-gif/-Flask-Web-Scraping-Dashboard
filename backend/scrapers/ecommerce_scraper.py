import logging
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# -----------------------------------
# Add backend folder to Python path
# -----------------------------------
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

from utils.cleaners import clean_items, clean_price, clean_rating
from utils.exceptions import ScraperError

logger = logging.getLogger(__name__)


def scrape_ecommerce(
    url="https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
):
    """Scrape electronics from WebScraper.io."""

    content = None

    for attempt in range(1, 4):

        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 429:
                response.raise_for_status()

            if response.status_code >= 500:
                response.raise_for_status()

            if response.status_code >= 400:
                raise ScraperError(
                    "Retail Goods",
                    url,
                    f"HTTP_ERROR_{response.status_code}",
                    status_code=response.status_code
                )

            content = response.content
            break

        except (requests.Timeout, requests.ConnectionError) as exc:

            logger.warning(
                "E-commerce scrape attempt %s failed with connection error: %s",
                attempt,
                exc
            )

            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError(
                    "Retail Goods",
                    url,
                    "CONNECTION_ERROR"
                )

        except requests.RequestException as exc:

            logger.warning(
                "E-commerce scrape attempt %s failed with HTTP error: %s",
                attempt,
                exc
            )

            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError(
                    "Retail Goods",
                    url,
                    "HTTP_SERVER_ERROR"
                )

    if content is None:
        raise ScraperError(
            "Retail Goods",
            url,
            "MAX_RETRIES_EXCEEDED"
        )

    try:

        soup = BeautifulSoup(content, "html.parser")

        product_names = soup.select(".title")
        prices = soup.select('span[itemprop="price"]')
        ratings = soup.select("p[data-rating]")
        review_counts = soup.select('span[itemprop="reviewCount"]')

        items = []

        for i in range(len(product_names)):

            price_text = (
                prices[i].get_text(strip=True)
                if i < len(prices)
                else "0"
            )

            rating_text = (
                ratings[i].get("data-rating")
                if i < len(ratings)
                else 0
            )

            review_text = (
                review_counts[i].get_text(strip=True)
                if i < len(review_counts)
                else "0"
            )

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

    except (AttributeError, IndexError, TypeError, ValueError):
        raise ScraperError(
            "Retail Goods",
            url,
            "HTML_PARSE_ERROR"
        )

    return clean_items(items)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    print("Scraping e-commerce products...")

    products = scrape_ecommerce()

    if products:

        # Load items already in items.json
        existing_items = load_items()

        # Combine existing + new products
        all_items = existing_items + products

        # Save everything
        save_items(all_items)

        # Load statistics
        statistics = load_statistics()

        if not statistics:
            statistics = {}

        # Keep your existing statistics.json format
        statistics["total_items"] = len(all_items)
        statistics["total_websites"] = len(load_websites())
        statistics["successful_scrapes"] = statistics.get("successful_scrapes", 0) + 1
        statistics["last_scrape"] = datetime.now().isoformat()

        # Keep compatibility with the dashboard
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

        statistics["markets"]["Retail Goods"] = {
            "item_count": len(products),
            "avg_price": sum(item["price"] for item in products) / len(products),
            "last_updated": datetime.now().isoformat()
        }

        save_statistics(statistics)

        # Save history
        add_history({
            "timestamp": datetime.now().isoformat(),
            "target": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
            "market": "Retail Goods",
            "items_found": len(products),
            "status": "Success"
        })

        print(f"\nSaved {len(products)} products.")
        print(f"Total items in storage: {len(all_items)}")

    else:
        print("No products found.")