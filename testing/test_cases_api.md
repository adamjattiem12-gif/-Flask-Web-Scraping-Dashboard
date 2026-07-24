Test Case (23/07/2026): TC-01: Names extracted
Input: Live/mock page, 2+ products
Expected: product_names count = number of products on page
Actual: Pass (2/2 found)
Notes: .title selector is correct

Test Case (23/07/2026): TC-02: Prices extracted
Input: Same page
Expected: prices count = number of products
Actual: Pass (2/2 found)
Notes: span[itemprop="price"] selector correct

Test Case (23/07/2026): TC-03: Ratings extracted
Input: Same page
Expected: ratings count = number of products
Actual: Pass (2/2 found)
Notes: p[data-rating] selector correct

Test Case (23/07/2026): TC-04: Review counts extracted
Input: Same page
Expected: review_counts count = number of products
Actual: Pass (2/2 found)
Notes: span[itemprop="reviewCount"] selector is correct

Test Case (23/07/2026): TC-05: Function returns populated list
Input: Same page
Expected: List of dicts, one per product
Actual: Pass (2/2 found)
Notes: index has the correct number of entries 

Test Case (23/07/2026): TC-06: Non-200 response handling
Input: Simulate 403/404
Expected: Function raises a clear, handled error or returns [] gracefully
Actual: Fail
Notes: No status check; a 403 (as I actually got hitting the live URL from this sandbox — blocked at network egress) is parsed as normal HTML and silently yields 0 products

Test Case (23/07/2026): TC-07: Price with thousands separator
Input: Price = $1,299.00
Expected: Correctly parsed as 1299.00
Actual: Fail
Notes: .replace('$','') leaves the comma; float() raises ValueError

Test Case (23/07/2026): TC-08: Malformed/missing data-rating
Input: Rating attr missing
Expected: Graceful default or clear error
Actual: Fail
Notes: int(None) raises TypeError

Test Case (23/07/2026): TC-09: Network/timeout failure
Input: No connectivity
Expected: Clear error, no crash
Actual: Fail
Notes: No timeout param, no try/except around requests.get