import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.cleaners import clean_items

def scrape_ecommerce():
    """Scrape electronics from WebScraper.io E-Commerce Sandbox"""
    
    url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all products
    product_names = soup.select('.title')
    prices = soup.select('span[itemprop="price"]')
    ratings = soup.select('p[data-rating]')
    review_counts = soup.select('span[itemprop="reviewCount"]')
    
    items = []
    
    # Loop through and build item objects
    for i in range(len(product_names)):
        item = {
            "id": i + 1,
            "name": product_names[i].get_text(strip=True),
            "price": float(prices[i].get_text(strip=True).replace('$', '')),
            "price_display": prices[i].get_text(strip=True),
            "currency": "USD",
            "source": "WebScraper.io E-Commerce",
            "market": "Retail Goods",
            "scraped_at": datetime.now().isoformat(),
            "extra": {
                "rating": int(ratings[i].get('data-rating')),
                "review_count": int(review_counts[i].get_text(strip=True))
            }
        }
        items.append(item)
    
    return clean_items(items)


if __name__ == '__main__':
    # Test it
    products = scrape_ecommerce()
    for product in products:
        print(f"{product['name']} - {product['price_display']} - Rating: {product['extra']['rating']}")