from argparse import ArgumentParser

from lib import local
from lib.snips.alert import LEVELS, ROOT_LOGGER, make_bucket, make_stream
from lib.snips.files import base_loc, sure_loc

STREAM = make_stream(LEVELS[-1])
ROOT_LOGGER.addHandler(STREAM)

PROGNAME = 'shove'
FLAGS = dict(
    lift='launch direction to run [raise up/put down]',
    slow='walk through all dependencies [unoptimized]',
    dump='do not launch anything, just print the path',
)


def collect_local():
    def _pull(inst):
        return [lc for lc in vars(local).values() if isinstance(lc, inst)]

    return dict((
        str(module.__name__).lower(), list((
            str(action.ident).lower(), str(action.prime).lower(), action
        ) for action in _pull(module))
    ) for module in _pull(type))


def logging_setup(args):
    STREAM.setLevel(LEVELS[len(LEVELS) - args.log_level - 1])
    ROOT_LOGGER.addHandler(make_bucket(LEVELS[0], sure_loc(args.log_file)))


def logging_arguments(prs):
    prs.add_argument(
        '-v', action='count', dest='log_level', default=0,
        help='increase verbosity'
    )
    prs.add_argument(
        '--log', action='store', dest='log_file',
        default=base_loc('log', 'debug.log'),
        help='log file location (default: \'%(default)s\')'
    )


def main_arguments():
    instances = collect_local()

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
            'action', action='store', type=str.lower,
            choices=sorted(set(fl for at in (
                (idt, prm) for idt, prm, _ in actions
            ) for fl in at)),
            help='{} module actions'.format(module),
        )
        for flag, text in FLAGS.items():
            act_prs.add_argument(
                '-{f}'.format(f=flag[0]), '--{flag}'.format(flag=flag),
                action='store_true',
                help='{text} (default: \'%(default)s\')'.format(text=text)
            )
        logging_arguments(act_prs)

    args = arg_prs.parse_args()
    logging_setup(args)
    return instances, args
