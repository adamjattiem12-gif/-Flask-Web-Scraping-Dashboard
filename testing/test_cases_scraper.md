Test Case: Scraper handles missing/non-existent page gracefully
Endpoint: Scraper - fake URL / bad selector simulation
Input: Selector '.this-class-does-not-exist' run against valid page
Expected: Returns 0 results, prints clear warning instead of crashing
Actual: Pass
Notes: Output correctly showed "No products found — check if selectors are still valid or page structure changed"

Test Case: Scraper returns 200 status code
Endpoint: GET https://webscraper.io/test-sites/e-commerce/allinone
Input: None
Expected: Status code 200
Actual: Pass
Notes: Confirmed "PASS: Status code is 200"

Test Case: data-rating attribute present for all products
Endpoint: Scraper - allinone page
Input: Loop through all rating tags, check for None
Expected: Every product has a valid data-rating value
Actual: Pass
Notes: Ratings returned were 1, 3, 4 — no missing attributes found

Test Case: Product lists (names, prices, ratings) are equal length
Endpoint: Scraper - allinone page
Input: Compare len(product_names), len(prices), len(ratings)
Expected: All three lists match in length
Actual: Pass
Notes: All three returned length 3 — no misalignment