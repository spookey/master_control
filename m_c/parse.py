from argparse import ArgumentParser

from m_c import local


def local_actions():
    def _pull(inst):
        return [lc for lc in vars(local).values() if isinstance(lc, inst)]

    return dict((
        str(pkg.__name__).lower(), dict((
            str(mod.ident).lower(), mod
        ) for mod in _pull(pkg))
    ) for pkg in _pull(type))


def arguments(actions):
    def _glob(pars):
        return [pars.add_argument(
            '-{name}'.format(name=name[0]),
            '--{name}'.format(name=name),
            action='store_true',
            help='{text} (default: \'%(default)s\')'.format(text=text)
        ) for name, text in [
            ('lift', 'launch direction to run [raise up/put down]'),
            ('slow', 'walk through all dependencies [unoptimized]'),
            ('dump', 'do not launch anything, just print the path'),
        ]]

    arg_prs = ArgumentParser(
        add_help=True, allow_abbrev=True, prog='master control',
    )
    sub_prs = arg_prs.add_subparsers(dest='pkg')
    sub_prs.type = str.lower
    sub_prs.required = True

    for pkg, mods in sorted(actions.items()):
        choices = sorted(mods.keys())
        pkg_prs = sub_prs.add_parser(
            pkg, help='{{{}}}'.format(','.join(sorted(mods.keys())))
        )
        pkg_prs.add_argument(
            'mod', action='store', choices=choices,
            help='{} package actions'.format(pkg), type=str.lower,
        )
        _glob(pkg_prs)

    return arg_prs.parse_args()
