# StyleHub × MatchBuy AI

> **AI outfit-matching shopping assistant** — *find the match. Complete the look. Buy it.*
> A working prototype: a Dior-inspired storefront where every product is real, every match is explainable, and every purchase happens on the retailer's own website.

**Course:** AI + Innovative Design (Master's) · **Deliverable:** clickable web prototype

## Submission links

| | Link |
|---|---|
| **GitHub repository (source code)** | https://github.com/Clarbel21/AIID-Product-Idea |
| **Public deployment (GitHub Pages)** | https://clarbel21.github.io/AIID-Product-Idea/ |
| **Run locally** | `python serve.py` → http://localhost:8377 (or double-click `index.html`) |

GitHub Pages auto-deploys on every push to `main`. (github.io can be intermittent from mainland China — the local run is identical.)

---

## 1. What this is

StyleHub is a curated multi-brand storefront with **105 real products from 12 real brands** (Urban Revivo, Zara, Forever 21, Nike, Adidas, ASOS, Charles & Keith, APM Monaco, JW PEI, Songmont, DeMellier, Swarovski, 73Hours). **MatchBuy AI** is the layer on top: you pick one product, answer three quick questions (occasion, mood, budget), and a transparent scoring algorithm assembles a complete outfit from pieces across all the houses.

There is no cart and no payment: **every "Buy" button opens the product on the retailer's real website.** This is a concept prototype for studying how an AI shopping assistant should behave — honestly, explainably, and without faking intelligence.

## 2. Features

### The catalogue — real products, trustworthy data
- 105 products, each linking to its own page on the retailer's real website
- Every product carries a normalized source record (`src`: retailer, link type, last-checked date) — the adapter point where authorized retailer feeds could plug in
- Prices are labelled **reference prices** (converted when the product was added — not live quotes)
- Verified per-product **size runs** fetched from each retailer (clothing S/M/L variants incl. XXS–XXXL, shoe runs per retailer in EU/US/UK, jewellery and bags show no sizes)
- Real product photography stored locally, so the prototype works offline
- **See an example match** button runs a pre-filled, fully editable matching demo for first-time visitors

### MatchBuy AI matching
- Style brief: occasion (everyday / office / date / party), mood (minimal / cute / elegant / sexy), budget (¥2,000 / ¥3,000 / ¥4,000 / no limit), and which slots to fill
- Transparent scoring across five dimensions (style, colour harmony, silhouette balance, occasion, budget) — every recommendation shows **why** it was picked
- The look board is ordered by **body position**: outerwear → necklace → top → bottom → bag → shoes, with your selected piece at its natural place
- Slot re-roll (⟳) re-scores any single slot; the budget line reports honestly whether the total fits or is over by how much

### Wishlist & feedback
- Heart an item on its product page → saved to the Wishlist panel (persists across reloads)
- Rate every recommendation 👍 Helpful / 👎 Not for me, with optional reasons (style mismatch, wrong occasion, over budget, unavailable, incorrect link, other)
- Before anything is saved, a consent notice explains what is stored — **feedback is anonymous and never leaves your device** (no backend exists)
- A live summary shows counts, top reasons and **rule-based suggestions** for the matching weights, plus one-click JSON export

## 3. How the matching works

```
score = 0.20·style + 0.22·moodFit + 0.14·colourHarmony + 0.10·silhouetteBalance
      + 0.24·occasionFit + 0.10·budgetFit        (per candidate, per slot)
```
- `style` — style-family match against the chosen mood
- `moodFit` — the item's own mood tags vs. the chosen mood
- `colourHarmony` — neutral↔neutral / same-tone / contrast rules from photo-derived colour analysis
- `occasionFit` — whether the item is tagged for the chosen occasion
- `budgetFit` — keeps combinations inside the chosen budget; over-budget candidates are steered away
- Best-scoring candidate per slot wins; one brand-diversity bonus encourages crossing houses

Colours shown in the analysis table are **derived offline from each product photo** (dominant garment clusters), then hand-reviewed — they are not a live AI service.

## 4. What we did in this iteration

- Rebuilt the catalogue from live retailer data (Shopify product feeds, retailer product pages): 105 products across 12 houses with verified titles, prices, imagery, size runs and colours
- Added data-provenance labelling (exact product page vs. browse-the-retailer links, reference prices, last-checked dates) with an adapter point for authorized retailer feeds
- Added the 3-step onboarding with an editable example match
- Made matching context-sensitive (mood + occasion now dominate the score; no more repetitive picks) and ordered the look board by human body position
- Re-cropped model shots to the sold item (pose-assisted, then hand-reviewed) so users can picture the outfit
- Fixed sizing to match what retailers actually sell (letters for clothing, per-retailer shoe runs, no sizes for bags/jewellery)
- Added the anonymous, consent-gated feedback system with insights and JSON export
- Removed the AI Try-On experiment after review (local masking quality was not realistic); documented as future work

## 5. Data honesty

- No scraping claims and no live-data claims: data was captured from retailer product pages at build time
- Stock and size availability are treated as unknown and never shown; prices are marked as reference values
- Retailer checkout stays on the retailer's website — MatchBuy never handles payment
- No personal data is collected; feedback is device-local and exportable

## 6. Removed / future work

- **AI virtual try-on** — prototyped locally (pose + segmentation composite) and as a serverless integration; removed after review because fitting quality was not realistic without a generative VTON model. Future work: integrate a production VTON API with user consent.
- **Live retailer feeds** — replace captured prices/availability with authorized retailer APIs
- **Backend feedback analysis** — move the device-local feedback store behind a real service once real users exist

## 7. Project structure

| Path | Purpose |
|---|---|
| `index.html` | Entire prototype: storefront, per-house catalogue, product pages, matching algorithm, wishlist, feedback |
| `assets/` | Real product photography (stored locally so the site works offline) |
| `serve.py` | Tiny local server (`python serve.py` → http://localhost:8377) |
| `reference/` | Original project handbook material the prototype was modelled on |
| `versions/` | Archived earlier versions of the prototype |

## 8. Tech notes

- Single-file vanilla HTML/CSS/JS — no build step, no framework, no backend
- Matching, colour analysis and feedback all run locally in the browser
- The GitHub Pages deployment serves the same static file; nothing is generated

---

*Concept prototype for coursework. All product data is captured from the retailers' own public pages and credited to them; MatchBuy is not a store.*

## 9. Grounded in real user feedback

The problem space was grounded in public shopper voices (Reddit's r/femalefashionadvice and r/fashionwomens35): putting outfits together takes effort and a "creative eye" people feel they lack; shoppers want outfit ideas from pieces they already own and ways to organise combinations; coordinated sets appeal because they look put-together without effort; finding reputable products online is exhausting; and people want outfit-recommendation apps that link to where pieces can be bought. Short quotes and links are displayed in the prototype (home page, "The problem, in real words"), and each pain point maps to a design decision: complete-outfit building around one item with explanations, occasion/mood/budget controls, direct retailer product links with exact-vs-browse labelling — while "use pieces I already own" and saving whole combinations are documented as future work.
