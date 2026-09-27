const browserPluginRoot =
  process.env.ZCODE_PLUGIN_ROOT ?? process.env.CLAUDE_PLUGIN_ROOT;
const { join } = await import("node:path");
const { pathToFileURL } = await import("node:url");
const browserClientUrl = pathToFileURL(
  join(browserPluginRoot, "scripts", "browser-client.mjs"),
).href;
const { setupBrowserRuntime } = await import(browserClientUrl);
await setupBrowserRuntime({ globals: globalThis });
const browser = await agent.browsers.getForUrl("http://localhost:8377/");
const tabs = await browser.tabs.list();
const info = tabs.find(t => (t.url||"").includes("8377"));
const tab = await browser.tabs.get(info.id);
const dbg = await tab.playwright.evaluate(() => {
  const log = [];
  try {
    openProduct('ur1');
    log.push('product ok');
    openDrawer();
    log.push('drawer ok');
    renderBrief();
    log.push('brief ok, budget chips=' + document.querySelectorAll('[data-action="pick-budget"]').length + ', slot chips=' + document.querySelectorAll('[data-action="pick-slot"]').length);
    document.querySelector('[data-action="pick-occ"][data-id="everyday"]').click();
    document.querySelector('[data-action="pick-mood"][data-id="cute"]').click();
    document.querySelector('[data-action="pick-budget"][data-id="b2000"]').click();
    log.push('picked');
    startScan();
    log.push('scan ok');
  } catch(e) {
    log.push('CRASH: ' + e.message + ' @ ' + (e.stack||'').split('\n')[1]);
  }
  return log;
});
JSON.stringify(dbg, null, 1);
