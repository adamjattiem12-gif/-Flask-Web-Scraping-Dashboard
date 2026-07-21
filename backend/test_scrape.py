import requests
from bs4 import BeautifulSoup

# Fetch the page
url = "https://webscraper.io/test-sites/e-commerce/allinone"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find ALL products
product_names = soup.select('.title')
prices = soup.select('span[itemprop="price"]')
ratings = soup.select('p[data-rating]')

# Loop through and print each product
for i in range(len(product_names)):
    name = product_names[i].get_text(strip=True)
    price = prices[i].get_text(strip=True)
    rating = ratings[i].get('data-rating')
    
    print(f"{i+1}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Rating: {rating}")
    print()  # Blank line for readability