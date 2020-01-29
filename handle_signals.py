#!/usr/bin/env python

import signal
import sys

def quit_on_ctrl_c(sig, frame):
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, quit_on_ctrl_c)
