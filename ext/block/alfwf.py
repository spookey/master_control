from ext.snaps.nodes import (
    connect_nodes, node_arguments, node_keyword, node_notification,
    node_remote, node_script, workflow_base
)
from ext.snaps.plist import Plist
from lib.parse import PROGNAME, collect_local
from lib.snips.files import base_loc

COMMAND = '''
$@ > /dev/null 2>&1
case $? in
  0) echo "ok";;
  *) echo "failed";;
esac
'''.strip()
INTERPRETER = '/usr/local/bin/python3'


def pull_elems():
    for module, actions in sorted(collect_local().items()):
        for ident, _, _ in actions:
            for state, flag, sign in [('full', '-l', '+'), ('null', '', '-')]:
                yield (
                    'the_{}_{}_{}'.format(state, module, ident),
                    '{} {} {}'.format(module, ident, flag).strip(),
                    '{}{}_{}'.format(sign, module, ident),
                )


def gen_alfwf():
    connections = dict(
        the_script=connect_nodes('the_notification'),
        the_main_arguments=connect_nodes('the_script'),
    )

    objects = [
        node_notification(
            'the_notification', title='{var:cmd}', text='{var:name} {query}'
        ),
        node_script(
            'the_script', script=COMMAND
        ),
        node_arguments(
            'the_main_arguments',
            argument='{interpreter} {command} {text}'.format(
                command=base_loc(PROGNAME),
                interpreter=INTERPRETER,
                text='{var:cmd}',
            ),
            variables=dict(name=PROGNAME),
        ),
    ]

    uidata = dict(
        the_notification=dict(xpos=720, ypos=65),
        the_script=dict(xpos=570, ypos=65),
        the_main_arguments=dict(xpos=500, ypos=95),
    )

    ypos = 10
    for uid, cmd, name in pull_elems():
        args = '{}_arguments'.format(uid)
        objects.append(node_arguments(args, variables=dict(cmd=cmd)))
        uidata[args] = dict(xpos=200, ypos=ypos + 85)
        connections[args] = connect_nodes('the_main_arguments')

        remo = '{}_remote'.format(uid)
        objects.append(node_remote(remo, name=name))
        uidata[remo] = dict(xpos=10, ypos=ypos)
        connections[remo] = connect_nodes(args)

        keyw = '{}_keyword'.format(uid)
        objects.append(node_keyword(keyw, keyword=name))
        uidata[keyw] = dict(xpos=10, ypos=ypos + 115)
        connections[keyw] = connect_nodes(args)

        ypos += 230

    plist = Plist()
    result = workflow_base(PROGNAME, name='Master Control')
    result.update(
        connections=connections,
        objects=objects,
        uidata=uidata,
    )
    return plist(result)
