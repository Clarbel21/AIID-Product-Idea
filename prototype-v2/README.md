# MatchBuy AI browser simulation

This is a separate prototype version based on the existing StyleHub × MatchBuy AI project. The original `main` branch remains unchanged.

Open `index.html` in a browser to explore the simulated retailer product page and floating MatchBuy AI assistant.

## Prototype flow

1. View a Zara product page with the MatchBuy AI panel.
2. Select **Match my outfit** to see the simulated product analysis.
3. Build the outfit and switch between **Any brand**, **Same brand**, and **Under ¥500**.
4. Open a recommendation to see the retailer handoff confirmation, or use **Shop this look** to see the multi-retailer explanation.
5. Scroll to **Where we’re going** for the future extension journey.

Product data, analysis and recommendations are predefined for this prototype. Retailer pages are represented with external links; there are no shopping APIs, real AI, or checkout integrations.

## Browser extension prototype

The separate [`extension`](extension/README.md) folder contains an installable Chrome extension and a local Node service. It can read product details after you click the extension button, request AI analysis and shopping results when API keys are configured, and link to retailer offers. See its setup guide for the local service and extension installation steps.

