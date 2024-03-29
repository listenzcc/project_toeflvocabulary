import os
import json
import random
import webbrowser
import urllib.parse
from pprint import pprint
from random_word import random_word
from checkout_online import explain_word
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
        word = parsed_result.query
        html_path = parsed_result.path[1:]

        Right_side_contents = []
        print(word)
        if word == '[random]':
            word = random_word()
            print(word)
        word_explains = explain_word(word)
        # pprint(word_explains)
        for name in word_explains:
            Right_side_contents.append(wrap('h2', name))
            Right_side_contents.append(wrap('p', word_explains[name]))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(os.path.join('.', html_path), 'r') as f:
            s = f.readlines()
            html = ''.join(s).format(query_word=word, Right_side_contents='\n'.join(Right_side_contents))

        self.wfile.write(html.encode('utf-8', errors='ignore')) # json.dumps(data).encode())


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    url = 'http://%s:%s/checkout.html?[random]' % host
    print("Open {} to start.".format(url))
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupt received: EXITING')
    finally:
        server.server_close()