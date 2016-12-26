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
