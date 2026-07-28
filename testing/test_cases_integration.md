# Integration Test Cases — Backend

**Scope:** multi-component flows through the backend (storage layer + two or
more routes together), as opposed to a single function/route in isolation.
Frontend-to-backend integration is out of scope for this document.

**QA Tester:** Azhar Manie
**Date executed:** 28/07/2026

**Result:** 2 of 2 executed test cases pass. The one integration flow that
matters most for the demo — a real `POST /api/scrape` run flowing through to
`/api/items`, `/api/statistics`, and `/api/history` — **cannot currently be
executed end-to-end**, because `routes/scrape.py` cannot even be imported
(see Bug 05 in `bug_log.md`). The two cases below simulate the same data flow
by calling the storage layer directly the way `routes/scrape.py` does, so the
routes downstream of a scrape can still be verified.

---

## How to Run These Tests

Same setup as `test_cases_backend.md`:

1. Copy `backend/tests/test_integration_flow.py` (and `conftest.py`, if not
   already present) into `backend/tests/`.
2. From `backend/`, with dependencies installed:
   ```bash
   pytest tests/test_integration_flow.py -v
   ```

---

## Test Cases

Test Case (28/07/2026): TC-INT-01: Simulated scrape flows through to items, statistics, and history
Input: Directly call `storage.save_items([...2 new items...])` and
`storage.add_history(...)` twice (one Retail Goods record, one Digital Assets
record) — mirroring exactly what `routes/scrape.py` does after a real scrape
Expected:
  - `GET /api/items` reflects the new 2-item snapshot (not the old 21)
  - `GET /api/statistics` (fallback calculation) shows `total_items=2` and both
    new markets present
  - `GET /api/history` shows the two new records appended at the end
  - The previous 21-item snapshot is preserved in `items_history.json` for
    Top Movers calculations
Actual: Pass
Notes: Confirms the storage → routes wiring is correct. This is the strongest
evidence available that the API layer *would* work correctly once the scrape
endpoint itself is fixed (Bug 04 + Bug 05 resolved).

Test Case (28/07/2026): TC-INT-02: Website registry supplies the URLs `routes/scrape.py` depends on
Input: `GET /api/websites`
Expected: Registry contains one entry with `market == "E-Commerce"` and one
with `market == "Cryptocurrency"` — the two lookups `routes/scrape.py` performs
via `next((w['url'] for w in websites if w.get('market') == 'E-Commerce'), None)`
Expected (cont'd): Both lookups succeed against the real seeded data
Actual: Pass
Notes: If either market string in `websites.json` is ever renamed without
updating `routes/scrape.py` (or vice versa), the scraper silently falls back
to its hard-coded default URL instead of the registered one — worth keeping
these two in sync if the registry becomes user-editable later.

---

## Blocked / Not Yet Testable

Test Case (28/07/2026): TC-INT-03: `POST /api/scrape` end-to-end (real scrape → save → stats → history)
Input: `POST /api/scrape` against a running Flask app
Expected: 200 response with `ecommerce_count`, `crypto_count`, `total_count`,
and updated `/api/items` / `/api/statistics` / `/api/history`
Actual: **Blocked — cannot run**
Notes: The Flask app fails to start at all (`app.py` imports `routes.health`,
which doesn't exist — Bug 04), and even in isolation `routes/scrape.py`
cannot be imported because it imports `scrapers.ecommerce_scraper` and
`scrapers.crypto_scraper`, both of which fail on `from utils.cleaners import
...` (Bug 05). This test case should be re-run as soon as both bugs are
fixed. Note that live scraping also depends on outbound network access to
`webscraper.io` and `api.coingecko.com`, which may itself be restricted
depending on where these tests are executed (sandboxed CI, etc.) — a mocked
version of this test (patching `scrape_ecommerce`/`scrape_crypto` to return
canned data) is recommended once the imports are fixed, so the integration
test doesn't depend on live external sites.

---

## Summary Table

| Category                | Executed | Passed | Failed | Blocked |
|--------------------------|:--------:|:------:|:------:|:-------:|
| Integration (backend)    | 2        | 2      | 0      | 1       |