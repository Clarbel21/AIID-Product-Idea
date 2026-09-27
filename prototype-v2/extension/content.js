(() => {
  if (document.getElementById("matchbuy-ai-host")) return;

  function readProduct() {
    const meta = (selector) => document.querySelector(selector)?.content?.trim() || "";
    const productJson = [...document.querySelectorAll('script[type="application/ld+json"]')].map((node) => {
      try { return JSON.parse(node.textContent); } catch { return null; }
    }).flatMap((item) => Array.isArray(item) ? item : item ? [item] : []).flatMap((item) => item["@graph"] || [item]).find((item) => {
      const type = item?.["@type"];
      return type === "Product" || (Array.isArray(type) && type.includes("Product"));
    });
    const offer = Array.isArray(productJson?.offers) ? productJson.offers[0] : productJson?.offers;
    const imageValue = productJson?.image;
    const imageFromJson = Array.isArray(imageValue) ? imageValue[0] : typeof imageValue === "string" ? imageValue : imageValue?.url;
    const title = productJson?.name || meta('meta[property="og:title"]') || document.querySelector("h1")?.innerText?.trim() || document.title;
    const rawPrice = offer?.price || offer?.lowPrice || meta('meta[property="product:price:amount"]') || meta('meta[itemprop="price"]');
    const currency = offer?.priceCurrency || meta('meta[property="product:price:currency"]') || "";
    const image = imageFromJson || meta('meta[property="og:image"]') || document.querySelector('main img[src], [role="main"] img[src], img[src]')?.src || "";
    const brandValue = productJson?.brand;
    const brand = typeof brandValue === "string" ? brandValue : brandValue?.name || "";
    return {
      title: String(title || "Product on this page").slice(0, 240),
      brand: String(brand).slice(0, 100),
      price: rawPrice ? Number(String(rawPrice).replace(/[^\d.]/g, "")) || null : null,
      currency: String(currency).slice(0, 8),
      imageUrl: image ? new URL(image, location.href).href : "",
      pageUrl: location.href,
      retailer: location.hostname.replace(/^www\./, "")
    };
  }

  const host = document.createElement("div");
  host.id = "matchbuy-ai-host";
  host.style.cssText = "all:initial;position:fixed;z-index:2147483647;inset:auto 20px 20px auto;";
  document.documentElement.appendChild(host);
  const root = host.attachShadow({ mode: "closed" });
  root.innerHTML = `
    <style>
      *{box-sizing:border-box} .panel{width:358px;max-height:min(690px,calc(100vh - 40px));overflow:auto;background:#fff;color:#292823;border:1px solid #e7e1dd;border-radius:15px;box-shadow:0 18px 54px #29251d30;font:13px/1.45 Arial,sans-serif}button{font:inherit;cursor:pointer}.head{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid #ece9e4;position:sticky;top:0;background:white;z-index:2}.brand{display:flex;align-items:center;gap:9px}.mark{width:30px;height:30px;border-radius:9px;background:#f7edee;color:#b77b82;display:grid;place-items:center;font-size:17px}.brand strong{font:600 14px Georgia,serif}.brand small{display:block;font:10px Arial,sans-serif;color:#777;margin-top:2px}.close{border:1px solid #e8e6e0;background:white;border-radius:50%;width:28px;height:28px;color:#777}.body{padding:16px}.kicker{font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:#a66d75;font-weight:bold}.title{font:500 21px/1.25 Georgia,serif;margin:6px 0}.copy{color:#777;font-size:11px;margin:5px 0 12px}.product{display:flex;gap:10px;background:#faf9f7;border-radius:9px;padding:9px;margin:12px 0}.product img{width:48px;height:56px;border-radius:5px;object-fit:cover;background:#eee}.product strong{font-size:11px;display:block}.product small{font-size:9px;color:#777;display:block;margin-top:3px;overflow-wrap:anywhere}.primary{width:100%;height:42px;background:#292823;color:white;border:0;border-radius:7px;font-weight:bold;letter-spacing:.07em}.primary:disabled{opacity:.55;cursor:wait}.privacy{font-size:9px;color:#777;text-align:center;margin:8px 4px 0;line-height:1.4}.notice{background:#f7f5f0;border-radius:8px;padding:10px;font-size:10px;color:#67655f;margin:10px 0}.analysis{border-top:1px solid #efede8;margin-top:14px;padding-top:12px}.analysis h3{font:500 17px Georgia,serif;margin:4px 0 9px}.facts{list-style:none;padding:0;margin:0}.facts li{font-size:10px;padding:6px 0;border-bottom:1px solid #f0eeea}.facts b{display:inline-block;width:74px}.card{border:1px solid #e8e6e0;border-radius:9px;margin:9px 0;overflow:hidden}.card-main{display:grid;grid-template-columns:78px 1fr;min-height:94px}.card img{width:78px;height:100%;min-height:94px;object-fit:cover;background:#eee}.card-copy{padding:8px}.card-copy small{font-size:9px;color:#777}.card-copy strong{display:block;font:500 13px/1.25 Georgia,serif;margin:2px 0}.price{font-weight:bold;font-size:11px}.why{font-size:9px;color:#696760;margin:4px 0 0}.retailer{font-size:9px;color:#777}.card a{display:block;border-top:1px solid #eee;padding:8px 10px;text-align:center;text-decoration:none;color:#333;font-size:10px;font-weight:bold}.empty{padding:13px;background:#faf9f7;border-radius:8px;font-size:10px;color:#777}.muted{font-size:9px;color:#777;text-align:center;margin-top:10px}.error{color:#8a424a;font-size:10px;margin:9px 0}.loading{color:#6d6a63;font-size:10px;margin:10px 0}.hide{display:none!important}
      @media(max-width:480px){.panel{width:min(358px,calc(100vw - 24px));max-height:calc(100vh - 24px)}:host{inset:auto 12px 12px auto!important}}
    </style>
    <section class="panel" role="dialog" aria-label="MatchBuy AI assistant">
      <header class="head"><div class="brand"><div class="mark">✦</div><div><strong>MatchBuy AI</strong><small>Your shopping sidekick</small></div></div><button class="close" aria-label="Close">×</button></header>
      <div class="body">
        <div class="kicker">For this product</div><h2 class="title">Find what goes with it.</h2>
        <p class="copy">A style-aware edit from stores across the web.</p>
        <div class="product"><img class="anchor-image" alt=""><div><strong class="anchor-title"></strong><small class="anchor-detail"></small></div></div>
        <div class="notice privacy-notice">When you ask for matches, product details and the product image URL are sent to your local MatchBuy service. AI analysis sends this product information to its configured AI provider.</div>
        <button class="primary match-button">✦ &nbsp; Match my outfit</button>
        <div class="error hide"></div><div class="loading hide">Reading the item and finding compatible products…</div>
        <div class="results hide"></div>
      </div>
    </section>`;

  const product = readProduct();
  const setText = (selector, text) => { const node = root.querySelector(selector); node.textContent = text; };
  setText(".anchor-title", product.title);
  setText(".anchor-detail", [product.brand, product.price ? `${product.currency || ""} ${product.price}`.trim() : "Price not found", product.retailer].filter(Boolean).join(" · "));
  if (product.imageUrl) root.querySelector(".anchor-image").src = product.imageUrl;

  root.querySelector(".close").addEventListener("click", () => host.remove());
  root.querySelector(".match-button").addEventListener("click", async () => {
    const button = root.querySelector(".match-button");
    const loading = root.querySelector(".loading");
    const error = root.querySelector(".error");
    button.disabled = true;
    loading.classList.remove("hide");
    error.classList.add("hide");
    try {
      const response = await chrome.runtime.sendMessage({ type: "MATCHBUY_RECOMMEND", product });
      if (!response?.ok) throw new Error(response?.error || "MatchBuy could not connect to the local service.");
      render(response.data);
    } catch (err) {
      error.textContent = `${err.message} Check the local service setup guide.`;
      error.classList.remove("hide");
    } finally {
      button.disabled = false;
      loading.classList.add("hide");
    }
  });

  function render(data) {
    const result = root.querySelector(".results");
    const analysis = data.analysis || {};
    const products = Array.isArray(data.recommendations) ? data.recommendations : [];
    result.replaceChildren();
    const status = document.createElement("div");
    status.className = "notice";
    status.textContent = `${data.integrations?.ai ? "Live AI analysis" : "Prototype analysis"} · ${data.integrations?.shopping ? "Live shopping results" : "Sample catalog"}`;
    result.append(status);
    const heading = document.createElement("div");
    heading.innerHTML = `<div class="kicker">Product analysis</div><h3>Style notes</h3>`;
    result.append(heading);
    const facts = document.createElement("ul");
    facts.className = "facts";
    for (const [label, value] of [["Colour", analysis.colour], ["Style", analysis.style], ["Shape", analysis.silhouette], ["Occasion", analysis.occasion]]) {
      if (!value) continue;
      const item = document.createElement("li");
      const strong = document.createElement("b"); strong.textContent = label;
      const span = document.createElement("span"); span.textContent = value;
      item.append(strong, span); facts.append(item);
    }
    result.append(facts);
    const recommendHeading = document.createElement("h3");
    recommendHeading.textContent = "Pieces to complete the look";
    result.append(recommendHeading);
    if (!products.length) {
      const empty = document.createElement("div"); empty.className = "empty"; empty.textContent = "No matches came back. Try a different product page."; result.append(empty);
    }
    for (const item of products) {
      const card = document.createElement("article"); card.className = "card";
      const main = document.createElement("div"); main.className = "card-main";
      const image = document.createElement("img"); image.alt = item.title || "Recommended product"; image.src = item.imageUrl || "";
      const copy = document.createElement("div"); copy.className = "card-copy";
      const source = document.createElement("small"); source.className = "retailer"; source.textContent = item.brand || item.retailer || "Retailer";
      const title = document.createElement("strong"); title.textContent = item.title || "Product";
      const price = document.createElement("div"); price.className = "price"; price.textContent = item.price || "Price not listed";
      const why = document.createElement("p"); why.className = "why"; why.textContent = item.reason || "Selected to complement this product’s style.";
      copy.append(source, title, price, why); main.append(image, copy); card.append(main);
      if (item.url) {
        const link = document.createElement("a"); link.href = item.url; link.target = "_blank"; link.rel = "noopener noreferrer"; link.textContent = item.linkType === "shopping" ? "See offers on Google Shopping ↗" : `View at ${item.retailer || "retailer"} ↗`; card.append(link);
      }
      result.append(card);
    }
    const foot = document.createElement("p"); foot.className = "muted"; foot.textContent = "MatchBuy recommends. The retailer completes the transaction."; result.append(foot);
    result.classList.remove("hide");
  }
})();

