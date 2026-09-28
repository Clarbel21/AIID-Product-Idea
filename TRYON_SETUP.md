# Natural AI Try-On setup

The website's try-on UI is ready, but the live FASHN generation cannot run on GitHub Pages alone. GitHub Pages serves the HTML but does not run the private `/api/tryon` server function. Keep the API key off the public page.

## Before you start

1. Create a FASHN developer account and API key in the [FASHN API dashboard](https://app.fashn.ai/).
2. Purchase credits in the FASHN dashboard. The configured Try-On Max `balanced`, `1k`, one-image request uses 2 credits.
3. Create a Vercel account and import this GitHub repository. Deploy the repository root; Vercel automatically serves `index.html` and the `api/tryon.js` function.

## Set the private server values in Vercel

In the Vercel project, open **Settings → Environment Variables** and add:

- `FASHN_API_KEY`: your private key from FASHN.
- `MATCHBUY_TRYON_ACCESS_CODE`: a long random passcode that you will give only to your testers.
- `MATCHBUY_ALLOWED_ORIGINS`: the exact website origin Vercel gives your deployment, such as `https://your-project.vercel.app` (no trailing slash).

Redeploy after adding the variables. Do not put the FASHN key or access code in `index.html`, GitHub commits, or public screenshots. `.env.example` is a template only.

## Use the natural try-on

1. Open the Vercel website URL (the GitHub Pages URL cannot execute the API).
2. Choose a clothing item and open AI Try-On.
3. Select a clear, full-body photo. The browser compresses it locally first.
4. Read and accept the image-processing notice, then enter the private demo access code.
5. Select **Generate natural try-on**. The photo is sent to FASHN after consent; one FASHN generation uses credits.
6. The result is an AI-generated visual approximation, not a guarantee of exact color, size, or fit.

The interface links to FASHN's current [data-retention details](https://docs.fashn.ai/api-overview/data-retention-privacy). Base64 uploads are processed by FASHN; request metadata remains in its request history. MatchBuy does not save the uploaded or generated image. Closing the try-on panel clears the in-page image state.

## If the site says the service is not configured

Check that the website is open on the Vercel deployment, all three environment variables are set correctly, and the deployment has been rebuilt. If FASHN has no credits or rejects its key, the page displays a service error rather than showing a fake try-on.
