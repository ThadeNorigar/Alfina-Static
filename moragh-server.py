"""
Moragh + Vael Karten-Editor Server
Startet einen lokalen Server der:
- Moragh-Editor unter /            → schreibt buch/moragh-karte.json
- Vael-Editor unter /vael          → schreibt buch/vael-karte.json
- GET/POST /data                   → Moragh-Daten
- GET/POST /vael-data              → Vael-Daten
"""
import http.server
import json
import os

PORT = 8090
BASE = os.path.dirname(__file__)
MORAGH_DATA = os.path.join(BASE, 'buch', 'moragh-karte.json')
MORAGH_EDITOR = os.path.join(BASE, 'moragh-editor.html')
VAEL_DATA = os.path.join(BASE, 'buch', 'vael-karte.json')
VAEL_EDITOR = os.path.join(BASE, 'vael-editor.html')

ROUTES = {
    '/data':      {'file': MORAGH_DATA, 'label': 'cities'},
    '/vael-data': {'file': VAEL_DATA,   'label': 'places'},
}
PAGES = {
    '/':            MORAGH_EDITOR,
    '/index.html':  MORAGH_EDITOR,
    '/vael':        VAEL_EDITOR,
    '/vael.html':   VAEL_EDITOR,
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ROUTES:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(ROUTES[self.path]['file'], 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        elif self.path in PAGES:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(PAGES[self.path], 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path in ROUTES:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                with open(ROUTES[self.path]['file'], 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                label = ROUTES[self.path]['label']
                count = len(data.get(label, [])) if isinstance(data.get(label), list) else 0
                self.wfile.write(json.dumps({"ok": True, label: count}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        if '/data' in str(args[0]):
            print(f"  {args[0]}")

if __name__ == '__main__':
    print(f"Moragh Editor: http://localhost:{PORT}")
    print(f"Daten: {DATA_FILE}")
    server = http.server.HTTPServer(('', PORT), Handler)
    server.serve_forever()
