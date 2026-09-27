# MatchBuy AI browser extension prototype

This folder contains an installable Chrome Manifest V3 extension and a local Node service. It is a new version alongside the website simulation; the original GitHub `main` remains unchanged.

## What works

- Click the extension button on a product page to show the MatchBuy panel. The extension uses Chrome's `activeTab` permission and reads the current page only after that click.
- Detect common product details from JSON-LD Product data, Open Graph metadata, and visible page headings: title, brand, price, currency, and image.
- Send the selected product to the local service for product analysis and cross-store recommendations.
- Use OpenAI for live text and image analysis when `OPENAI_API_KEY` is set.
- Use SerpApi's Google Shopping results when `SERPAPI_API_KEY` is set. Results can contain product, price, image, merchant, and outbound link data. When the provider supplies a direct merchant link, the card opens it; otherwise it clearly opens the Google Shopping offer page.
- Open recommendation links in a separate tab. MatchBuy does not collect payment or handle checkout.
- Use a clearly labeled sample analysis and sample catalog when API keys are not configured.

## Run the local service

You need Node.js 20 or newer. Copy `.env.example` to `.env` in this `server` folder and add your own API keys there. `server/.env` is ignored by Git.

```powershell
cd path\to\MatchBuy-AI-v2\server
Copy-Item .env.example .env
notepad .env
npm start
```

Set `OPENAI_API_KEY` to enable live AI analysis. Set `SERPAPI_API_KEY` to enable live shopping search. You can configure `SHOPPING_GL` and `SHOPPING_HL` for the shopping market and language; the market setting also determines the displayed local currency. API providers may charge for usage under their own plans.

The service listens on `127.0.0.1:4177`. It never sends API keys to the extension; keys remain in the local service environment.

## Load the extension in Chrome

1. Open `chrome://extensions` and turn on **Developer mode**.
2. Choose **Load unpacked** and select this `extension` folder.
3. Open a normal shopping product page and click the MatchBuy extension button.
4. Click **Show MatchBuy on this page**, then **Match my outfit**.

Browser settings pages and the Chrome Web Store do not allow the panel to be injected. Some retailer pages have limited product metadata; those pages may show the title and image but omit brand or price.

## Privacy and prototype limits

The extension does not read shopping pages until you click its toolbar button. When you ask for matches, it sends the page title, detected product fields, page URL, retailer hostname, and product image URL to the local service. When configured, product information and the image URL are sent to OpenAI for analysis; search terms are sent to SerpApi. Review those providers' terms and privacy policies before using real shoppers' data.

The extension does not sign into retailer accounts, read cart contents, buy items, or process payment. Retailer policies and stock can change. SerpApi's Google Shopping integration is a third-party shopping search source, not an official feed from each retailer. For stable retailer product links, affiliate attribution, and commercial use, MatchBuy would need direct retailer feeds or approved affiliate-network access. This is a prototype, not a production extension or affiliate integration.

