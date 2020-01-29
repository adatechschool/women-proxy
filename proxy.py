#!/usr/bin/env python

import requests
from socket import *
from requests.exceptions import HTTPError
from handle_requests import *

class proxy(socket):
    def __init__(self, ip, port, backlog = 0): 
        self.bind_ip = ip
        self.bind_port = port

        super().__init__(AF_INET, SOCK_STREAM)
        super().bind((self.bind_ip, self.bind_port))
        super().listen(backlog)

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

        client_socket.close()
