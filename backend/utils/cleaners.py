import logging

logger = logging.getLogger(__name__)

def clean_price(price_str):
    """Convert price string to float, remove currency symbols."""
    if price_str is None:
        return 0.0
    try:
        cleaned = str(price_str).replace('$', '').replace('€', '').replace('£', '').replace(',', '').strip()
        return float(cleaned)
    except (ValueError, TypeError) as e:
        logger.warning("clean_price failed for value %r: %s", price_str, e)
        return 0.0

def clean_name(name_str):
    """Strip whitespace from product name."""
    return str(name_str).strip() if name_str is not None else ""

def clean_rating(rating):
    """Ensure rating is an integer."""
    if rating is None:
        return 0
    try:
        return int(rating)
    except (ValueError, TypeError) as e:
        logger.warning("clean_rating failed for value %r: %s", rating, e)
        return 0

def remove_duplicates(items):
    """Remove duplicate items based on id and source."""
    seen = set()
    unique_items = []
    for item in items:
        key = (item.get('id'), item.get('source'))
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    return unique_items

def clean_items(items):
    """Clean all items: strip whitespace, convert types, remove duplicates.
    Creates copies to avoid mutating the caller's data structures."""
    cleaned_items = []
    for original_item in items:
        item = dict(original_item)
        item['name'] = clean_name(item.get('name', ''))
        item['price'] = clean_price(item.get('price_display'))
        extra = dict(item.get('extra', {})) if isinstance(item.get('extra'), dict) else {}
        extra['rating'] = clean_rating(extra.get('rating'))
        extra['review_count'] = clean_rating(extra.get('review_count'))
        item['extra'] = extra
        cleaned_items.append(item)
    return remove_duplicates(cleaned_items)
