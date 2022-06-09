from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer
import http.server
import socketserver

import threading
from os import getenv


class HTTPServerThread(threading.Thread):
    def __init__(self, port, directory):
        threading.Thread.__init__(self)
        self.port = int(port)
        self.directory = directory

    def run(self):
        DIRECTORY = self.directory
        print("[SERVER] Starting the server...")

        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=DIRECTORY, **kwargs)

        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            print("[SERVER] Result serving at port: ", self.port)
            httpd.serve_forever()


class FTPServerThread(threading.Thread):
    def __init__(self, port, directory, address="127.0.0.1"):
        threading.Thread.__init__(self)

        authorizer = DummyAuthorizer()
        authorizer.add_user(getenv('FTP_USER'),
                            getenv('FTP_PASSWORD'), directory)

        handler = FTPHandler
        handler.authorizer = authorizer

        self.server = FTPServer((address, port), handler)

    def run(self):
        self.server.serve_forever()
