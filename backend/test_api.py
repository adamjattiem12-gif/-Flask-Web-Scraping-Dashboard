import time
from app import app
from services.storage import save_websites, load_websites
import json

def test():
    client = app.test_client()
    
    print("SCENARIO 1: Valid URLs")
    t0 = time.time()
    res1 = client.post('/api/scrape')
    t1 = time.time()
    print(f"Status Code: {res1.status_code}")
    print(f"Time Taken: {t1 - t0:.2f} seconds")
    
    print("\nModifying websites.json to break Crypto URL...")
    websites = load_websites()
    original_crypto_url = next(w['url'] for w in websites if w['market'] in ('Cryptocurrency', 'Digital Assets'))
    
    for w in websites:
        if w['market'] in ('Cryptocurrency', 'Digital Assets'):
            # Use a blackhole IP to force a timeout
            w['url'] = 'http://10.255.255.1/api/v3/coins/markets'
    save_websites(websites)
    
    print("\nSCENARIO 2: Broken CoinGecko URL (timeout expected)")
    t2 = time.time()
    res2 = client.post('/api/scrape')
    t3 = time.time()
    print(f"Status Code: {res2.status_code}")
    print(f"Time Taken: {t3 - t2:.2f} seconds")
    try:
        print("Response JSON:")
        print(json.dumps(res2.get_json(), indent=2))
    except:
        pass
        
    # Restore
    print("\nRestoring websites.json...")
    for w in websites:
        if w['market'] in ('Cryptocurrency', 'Digital Assets'):
            w['url'] = original_crypto_url
    save_websites(websites)
    
if __name__ == '__main__':
    test()
