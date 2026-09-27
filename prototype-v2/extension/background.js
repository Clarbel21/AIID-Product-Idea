const API_BASE = "http://127.0.0.1:4177";

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "MATCHBUY_HEALTH") {
    fetch(`${API_BASE}/api/health`)
      .then((response) => response.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch(() => sendResponse({ ok: false, error: "Local MatchBuy service is not running." }));
    return true;
  }

  if (message?.type === "MATCHBUY_RECOMMEND") {
    fetch(`${API_BASE}/api/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(message.product)
    })
      .then(async (response) => {
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || `MatchBuy service returned ${response.status}`);
        sendResponse({ ok: true, data });
      })
      .catch((error) => sendResponse({ ok: false, error: error.message }));
    return true;
  }
});

