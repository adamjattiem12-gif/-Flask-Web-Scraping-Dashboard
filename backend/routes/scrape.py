import logging
import time
from datetime import datetime

from flask import Blueprint, jsonify, request

from scrapers.crypto_scraper import scrape_crypto
from scrapers.ecommerce_scraper import scrape_ecommerce
from services.storage import add_history, load_history, load_items, load_websites, save_items, save_statistics
from utils.exceptions import ScraperError
from utils.validators import health_check, validate_scrape_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scrape_bp = Blueprint('scrape', __name__)


def validate_items(items):
    """
    Validate that items have required fields.
    Returns: (is_valid, error_message)
    """
    if not items:
        return True, None

    required_fields = ['name', 'price', 'price_display', 'market', 'source']

    for item in items:
        for field in required_fields:
            if field not in item or item[field] is None:
                return False, f"Item missing required field: {field}"

    return True, None


def calculate_statistics(items, history_limit=100):
    if not items:
        return {
            "total_items": 0,
            "active_sites": 0,
            "success_rate": 0,
            "last_scrape": datetime.now().isoformat(),
            "markets": {}
        }

    markets = {}
    for item in items:
        market_name = item.get('market', 'Unknown')
        if market_name not in markets:
            markets[market_name] = []
        markets[market_name].append(item)

    markets_stats = {}
    for market_name, market_items in markets.items():
        prices = [item['price'] for item in market_items if 'price' in item]
        avg_price = round(sum(prices) / len(prices), 2) if prices else 0.0
        last_updated = max(
            (item.get('scraped_at', '') for item in market_items),
            default=datetime.now().isoformat()
        )
        markets_stats[market_name] = {
            "item_count": len(market_items),
            "avg_price": avg_price,
            "last_updated": last_updated
        }

    history = load_history()
    if not history:
        success_rate = 100.0
    else:
        recent_history = history[-history_limit:]
        successes = sum(1 for record in recent_history if record.get('success', False))
        success_rate = round((successes / len(recent_history)) * 100, 1)

    return {
        "total_items": len(items),
        "active_sites": len(load_websites()),
        "success_rate": success_rate,
        "last_scrape": datetime.now().isoformat(),
        "markets": markets_stats
    }


def run_scraper_with_fallback(scraper_func, scraper_type, registry_url, default_url, market_name, path_keywords=None):
    target_url = registry_url
    original_failure = None

    is_valid, reason = validate_scrape_url(target_url, scraper_type, path_keywords=path_keywords)
    if not is_valid:
        original_failure = f"URL_VALIDATION_FAILED: {reason}"
        logger.warning(f"{market_name} URL validation failed for {target_url}, falling back to {default_url}")
        target_url = default_url
        # The fallback URL is one of our own known-good defaults, so it
        # should be checked against the built-in keyword list rather than
        # a possibly-unrelated custom one from the registry entry.
        is_valid, reason = validate_scrape_url(target_url, scraper_type)
        if not is_valid:
            raise ScraperError(market_name, registry_url, original_failure)

    if not health_check(target_url, scraper_type):
        if target_url == default_url:
            if original_failure:
                raise ScraperError(market_name, registry_url, original_failure)
            raise ScraperError(market_name, target_url, f"Health check failed for {target_url}")
        else:
            logger.warning(f"{market_name} health check failed for {target_url}, falling back to {default_url}")
            target_url = default_url
            if not health_check(target_url, scraper_type):
                raise ScraperError(
                    market_name,
                    registry_url,
                    "Health check failed for registry URL; fallback also failed"
                )

    try:
        return scraper_func(url=target_url)
    except ScraperError as e:
        if target_url != default_url and original_failure is None:
            logger.warning(f"{market_name} scrape failed ({e.reason}), falling back to {default_url}")
            target_url = default_url
            if not health_check(target_url, scraper_type):
                raise e
            try:
                items = scraper_func(url=target_url)
                logger.warning(f"{market_name} fallback succeeded")
                return items
            except ScraperError:
                raise e
        else:
            if original_failure:
                raise ScraperError(market_name, registry_url, original_failure)
            raise e


VALID_MARKETS = ('Retail Goods', 'Digital Assets')


def _get_requested_market():
    """
    Reads the optional 'market' parameter from the query string or JSON
    body. Returns one of VALID_MARKETS, or None to scrape everything.
    """
    market = request.args.get('market')
    if not market and request.is_json:
        body = request.get_json(silent=True) or {}
        market = body.get('market')

    if not market or market == 'All':
        return None

    if market not in VALID_MARKETS:
        raise ValueError(f"Unknown market '{market}'. Expected one of {VALID_MARKETS} or omitted for both.")

    return market


