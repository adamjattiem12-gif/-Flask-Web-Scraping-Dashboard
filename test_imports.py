# Test if imports work
print("Testing imports...")

try:
    from scrapers.ecommerce_scraper import scrape_ecommerce
    print("✓ ecommerce_scraper imported")
except Exception as e:
    print(f"✗ ecommerce_scraper failed: {e}")

try:
    from scrapers.crypto_scraper import scrape_crypto
    print("✓ crypto_scraper imported")
except Exception as e:
    print(f"✗ crypto_scraper failed: {e}")

try:
    from services.storage import save_items, add_history, load_items
    print("✓ storage functions imported")
except Exception as e:
    print(f"✗ storage functions failed: {e}")

print("\nAll tests complete!")