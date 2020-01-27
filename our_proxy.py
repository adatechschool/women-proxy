#!/usr/bin/env python

import socket
import threading
import requests

from http.server import BaseHTTPRequestHandler
from io import BytesIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print (f'Listening on {bind_ip}:{bind_port}')

def handle_client_connection(client_socket):
    raw_request = client_socket.recv(1024)
    request = HTTPRequest(raw_request)
    print (f'Received {request.path} {request.command}')
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print (f'Accepted connection from {address[0]}:{address[1]}')
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()

