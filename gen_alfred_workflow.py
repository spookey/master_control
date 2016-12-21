#!/usr/bin/env python3

from datetime import datetime
from os import path
from sys import stderr
from xml.dom import minidom

from lib.parse import collect_local

WORKING = path.expanduser('~/bin')
COMMAND = '''
date
echo "LAUNCH: $*"
$@ 2>&1
echo "RESULT: $?"
'''.strip()
CONFIG_TEMPLATE = dict(
    command=path.join(WORKING, 'shove'),
    interpreter='/usr/local/bin/python3',
    logfile=path.join(WORKING, '_alfred_auto.log'),
)
ALFRED_TEMPLATE = dict(
    bundleid='de.der-beweis.code.master_control.alfred_workflow.autogen.bbq',
    category='Productivity',
    createdby='spky',
    description='autogenerated alfred workflow for master control',
    disabled=False,
    name='Master Control (autogenerated)',
    readme='master_control - alfred_workflow',
    version=datetime.utcnow().strftime('%Y.%m.%d-%H%M'),
    webaddress='www.der-beweis.de',
)


class Plist(object):
    def __init__(self):
        impl = minidom.getDOMImplementation()
        doct = impl.createDocumentType(
            'plist', '-//Apple//DTD PLIST 1.0//EN',
            'http://www.apple.com/DTDs/PropertyList-1.0.dtd'
        )
        self.tree = impl.createDocument(None, 'plist', doct)
        self.tree.documentElement.setAttribute('version', '1.0')

    def _append(self, *nodes, parent):
        parent = parent if parent else self.tree.documentElement
        for node in nodes:
            parent.appendChild(node)

    def gen_node(self, name):
        return self.tree.createElement(name)

    def gen_text(self, name, content):
        node = self.gen_node(name)
        self._append(self.tree.createTextNode(str(content)), parent=node)
        return node

    def _raw_pair(self, key, *nodes, parent):
        if key is None:
            stderr.write(' '.join(['ERROR: empty key:', str(nodes), '\n']))
            stderr.flush()
        self._append(self.gen_text('key', key), *nodes, parent=parent)

    def pair_string(self, key, value, parent):
        node = self.gen_text('string', value)
        self._raw_pair(key, node, parent=parent)

    def pair_integer(self, key, value, parent):
        node = self.gen_text('integer', value)
        self._raw_pair(key, node, parent=parent)

    def pair_bool(self, key, value, parent):
        node = self.gen_node('true' if value else 'false')
        self._raw_pair(key, node, parent=parent)

    def select(self, elem):
        for inst, func in [
                (bool, self.pair_bool),
                (dict, self.pair_dict),
                (int, self.pair_integer),
                (list, self.pair_array),
                (str, self.pair_string),
        ]:
            if isinstance(elem, inst):
                return func
        stderr.write(' '.join([
            'ERROR: uncovered type:', str(type(elem)), str(elem), '\n'
        ]))
        stderr.flush()

    def pair_dict(self, key, values, parent=None):
        node = self.gen_node('dict')
        if key is None:
            self._append(node, parent=parent)
        else:
            self._raw_pair(key, node, parent=parent)
        for elem, content in sorted(values.items()):
            func = self.select(content)
            func(elem, content, parent=node)

    def pair_array(self, key, values, parent):
        node = self.gen_node('array')
        if key is None:
            self._append(node, parent=parent)
        else:
            self._raw_pair(key, node, parent=parent)
        for content in values:
            func = self.select(content)
            func(None, content, parent=node)

    def __call__(self, content):
        self.pair_dict(None, content, parent=None)
        return self.tree.toprettyxml(
            encoding='UTF-8', indent='\t'
        ).decode('UTF-8')


def _raw_object(uid, config, ptype='trigger.remote', version=1):
    return dict(
        config=config, uid=uid, version=version,
        type='alfred.workflow.{}'.format(ptype),
    )


def object_remote(uid, name):
    return _raw_object(
        uid, config=dict(
            argument='', argumenttype=0,
            triggerid=name, triggername=name,
            workflowonly=False
        ),
        ptype='trigger.remote', version=1
    )


def object_logfile(uid, filename):
    return _raw_object(
        uid=uid, config=dict(
            adduuid=False,
            allowemptyfiles=True,
            createintermediatefolders=False,
            filename=filename,
            filetext='{query}',
            relativepathmode=0,
            type=2,
        ), ptype='output.writefile', version=1
    )


def object_script(uid, script):
    return _raw_object(
        uid=uid, config=dict(
            concurrently=False,
            escaping=102,
            script=script,
            scriptargtype=1,
            scriptfile='',
            type=0,
        ), ptype='action.script', version=2
    )


def object_arguments(uid, argument):
    return _raw_object(
        uid=uid, config=dict(
            argument=argument,
            variables=dict(),
        ),
        ptype='utility.argument', version=1
    )


def object_keyword(uid, keyword, subtext):
    return _raw_object(
        uid=uid, config=dict(
            argumenttype=2,
            keyword=keyword,
            subtext=subtext,
            text=keyword.capitalize(),
            whitespace=False,
        ),
        ptype='input.keyword', version=1
    )


def connect(*targets):
    return list(dict(
        destinationuid=target,
        modifiers=0,
        modifiersubtext='',
        vitoclose=False,
    ) for target in targets)


def pull_elems():
    for module, actions in sorted(collect_local().items()):
        for ident, _, _ in actions:
            for state, flag, sign in [('full', '-l', '+'), ('null', '', '-')]:
                yield (
                    'the_{}_{}_{}'.format(state, module, ident),
                    '{} {} {}'.format(module, ident, flag).strip(),
                    '{}{}_{}'.format(sign, module, ident),
                )


def generate():
    objects = [
        object_logfile(
            'the_logfile', filename=CONFIG_TEMPLATE['logfile']
        ),
        object_script(
            'the_script', script=COMMAND
        ),
        object_arguments(
            'the_main_arguments',
            argument='{interpreter} {command} {{query}}'.format(
                command=CONFIG_TEMPLATE['command'],
                interpreter=CONFIG_TEMPLATE['interpreter']
            ),
        ),
    ]
    uidata = dict(
        the_logfile=dict(xpos=720, ypos=65),
        the_script=dict(xpos=570, ypos=65),
        the_main_arguments=dict(xpos=500, ypos=95),
    )
    connections = dict(
        the_script=connect('the_logfile'),
        the_main_arguments=connect('the_script'),
    )

    ypos = 10
    for uid, argument, name in pull_elems():
        args = '{}_arguments'.format(uid)
        objects.append(object_arguments(args, argument=argument))
        uidata[args] = dict(xpos=200, ypos=ypos + 85)
        connections[args] = connect('the_main_arguments')

        remo = '{}_remote'.format(uid)
        objects.append(object_remote(remo, name))
        uidata[remo] = dict(xpos=10, ypos=ypos)
        connections[remo] = connect(args)

        keyw = '{}_keyword'.format(uid)
        objects.append(object_keyword(keyw, keyword=name, subtext=''))
        uidata[keyw] = dict(xpos=10, ypos=ypos + 115)
        connections[keyw] = connect(args)

        ypos += 230

    return connections, objects, uidata


def main():
    plist = Plist()
    connections, objects, uidata = generate()
    output = ALFRED_TEMPLATE
    output.update(
        connections=connections,
        objects=objects,
        uidata=uidata,
    )
    return plist(output)


if __name__ == '__main__':
    print(main())
