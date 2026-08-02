# API Response Shapes

All endpoints are prefixed with the Flask app's root (default `http://127.0.0.1:5000`).

## GET /api/health

```json
{ "status": "ok" }
```

## GET /api/health/check?url=<url>&type=<crypto|ecommerce>

```json
{
  "healthy": true,
  "url": "https://api.coinpaprika.com/v1/tickers",
  "type": "crypto",
  "checked_at": "2026-07-20T14:30:00"
}
```
Returns `400` if `url` or `type` is missing.

## GET /api/items

Query params: `page` (default 1), `per_page` (default 20, max 100), `market` (optional filter).

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
Returns `400` if `page`/`per_page` are invalid or `per_page` exceeds 100.

## GET /api/statistics

```json
{
  "total_items": 40,
  "active_sites": 2,
  "success_rate": 96.5,
  "last_scrape": "2026-07-20T14:30:00",
  "markets": {
    "Retail Goods": { "item_count": 20, "avg_price": 450.0, "last_updated": "2026-07-20T14:30:00" },
    "Digital Assets": { "item_count": 20, "avg_price": 28450.0, "last_updated": "2026-07-20T14:30:00" }
  }
}
```

## POST /api/scrape

Optional query param or JSON body: `market` (`"Retail Goods"` | `"Digital Assets"`). Omit to scrape both.

```json
{
  "status": "success",
  "message": "Successfully scraped 40 items",
  "data": {
    "ecommerce_count": 20,
    "crypto_count": 20,
    "total_count": 40,
    "scrape_timestamp": "2026-07-20T14:30:00",
    "stats": { "...": "same shape as GET /api/statistics" }
  }
}
```
Returns `400` for an unrecognized `market` value, `500` if both scrapers fail.

## GET /api/scrape/status

```json
{ "status": "ok", "data": { "...": "same shape as GET /api/statistics" } }
```

## GET /api/search

Query params: `q` (search text, matched against item name), `market` (optional), `page`, `per_page`.

```json
{
  "items": [ "...same item shape as GET /api/items" ],
  "total": 3,
  "page": 1,
  "per_page": 20
}
```

## GET /api/history

Query params: `market` (optional filter), `limit` (return only the most recent N records),
or `page`/`per_page` for full pagination (ignored if `limit` is set).

```json
{
  "history": [
    {
      "id": 12,
      "timestamp": "2026-07-20T14:30:00",
      "scraper_type": "ecommerce",
      "market": "Retail Goods",
      "items_found": 20,
      "success": true,
      "error": null
    }
  ],
  "total": 12,
  "page": 1,
  "per_page": 20
}
```

## GET /api/websites

```json
[
  { "id": 1, "name": "WebScraper E-Commerce Sandbox", "url": "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets", "market": "Retail Goods" },
  { "id": 2, "name": "CoinPaprika API", "url": "https://api.coinpaprika.com/v1/tickers", "market": "Digital Assets" }
]
```

## POST /api/websites

Body:
```json
{
  "name": "My News Source",
  "url": "https://example.com/news",
  "market": "Retail Goods",
  "path_keywords": ["news", "articles"]
}
```
`path_keywords` is optional — when provided, the scraper's URL-safety check accepts any of these
substrings in the target's path instead of the built-in defaults. Returns `201` with the created
record (including its new `id`), or `400` if `name`/`url`/`market` are missing/invalid.

## DELETE /api/websites/<id>

```json
{ "deleted": true, "id": 3 }
```
Returns `404` if no website exists with that id.

## Error shape

All error responses (400/404/500) follow:
```json
{ "error": "human-readable message" }
```
