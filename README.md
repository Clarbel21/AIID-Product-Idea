# StyleHub × MatchBuy AI — Product Handbook Edition (v6.1)

**Course:** AI + Innovative Design (Master's) · **Deliverable:** clickable web prototype

> *Find the match. **Complete the look.** Buy it.*

A Dior-inspired storefront for **StyleHub × MatchBuy AI** with a catalogue of **real products from real houses** — every card links to the product’s own page on the brand’s real website. The MatchBuy AI layer asks your occasion and mood, then a transparent scoring algorithm builds a complete look from pieces across all the houses. No cart, no payment: Buy Now goes directly to the brand.

---

## 1. Run / access online

- **Live online:** https://clarbel21.github.io/AIID-Product-Idea/ (GitHub Pages — auto-deploys on every push; note github.io can be intermittent from mainland China)
- **Offline:** double-click `index.html` (photos are local; works fully offline)
- **Local server:** `python -m http.server 8000` or `python serve.py`

Fonts load from Google Fonts when online; graceful fallback offline.

## 2. Files

| File | Purpose |
|---|---|
| `index.html` | Entire prototype: home, per-house catalogue, product pages, matching algorithm, try-on, wishlist |
| `assets/` | Real product photography downloaded from the houses (50+ shots) + generated colourways + campaign image |
| `reference/` | The source handbook + extracted text |

## 3. The houses & the 50+ real products

| House | Pieces | Deep links |
|---|---|---|
| Sporty & Rich (the icon) | Cropped Tank — white/black/sky | sportyandrich.com |
| Urban Revivo | 8 shirts, blouses & skirts | global.urbanrevivo.com product pages |
| Zara | 5 (jacket, trench, metallic dress, parka, boots) | zara.cn product pages |
| Forever 21 | 6 (peplum top, cami, set, fleece, shorts ×2) | forever21.com product pages |
| Max Mara | 5 (camel coat + 4 Teddy Bear coats) | us.maxmara.com |
| 73Hours | 5 (heels, mules, sandals) | 73hours.com.cn |
| Nike | 5 (AF1 ×3, Dunk ×2) | nike.com product / collection pages |
| Adidas | 5 (Samba OG colourways) | adidas.com/us/samba-og-shoes |
| JW PEI | 5 (Cleo, Noor, Hana, Tulip, Nala) | jwpei.com product pages |
| Songmont | 5 (tote, Luna crescents, bucket) | songmontofficial.com |
| DeMellier | 5 (Hudson, Brooklyn, Stockholm, Florence, Siena) | demellierlondon.com product pages |
| Swarovski | 8 (Classica, Mesmera, Gema, Matrix, Symbolica, Swan ×2, Una) | swarovski.com.cn product pages |

Data provenance: Urban Revivo, DeMellier and JW PEI were pulled live from their Shopify product endpoints (exact title, price, image). Zara, Forever 21 and Swarovski were captured from their product pages. All prices are shown in **RMB** (converted where the house sells in USD/GBP — indicative). Photos are the houses’ own product imagery, stored locally so the prototype works offline.

Removed in this version: Brandy Melville and Charles & Keith (website access issues, per feedback) and the Sporty & Rich “icon” section (per feedback).

## 4. The matching algorithm — why moods differ

`matchOutfit()` scores every compatible piece in the edit for each needed slot (top / bottom / shoes / bag / jewelry — the slots depend on the anchor’s category):

```
score = 50
 + 30  mood match      − 25  mood mismatch   (cute · elegant · sexy · minimal)
 + 18  occasion match  − 12  occasion mismatch (everyday · office · date · party)
 + colour harmony      (light↔dark contrast +10, same tone +8, warm/cool clash +4)
 + 8   cross-house bonus
 − price drift (a piece > 4× the anchor’s price)
 + stable tie-break
```

Because mood mismatch is *penalised*, each feeling builds a genuinely different look. Verified on the same anchor: **Minimal** → pinstripe skirt + cream Samba + navy Hana tote + Classica pendant; **Cute** → denim skirt + taupe Samba + Cleo bag + Symbolica stars; **Elegant** → fishtail skirt + pony-hair AF1 LX + Swan earrings; **Sexy** → suede micro shorts + pink Noor bag + pink Swan bracelet.

## 5. Feature notes (per latest feedback)

- **Real imagery only** — all product photos are the houses’ own shots; no generated stand-ins. (The Zara images required the browser session to download due to CDN protection — they’re stored locally now.)
- **No unverified policies** — the “30-day returns / free shipping” claims were removed; the product page now says returns & shipping follow *each house’s own policy*, and Buy Now happens on the house’s site.
- **Sizes only where they make sense** — jewelry and bags show no size selector; shoes show EU sizes, clothing shows XS–XL (category defaults in `DEF_SIZES`).
- **Wishlist fixed** — the panel now opens correctly, hearts **fill and pop in blush** when tapped, and the list persists in `localStorage`. Stale entries for removed products are filtered on load.
- **Sporty & Rich section removed** per feedback. To re-enable true colour switching elsewhere, add `colors:[{name,img},…]` to any product.
- **Direct shopping (FN-06)** — Buy Now opens the piece on the house’s real website; StyleHub never handles payment.

## 6. Modify

- **Products:** the `CATALOGUE` array — `{id, brand, name, price(RMB), img, url, cat, tone, moods, occs, styles, why}`. `cat` ∈ top/outerwear/bottom/dress/shoes/bag/accessory.
- **Houses/links:** `BRANDS` (with `url`) + `BRAND_ORDER`.
- **Matching weights:** the `matchOutfit()` scoring block; stylist sentences in `matchReason()`.
- **Size defaults per category:** the `DEF_SIZES` map.

## 7. Demo script

1. **Home** — scroll the houses: five real products each, every card opens the real product page.
2. **Pick a piece** (e.g., the Zara metallic dress) → **Match My Outfit** → occasion *Party* + feeling *Sexy*.
3. **The look** — assembled board from four houses with match index and budget line.
4. **Change the mood to Elegant** — the picks change; the algorithm decides.
5. **Item details → Buy Now on {house} ↗** — direct to the real product page.
6. **Wishlist** — ♡ pieces → panel → reload → still saved.
7. **Try-On** — upload a body photo → simulated render.
