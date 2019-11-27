from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import os

data = {'result': 'this is a test'}
host = ('localhost', 8619)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        print('-' * 80)
        get = urllib.parse.urlparse(self.path)
        print(get)
        word = get.query
        print(word)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join('html_format', 'text.html')) as f:
            s = f.readlines()
            html = ''.join(s).format(**{'query_word': word})

        self.wfile.write(html.encode()) # json.dumps(data).encode())


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received: EXITING')
    finally:
        server.server_close()