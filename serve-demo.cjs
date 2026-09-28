const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const root = path.resolve(__dirname);
const port = 8377;
const mime = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
  '.svg': 'image/svg+xml', '.webp': 'image/webp', '.ico': 'image/x-icon'
};
const url = `http://127.0.0.1:${port}/`;
function openBrowser() {
  const child = spawn('cmd.exe', ['/c', 'start', '', url], { detached: true, stdio: 'ignore', windowsHide: true });
  child.unref();
}
const server = http.createServer((req, res) => {
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, url).pathname); }
  catch { res.writeHead(400).end('Bad request'); return; }
  const file = path.resolve(root, `.${pathname}`);
  if (file !== root && !file.startsWith(root + path.sep)) { res.writeHead(403).end('Forbidden'); return; }
  const target = file === root ? path.join(root, 'index.html') : file;
  fs.stat(target, (err, stat) => {
    if (err || !stat.isFile()) { res.writeHead(404).end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': mime[path.extname(target).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    if (req.method === 'HEAD') { res.end(); return; }
    fs.createReadStream(target).pipe(res);
  });
});
server.on('error', err => {
  if (err.code === 'EADDRINUSE') {
    console.log(`StyleHub is already running at ${url}; opening it now.`);
    openBrowser();
    return;
  }
  console.error(err.message);
  process.exitCode = 1;
});
server.listen(port, '127.0.0.1', () => {
  console.log(`StyleHub is running at ${url}. Keep this window open while you use it.`);
  openBrowser();
});
