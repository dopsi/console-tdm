#! /usr/bin/env python3

from tdm.core import get_interface, XRunningException
from os import execlp,readlink
import sys
ui = get_interface()

import sys

try:
    if sys.argv[1] == '--xstart':
        ui.run()
    else:
        raise ValueError('The argument was not "--xstart"')
except IndexError:
    try:
        ui.select()
    except XRunningException:
        print("tdm: error: X is already running")
        sys.exit(0)
    if ui.isX():
        command = 'startx'
    else:
        command = readlink('/tmp/tdmdefault')
    execlp(command, command)
