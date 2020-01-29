#!/usr/bin/env python

import requests
from requests.exceptions import HTTPError
from handle_requests import *

def handle_client_connection(client_socket):
    raw_request = client_socket.recv(1024)
    request = HTTPRequest(raw_request)
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
