# MatchBuy AI — website prototype v3

Open index.html in a browser. This is a standalone website; no extension, server, or API key is required.

## Working features
- Search and filter catalog pieces by category.
- Select a product, choose a category, and show up to three simple style matches.
- Open the corresponding retailer product page in a new browser tab.
- Responsive layout for desktop and mobile.

## Product data integrity
This demo uses a curated subset of products already present in the original MatchBuy catalog. Images load from the original project’s public assets; product links point to brand/retailer pages. Prices are reference values inherited from the old prototype, not live prices. Current availability is unknown. The interface says so and sends shoppers to the retailer to confirm.

The match logic ranks this curated catalog by its existing tags. It is not a live AI feed and does not invent products. For a production catalog, use retailer-authorized product feeds, affiliate APIs, or retailer APIs, and retain the product source URL, retrieval time, currency, and confirmed price/availability timestamps. If price or stock cannot be confirmed, say “check retailer” instead of guessing.

## Backup
This page is in prototype-v3/ on prototype/matchbuy-curated-web-v3. It does not overwrite the original site or the earlier v2 simulation/extension work.
