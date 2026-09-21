"""One-shot mock: answers every POST with z.ai's 429 rate-limit shape.
Used only by cli verification of the graceful-limit path.  python mock429.py
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

BODY = json.dumps({
    "error": {
        "code": 1302,
        "message": "Your request has been rate limited due to too many requests per second",
    }
}).encode()


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.send_response(429)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(BODY)))
        self.end_headers()
        self.wfile.write(BODY)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *_):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8125), H).serve_forever()
