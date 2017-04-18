from lib.brick.basic import Basic
from lib.snips.shell import launch, launch_repeat


class Audio(Basic):
    def __init__(self, *args, delay=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = delay

    def do_fire(self, lift=True):
        for _, (_, out, err) in launch_repeat(
                'osascript', '-e', SCRIPT_ACTION.format(
                    device=self.prime,
                    desired=('Connect' if lift else 'Disconnect'),
                    already=('Disconnect' if lift else 'Connect'),
                ), times=2, patience=self.delay,
        ):
            launch('osascript', '-e', SCRIPT_ESCAPE)
            if err:
                self.log.debug('bluetooth says: {}', ' '.join(err))
            if ''.join(out) == 'success':
                return True
        return False

    def full(self):
        return self.do_fire(True)

    def null(self):
        return self.do_fire(False)


SCRIPT_ACTION = '''
tell application "System Events" to tell process "SystemUIServer"
    tell first menu bar
        tell (first menu bar item whose description is "bluetooth")
            click
            tell first menu
                tell (first menu item whose title is "{device}")
                    click
                    tell first menu
                        if exists (menu item "{desired}") then
                            click menu item "{desired}"
                            return "success"
                        else if exists (menu item "{already}") then
                            log "already there"
                            return "success"
                        end if
                    end tell
                end tell
            end tell
        end tell
    end tell
end tell
log "some weird error"
return "script failed"
'''

SCRIPT_ESCAPE = '''
tell application "System Events"
    key code 53
end tell
'''
