#!/usr/bin/env python3
"""Development preview serving only the same public files staged for Pages."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = {'/', '/index.html', '/styles.css', '/app.js', '/lib.js', '/assets/mark.svg', '/data/research.json'}


class PublicHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def allowed(self):
        return unquote(urlsplit(self.path).path) in PUBLIC

    def do_GET(self):
        if not self.allowed():
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.allowed():
            self.send_error(404)
            return
        super().do_HEAD()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()


if __name__ == '__main__':
    print('Sunset Repair preview on 0.0.0.0:4173 (public files only)', flush=True)
    ThreadingHTTPServer(('0.0.0.0', 4173), PublicHandler).serve_forever()
