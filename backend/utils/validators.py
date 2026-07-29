import requests
from urllib.parse import urlparse

def validate_scrape_url(url, scraper_type):
    if not url:
        return False, "URL is empty"
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False, "Invalid scheme"
    if not parsed.netloc:
        return False, "Invalid netloc"

    path = parsed.path.lower()
    if scraper_type == 'crypto':
        if not any(word in path for word in ['api', 'coins', 'markets']):
            return False, "Invalid crypto path"
    elif scraper_type == 'ecommerce':
        if not any(word in path for word in ['e-commerce', 'allinone', 'computers', 'tablets']):
            return False, "Invalid ecommerce path"
    
    return True, None

def health_check(url, scraper_type):
    try:
        if scraper_type == 'crypto':
            res = requests.get(url, params={'vs_currency': 'usd', 'per_page': 1}, timeout=3)
            if res.status_code == 200:
                try:
                    data = res.json()
                    return isinstance(data, list)
                except ValueError:
                    return False
            return False
        elif scraper_type == 'ecommerce':
            # E-commerce health check: HEAD request (or lightweight GET)
            res = requests.head(url, timeout=3)
            if res.status_code == 405: # Method Not Allowed, fallback to GET
                res = requests.get(url, timeout=3, stream=True)
                res.close()
            return 200 <= res.status_code < 400
    except requests.RequestException:
        return False
    return False
