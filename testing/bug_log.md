# Bug Report — E-Commerce & Finance Scraping Dashboard

**QA Tester:** Azhar
**Last updated:** 28/07/2026
**Source:** `bug_log.md`, `test_cases_backend.md`, `test_cases_integration.md`, `test_summary.md`

## Summary

| Status      | Count |
|-------------|:-----:|
| Total found |   5   |
| Resolved    |   0   |
| Still open  |   5   |

Two additional non-blocking issues were observed during testing but not filed as numbered bugs (see [Additional Observations](#additional-observations)).


## Bug 01 — No HTTP status check in e-commerce scraper

- **Test case:** TC-06
- **Date:** 23/07/2026
- **Severity:** High
- **Status:** Open
- **Developer:** Adam
- **Description:** There is no HTTP status check after `requests.get()`; a blocked or error response is parsed as if it were valid.
- **Fix:** Check `response.status_code` (or use `response.raise_for_status()`) before parsing.

---

## Bug 02 — Price parser doesn't strip thousands-separator commas

- **Test case:** TC-07
- **Date:** 23/07/2026
- **Severity:** Medium
- **Status:** Open
- **Developer:** Adam
- **Description:** The price parser doesn't strip thousands-separator commas (e.g. `"1,299.00"`), which will break numeric conversion for higher-priced items.
- **Fix:** Strip commas (or other locale separators) before converting price strings to numbers.

---

## Bug 03 — No exception handling around network calls / type conversions

- **Test case:** TC-09
- **Date:** 23/07/2026
- **Severity:** High
- **Status:** Open
- **Developer:** Adam
- **Description:** There is no exception handling around the network call or the `int()`/`float()` conversions. Any failure in these turns into an unhandled crash rather than a logged failure.
- **Fix:** Wrap network calls and numeric conversions in try/except, and log failures instead of crashing.
---

## Bug 04 — Flask app fails to start (`app.py`)

- **Test case:** TC-BE-01
- **Date:** 28/07/2026
- **Severity:** Critical
- **Status:** Open
- **Developer:** Unassigned
- **Description:** `backend/app.py` imports `from routes.health import health_bp`, but `backend/routes/health.py` does not exist in this branch. As a result, the Flask app cannot start at all.
- **Impact:** Blocks the entire application. Every other backend fix is moot until this is resolved.
- **Fix:** Add the missing `backend/routes/health.py` module.

---

## Bug 05 — Scraper modules fail to import (`utils.cleaners` missing)

- **Test cases:** TC-BE-02, TC-BE-03
- **Date:** 28/07/2026
- **Severity:** Critical
- **Status:** Open
- **Developer:** Unassigned
- **Description:** Both `backend/scrapers/ecommerce_scraper.py` and `backend/scrapers/crypto_scraper.py` do `from utils.cleaners import ...`, but there is no `backend/utils/cleaners.py`. A copy of `cleaners.py` exists in the repo, but at the wrong path: `backend/services/__pycache__/utils/cleaners.py` — apparently accidentally committed from a stray `__pycache__` directory instead of being placed at `backend/utils/cleaners.py`.
- **Impact:** Because `routes/scrape.py` imports both scraper modules at the top of the file, this also blocks `POST /api/scrape` and `GET /api/scrape/status` from being importable, let alone testable. It also blocks a full end-to-end integration test (TC-INT-03).
- **Fix:** Move `cleaners.py` to `backend/utils/cleaners.py`.

---



---

## Additional Observations

These were noted during testing but **not filed as numbered bugs** — flagged for team discussion.

### `/api/items` market filter is case-sensitive (inconsistent with `/api/search`)
- **Test case:** TC-BE-28 (contrast with TC-BE-31)
- `GET /api/items?market=retail goods` (lowercase) returns 0 items even though `"Retail Goods"` exists in storage — no case normalization is applied.
- `/api/search`'s market filter, by contrast, lower-cases both sides of the comparison and is case-insensitive.
- **Risk:** If the frontend ever sends a market name with different casing than what's stored, `/api/items` results will silently come back empty.
- Not filed as a bug since current frontend always sends canonical values — recommend a follow-up conversation with the developer on whether this is intentional.

### `/api/search` 500s on a stored item missing its `name` field
- **Test case:** TC-BE-33
- The route accesses `item["name"]` directly. A stored item without a `name` key causes a `KeyError`, which Flask surfaces as an HTTP 500.
- **Fix suggestion:** Use `item.get("name", "")` so one malformed record doesn't take down the whole endpoint.
- Not filed as a numbered bug since it requires malformed data to trigger (shouldn't happen if `scrapers/` always produces well-formed items), but it's a latent risk.

### `/api/history?limit=0` is silently ignored
- **Test case:** TC-BE-40
- The route uses `if limit:`, and `0` is falsy in Python, so `?limit=0` behaves identically to no limit at all (returns all records) instead of returning zero records.
- **Fix suggestion:** Change to `if limit is not None:`.
- Low impact/unusual query, but a one-line correctness fix if the team wants it.

---

## Overall Assessment

The backend's individual routes and storage layer are solid once the app can actually start — 41/44 unit-level backend tests pass, and both integration tests confirm the storage → API wiring behaves correctly. However, the application **cannot run at all in its current state** (Bug 04), and the scrape endpoint specifically cannot even be imported (Bug 05). Both are quick fixes (add the missing `routes/health.py`, move `cleaners.py` to `backend/utils/cleaners.py`), but until they land, this build is **not demo-ready**.