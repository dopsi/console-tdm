#! /usr/bin/env python3

from tdm.core import get_interface
from os import execlp
ui = get_interface()

import sys

try:
    if sys.argv[1] == '--xstart':
        ui.run()
    else:
        raise ValueError('The argument was not "--xstart"')
except IndexError:
    ui.select()
    command = 'startx'
    execlp(command)
