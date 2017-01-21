from ctypes import CDLL

from lib.snips.shell import launch
from lib.snips.alert import Log

LOG = Log.get(__name__)


def lock_screen(prime):
    res = None
    try:
        res = CDLL('''
/System/Library/PrivateFrameworks/login.framework/Versions/Current/login
        '''.strip()).SACLockScreenImmediate()
    except OSError as ex:
        LOG.error('{} could not load framework: {}', prime, ex)
    except AttributeError as ex:
        LOG.error('{} requested function not available: {}', prime, ex)

    return res == 0


def launch_wrap(command):
    def wrap(prime):
        code, _, err = launch(*command)
        if code == 0:
            return True
        LOG.error('command {} failed: {}', prime, ' '.join(err))
    return wrap


def management_summary(name):
    if name in COMMANDS.keys():
        return launch_wrap(COMMANDS[name])
    elif name == 'lock_screen':
        return lock_screen


COMMANDS = dict(
    log_out=['osascript', '-e', 'tell app "System Events" to log out'],
    re_start=['osascript', '-e', 'tell app "System Events" to restart'],
    save_screen=['open', '-a', 'ScreenSaverEngine.app'],
    shut_down=['osascript', '-e', 'tell app "System Events" to shut down'],
    sleep_now=['pmset', 'sleepnow'],
    sleep_screen=['pmset', 'displaysleepnow'],
)
