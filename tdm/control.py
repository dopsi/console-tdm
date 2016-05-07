"""
This module is the TDM control module, which does perform the
operations that were part of tdmctl(1).
"""

from abc import ABC, abstractmethod
from pathlib import Path
import os
import shutil

def make_ternary(true=True, false=False):
    """
    This function works a a ternary builder.

    It takes two arguments and build a lambda function, 
    taking one argument, which will return one of the arguments
    depending on the logical value of the argument provided to
    the lambda function.
    """
    return lambda x: true if x else false

class TdmHandler(ABC):
    def __init__(self):
        """
        Create a new TDM handler
        """
        self._sessions = {}
        self._cache = {}

    def __del__(self):
        pass

    @abstractmethod
    def sessions(self, x=True, extra=True, pprint=False):
        """
        List available sessions.

        The returned dictionnary has the following form :
        d = { session: (command, executable, extra) }
        where session and command are strings and executable and
        extra are boolean values.

        If x or extra are set to False, the sessions in the relevant 
        category are not taken in account.

        If pprint is True, the sessions are pretty printed.
        """
        pass

    @abstractmethod
    def cache(self, name=None, pprint=False):
        """
        List cached sessions.

        The returned dictionnary has the following form :
        d = { session: (command, executable) }
        where session and command are strings and executable
        are boolean values.

        If pprint is True, the sessions are pretty printed.
        """
        pass

    @abstractmethod
    def add(self, name, command, category='X', pprint=False, dryrun=False):
        """
        Add a new session.

        name should be the name of the session.
        command should be a filename to the executable file of the session.
        category either 'X' or 'extra'

        If pprint is True, the result of the operation will be printed out.

        If dryrun is True, no actual operation will be performed.
        """
        pass

    @abstractmethod
    def delete(self, name, pprint=False, dryrun=False):
        """
        Delete a session.

        name should be the name of the session.

        If pprint is True, the result of the operation will be printed out.

        If dryrun is True, no actual operation will be performed.
        """
        pass

    @abstractmethod
    def enable(self, name, pprint=False, dryrun=False):
        """
        Move a session from cache to the active sessions.

        name should be the name of the session.

        If pprint is True, the result of the operation will be printed out.

        If dryrun is True, no actual operation will be performed.
        """
        pass

    @abstractmethod
    def disable(self, name, pprint=False, dryrun=False):
        """
        Move a session from the active ones to the cache.

        name should be the name of the session.

        If pprint is True, the result of the operation will be printed out.

        If dryrun is True, no actual operation will be performed.
        """
        pass

    @abstractmethod
    def init(self):
        """
        Create the initial configuration.

        If force is True, any existing configuration will be overwritten.
        """
        pass

    @abstractmethod
    def verify(self, pprint=False):
        """
        Return True if the configuration is valid.
        
        If pprint is True, the result of the operation will be printed out.
        """
        pass

    @abstractmethod
    def default(self, name=None, pprint=False):
        """
        Check or set the default session.

        If name is None the default is shown otherwise it is
        set.
        
        If pprint is True, the result of the operation will be printed out.
        """
        pass

class TdmHandlerV1(TdmHandler):
    """
    This is a TdmHandler implementation to support a version 1 installation (i.e. in 
    the $HOME/.tdm directory).

    For a more in-depth documentation, see the TdmHandler class in the same module.
    """
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
        if category == 'X' or category == 'x':
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

    def default(self, name=None, pprint=False):
        if name:
            # Set the default
            value = name
        else:
            value = os.path.basename(os.readlink(os.path.join(self.confdir, 'default')))
            if pprint:
                print(value)

        return value

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
                rl.append(TdmHandler.__subclasses__()[i]())
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
