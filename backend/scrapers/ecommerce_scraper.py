import logging
import sys
import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

# Allow running this file directly from any working directory
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

from utils.cleaners import clean_items, clean_price, clean_rating
from utils.exceptions import ScraperError
from utils.validators import validate_scrape_url

logger = logging.getLogger(__name__)


def scrape_ecommerce(url="https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"):
    """Scrape electronics from a WebScraper.io E-Commerce Sandbox URL.

    Parameters:
        url (str): Target URL to scrape. Defaults to the tablets page.
                   Pass a custom URL from the website registry to override.
    """

    is_valid, reason = validate_scrape_url(url, 'ecommerce')
    if not is_valid:
        raise ScraperError("Retail Goods", url, f"URL_VALIDATION_FAILED: {reason}")

    content = None
    for attempt in range(1, 4):
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 429:
                response.raise_for_status() # Trigger retry
                
            if response.status_code >= 500:
                response.raise_for_status() # Trigger retry
                
            if response.status_code >= 400:
                raise ScraperError("Retail Goods", url, f"HTTP_ERROR_{response.status_code}", status_code=response.status_code)
                
            content = response.content
            break
            
        except (requests.Timeout, requests.ConnectionError) as exc:
            logger.warning("E-commerce scrape attempt %s failed with connection error: %s", attempt, exc)
            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Retail Goods", url, "CONNECTION_ERROR")
        except requests.RequestException as exc:
            logger.warning("E-commerce scrape attempt %s failed with HTTP error: %s", attempt, exc)
            if attempt < 3:
                time.sleep(1 if attempt == 1 else 2)
            else:
                raise ScraperError("Retail Goods", url, "HTTP_SERVER_ERROR")

    if content is None:
        raise ScraperError("Retail Goods", url, "MAX_RETRIES_EXCEEDED")

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
        raise ScraperError("Retail Goods", url, "HTML_PARSE_ERROR")

    return clean_items(items)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Scraping e-commerce products...")
    products = scrape_ecommerce()
    if products:
        print(f"\nFetched {len(products)} products:")
        for product in products:
            print(f"  {product['name']} - {product['price_display']} - Rating: {product['extra']['rating']}")
        print("\n[OK] Scraper test complete. Use POST /api/scrape to persist data.")
    else:
        print("No data returned — check your network connection.")