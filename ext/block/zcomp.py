from lib.parse import FLAGS, PROGNAME, collect_local


def gen_zcomp():
    def _sh_list(data):
        return '\'{lst}\''.format(lst='\' \''.join(sorted(data)))

    def _actions(actions):
        return _sh_list(set(fl for at in (
            (idt, prm) for idt, prm, _ in actions
        ) for fl in at))

    def _flags():
        return _sh_list(fl for at in ((
            '-{}'.format(flag[0]), '--{}'.format(flag)
        ) for flag in FLAGS.keys()) for fl in at)

    actions_case = list()
    modules_list = list()

    for module, actions in sorted(collect_local().items()):
        actions_case.append(TEMPLATE_ACTIONS.format(
            actions_listing=_actions(actions),
            module=module
        ))
        modules_list.append(module)

    return TEMPLATE_PRIMARY.format(
        progname=PROGNAME,
        actions_blocks='\n'.join(actions_case),
        modules_listing=_sh_list(modules_list),
        flags_listing=_flags(),
    )


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
