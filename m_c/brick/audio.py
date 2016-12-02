from m_c.brick.basic import Basic
from m_c.snips.shell import launch_repeat, launch


class Audio(Basic):
    def __init__(self, *args, delay=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay = delay

    def full(self):
        for step, (_, out, err) in launch_repeat(
                'osascript', '-e',
                SCRIPT_DIALUP.format(device=self.prime),
                times=2, patience=self.delay,
        ):
            launch('osascript', '-e', SCRIPT_ESCAPE)
            if ''.join(out) == 'connected':
                return True
            self.message(
                'bluetooth dialup try #{:02}'.format(step),
                err, out, lvl='error'
            )
        return False

    def null(self):
        return True

SCRIPT_DIALUP = '''
tell application "System Events" to tell process "SystemUIServer"
    tell first menu bar
        tell (first menu bar item whose description is "bluetooth")
            click
            tell first menu
                tell (first menu item whose title is "{device}")
                    click
                    tell first menu
                        if exists (menu item "Connect") then
                            click menu item "Connect"
                            return "connected"
                        else if exists (menu item "Disconnect") then
                            log "already connected"
                            return "connected"
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
