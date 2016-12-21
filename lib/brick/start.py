from lib.brick.basic import Basic
from lib.snips.shell import launch


class Start(Basic):
    def __init__(self, *args, script=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.script = script

    def full(self):
        if self.script:
            _, out, err = launch(
                'osascript', '-e',
                SCRIPT_LAUNCH.format(script=self.prime)
            )
            self.message('open script in new window', err, out, lvl='alert')
            return True

        code, _, _ = launch('open', '-a', self.prime)
        return not code

    def null(self):
        flag = '-if' if self.script else '-ix'
        code, _, _ = launch('pgrep', flag, self.prime)
        if code:
            return True
        code, _, _ = launch('pkill', flag, self.prime)
        return not code

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
