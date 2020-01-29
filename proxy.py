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

    def handle_client_connection(client_socket):
        request = HTTPRequest(client_socket.recv(1024))
        if request.error_code:
            print(f'Error : {request.error_code} : {request.error_message}')
        else:
            print(f'Received {request.command} {request.path}')
            try:
                response = requests.get(request.path)
                response.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                print(f'Other error occurred: {err}')
            else:
                print(response.text)
                client_socket.send(response.content)

        client_socket.close()

    def wait_and_thread(self):
        client_sock, address = self.accept()
        print(f'Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(
                target=proxy.handle_client_connection,
                args=(client_sock,)
                )
        client_handler.start()
