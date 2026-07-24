import requests
from datetime import datetime
from backend.utils.cleaners import clean_items

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
    
    # Fetch the data
    response = requests.get(url, params=params)
    data = response.json()              # Convert JSON to Python dictionary
    
    items = []
    
    # Loop through each cryptocurrency
    for i, crypto in enumerate(data):
        item = {
            "id": crypto.get('id'),
            "name": crypto.get('name'),
            "price": float(crypto.get('current_price', 0)),
            "price_display": f"${crypto.get('current_price', 0):.2f}",
            "currency": "USD",
            "source": "CoinGecko API",
            "market": "Digital Assets",
            "scraped_at": datetime.now().isoformat(),
            "extra": {
                "rating": i + 1,
                "review_count": 0
            }
        }
        items.append(item)
    
    return clean_items(items)


if __name__ == '__main__':
    # Test it
    cryptos = scrape_crypto()
    for crypto in cryptos:
        print(f"{crypto['name']} - {crypto['price_display']} - Rank: {crypto['extra']['rating']}")