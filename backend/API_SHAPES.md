# API Response Shapes

## GET /api/items

```json
{
  "items": [
    {
      "id": 1,
      "name": "Asus VivoBook X441NA-GA190",
      "price": 295.99,
      "price_display": "$295.99",
      "currency": "USD",
      "source": "WebScraper.io E-Commerce",
      "market": "Retail Goods",
      "scraped_at": "2026-07-20T14:30:00",
      "extra": { "rating": 4, "review_count": 14 }
    }
  ],
  "total": 2,
  "page": 1,
  "per_page": 20
}
```

## GET /api/statistics

```json
{
  "total_items": 40,
  "active_sites": 2,
  "success_rate": 96.5,
  "last_scrape": "2026-07-20T14:30:00",
  "markets": {
    "Retail Goods": {
      "item_count": 20,
      "avg_price": 450.0,
      "last_updated": "2026-07-20T14:30:00"
    },
    "Digital Assets": {
      "item_count": 20,
      "avg_price": 28450.0,
      "last_updated": "2026-07-20T14:30:00"
    }
  }
}

