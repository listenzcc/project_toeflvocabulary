import os
import json
import random
import webbrowser
import urllib.parse
from pprint import pprint
from random_word import random_word
from http.server import HTTPServer, BaseHTTPRequestHandler

data = {'result': 'this is a test'}
host = ('localhost', 8619)

def wrap(label, content):
    return '<{label}> {content} </{label}>'.format(label=label, content=content)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        print('-' * 80)
        parsed_result = urllib.parse.urlparse(self.path)
        print(parsed_result)

        html_path = parsed_result.path[1:]

        word = parsed_result.query
        if word == '[random]':
            word = random_word()

        Right_side_contents = []

        replace = {
            'query_word': word,
            'Right_side_contents': '\n'.join(Right_side_contents),
        }

        with open(os.path.join('.', html_path), 'r') as f:
            s = f.readlines()
            html = ''.join(s)
            for r in replace:
                html = html.replace('{--'+r+'--}', replace[r])

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8', errors='ignore')) # json.dumps(data).encode())


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    url = 'http://%s:%s/checkword.html?[random]' % host
    print("Open {} to start.".format(url))
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received: EXITING')
    finally:
        server.server_close()