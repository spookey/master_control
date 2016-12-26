from ext.snaps.nodes import (
    connect_nodes, node_applescript, node_filter, node_notification,
    node_remote, workflow_base
)
from ext.snaps.plist import Plist
from lib.parse import PROGNAME


def triggers():
    for state, sign in [('less', '-'), ('more', '+'), ('mute', '=')]:
        yield (
            'the_{}'.format(state),
            state,
            '{}{}_volume'.format(sign, state),
        )


def gen_volwf():
    connections = dict(
        the_filter=connect_nodes('the_notification'),
        the_script=connect_nodes('the_filter')
    )
    objects = [
        node_notification('the_notification'),
        node_filter('the_filter', matchstring='[0-9]?[0,5]%'),
        node_applescript('the_script', script=COMMAND, cachescript=True),
    ]
    uidata = dict(
        the_notification=dict(xpos=470, ypos=125),
        the_filter=dict(xpos=400, ypos=155),
        the_script=dict(xpos=250, ypos=125),
    )

    ypos = 10
    for uid, arg, name in triggers():
        objects.append(
            node_remote(uid, name=name, argument=arg, argumenttype=3)
        )
        uidata[uid] = dict(xpos=10, ypos=ypos)
        connections[uid] = connect_nodes('the_script')

        ypos += 115

    plist = Plist()
    result = workflow_base(PROGNAME, name='Volume Control')
    result.update(
        connections=connections,
        objects=objects,
        uidata=uidata,
    )
    return plist(result)


COMMAND = '''
on alfred_script(action)
    if action is "mute" then
        set now_muted to (output muted of (get volume settings))
        set volume output muted (not now_muted)
        return
    else
        set now_volume to (output volume of (get volume settings))

        if (action is "more") and (now_volume < 100) then
            set now_volume to (now_volume + 1)
        else if (action is "less") and (now_volume > 0) then
            set now_volume to (now_volume - 1)
        end if

        set volume output volume now_volume
        return "" & now_volume & "%"
    end if
end alfred_script
'''.strip()
