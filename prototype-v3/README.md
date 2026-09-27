# MatchBuy AI — complete website prototype v3

Open `index.html` in this folder, or the root `index.html` in the branch. The version in this folder uses the full original catalog and its shared assets one directory above.

## What it includes

- The complete original storefront and retailer catalog (57 product records across 11 brands).
- Product detail views, a product-based MatchBuy flow, adjustable occasion/mood/budget choices, and cross-store outfit suggestions.
- Searchable retailer links, product imagery, wishlist, and local concept try-on preview.
- Responsive layout and the original visual direction.

## Product data and limits

The catalog is carried forward from the original MatchBuy project, including retailer product names, brand imagery, reference prices, and retailer URLs. Original project documentation says some catalog data was captured from brand pages and Shopify product endpoints. The capture dates are not recorded, so prices are indicative RMB references and current stock is not verified.

Most catalog URLs are product pages. Some Nike, Adidas, and 73Hours entries point to brand collections or homepages; the interface identifies those as browsing links instead of claiming an exact SKU page. Confirm current product, price, size, and availability with the retailer.

Matching uses the catalog's tagged attributes and a scoring algorithm. It does not call a live AI shopping API. The try-on panel is a local concept preview, not a live generative model. The retailer remains responsible for checkout and payment.

## Backups

This improvement is on `prototype/matchbuy-curated-web-v3`. It leaves the original `main` branch and earlier v2 simulation/extension branch intact.
