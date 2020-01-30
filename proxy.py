#!/usr/bin/env python

import requests
import threading
from socket import *
from requests.exceptions import HTTPError
from handle_requests import *

class proxy(socket):
    def __init__(self, ip, port, backlog = 0): 
        super().__init__(AF_INET, SOCK_STREAM)

        self.bind_ip = ip
        self.bind_port = port

        self.bind((self.bind_ip, self.bind_port))
        self.listen(backlog)

        print(f'Listening on {self.bind_ip}:{self.bind_port}')

    def handle_client_method(request):
        try:
            response = requests.get(request.path, headers=request.headers)
            response.raise_for_status()
        except HTTPError as http_error:
            print(f'HTTP error: {http_error}')
        except Exception as error:
            print(f'Error: {error}')
        else:
            print(f'request headers from server: {response.headers}')
            return response

    def handle_client_connection(client_socket):
        request = HTTPRequest(client_socket.recv(1024))
        if request.error_code:
            print(f'Parsing error: {request.error_code}: {request.error_message}')
            return request.error_code

        print(f'Received {request.command} {request.path}')
        print(f'request headers from client: {request.headers}')

        client_socket.send(proxy.handle_client_method(request).content)
        client_socket.close()

    def wait_and_thread(self):
        client_sock, address = self.accept()
        print(f'Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(
                target=proxy.handle_client_connection,
                args=(client_sock,)
                )
        client_handler.start()
