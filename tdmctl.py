#! /usr/bin/env python3.5

import tdm.control
import sys

def usage(handler=None, message=None, epilog=None):
    if message:
        print(message, '\n')
    _usage="""tdmctl init: initialize the config directory.
tdmctl list: list available sessions  (X and extra).
tdmctl cache: list cached files.
tdmctl check <session>: see what <session> is.
tdmctl default [session]: show/set default X session.
tdmctl add <name> <path> [X(default)/extra]: add a session.
tdmctl remove <name>
tdmctl enable/disable <session>: enable/disable session.
tdmctl usage/help: display this message."""
    print(_usage)
    if epilog:
        print('\n',epilog)

def add(handler, name, command, category='X'):
    handler.add(name, command, category, pprint=True)

def remove(handler, name):
    handler.remove(name, pprint=True)

def enable(handler, name):
    handler.enable(name, pprint=True)

def disable(handler, name):
    handler.disable(name, pprint=True)

def init(handler):
    handler = tdm.control.get_handler(init=True)
    handler.init(pprint=True)

def check(handler, name):
    s = handler.sessions()
    if name in s:
        print(s[name][0])

def default(handler, name=None):
    handler.default(name, pprint=True)

def lst(handler):
    handler.sessions(pprint=True)

def cache(handler):
    handler.cache(pprint=True)

def select(value):
    return {
            'init': init,
            'list': lst,
            'cache': cache,
            'check': check,
            'default': default,
            'add': add,
            'remove': remove,
            'enable': enable,
            'disable': disable,
            'usage': usage,
            'help': usage,
            }[value]

if __name__ == '__main__':
    handler = tdm.control.get_handler()
    try:
        f = select(sys.argv[1])
    except KeyError as e:
        usage(message='Unknown command '+str(e))
    except IndexError as e:
        usage(message='Missing command')
    else:
        try:
            f(handler, *sys.argv[2:])
        except TypeError as e:
            usage(message=str(e))
        except AttributeError:
            usage(message='TDM does not seem to have been initialized. Please run tdmctl init.')
