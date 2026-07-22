import requests
from bs4 import BeautifulSoup

url = "https://webscraper.io/test-sites/e-commerce/allinone"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

if response.status_code != 200:
    print(f"FAIL: Expected status 200, got {response.status_code}")
else:
    print(f"PASS: Status code is {response.status_code}")

# Separate test — separate variable
bad_url = "https://webscraper.io/test-sites/e-commerce/nonexistent-page"
bad_response = requests.get(bad_url)
if bad_response.status_code == 404:
    print(f"PASS: Nonexistent page correctly returns 404")
else:
    print(f"FAIL: Expected 404, got {bad_response.status_code}")

# Find ALL products
product_names = soup.select('.title')
prices = soup.select('span[itemprop="price"]')
ratings = soup.select('p[data-rating]')

# Simulate selectors matching nothing
fake_products = soup.select('.this-class-does-not-exist')
print(len(fake_products))  # 0

if len(fake_products) == 0:
    print("No products found — check if selectors are still valid or page structure changed")

if len(product_names) == 0:
    print("WARNING: No products found. Selectors may be broken or page is empty.")
else:
    for i in range(len(product_names)):
        ...

for i, rating_tag in enumerate(ratings):
    rating = rating_tag.get('data-rating')
    if rating is None:
        print(f"Product {i+1}: MISSING rating attribute")
    else:
        print(f"Product {i+1}: rating = {rating}")

print(f"Names: {len(product_names)}, Prices: {len(prices)}, Ratings: {len(ratings)}")

if not (len(product_names) == len(prices) == len(ratings)):
    print("FAIL: Lists are misaligned — data may print against the wrong product")
else:
    print("PASS: All lists match in length")

assert len(product_names) == len(prices) == len(ratings), \
    f"Mismatch: {len(product_names)} names, {len(prices)} prices, {len(ratings)} ratings"

# Loop through and print each product
for i in range(len(product_names)):
    name = product_names[i].get_text(strip=True)
    price = prices[i].get_text(strip=True)
    rating = ratings[i].get('data-rating')
    
    print(f"{i+1}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Rating: {rating}")
    print()  # Blank line for readability