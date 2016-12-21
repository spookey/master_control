from contextlib import contextmanager
from ctypes import CDLL
from functools import partial

from lib.snips.alert import Log

LOG = Log.get(__name__)


def lock_screen(cmd_res=False):
    @contextmanager
    def _lock():
        try:
            login = CDLL('''
/System/Library/PrivateFrameworks/login.framework/Versions/Current/login
            '''.strip())
            yield login.SACLockScreenImmediate()
        except OSError as ex:
            LOG.error('could not load framework: {}', ex)
            yield
        except AttributeError as ex:
            LOG.error('requested function not available: {}', ex)
            yield

    with _lock() as res:
        if cmd_res:
            return (res if res is not None else 1), [], []
        return res == 0


def management_summary(func):
    res = dict((
        key, partial(func, val)
    ) for key, val in COMMANDS.items())
    res.update(lock_screen=partial(lock_screen, cmd_res=True))
    return res


COMMANDS = dict(
    log_out=['osascript', '-e', 'tell app "System Events" to log out'],
    re_start=['osascript', '-e', 'tell app "System Events" to restart'],
    save_screen=['open', '-a', 'ScreenSaverEngine.app'],
    shut_down=['osascript', '-e', 'tell app "System Events" to shut down'],
    sleep_now=['pmset', 'sleepnow'],
    sleep_screen=['pmset', 'displaysleepnow'],
)
