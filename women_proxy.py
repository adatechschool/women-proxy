#!/usr/bin/env python

import handle_basic_signals
from proxy import *

server = proxy('0.0.0.0', 9999)

while True:
    server.wait_and_thread()
