#!/usr/bin/env python

import requests
import threading
from socket import *
from requests.exceptions import HTTPError
from handle_requests import *

class Proxy(socket):
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
            #print(f'received from server: {response.headers} {response.text}')
            return response

    def handle_client_connection(client_socket):
        request = HTTPRequest(client_socket.recv(1024))
        if request.error_code:
            print(f'Parsing error: {request.error_code}: {request.error_message}')
            return request.error_code

        print(f'Received {request.command} {request.path}')
        response = Proxy.handle_client_method(request)
        # TODO
        # Send response.text as parameter to an arbitrary function parsing it.
        # Retrieve parsed response and convert it as BytesIO.
        # Check size of new parsed and set it in header.
        # Send it back to client.
        client_socket.send()
        client_socket.close()

    def wait_and_thread(self):
        client_sock, address = self.accept()
        print(f'Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(
                target=Proxy.handle_client_connection,
                args=(client_sock,)
                ).start()
