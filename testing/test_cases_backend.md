# Backend Test Cases

**Scope:** `backend/` folder only (Flask app, routes, services, storage, models,
scrapers). Frontend/UI is covered separately in `test_cases_ui.md`.

**QA Tester:** Azhar Manie
**Date executed:** 28/07/2026
**Tooling:** `pytest`, Flask's built‑in `test_client()`, Python 3.12

**Result:** 46 test cases executed — **43 Pass / 3 Fail**. All 3 failures are
caused by the same two root-cause bugs, logged in `bug_log.md` as Bug 04 and
Bug 05.

---

## How to Run These Tests

1. Copy the `backend/tests/` folder (shipped alongside this document) into
   your project so it sits next to `app.py`:
   ```
   backend/
     app.py
     routes/
     services/
     scrapers/
     models/
     data/
     tests/          <- add this folder here
       conftest.py
       test_app_startup.py
       test_scraper_imports.py
       test_storage.py
       test_item_model.py
       test_items_route.py
       test_search_route.py
       test_statistics_route.py
       test_history_route.py
       test_websites_route.py
       test_integration_flow.py
   ```
2. From inside `backend/`, create/activate a virtual environment and install
   dependencies:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate 
   pip install -r requirements.txt
   pip install pytest
   ```
3. Run the whole suite:
   ```bash
   pytest tests/ -v
   ```
4. Run a single file (e.g. just the storage tests):
   ```bash
   pytest tests/test_storage.py -v
   ```
5. Run a single test case:
   ```bash
   pytest tests/test_items_route.py::test_get_items_per_page_over_100_returns_400 -v
   ```

Every test in `test_storage.py`, `test_items_route.py`, `test_search_route.py`,
`test_statistics_route.py`, `test_history_route.py`, and `test_websites_route.py`
uses an `isolated_data` fixture (see `conftest.py`) that copies the real
`backend/data/*.json` files into a temp folder before each test, so **running
these tests never modifies your real data files**.

---

## 1. App Startup (`app.py`)

Test Case (28/07/2026): TC-BE-01: Flask app imports/starts successfully
Input: `import app` (equivalent to running `python app.py`)
Expected: Module imports cleanly and the Flask app object is created
Actual: **Fail**
Notes: `ModuleNotFoundError: No module named 'routes.health'`. `app.py` line 3
does `from routes.health import health_bp`, but there is no `health.py` file
anywhere under `backend/routes/`. The app cannot start at all in its current
state. See Bug 04.

---

## 2. Scraper Module Imports (`scrapers/`)

Test Case (28/07/2026): TC-BE-02: `scrapers/ecommerce_scraper.py` imports successfully
Input: `import scrapers.ecommerce_scraper`
Expected: Module imports cleanly
Actual: **Fail**
Notes: `ModuleNotFoundError: No module named 'utils'`. The module does
`from utils.cleaners import clean_items, clean_price, clean_rating`, but
`backend/utils/cleaners.py` does not exist. (A copy of `cleaners.py` exists,
but at the wrong path: `backend/services/__pycache__/utils/cleaners.py`.)
See Bug 05.

Test Case (28/07/2026): TC-BE-03: `scrapers/crypto_scraper.py` imports successfully
Input: `import scrapers.crypto_scraper`
Expected: Module imports cleanly
Actual: **Fail**
Notes: Same root cause as TC-BE-02 — `ModuleNotFoundError: No module named 'utils'`.

> Because both scrapers fail to import, and `routes/scrape.py` imports both of
> them at module level, `POST /api/scrape` and `GET /api/scrape/status` cannot
> currently be tested at all — the blueprint itself cannot be imported. Once
> Bug 05 is fixed, the scraper business logic (price/rating cleaning, malformed
> record handling, empty-response handling) still needs its own test pass —
> see the existing `test_cases_scraper.md` for the network-layer scraper tests
> that were runnable in isolation.

---

## 3. Storage Service (`services/storage.py`)

Test Case (28/07/2026): TC-BE-04: `load_items()` returns the seeded item list
Input: Sample `items.json` (21 items)
Expected: Returns a list of 21 dicts
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-05: `load_items()` with no items.json file
Input: `items.json` deleted before call
Expected: Returns `[]` instead of raising
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-06: `load_items()` with an empty items.json file
Input: `items.json` truncated to 0 bytes
Expected: Returns `[]` instead of raising a JSON decode error
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-07: `save_items()` → `load_items()` round trip
Input: `save_items([{...}])`
Expected: `load_items()` immediately returns the same list
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-08: `save_items()` versions the outgoing snapshot
Input: Save a new item list over an existing non-empty one
Expected: The previous item list is appended to `items_history.json` with a
`snapshot_at` timestamp before being overwritten
Actual: Pass
Notes: Confirms the Top-Movers versioning mechanism works as documented.

Test Case (28/07/2026): TC-BE-09: No history entry created on the very first save
Input: `items.json` starts as `[]`, then `save_items()` is called
Expected: `items_history.json` stays empty (nothing to version yet)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-10: `load_websites()` returns the seeded registry
Input: Sample `websites.json` (2 entries)
Expected: Returns both registered sites
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-11: `load_websites()` auto-seeds defaults when file is missing
Input: `websites.json` deleted before call
Expected: Returns the 2 hard-coded default websites and writes them to disk
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-12: `load_history()` returns the seeded history
Input: Sample `history.json` (20 records)
Expected: Returns all 20 records
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-13: `add_history()` appends a record
Input: `add_history({...})` on top of 20 existing records
Expected: History grows to 21 records; new record is last
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-14: `load_statistics()` with an empty `{}` file
Input: Sample `statistics.json` content is literally `{}`
Expected: Returns `{}` (falsy), which is what triggers the `/api/statistics`
fallback calculation
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-15: `save_statistics()` → `load_statistics()` round trip
Input: `save_statistics({...})`
Expected: `load_statistics()` returns the same dict
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-16: `ensure_data_folder()` creates a missing directory
Input: `DATA_FOLDER` pointed at a directory that doesn't exist yet
Expected: Directory is created, no error
Actual: Pass
Notes: —

---

## 4. Item Model (`models/item.py`)

Test Case (28/07/2026): TC-BE-17: `Item.to_dict()` includes all fields
Input: Construct an `Item` with all required fields
Expected: `to_dict()` returns a dict with matching values, `extra` defaults to `{}`
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-18: `extra` dict is not shared across instances
Input: Create two `Item`s, mutate `extra` on the first
Expected: The second instance's `extra` is unaffected (`field(default_factory=dict)` works correctly)
Actual: Pass
Notes: Confirms the dataclass avoids the classic "mutable default argument" bug.

---

## 5. `GET /api/items`

Test Case (28/07/2026): TC-BE-19: Default pagination
Input: `GET /api/items` (21 items in storage)
Expected: `page=1`, `per_page=20`, `total=21`, 20 items returned
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-20: Second page shows the remainder
Input: `GET /api/items?page=2&per_page=20`
Expected: 1 item returned (21 total − 20 on page 1)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-21: Filter by market
Input: `GET /api/items?market=Retail Goods`
Expected: Only items with `market == "Retail Goods"` returned
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-22: Filter by a market that doesn't exist
Input: `GET /api/items?market=Nonexistent Market`
Expected: `items: []`, `total: 0`
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-23: Non-integer `page` value
Input: `GET /api/items?page=abc`
Expected: HTTP 400 with an `error` message
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-24: `page=0`
Input: `GET /api/items?page=0`
Expected: HTTP 400 (page must be positive)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-25: Negative `per_page`
Input: `GET /api/items?per_page=-5`
Expected: HTTP 400
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-26: `per_page` over the 100 cap
Input: `GET /api/items?per_page=101`
Expected: HTTP 400 ("per_page cannot exceed 100")
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-27: `per_page` exactly at the 100 cap
Input: `GET /api/items?per_page=100`
Expected: HTTP 200 (boundary value is allowed, not rejected)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-28: Market filter is case-sensitive
Input: `GET /api/items?market=retail goods` (lowercase; stored value is "Retail Goods")
Expected: Documents current behaviour only — no case normalisation is applied
Actual: Pass (i.e., confirmed it returns 0 items for a differently-cased market)
Notes: **Possible UX bug** — worth flagging to the team: if the frontend ever
sends a market name with different casing than what's stored, results will
silently come back empty. Not filed as a bug since it may be intentional
(frontend always sends canonical values today), but recommend a follow-up
conversation with the developer.

---

## 6. `GET /api/search`

Test Case (28/07/2026): TC-BE-29: No query returns all items
Input: `GET /api/search` (no `q` param)
Expected: All 21 items returned
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-30: Partial, case-insensitive name match
Input: `GET /api/search?q=IDEATAB`
Expected: All items whose name contains "ideatab" (any case)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-31: Combined query + market filter
Input: `GET /api/search?q=&market=retail goods`
Expected: Only items in the Retail Goods market
Actual: Pass
Notes: Unlike `/api/items`, this route lower-cases both sides of the market
comparison, so it is *not* case-sensitive — inconsistent with TC-BE-28.

Test Case (28/07/2026): TC-BE-32: No matches
Input: `GET /api/search?q=zzz_no_such_product_zzz`
Expected: `[]`
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-33: Item missing the `name` field
Input: A stored item without a `name` key, then `GET /api/search?q=anything`
Expected: Ideally a clean 4xx/skip; currently the route does `item["name"]`
directly
Actual: Pass (test confirms it currently raises `KeyError` → Flask returns HTTP 500)
Notes: **Bug candidate** — the route should use `item.get("name", "")` so one
malformed record doesn't 500 the whole search endpoint. Recommend filing this
if the team wants defensive handling; not filed as a numbered bug here since
it requires malformed data to trigger, which shouldn't happen if `scrapers/`
always produces well-formed items — but it's a latent risk.

---

## 7. `GET /api/statistics`

Test Case (28/07/2026): TC-BE-34: Persisted statistics take priority
Input: `statistics.json` populated with a stats object
Expected: Route returns the persisted object as-is, no recalculation
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-35: Falls back to live calculation when `statistics.json` is `{}`
Input: Sample `statistics.json` (`{}`), 21 items in storage
Expected: `total_items=21`, `active_sites=2`, `markets` includes "Retail Goods"
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-36: Fallback success rate from history
Input: 20 history records, all `success: true`
Expected: `success_rate == 100.0`
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-37: Fallback with no items and no history
Input: `items.json` and `history.json` both `[]`
Expected: `total_items=0`, `success_rate=100.0` (default when history is empty), `markets={}`
Actual: Pass
Notes: —

---

## 8. `GET /api/history`

Test Case (28/07/2026): TC-BE-38: Default returns all records
Input: `GET /api/history` (20 seeded records)
Expected: All 20 records returned
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-39: `limit` returns the newest N records
Input: `GET /api/history?limit=5`
Expected: The last 5 records in storage order
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-40: `limit=0` is silently ignored
Input: `GET /api/history?limit=0`
Expected: Documents current behaviour only
Actual: Pass (confirms all 20 records are returned, not 0)
Notes: **Minor bug candidate** — the route uses `if limit:`, and `0` is falsy
in Python, so `?limit=0` behaves identically to no limit at all instead of
returning zero records. Low impact (an unusual query to send), but worth a
one-line fix (`if limit is not None:`) if the team wants strict correctness.

Test Case (28/07/2026): TC-BE-41: Filter by market
Input: A history record with `market: "Retail Goods"` added, then `GET /api/history?market=Retail Goods`
Expected: Only matching records returned
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-42: Market filter with no matches
Input: `GET /api/history?market=Nonexistent`
Expected: `[]`
Actual: Pass
Notes: —

---

## 9. `GET /api/websites`

Test Case (28/07/2026): TC-BE-43: Returns the seeded registry
Input: `GET /api/websites`
Expected: 2 sites, one per market (E-Commerce, Cryptocurrency)
Actual: Pass
Notes: —

Test Case (28/07/2026): TC-BE-44: Auto-seeds defaults when file is missing
Input: `websites.json` deleted, then `GET /api/websites`
Expected: Returns the 2 default sites (via `load_websites()`)
Actual: Pass
Notes: —

---

## Summary Table

| Section                          | Executed | Passed | Failed |
|-----------------------------------|:--------:|:------:|:------:|
| App startup                      | 1        | 0      | 1      |
| Scraper imports                  | 2        | 0      | 2      |
| Storage service                  | 13       | 13     | 0      |
| Item model                       | 2        | 2      | 0      |
| `/api/items`                     | 10       | 10     | 0      |
| `/api/search`                    | 5        | 5      | 0      |
| `/api/statistics`                | 4        | 4      | 0      |
| `/api/history`                   | 5        | 5      | 0      |
| `/api/websites`                  | 2        | 2      | 0      |
| **Total**                         | **44**   | **41** | **3**  |

(Integration-level test cases are tracked separately in
`test_cases_integration.md` — 2 executed, 2 passed.)
