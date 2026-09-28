# StyleHub × MatchBuy AI

> *Find the match. Complete the look. Buy it.*
> An AI outfit-matching shopping assistant, implemented as a clickable web prototype. Every product in the catalogue is real, every recommendation is explainable, and every purchase happens on the retailer's own website.

**Course:** AI + Innovative Design (Master's) · **Deliverable:** clickable web prototype

---

## Getting started

**Open the deployed version (recommended)**

The prototype is published on GitHub Pages and requires no installation:

**https://clarbel21.github.io/AIID-Product-Idea/**

**Run it locally**

1. Clone or download this repository.
2. Either double-click `index.html`, or start a small local server:

   ```
   python serve.py        # serves the project at http://localhost:8377
   ```

3. Open the address in any modern browser. No build step, no dependencies, no API keys.

The catalogue, matching, wishlist and feedback all work offline; product photography is stored locally. Only the typography loads from Google Fonts when online.

---

## About the project

StyleHub is a curated multi-brand storefront containing **105 real products from 12 brands** — Urban Revivo, Zara, Forever 21, Nike, Adidas, ASOS, Charles & Keith, APM Monaco, JW PEI, Songmont, DeMellier, Swarovski and 73Hours. Every card links to the product's own page on the brand's real website.

**MatchBuy AI** is the assistant layer on top of the storefront. The user selects one product and specifies an occasion, a mood and a budget; a rule-based scoring algorithm then assembles a complete outfit from complementary pieces across all of the brands, explains why each piece was chosen, and directs the user to the retailer to complete the purchase. The prototype is intentionally transparent: it shows how recommendations are produced rather than presenting them as opaque AI output.

## Features

### Catalogue
- 105 products across 12 brands, each linking to its own page on the retailer's website
- Normalized source record per product (retailer, link type, last-checked date) — designed as the adapter point for authorized retailer feeds
- Prices shown as **reference prices**: currency conversions captured when the product was added, not live quotes
- Per-product size runs verified against the retailers (letter sizes for clothing, EU/US/UK shoe runs per retailer; bags and jewellery show no sizes)
- Product photography stored locally, so the catalogue works offline

### Matching
- Style brief: occasion (everyday / office / date / party), mood (minimal / cute / elegant / sexy), budget (¥2,000 / ¥3,000 / ¥4,000 / no limit) and the slots to fill
- Transparent scoring across five dimensions — style, colour harmony, silhouette balance, occasion fit and budget fit — with a short explanation on every recommended piece
- The look board is ordered by body position (outerwear → necklace → top → bottom → bag → shoes), with the selected piece placed at its natural position
- Any slot can be re-rolled; the budget line states plainly whether the total fits or is over by how much

### Wishlist and feedback
- Items can be marked as liked from their product page and revisited in the wishlist panel; the list persists across page reloads
- Each recommendation can be rated **Helpful** or **Not for me**, with optional reasons (style mismatch, wrong occasion, over budget, unavailable, incorrect link, other)
- A consent notice explains what is stored before any rating is saved: feedback is anonymous, stays on the user's device and is never transmitted
- A summary view shows rating counts, recurring reasons and rule-based suggestions for the matching weights, with one-click JSON export

## How the matching works

```
score = 0.20·style + 0.22·moodFit + 0.14·colourHarmony + 0.10·silhouetteBalance
      + 0.24·occasionFit + 0.10·budgetFit        (per candidate, per slot)
```

| Dimension | Meaning |
|---|---|
| `style` | style-family match between the candidate and the chosen mood |
| `moodFit` | the candidate's own mood tags against the chosen mood |
| `colourHarmony` | neutral-pairing, same-tone and contrast rules based on photo-derived colour analysis |
| `occasionFit` | whether the candidate is tagged for the chosen occasion |
| `budgetFit` | keeps the combination inside the chosen budget |

The highest-scoring candidate fills each slot; a small diversity bonus encourages pieces from different brands. Colours shown in the analysis table are derived offline from each product photograph (dominant garment clusters) and were reviewed by hand — no live AI service is involved.

## Data transparency

- The matching engine is rule-based: it does not call a live AI model, learn from user feedback, or retrieve live retailer inventory

- Product data was captured from the retailers' own public product pages at build time; no scraping pipelines and no live-data claims
- Stock and size availability are treated as unknown and are not displayed
- Links are labelled so the user knows whether they open the exact product page or a general retailer page
- Checkout always happens on the retailer's website; the prototype never handles payment
- No personal data is collected — feedback is stored locally in the browser and can be exported as JSON

## Changes in this iteration

- Rebuilt the catalogue from live retailer data (Shopify product feeds and retailer product pages): verified titles, prices, imagery, size runs and colours for 105 products across 12 brands
- Added provenance labelling (exact-product vs. browse-the-retailer links, reference prices, last-checked dates) with a documented adapter point for authorized retailer feeds
- Added a three-step onboarding flow with an editable example match
- Made the matching context-sensitive (mood and occasion now dominate the score) and ordered the look board by human body position
- Re-framed model photographs to the garment being sold so users can picture the piece in an outfit
- Aligned sizes with what each retailer actually offers
- Added the consent-based feedback system with insights and JSON export
- Removed the AI try-on experiment after review; documented as future work

## Scope and future work

- **Virtual try-on** — a local pose-and-segmentation composite and a serverless integration were both prototyped and removed: realistic garment fitting requires a generative try-on model, which is out of scope for a static prototype. This is the main candidate for future work.
- **Live retailer feeds** — replace captured prices and availability with authorized retailer APIs
- **Backend feedback analysis** — move the device-local feedback store behind a service once real users exist
- **Personal closet** — let users combine recommended pieces with items they already own
- **Saved looks** — let users store and revisit complete outfit combinations

## Project structure

| Path | Purpose |
|---|---|
| `index.html` | The entire prototype: storefront, per-house catalogue, product pages, matching algorithm, wishlist, feedback |
| `assets/` | Product photography, stored locally so the site works offline |
| `serve.py` | Minimal local server (`python serve.py` → http://localhost:8377) |
| `reference/` | Original project handbook material the prototype was modelled on |
| `versions/` | Archived earlier versions of the prototype |

## Technical notes

- Single-file vanilla HTML/CSS/JavaScript — no build step, no framework, no backend
- Matching, colour analysis and feedback run entirely in the browser
- The GitHub Pages deployment serves the same static file as the repository

---

*Concept prototype prepared for coursework. All product data was captured from the retailers' own public pages and remains credited to them; MatchBuy is not a store.*
