from m_c.brick.basic import Basic
from m_c.snips.shell import launch


class Start(Basic):
    def full(self):
        if self.conf.get('script'):
            _, out, err = launch(
                'osascript', '-e',
                SCRIPT_LAUNCH.format(script=self.conf['prime'])
            )
            self.message('start script in new window', err, out, lvl='alert')
            return True

        code, _, _ = launch('open', '-a', self.conf['prime'])
        return code == 0

    def null(self):
        flag = '-if' if self.conf.get('script') else '-ix'
        code, _, _ = launch('pgrep', flag, self.conf['prime'])
        if code:
            return True
        code, _, _ = launch('pkill', flag, self.conf['prime'])
        return code == 0


SCRIPT_LAUNCH = '''
tell application "/Applications/iTerm.app"
    activate
    tell application "System Events" to keystroke "t" using command down
    select first window
    tell first window
        tell current session to write text "{script} && exit"
    end tell
end tell
'''