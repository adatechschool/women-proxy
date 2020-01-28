#!/usr/bin/env python

import socket
import threading
import requests
import signal
import sys

from http.server import BaseHTTPRequestHandler
from io import BytesIO

def quit_on_ctrl_c(sig, frame):
    print()
    sys.exit(0)
signal.signal(signal.SIGINT, quit_on_ctrl_c)

def handle_client_connection(client_socket):
    raw_request = client_socket.recv(1024)
    request = HTTPRequest(raw_request)
    if request.error_code:
        print (f'Error : {request.error_code} : {request.error_message}')
    else:
        print (f'Received {request.command} {request.path}')
    client_socket.close()

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

while True:
    client_sock, address = server.accept()
    print (f'Accepted connection from {address[0]}:{address[1]}')
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()
