"""
This module is the TDM control module, which does select the
session which will run.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import os
import shutil

def make_ternary(true=True, false=False):
    return lambda x: true if x else false

class TdmHandler(ABC):
    def __init__(self):
        """
        Created a new TDM handler
        """
        self._sessions = {}
        self._cache = {}

    def __del__(self):
        pass

    @abstractmethod
    def sessions(self, x=True, extra=True, pprint=False):
        """
        List sessions
        """
        pass

    @abstractmethod
    def cache(self, name=None, pprint=False):
        pass

    @abstractmethod
    def add(self, name, command, category='X', pprint=False, dryrun=False):
        pass

    @abstractmethod
    def delete(self, name, pprint=False, dryrun=False):
        pass

    @abstractmethod
    def enable(self, name, pprint=False, dryrun=False):
        pass

    @abstractmethod
    def disable(self, name, pprint=False, dryrun=False):
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def verify(self, pprint=False):
        pass

    def check(self, name, pprint=False):
        try:
            self._sessions[name]
        except IndexError:
            print('IndexError')

class TdmHandlerV1(TdmHandler):
    def __init__(self):
        """
        Create a version 1 TdmHandler.
        """
        self.confdir = os.path.join(os.getenv('HOME'), '.tdm')
        self._prefix = '/usr'
        self._executable_ternary = make_ternary(true='', false='(Not executable)')
        self._extra_ternary = make_ternary(true='extra/', false='')

    def sessions(self, x=True, extra=True, pprint=False):
        """
        List sessions
        """
        s = {}
        
        if x:
            p = Path(os.path.join(self.confdir, 'sessions'))
            for l in p.iterdir():
                s[os.path.basename(str(l))] = (os.readlink(str(l)), os.access(str(l), os.X_OK), False)
        
        if extra:
            p = Path(os.path.join(self.confdir, 'extra'))
            for l in p.iterdir():
                s[os.path.basename(str(l))] = (os.readlink(str(l)), os.access(str(l), os.X_OK), True)

        if pprint:
            for key, value in s.items():
                print(self._extra_ternary(value[2])+key+': '+value[0]+' '+self._executable_ternary(value[1]))
            
        return s

    def cache(self, name=None, pprint=False):
        s = {}
        
        p = Path(os.path.join(self.confdir, 'cache'))
        for l in p.iterdir():
            s[os.path.basename(str(l))] = (os.readlink(str(l)), os.access(str(l), os.X_OK))

        if pprint:
            for key, value in s:
                print(key+': '+value[0]+' '+self._executable_ternary(value[1]))
        
        return s

    def add(self, name, command, category='X', pprint=False, dryrun=False):
        if category == 'X':
            if pprint:
                print('"'+os.path.join(self.confdir, 'sessions', name)+
                        '" -> "'+command+'"')
            if not dryrun:
                os.symlink(command, os.path.join(self.confdir, 'sessions', name))

        elif category == 'extra':
            if pprint:
                print('"'+os.path.join(self.confdir, 'extra', name)+
                        '" -> "'+command+'"')
            if not dryrun:
                os.symlink(command, os.path.join(self.confdir, 'extra', name))
        else:
            raise ValueError('Category '+category+' does not exist')

    def delete(self, name, pprint=False, dryrun=False):
        if os.path.join(self.confdir, 'sessions', name):
            if pprint:
                print('Delete "'+os.path.join(self.confdir, 'sessions', name)+'"')
            if not dryrun:
                os.remove(os.path.join(self.confdir, 'sessions', name))

        elif os.path.join(self.confdir, 'sessions', name):
            if pprint:
                print('Delete "'+os.path.join(self.confdir, 'sessions', name)+'"')
            if not dryrun:
                os.remove(os.path.join(self.confdir, 'sessions', name))

        else:
            raise FileNotFoundError(name+' is not a valid session')

    def enable(self, name, pprint=False, dryrun=False):
        if os.path.exists(os.path.join(self.confdir, 'cache', 'X'+name)):
            if pprint:
                print('"'+os.path.join(self.confdir, 'cache', 'X'+name)+
                        '" -> "'+os.path.join(self.confdir, 'sessions', name)+'"')

            if not dryrun:
                shutil.move(os.path.join(self.confdir, 'cache', 'X'+name),
                        os.path.join(self.confdir, 'sessions', name))

            return True
        if os.path.exists(os.path.join(self.confdir, 'cache', 'E'+name)):
            if pprint:
                print('"'+os.path.join(self.confdir, 'cache', 'E'+name)+
                        '" -> "'+os.path.join(self.confdir, 'extra', name)+'"')

            if not dryrun:
                shutil.move(os.path.join(self.confdir, 'cache', 'E'+name),
                        os.path.join(self.confdir, 'extra', name))

            return True
        
        return False

    def disable(self, name, pprint=False, dryrun=False):
        if os.path.exists(os.path.join(self.confdir, 'sessions', name)):
            if pprint:
                print('"'+os.path.join(self.confdir, 'sessions', name)+
                        '" -> "'+os.path.join(self.confdir, 'cache', 'X'+name)+'"')

            if not dryrun:
                shutil.move(os.path.join(self.confdir, 'sessions', name),
                        os.path.join(self.confdir, 'cache', 'X'+name))

            return True
        elif os.path.exists(os.path.join(self.confdir, 'extra', name)):
            if pprint:
                print('"'+os.path.join(self.confdir, 'extra', name)+
                        '" -> "'+os.path.join(self.confdir, 'cache', 'E'+name)+'"')

            if not dryrun:
                shutil.move(os.path.join(self.confdir, 'extra', name),
                        os.path.join(self.confdir, 'cache', 'E'+name))

            return True
        
        return False

    def init(self, force=False):
        if force and os.path.exists(self.confdir):
            shutil.rmtree(self.confdir)

        if not os.path.exists(self.confdir):
            shutil.copytree(os.path.join(self._prefix,'share/tdm'), self.confdir)
        

    def verify(self, pprint=False):
        if not os.path.isdir(self.confdir):
            return False

        if not os.path.isdir(os.path.join(self.confdir, 'sessions')):
            return False

        if not os.path.isdir(os.path.join(self.confdir, 'extra')):
            return False

        return True

class TdmHandlerV2(TdmHandler):
    def __init__(self):
        """
        Create a version 1 TdmHandler.
        """
        pass

def get(priority=None):
    """
    Get the Tdm Handle for the current installation
    """
    rl = []

    if priority:
        for i in priority:
            try:
                rl.append(TdmHandler.__subclasses__[i]())
            except TypeError:
                rl.append(None)
    else:
        for i in TdmHandler.__subclasses__():
            try:
                rl.append(i())
            except TypeError:
                rl.append(None)

    for h in rl:
        if h and h.verify():
            return h

    return None

if __name__ == '__main__':
    h = get()
    h.sessions(pprint=True)
