from argparse import ArgumentParser

from lib import local

PROGNAME = 'shove'
FLAGS = dict(
    lift='launch direction to run [raise up/put down]',
    slow='walk through all dependencies [unoptimized]',
    dump='do not launch anything, just print the path',
)


def local_collect():
    def _pull(inst):
        return [lc for lc in vars(local).values() if isinstance(lc, inst)]

    return dict((
        str(module.__name__).lower(), list((
            str(action.ident).lower(), str(action.prime).lower(), action
        ) for action in _pull(module))
    ) for module in _pull(type))


def arguments(instances):
    arg_prs = ArgumentParser(
        add_help=True, allow_abbrev=True, prog='master control',
    )
    mod_prs = arg_prs.add_subparsers(dest='module')
    mod_prs.type = str.lower
    mod_prs.required = True

    for module, actions in sorted(instances.items()):
        act_prs = mod_prs.add_parser(
            module, help='{{{}}}'.format(','.join(sorted(
                idt for idt, _, _ in actions
            )))
        )
        act_prs.add_argument(
            'action', action='store', choices=[fl for at in [
                [idt, prm] for idt, prm, _ in actions
            ] for fl in at],
            help='{} module actions'.format(module), type=str.lower,
        )
        for flag, text in FLAGS.items():
            act_prs.add_argument(
                '-{f}'.format(f=flag[0]), '--{flag}'.format(flag=flag),
                action='store_true',
                help='{text} (default: \'%(default)s\')'.format(text=text)
            )

    return arg_prs.parse_args()
