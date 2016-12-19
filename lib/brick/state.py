from ctypes import CDLL

from lib.brick.basic import Basic
from lib.snips.shell import launch


class State(Basic):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = COMMANDS.get(command)

    def full(self):
        return True

    def lock_scr(self):
        try:
            login = CDLL(LOGINPTH)
            return login.SACLockScreenImmediate() == 0
        except OSError as ex:
            self.message('could not load framework', ex, lvl='error')
        except AttributeError as ex:
            self.message('function not available', ex, lvl='error')
        return False

    def null(self):
        if not self.command:
            self.message('command not found in preset', lvl='fatal')
            return False

        if self.command == 'lock_scr':
            return self.lock_scr()

        code, out, err = launch(*self.command)
        if out or err:
            self.message(
                'something happened', code, err, out,
                lvl='error' if code else 'alert'
            )
        return not code

LOGINPTH = (
    '/System/Library/PrivateFrameworks/login.framework/Versions/Current/login'
)
COMMANDS = dict(
    shutdown=['osascript', '-e', 'tell app "System Events" to shut down'],
    re_start=['osascript', '-e', 'tell app "System Events" to restart'],
    sign_off=['osascript', '-e', 'tell app "System Events" to log out'],
    lock_scr='lock_scr',
    sleepnow=['pmset', 'sleepnow'],
    sleepdsp=['pmset', 'displaysleepnow'],
    scrsaver=['open', '-a', 'ScreenSaverEngine.app'],
)
