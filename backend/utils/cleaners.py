def clean_price(price_str):
    """Convert price string to float, remove currency symbols"""
    cleaned = price_str.replace('$', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def clean_name(name_str):
    """Strip whitespace from product name"""
    return name_str.strip()


def clean_rating(rating):
    """Ensure rating is an integer"""
    return int(rating) if rating else 0


def remove_duplicates(items):
    """Remove duplicate items based on name and price"""
    seen = set()
    unique_items = []
    
    for item in items:
        key = (item['name'], item['price'])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    
    return unique_items


def clean_items(items):
    """Clean all items: strip whitespace, convert types, remove duplicates"""
    for item in items:
        item['name'] = clean_name(item['name'])
        item['price'] = clean_price(item['price_display'])
        item['extra']['rating'] = clean_rating(item['extra']['rating'])
    
    return remove_duplicates(items)