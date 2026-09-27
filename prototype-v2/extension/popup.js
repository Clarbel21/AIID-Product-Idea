const titleEl = document.getElementById("page-title");
const statusEl = document.getElementById("status");
const activateButton = document.getElementById("activate");

async function send(type) {
  return chrome.runtime.sendMessage({ type });
}

async function init() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  titleEl.textContent = tab?.title || "No active page";
  activateButton.disabled = !tab?.id || !/^https?:/.test(tab.url || "");
  if (!activateButton.disabled) {
    activateButton.addEventListener("click", async () => {
      activateButton.disabled = true;
      activateButton.textContent = "Opening assistant…";
      try {
        await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
        window.close();
      } catch (error) {
        activateButton.disabled = false;
        activateButton.textContent = "Show MatchBuy on this page";
        statusEl.textContent = error.message || "This page does not allow extension panels.";
      }
    });
  } else {
    statusEl.textContent = "Open a regular shopping page first. Browser settings pages cannot be read.";
  }

  const health = await send("MATCHBUY_HEALTH").catch(() => ({ ok: false }));
  if (!health.ok) {
    statusEl.textContent = "Local service is offline. Start it using the extension setup guide.";
    return;
  }
  const flags = health.data.integrations;
  statusEl.innerHTML = `<b>Local service connected.</b> AI ${flags.ai ? "ready" : "needs a key"} · Product search ${flags.shopping ? "ready" : "sample catalog"}.`;
}

init();

