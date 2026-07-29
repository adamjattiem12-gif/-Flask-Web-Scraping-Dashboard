import logging
from flask import Blueprint, jsonify
from datetime import datetime
import time

from scrapers.ecommerce_scraper import scrape_ecommerce
from scrapers.crypto_scraper import scrape_crypto
from services.storage import save_items, add_history, load_items, load_websites, save_statistics, load_history

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint for the scrape route
scrape_bp = Blueprint('scrape', __name__)


# ============================================================================
# VALIDATION FUNCTION
# ============================================================================

def validate_items(items):
    """
    Validate that items have required fields
    Returns: (is_valid, error_message)
    """
    if not items:
        return False, "No items to validate"
    
    required_fields = ['name', 'price', 'price_display', 'market', 'source']
    
    for item in items:
        for field in required_fields:
            if field not in item or item[field] is None:
                return False, f"Item missing required field: {field}"
    
    return True, None


# ============================================================================
# CALCULATE STATISTICS
# ============================================================================

def calculate_statistics(items):
    """
    Calculate statistics from the items list.
    """
    if not items:
        return {
            "total_items": 0,
            "active_sites": 0,
            "success_rate": 0,
            "last_scrape": datetime.now().isoformat(),
            "markets": {}
        }

    # Group items by market dynamically
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
        successes = sum(1 for record in history if record.get('success', False))
        success_rate = round((successes / len(history)) * 100, 1)

    return {
        "total_items": len(items),
        "active_sites": len(load_websites()),
        "success_rate": success_rate,
        "last_scrape": datetime.now().isoformat(),
        "markets": markets_stats
    }


# ============================================================================
# MAIN SCRAPE ENDPOINT
# ============================================================================

@scrape_bp.route('/api/scrape', methods=['POST'])
def scrape():
    """
    POST /api/scrape
    
    Triggers a scrape of both e-commerce and crypto sources.
    Saves results to storage and logs the event.
    
    Returns:
    {
        "status": "success" or "error",
        "message": "Human readable message",
        "data": {
            "ecommerce_count": 21,
            "crypto_count": 10,
            "total_count": 31,
            "stats": {...}
        }
    }
    """
    logger.info("=== SCRAPE ENDPOINT CALLED ===")
    
    try:
        # ====== STEP 1: Resolve URLs from website registry ======
        logger.info("Step 1: Resolving scrape URLs from website registry...")
        websites = load_websites()
        ecommerce_url = next(
            (w['url'] for w in websites if w.get('market') == 'E-Commerce'),
            None  # Falls back to scraper default if not found
        )
        crypto_url = next(
            (w['url'] for w in websites if w.get('market') == 'Cryptocurrency'),
            None  # Falls back to scraper default if not found
        )
        logger.info(f"  E-Commerce URL: {ecommerce_url or 'default'}")
        logger.info(f"  Cryptocurrency URL: {crypto_url or 'default'}")

        # ====== STEP 2: Scrape E-Commerce ======
        logger.info("Step 2: Scraping e-commerce...")
        scrape_kwargs_ec = {"url": ecommerce_url} if ecommerce_url else {}
        ecommerce_items = scrape_ecommerce(**scrape_kwargs_ec)
        logger.info(f"✓ E-commerce scrape complete: {len(ecommerce_items)} items")
        time.sleep(2)  # Delay between requests (be respectful to APIs)
        
        # ====== STEP 3: Scrape Crypto ======
        logger.info("Step 3: Scraping crypto...")
        scrape_kwargs_cr = {"url": crypto_url} if crypto_url else {}
        crypto_items = scrape_crypto(**scrape_kwargs_cr)
        logger.info(f"✓ Crypto scrape complete: {len(crypto_items)} items")
        
        # ====== STEP 4: Combine Results ======
        all_items = ecommerce_items + crypto_items
        logger.info(f"Step 4: Combined {len(all_items)} items total")
        
        # ====== STEP 5: Validate Data ======
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
            else:
                add_history({
                    "timestamp": ts,
                    "scraper_type": "ecommerce",
                    "market": "Retail Goods",
                    "items_found": len(ecommerce_items),
                    "success": True
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
            else:
                add_history({
                    "timestamp": ts,
                    "scraper_type": "crypto",
                    "market": "Digital Assets",
                    "items_found": len(crypto_items),
                    "success": True
                })

            error_msg = f"Data validation failed. E-Commerce: {ec_error if not is_ec_valid else 'Pass'}. Crypto: {cr_error if not is_cr_valid else 'Pass'}."
            return jsonify({
                "status": "error",
                "message": error_msg,
                "data": None
            }), 400
        logger.info("✓ Data validation passed")
        
        # ====== STEP 6: Save Items ======
        logger.info("Step 6: Saving items...")
        try:
            save_items(all_items)
            logger.info(f"✓ Items saved: {len(all_items)}")
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
        
        # ====== STEP 7: Calculate Statistics ======
        logger.info("Step 7: Calculating statistics...")
        stats = calculate_statistics(all_items)
        logger.info("✓ Statistics calculated")
        
        # ====== STEP 8: Persist Statistics ======
        logger.info("Step 8: Saving statistics to storage...")
        save_statistics(stats)
        logger.info("✓ Statistics persisted to statistics.json")
        
        # ====== STEP 9: Log Per-Market History Records ======
        logger.info("Step 9: Logging scrape event to history...")
        ts = datetime.now().isoformat()
        add_history({
            "timestamp": ts,
            "scraper_type": "ecommerce",
            "market": "Retail Goods",
            "items_found": len(ecommerce_items),
            "success": True
        })
        add_history({
            "timestamp": ts,
            "scraper_type": "crypto",
            "market": "Digital Assets",
            "items_found": len(crypto_items),
            "success": True
        })
        logger.info("✓ Scrape logged to history (2 market records)")
        
        # ====== STEP 10: Return Success Response ======
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
        logger.info(f"✓ SCRAPE COMPLETE: {len(all_items)} items scraped")
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"✗ SCRAPE FAILED: {str(e)}", exc_info=True)
        # Log the failed scrape
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
        except:
            pass  # Even if history fails, still return error to user
        
        return jsonify({
            "status": "error",
            "message": f"Scrape failed: {str(e)}",
            "data": None
        }), 500


# ============================================================================
# ADDITIONAL HELPER ENDPOINTS
# ============================================================================

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
    print("✓ scrape_bp imported successfully")
    print("✓ All imports working")
    print("\nStorage functions available:")
    print("  - save_items(items)")
    print("  - add_history(record)")
    print("  - load_items()")