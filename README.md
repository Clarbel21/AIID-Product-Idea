# StyleHub × MatchBuy AI

> A product-led outfit-matching concept prototype with direct links to retailer product pages.

## Project overview

StyleHub is a curated fashion storefront. MatchBuy AI helps a shopper start with one item, set an occasion, style preference and budget, then explore a coordinated outfit assembled from products in the catalogue. Each recommendation includes a short explanation and a link to the retailer.

This is a **static coursework prototype**. Despite the product name, the current matching engine is rule-based: it does not call a live AI model, learn from user feedback, or retrieve live retailer inventory. Checkout and payment take place on the retailer’s website; this prototype does not process purchases.

## Open the prototype

- **GitHub Pages:** [clarbel21.github.io/AIID-Product-Idea](https://clarbel21.github.io/AIID-Product-Idea/)
- **Local:** open `index.html` in a modern browser, or run `python serve.py` and open [http://localhost:8377](http://localhost:8377).
- No build step, package installation or API key is required. Product images are stored in `assets/`; web fonts load from Google Fonts when an internet connection is available.

## What the prototype includes

### Product catalogue and retailer handoff

The catalogue contains **94 products from 12 brands**: Urban Revivo, Forever 21, ASOS, Charles & Keith, APM Monaco, Zara, Nike, Adidas, JW PEI, Songmont, DeMellier and Swarovski. Product images are stored locally. Product links are labelled according to whether they open the specific item or a general retailer page.

Prices are reference values captured or converted when product records were added; they are not live quotes. Stock and size availability are not verified in real time. Shoppers should confirm current price, sizes and availability on the retailer’s site.

### Outfit matching

The shopper selects a starting product and provides an occasion (everyday, office, date or party), a mood (minimal, cute, elegant or sexy) and a budget. A transparent scoring function ranks compatible catalogue items for the available outfit slots and provides a brief reason for each recommendation. Users can reroll eligible slots and review the estimated outfit total before following retailer links.

The score combines six weighted components:

| Component | Weight | Purpose |
|---|---:|---|
| Style | 0.20 | Relates the product’s style family to the requested mood |
| Mood fit | 0.22 | Compares product mood tags with the selected mood |
| Colour harmony | 0.14 | Compares product tone tags using neutral, same-tone and warm/cool pairing rules |
| Silhouette balance | 0.10 | Compares the shapes of the starting item and recommendation |
| Occasion fit | 0.24 | Favors items tagged for the selected occasion |
| Budget fit | 0.10 | Scores candidate prices against the selected limit; the full outfit total is shown separately |

Scores and colour pairings are prototype heuristics, not objective measures of taste or fit. Colour compatibility uses product tone tags and fixed rules; no visual-recognition model or live AI service is used.

### Wishlist and recommendation feedback

- Shoppers can save items to a wishlist stored in their browser.
- With consent, shoppers can rate recommendations as **Helpful** or **Not for me** and optionally select a reason.
- Feedback remains in that browser’s local storage. It is not sent to a server and does not train the matching rules. Users can export the records as JSON.

## Problem framing

The prototype’s problem framing draws on brief excerpts from public discussions in Reddit’s [r/femalefashionadvice](https://www.reddit.com/r/femalefashionadvice/) and [r/fashionwomens35](https://www.reddit.com/r/fashionwomens35/) communities. The page links each excerpt to its original discussion. These posts are qualitative examples, not a formal user study, a representative sample, or proof of market demand. Their authors are not affiliated with or endorsing MatchBuy AI.

## Data and privacy

- Product records were assembled from retailer product pages and other public product information at the time of capture; there is no live shopping feed or automated scraping pipeline.
- Records distinguish exact-product links from general retailer links and may include a last-checked date.
- Reference prices can change. Availability is not asserted.
- Wishlist and consented recommendation feedback are stored locally in the browser. The prototype has no account system or feedback backend.
- The prototype does not handle checkout or payment information.

## Run-time and limitations

The application is a single HTML file with vanilla CSS and JavaScript. Matching, rule-based colour pairing, wishlist and feedback run in the browser. The static GitHub Pages deployment serves the same prototype as the local copy.

Current limitations include the absence of live retailer APIs, server-side feedback analysis, personalized learning, and generative virtual try-on. These would require separate data access, infrastructure and evaluation. The present build focuses on demonstrating the outfit-matching flow and retailer handoff transparently.

## Repository layout

| Path | Purpose |
|---|---|
| `index.html` | Storefront, catalogue, outfit matching, wishlist, feedback and public-discussion excerpts |
| `assets/` | Locally stored product and campaign images |
| `reference/` | Source project materials |
| `serve.py` | Optional local web server on port 8377 |
| `versions/` | Archived prototype versions |

---

*Prepared as a coursework concept prototype. Product names, images and marks belong to their respective retailers and rights holders. MatchBuy AI is not a retailer.*