import http.server
import socketserver

PORT = 8377

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, *args):
        pass

class ThreadedServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

with ThreadedServer(("", PORT), NoCacheHandler) as httpd:
    print(f"Serving StyleHub × MatchBuy AI on http://localhost:{PORT} (threaded, no-cache)")
    httpd.serve_forever()
