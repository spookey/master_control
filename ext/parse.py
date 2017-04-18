from argparse import ArgumentParser

from ext.block.alfwf import gen_alfwf
from ext.block.volwf import gen_volwf
from ext.block.zcomp import gen_zcomp
from lib.local import POWER
from lib.parse import logging_arguments, logging_setup

BUILDERS = dict(
    alfwf=gen_alfwf,
    volwf=gen_volwf,
    zcomp=gen_zcomp,
)


def inst_arguments():
    arg_prs = ArgumentParser(
        add_help=True, allow_abbrev=True, prog='master generate',
    )
    arg_prs.add_argument(
        'what', action='store', choices=sorted(BUILDERS.keys()),
        help='what to generate'
    )
    arg_prs.add_argument(
        'location', action='store',
        help='target file'
    )
    logging_arguments(arg_prs, name='install')
    args = arg_prs.parse_args()
    logging_setup(args)
    return BUILDERS, args


def color_arguments():
    def _color(val):
        if val.lower().startswith('0x'):
            return int(val, 16)
        return int(val)

    arg_prs = ArgumentParser(
        add_help=True, allow_abbrev=True, prog='master color',
    )
    arg_prs.add_argument(
        'points', action='store', type=int,
        help='number of hi points per day',
    )
    arg_prs.add_argument(
        '--hi', action='store', type=_color, default=0xffffff,
        help='highest color value (default: \'0xffffff\')'
    )
    arg_prs.add_argument(
        '--lo', action='store', type=_color, default=0x000000,
        help='lowest color value (default: \'0x000000\')'
    )
    arg_prs.add_argument(
        '--dump', '-d', action='store_true',
        help='do not send anything, only dump color (default: \'%(default)s\')'
    )

    logging_arguments(arg_prs, name='color')
    args = arg_prs.parse_args()
    logging_setup(args)
    if not args.points >= 1:
        arg_prs.error('points must be >= 1')
    if args.lo >= args.hi:
        arg_prs.error('hi must be > lo')
    return POWER['hostname'], args
