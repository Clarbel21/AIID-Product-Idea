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

## 3. The houses & the 90+ real products

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

Data provenance: Urban Revivo, DeMellier and JW PEI were pulled live from their Shopify product endpoints (exact title, price, image). Zara, Forever 21 and Swarovski were captured from their product pages. All prices are shown in **RMB** (converted where the house sells in USD/CAD — Urban Revivo from its USD global store, Charles & Keith from its CAD store, ASOS as displayed in CNY — indicative). Photos are the houses’ own product imagery, stored locally so the prototype works offline.

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
- **Budget matching (FN-05)** — the style brief asks your budget (Under ¥2,000 / ¥2,000–3,000 / ¥3,000–4,000 / No limit); the scoring steers every slot and the results line reports honestly (fits / over by X).

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

## v2 branch (`v2-trust-feedback`) — trustworthy data, onboarding, feedback

Built on branch `v2-trust-feedback`; `main` remains untouched as the previous prototype.

**Section 1 · Data provenance.** Every product carries a normalized source record (`p.src = {retailer, url, type, checked, via}`):
- `type: 'exact'` = the link opens that exact product page; `type: 'browse'` = it goes to the retailer's page/collection (button then reads **Browse retailer**). Currently the 5 Songmont entries are `browse` (homepage links); all others are exact product pages.
- Prices are labelled **reference prices** — currency conversions captured when the product was added, not live quotes. Stock and size availability are labelled **not verified** everywhere.
- `checked` records when the link was last verified live (the Urban Revivo/ASOS/Charles & Keith/new Forever 21 groups: 2026-09-28; older groups: `null` → shown as "not recently checked").
- No scraping and no live data are claimed. The normalizer (`normalizeProvenance()` in `index.html`) is the adapter point where an authorized retailer feed or API could populate `price`, `availability` and `checked` later.
- The detailed source line is deliberately **not shown on the product page** (user preference) — the record lives in the data layer and drives the exact-vs-browse button labels; the page itself shows only the reference-price and availability-not-verified labels.

**Section 2 · Onboarding.** The hero shows the 3-step flow (pick a product → occasion & mood → budget) with a **See an example match** button that pre-runs a real, editable example (camel coat · date night · elegant · under ¥2,000). The brief responds visibly to every answer; catalogue cards and chips are keyboard-operable (Enter/Space, real buttons); responsive CSS covers ≤640px phones.

**Section 3 · Feedback (anonymous, device-only).** Every recommended item can be marked 👍 Helpful or 👎 Not for me. Negative marks optionally record a reason (style mismatch · wrong occasion · over budget · unavailable · incorrect product/link · other). Before anything is saved, a consent notice explains that feedback is stored only in the browser (localStorage), anonymously, with no names/emails/photos, and is never sent anywhere. The results view shows a live summary (helpful vs not, top reasons, weakest slot) with **rule-based** suggestions for the matching weights — no training or learning is claimed. Feedback can be exported as JSON (`matchbuy-feedback.json`).

**What still needs a real backend / retailer integration:** verified live prices & stock (retailer feed/API), server-side feedback collection and analysis (none exists — feedback is device-local by design), and real shopper feedback data.
