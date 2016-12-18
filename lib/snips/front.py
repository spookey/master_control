from pprint import pformat
from sys import stderr, stdout
from textwrap import indent


def message(msg, *txt, pkg=None, lvl=None):
    pkg = str(pkg if pkg else 'prime').lower()
    lvl = str(lvl if lvl else 'alert').upper()
    out = dict(FATAL=stderr, ERROR=stderr).get(lvl, stdout)
    out.write('# {pkg:<8} {lvl:<8} {msg}\n'.format(
        lvl=lvl, msg=msg, pkg=pkg
    ))
    for elem in txt:
        out.write('{txt}\n'.format(
            txt=indent(pformat(elem), ' ' * 2)
        ))
    out.flush()
