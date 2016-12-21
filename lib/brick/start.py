from lib.brick.basic import Basic
from lib.snips.shell import launch


class Start(Basic):
    def __init__(self, *args, script=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.script = script

    def full(self):
        if self.script:
            self.log.info('opening script in new window...')
            launch('osascript', '-e', SCRIPT_LAUNCH.format(script=self.prime))
            return True

        code, _, err = launch('open', '-a', self.prime)
        if code == 0:
            return True
        self.log.error('could not start: {}', ' '.join(err))
        return False

    def null(self):
        flag = '-if' if self.script else '-ix'
        code, _, _ = launch('pgrep', flag, self.prime)
        if code != 0:
            self.log.debug('{} is not running', self.prime)
            return True
        code, _, _ = launch('pkill', flag, self.prime)
        if code == 0:
            return True
        self.log.error('{} could not be killed', self.prime)
        return False

SCRIPT_LAUNCH = '''
tell application "iTerm"
    activate
    create window with default profile
    tell the first window
        select
        tell current session to write text "{script} && exit"
    end tell
end tell
'''
