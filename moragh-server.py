"""
Moragh Karten-Editor Server
Startet einen lokalen Server der:
- Den Editor unter / ausliefert
- GET /data liefert die Kartendaten
- POST /data speichert die Kartendaten permanent in buch/moragh-karte.json
"""
import http.server
import json
import os

PORT = 8090
DATA_FILE = os.path.join(os.path.dirname(__file__), 'buch', 'moragh-karte.json')
EDITOR_FILE = os.path.join(os.path.dirname(__file__), 'moragh-editor.html')

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        elif self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(EDITOR_FILE, 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/data':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "cities": len(data.get("cities", []))}).encode())
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
