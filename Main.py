from http.server import HTTPServer, BaseHTTPRequestHandler
from Logging import LOG; LOG.name = ... # Name your logger here
import HTTPHandler, re

PORT = ... # Assign your port here


class Server(BaseHTTPRequestHandler):
    with open('./http/404/index.html') as file_in: index = file_in.buffer.read()
    fourohfour = 404, [], index # This variable is for the default 404 page in "/http/404"

    def do_GET(self) -> None:
        url, pairs = self.path.split('?') + [""]
        if re.search("^([^.]*[^/])$", url): return self.send_data(308, [("Location", f'{"/".join(self.path.split("?") + [""])}{("?" + pairs) if pairs else ""}')], "")
        url = url.removeprefix('/').removesuffix('/')
        parameters = {}
        for pair in pairs.split('&'):
            pair = pair.split('=') + [True]
            parameters[pair[0]] = pair[1]

        status, headers, data = HTTPHandler.handle_GET_request(url.lower().split('/'), parameters)
        self.send_data(status, headers, data)


    def do_POST(self) -> None:
        body = self.rfile.read(int(self.headers['Content-Length']))

        status, headers, data = HTTPHandler.handle_POST_request(body)
        self.send_data(status, headers, data)


    def send_data(self, status, headers, data) -> None:
        self.send_response(status)
        # self.send_header("Access-Control-Allow-Origin", "*") # Uncomment this if you are using a reverse proxy system.
        for header in headers: self.send_header(*header)
        self.end_headers()
        if not isinstance(data, (bytes, bytearray)): data = bytes(data, 'utf-8')
        self.wfile.write(data)

    def log_message(self, format, *args): pass


if __name__ == '__main__':
    LOG.info("Opening HTTP Server.")
    server = HTTPServer(("0.0.0.0", PORT), Server)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    except Exception as e: LOG.critical(e)
    LOG.warning("Closed HTTP Server.")