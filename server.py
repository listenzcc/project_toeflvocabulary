from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json

data = {'result': 'this is a test'}
host = ('localhost', 8619)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        get = urllib.parse.urlparse(self.path)
        print(get)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()