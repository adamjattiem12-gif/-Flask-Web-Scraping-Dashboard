import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
    # Test it
    products = scrape_ecommerce()
    for product in products:
        print(f"{product['name']} - {product['price_display']} - Rating: {product['extra']['rating']}")