@scrape_bp.route('/api/scrape', methods=['POST'])
def scrape():
    """
    POST /api/scrape
    POST /api/scrape?market=Retail%20Goods
    POST /api/scrape?market=Digital%20Assets

    Triggers a scrape of e-commerce and/or crypto sources. By default both
    markets are scraped. Passing ?market=Retail Goods or
    ?market=Digital Assets (or the same key in a JSON body) scrapes only
    that market, leaving the other market's stored items untouched.
    Saves results to storage and logs the event.
    """
    logger.info("=== SCRAPE ENDPOINT CALLED ===")

    try:
        requested_market = _get_requested_market()
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "data": None}), 400

    scrape_ecommerce_market = requested_market in (None, "Retail Goods")
    scrape_crypto_market = requested_market in (None, "Digital Assets")

    try:
        logger.info("Step 1: Resolving scrape URLs from website registry...")
        websites = load_websites()
        ecommerce_site = next(
            (w for w in websites if w.get('market') in ('E-Commerce', 'Retail Goods')),
            None
        )
        crypto_site = next(
            (w for w in websites if w.get('market') in ('Cryptocurrency', 'Digital Assets')),
            None
        )
        ecommerce_url = ecommerce_site['url'] if ecommerce_site else \
            "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
        crypto_url = crypto_site['url'] if crypto_site else \
            "https://api.coinpaprika.com/v1/tickers"
        # Custom sites registered via POST /api/websites can carry their own
        # path_keywords so validate_scrape_url doesn't need editing per site.
        ecommerce_keywords = ecommerce_site.get('path_keywords') if ecommerce_site else None
        crypto_keywords = crypto_site.get('path_keywords') if crypto_site else None
        logger.info(f"  E-Commerce URL: {ecommerce_url}")
        logger.info(f"  Cryptocurrency URL: {crypto_url}")

        ecommerce_items = []
        crypto_items = []
        ec_failed = False
        cr_failed = False
        ec_error_reason = None
        cr_error_reason = None

        if scrape_ecommerce_market:
            logger.info("Step 2: Scraping e-commerce...")
            try:
                ecommerce_items = run_scraper_with_fallback(
                    scrape_ecommerce,
                    'ecommerce',
                    ecommerce_url,
                    "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets",
                    "Retail Goods",
                    path_keywords=ecommerce_keywords
                )
                logger.info(f"E-commerce scrape complete: {len(ecommerce_items)} items")
            except ScraperError as e:
                logger.error(f"E-commerce scrape failed: {e.reason}")
                ec_failed = True
                ec_error_reason = e.reason
                add_history({
                    "timestamp": datetime.now().isoformat(),
                    "scraper_type": "ecommerce",
                    "market": "Retail Goods",
                    "items_found": 0,
                    "success": False,
                    "error": e.reason
                })
        else:
            logger.info("Step 2: Skipping e-commerce (market-specific scrape requested)")

        if not ec_failed and scrape_ecommerce_market and scrape_crypto_market:
            time.sleep(2)

        if scrape_crypto_market:
            logger.info("Step 3: Scraping crypto...")
            try:
                crypto_items = run_scraper_with_fallback(
                    scrape_crypto,
                    'crypto',
                    crypto_url,
                    "https://api.coinpaprika.com/v1/tickers",
                    "Digital Assets",
                    path_keywords=crypto_keywords
                )
                logger.info(f"Crypto scrape complete: {len(crypto_items)} items")
            except ScraperError as e:
                logger.error(f"Crypto scrape failed: {e.reason}")
                cr_failed = True
                cr_error_reason = e.reason
                add_history({
                    "timestamp": datetime.now().isoformat(),
                    "scraper_type": "crypto",
                    "market": "Digital Assets",
                    "items_found": 0,
                    "success": False,
                    "error": e.reason
                })
        else:
            logger.info("Step 3: Skipping crypto (market-specific scrape requested)")

        if ec_failed and cr_failed:
            return jsonify({
                "status": "error",
                "message": f"Both scrapers failed. E-Commerce: {ec_error_reason}. Crypto: {cr_error_reason}.",
                "data": {
                    "ecommerce_count": 0,
                    "crypto_count": 0,
                    "total_count": 0,
                    "scrape_timestamp": datetime.now().isoformat(),
                    "stats": calculate_statistics([])
                }
            }), 500

        all_items = ecommerce_items + crypto_items

        # If this was a market-specific scrape, the other market's items were
        # never touched above (they're still []), so pull them from storage
        # to avoid wiping them out when we save.
        if requested_market is not None:
            existing_items = load_items()
            if not scrape_ecommerce_market:
                all_items = [i for i in existing_items if i.get('market') == 'Retail Goods'] + all_items
            if not scrape_crypto_market:
                all_items = all_items + [i for i in existing_items if i.get('market') == 'Digital Assets']

        logger.info(f"Step 4: Combined {len(all_items)} items total")

        logger.info("Step 5: Validating data...")
        is_ec_valid, ec_error = validate_items(ecommerce_items)
        is_cr_valid, cr_error = validate_items(crypto_items)

        if not is_ec_valid or not is_cr_valid:
            ts = datetime.now().isoformat()
            if not is_ec_valid:
                logger.error(f"E-Commerce validation failed: {ec_error}")
                add_history({
                    "timestamp": ts,
                    "scraper_type": "ecommerce",
                    "market": "Retail Goods",
                    "items_found": 0,
                    "success": False,
                    "error": ec_error
                })
            if not is_cr_valid:
                logger.error(f"Crypto validation failed: {cr_error}")
                add_history({
                    "timestamp": ts,
                    "scraper_type": "crypto",
                    "market": "Digital Assets",
                    "items_found": 0,
                    "success": False,
                    "error": cr_error
                })

            error_msg = f"Data validation failed. E-Commerce: {ec_error if not is_ec_valid else 'Pass'}. Crypto: {cr_error if not is_cr_valid else 'Pass'}."
            return jsonify({
                "status": "error",
                "message": error_msg,
                "data": {
                    "ecommerce_count": len(ecommerce_items),
                    "crypto_count": len(crypto_items),
                    "total_count": len(all_items),
                    "scrape_timestamp": datetime.now().isoformat(),
                    "stats": calculate_statistics(all_items)
                }
            }), 400

        logger.info("Data validation passed")

        logger.info("Step 6: Saving items...")
        try:
            save_items(all_items)
            logger.info(f"Items saved: {len(all_items)}")
        except Exception as e:
            logger.error(f"Failed to save items: {str(e)}")
            ts = datetime.now().isoformat()
            add_history({
                "timestamp": ts,
                "scraper_type": "ecommerce",
                "market": "Retail Goods",
                "items_found": len(ecommerce_items),
                "success": False,
                "error": f"Failed to save items: {str(e)}"
            })
            add_history({
                "timestamp": ts,
                "scraper_type": "crypto",
                "market": "Digital Assets",
                "items_found": len(crypto_items),
                "success": False,
                "error": f"Failed to save items: {str(e)}"
            })
            return jsonify({
                "status": "error",
                "message": "Failed to save scraped items to storage",
                "data": None
            }), 500

        logger.info("Step 7: Calculating statistics...")
        stats = calculate_statistics(all_items)
        logger.info("Statistics calculated")

        logger.info("Step 8: Saving statistics to storage...")
        save_statistics(stats)
        logger.info("Statistics persisted to statistics.json")

        logger.info("Step 9: Logging scrape event to history...")
        ts = datetime.now().isoformat()
        if not ec_failed:
            add_history({
                "timestamp": ts,
                "scraper_type": "ecommerce",
                "market": "Retail Goods",
                "items_found": len(ecommerce_items),
                "success": True
            })
        if not cr_failed:
            add_history({
                "timestamp": ts,
                "scraper_type": "crypto",
                "market": "Digital Assets",
                "items_found": len(crypto_items),
                "success": True
            })
        logger.info("Scrape logged to history")

        response = {
            "status": "success",
            "message": f"Successfully scraped {len(all_items)} items",
            "data": {
                "ecommerce_count": len(ecommerce_items),
                "crypto_count": len(crypto_items),
                "total_count": len(all_items),
                "scrape_timestamp": datetime.now().isoformat(),
                "stats": stats
            }
        }
        logger.info(f"SCRAPE COMPLETE: {len(all_items)} items scraped")
        return jsonify(response), 200

    except ScraperError as e:
        logger.error(f"Scrape failed (ScraperError): {e.reason}")
        try:
            ts = datetime.now().isoformat()
            add_history({
                "timestamp": ts,
                "scraper_type": "ecommerce",
                "market": "Retail Goods",
                "items_found": 0,
                "success": False,
                "error": e.reason
            })
            add_history({
                "timestamp": ts,
                "scraper_type": "crypto",
                "market": "Digital Assets",
                "items_found": 0,
                "success": False,
                "error": e.reason
            })
        except Exception:
            pass
        return jsonify({"status": "error", "message": f"Scrape failed: {e.reason}", "data": None}), 500
    except (RuntimeError, ValueError, TypeError, KeyError) as e:
        logger.error(f"Scrape failed (Runtime error): {str(e)}", exc_info=True)
        try:
            ts = datetime.now().isoformat()
            add_history({
                "timestamp": ts,
                "scraper_type": "ecommerce",
                "market": "Retail Goods",
                "items_found": 0,
                "success": False,
                "error": str(e)
            })
            add_history({
                "timestamp": ts,
                "scraper_type": "crypto",
                "market": "Digital Assets",
                "items_found": 0,
                "success": False,
                "error": str(e)
            })
        except Exception:
            pass
        return jsonify({"status": "error", "message": f"Scrape failed: {str(e)}", "data": None}), 500


@scrape_bp.route('/api/scrape/status', methods=['GET'])
def scrape_status():
    """
    GET /api/scrape/status

    Returns current status: how many items are in storage, last scrape time, etc.
    """
    try:
        items = load_items()
        stats = calculate_statistics(items)
        return jsonify({
            "status": "ok",
            "data": stats
        }), 200
    except Exception as e:
        logger.error(f"Error getting scrape status: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    print("scrape_bp imported successfully")
    print("All imports working")
    print("\nStorage functions available:")
    print("  - save_items(items)")
    print("  - add_history(record)")
    print("  - load_items()")
