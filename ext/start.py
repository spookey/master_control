from lib.snips.alert import Log
from ext.snaps.write import write_file
from ext.parse import inst_arguments

LOG = Log.get(__name__)


def run():
    gens, args = inst_arguments()
    func = gens.get(args.what)
    if func:
        LOG.debug('found {} for {}', func.__name__, args.what)
        return write_file(args.location, func())
    LOG.critical('{} not found', args.what)
    return False