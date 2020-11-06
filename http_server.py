import sys
import http.server
import socketserver
from argparse import ArgumentParser


DEFAULT_PORT = 8000


class FakeHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")
        self._set_response()
        self.wfile.write("{}".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(
            f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:"
            "\n{post_data.decode('utf-8')}\n"
        )

        self._set_response()
        self.wfile.write("{}".encode('utf-8'))

def start_webserver(port):
    Handler = FakeHTTPRequestHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


if __name__ == '__main__':
    parser = ArgumentParser(description="Fake HTTP server")
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help='HTTP Port to serve'
    )
    args = parser.parse_args(sys.argv[1:])

    start_webserver(args.port)
