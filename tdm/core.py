"""
This module is the TDM core module, which does select the
session which will run.
"""

import subprocess
import getpass
import os
import sys
import errno
from .control import get_handler
from abc import ABC, abstractmethod
    
class XRunningException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidTtyException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TdmInterface(ABC):
    def __init__(self):
        self._handler = get_handler()
        self._command = self._handler.sessions()[self._handler.default()][0]
        self._is_x = True
        

    def X_running(self):
        X = subprocess.Popen('ps h -eo user,comm', shell=True, stdout=subprocess.PIPE,
                universal_newlines=True)
        stdout, stderr = X.communicate()
        for x in stdout.split('\n'):
            if 'Xorg' in x and getpass.getuser() in x:
                return True
    
        return False
    
    def is_tty(self):
        if 'tty' in os.path.basename(os.ttyname(sys.stdout.fileno())):
            return True
        else:
            return False

    def run(self):
        try:
            subprocess.call(self._handler.scripts()['exit'])
        except KeyError:
            pass

## Set the default session if it has to be saved

        if int(os.getenv('SAVELAST', 1)) == 1:
            linkname = os.path.join(self._handler.confdir, 'default')
            try:
                os.symlink(self._command, linkname)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    os.remove(linkname)
                    os.symlink(self._command, linkname)
                else:
                    raise e

        try:
            command = os.readlink('/tmp/tdmdefault')
            os.remove('/tmp/tdmdefault')
            os.execvp(command, [command])
        except FileNotFoundError:
            try:
                os.execvp(self._handler.default(), [self._handler.default()])
            except FileNotFoundError as e:
                pass

    def select(self):
        if not self.is_tty():
            raise InvalidTtyException('Invalid tty')

        if self.X_running():
            raise XRunningException('X is already running')

        try:
            subprocess.call(self._handler.scripts()['init'])
        except KeyError:
            pass

        self.display()
        os.symlink(self._command, '/tmp/tdmdefault')

    def isX(self):
        return self._is_x

    @abstractmethod
    def display(self):
        pass

class TdmInterfaceText(TdmInterface):
    def display(self):
        s = self._handler.sessions(extra_prefix='extra/')
        print('This is TDM 2.0.0, a tiny display manager')
        print('Please select from the following (default: '+self._handler.default()+')')
        n = 0
        k = []
        sort_key = lambda t: t[0].lower().replace('extra/', '2') if 'extra/' in t[0] else '1'+t[0].lower()
        for key, value in sorted(s.items(), key=sort_key):
            if value[1]:
                k.append(key)
                print(str(n)+' '+key)
                n+=1
        try:
            value = int(input('Program ID: '))
        except (EOFError, ValueError):
            print('No value, using default')
            pass
        else:
            try:
                self._command = s[k[value]][0]
            except IndexError:
                print('Unknown value, using default')
                pass

class TdmInterfaceDialog(TdmInterface):
    def __init__(self):
        import dialog
        TdmInterface.__init__(self)
        self._widget = dialog.Dialog()
        self._widget.set_background_title('TDM 2.0.0')

    def display(self):
        s = self._handler.sessions(extra_prefix='extra/')
        defopt = self._handler.default()
        defopt_id = 0
        n = 0
        k = []
        ch = []
        sort_key = lambda t: t[0].lower().replace('extra/', '2') if 'extra/' in t[0] else '1'+t[0].lower()
        for key, value in sorted(s.items(), key=sort_key):
            if value[1]:
                k.append(key)
                ch.append((str(n), key))
                if defopt == key:
                    defopt_id = n
                n+=1
        title='Please select from the following (default: '+self._handler.default()+')'
        code, value = self._widget.menu(title, choices=ch)
        for i in ch:
            if i[0] == value:
                self._command = s[i[1]][0]
                self._is_x = not s[i[1]][2]

        

def get_interface():
    if os.getenv('TDMUI', 'tdm_dialog') == 'tdm_text':
        return TdmInterfaceText()
    else:
        try:
            return TdmInterfaceDialog()
        except ImportError:
            return TdmInterfaceText()

if __name__ == '__main__':
    ui = get_interface()

    import sys
    
    try:
        if sys.argv[1] == '--xstart':
            ui.run()
        else:
            raise ValueError('The argument was not "--xstart"')
    except IndexError:
        ui.select()

