#!/usr/bin/env python3

from lib.parse import local_collect, FLAGS

TEMPLATE_ACTIONS = '''
        ({module})
          actions=({actions_listing})
        ;;
'''.rstrip()
TEMPLATE_PRIMARY = '''
#compdef {progname}

_{progname}() {{
  typeset -A opt_args

  _arguments -C \\
    '1:module:->modules' \\
    '2:action:->actions' \\
    '*:flags:->flags'

  case $state in
    (modules)
      local modules
      modules=({modules_listing})
      _describe -t modules 'module' modules
    ;;
    (actions)
      local actions
      case $line[1] in {actions_blocks}
      esac
      _describe -t actions 'action' actions
    ;;
    (flags)
      local flags
      flags=({flags_listing})
      _describe -t flags 'flag' flags
    ;;
  esac

}}

_{progname} "$@"
'''.strip()


def _listing(*data):
    return '\'{lst}\''.format(lst='\' \''.join(sorted(data)))


def main(progname='shove'):
    def _flags_list():
        for flag in FLAGS.keys():
            yield '-{}'.format(flag[0])
            yield '--{}'.format(flag)

    def _actions_list(actions):
        for ident, prime, _ in actions:
            yield ident
            if prime and prime != ident:
                yield prime

    modules_list = []
    actions_case = []

    for module, actions in sorted(local_collect().items()):
        modules_list.append(module)
        actions_case.append(TEMPLATE_ACTIONS.format(
            actions_listing=_listing(*_actions_list(actions)),
            module=module
        ))

    return TEMPLATE_PRIMARY.format(
        progname=progname,
        actions_blocks='\n'.join(actions_case),
        modules_listing=_listing(*modules_list),
        flags_listing=_listing(*_flags_list()),
    )

if __name__ == '__main__':
    print(main())
