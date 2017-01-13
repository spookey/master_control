from ext.block.color import chroma
from ext.parse import color_arguments, inst_arguments
from ext.snaps.write import write_file
from lib.snips.alert import Log

LOG = Log.get(__name__)


def i_run():
    gens, args = inst_arguments()
    func = gens.get(args.what)
    if func:
        LOG.debug('found {} for {}', func.__name__, args.what)
        return write_file(args.location, func())
    LOG.critical('{} not found', args.what)
    return False


def c_run():
    return chroma(*color_arguments())
