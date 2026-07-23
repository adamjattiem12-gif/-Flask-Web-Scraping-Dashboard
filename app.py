import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Import your storage functions
from services.storage import (
    save_items,
    add_history,
    load_websites,
    load_statistics,
    save_statistics
)


def scrape_ecommerce():
    """Scrape products from WebScraper.io"""

    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    product_names = soup.select(".title")
    prices = soup.select('span[itemprop="price"]')
    ratings = soup.select("p[data-rating]")
    review_counts = soup.select('span[itemprop="reviewCount"]')

    items = []

    # Build a list of scraped products
    for i in range(len(product_names)):

        item = {
            "id": i + 1,
            "name": product_names[i].get_text(strip=True),
            "price": float(prices[i].get_text(strip=True).replace("$", "")),
            "price_display": prices[i].get_text(strip=True),
            "currency": "USD",
            "source": "WebScraper.io",
            "market": "Retail Goods",
            "scraped_at": datetime.now().isoformat(),
            "extra": {
                "rating": int(ratings[i]["data-rating"]),
                "review_count": int(review_counts[i].get_text(strip=True))
            }
        }

        items.append(item)

    # Save the scraped products
    save_items(items)


    # Create statistics
    # Load the current statistics
# Load previous statistics
    statistics = load_statistics()

    if not statistics:
        statistics = {
            "total_items": 0,
            "total_websites": 0,
            "successful_scrapes": 0,
            "failed_scrapes": 0,
            "last_scrape": "",
            "markets": {}
        }

    statistics["total_items"] = len(items)
    statistics["total_websites"] = len(load_websites())
    statistics["successful_scrapes"] += 1
    statistics["last_scrape"] = datetime.now().isoformat()
    statistics["markets"]["Retail Goods"] = len(items)

    save_statistics(statistics)

    # Save scrape history
    add_history({
    "timestamp": datetime.now().isoformat(),
    "target": url,
    "market": "Retail Goods",
    "items_found": len(items),
    "status": "Success"
})

    return items

if __name__ == "__main__":

    # Create websites.json if it doesn't exist
    load_websites()

    # Run the scraper
    products = scrape_ecommerce()

    print(f"Saved {len(products)} products.")