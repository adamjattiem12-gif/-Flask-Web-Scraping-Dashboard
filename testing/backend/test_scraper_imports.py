"""TC-BE-02 / TC-BE-03: Do the scraper modules import cleanly?"""
import importlib
import sys


def test_ecommerce_scraper_imports():
    sys.modules.pop("scrapers.ecommerce_scraper", None)
    importlib.import_module("scrapers.ecommerce_scraper")


def test_crypto_scraper_imports():
    sys.modules.pop("scrapers.crypto_scraper", None)
    importlib.import_module("scrapers.crypto_scraper")
