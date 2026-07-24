import logging
from flask import Blueprint, jsonify
from datetime import datetime
import time

# Import your scrapers
from backend.scrapers.ecommerce_scraper import scrape_ecommerce
from backend.scrapers.crypto_scraper import scrape_crypto

# Import Purrity's storage functions
from backend.services.storage import save_items, add_history, load_items

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
    Calculate statistics from the items list
    """
    if not items:
        return {
            "total_items": 0,
            "active_sites": 0,
            "success_rate": 0,
            "last_scrape": datetime.now().isoformat(),
            "markets": {}
        }
    
    ecommerce_items = [item for item in items if item.get('market') == 'Retail Goods']
    crypto_items = [item for item in items if item.get('market') == 'Digital Assets']
    
    stats = {
        "total_items": len(items),
        "active_sites": 2,
        "success_rate": 100.0,
        "last_scrape": datetime.now().isoformat(),
        "markets": {
            "Retail Goods": {
                "item_count": len(ecommerce_items),
                "avg_price": sum([item['price'] for item in ecommerce_items]) / len(ecommerce_items) if ecommerce_items else 0,
                "last_updated": datetime.now().isoformat()
            },
            "Digital Assets": {
                "item_count": len(crypto_items),
                "avg_price": sum([item['price'] for item in crypto_items]) / len(crypto_items) if crypto_items else 0,
                "last_updated": datetime.now().isoformat()
            }
        }
    }
    return stats


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
        # ====== STEP 1: Scrape E-Commerce ======
        logger.info("Step 1: Scraping e-commerce...")
        ecommerce_items = scrape_ecommerce()
        logger.info(f"✓ E-commerce scrape complete: {len(ecommerce_items)} items")
        time.sleep(2)  # Delay between requests (be respectful to APIs)
        
        # ====== STEP 2: Scrape Crypto ======
        logger.info("Step 2: Scraping crypto...")
        crypto_items = scrape_crypto()
        logger.info(f"✓ Crypto scrape complete: {len(crypto_items)} items")
        
        # ====== STEP 3: Combine Results ======
        all_items = ecommerce_items + crypto_items
        logger.info(f"Step 3: Combined {len(all_items)} items total")
        
        # ====== STEP 4: Validate Data ======
        logger.info("Step 4: Validating data...")
        is_valid, error_msg = validate_items(all_items)
        if not is_valid:
            logger.error(f"Validation failed: {error_msg}")
            # Log the failed scrape
            add_history({
                "timestamp": datetime.now().isoformat(),
                "scraper_type": "combined",
                "items_found": 0,
                "success": False,
                "error": error_msg
            })
            return jsonify({
                "status": "error",
                "message": f"Data validation failed: {error_msg}",
                "data": None
            }), 400
        logger.info("✓ Data validation passed")
        
        # ====== STEP 5: Save Items (using Purrity's function) ======
        logger.info("Step 5: Saving items...")
        try:
            save_items(all_items)
            logger.info(f"✓ Items saved: {len(all_items)}")
        except Exception as e:
            logger.error(f"Failed to save items: {str(e)}")
            add_history({
                "timestamp": datetime.now().isoformat(),
                "scraper_type": "combined",
                "items_found": len(all_items),
                "success": False,
                "error": f"Failed to save items: {str(e)}"
            })
            return jsonify({
                "status": "error",
                "message": "Failed to save scraped items to storage",
                "data": None
            }), 500
        
        # ====== STEP 6: Calculate Statistics ======
        logger.info("Step 6: Calculating statistics...")
        stats = calculate_statistics(all_items)
        logger.info("✓ Statistics calculated")
        
        # ====== STEP 7: Log Scrape Event (using Purrity's function) ======
        logger.info("Step 7: Logging scrape event...")
        add_history({
            "timestamp": datetime.now().isoformat(),
            "scraper_type": "combined",
            "items_found": len(all_items),
            "success": True,
            "ecommerce_count": len(ecommerce_items),
            "crypto_count": len(crypto_items)
        })
        logger.info("✓ Scrape logged to history")
        
        # ====== STEP 8: Return Success Response ======
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
            add_history({
                "timestamp": datetime.now().isoformat(),
                "scraper_type": "combined",
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