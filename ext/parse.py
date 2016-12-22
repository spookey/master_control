from argparse import ArgumentParser
from lib.parse import logging_arguments, logging_setup

from ext.block.zcomp import gen_zcomp
from ext.block.alfwf import gen_alfwf

BUILDERS = dict(
    zcomp=gen_zcomp,
    alfwf=gen_alfwf,
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
