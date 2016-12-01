from m_c.brick.basic import Basic
from m_c.snips.shell import launch


class Audio(Basic):
    def full(self):
        _, out, err = launch(
            'osascript', '-e',
            SCRIPT_DIALUP.format(device=self.conf['prime'])
        )
        if err:
            self.message('bluetooth dialup error', err, out, lvl='error')
        launch('osascript', '-e', SCRIPT_ESCAPE)
        return ''.join(out) == 'connected'

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
