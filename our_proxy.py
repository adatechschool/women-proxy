#!/usr/bin/env python

import threading

import handle_basic_signals
from proxy import *

server = proxy('0.0.0.0', 9999)

while True:
    client_sock, address = server.accept()
    print (f'Accepted connection from {address[0]}:{address[1]}')
    client_handler = threading.Thread(
        target=proxy.handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()
