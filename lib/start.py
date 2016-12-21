from lib.parse import main_arguments
from lib.snips.alert import Log

LOG = Log.get(__name__)


def run():
    inst, args = main_arguments()
    for instance in [
            insta for ident, prime, insta in inst.get(args.module)
            if any(args.action == act for act in [ident, prime])
    ]:
        LOG.debug('found {} for {}', instance, args.action)
        return instance.fire(lift=args.lift, slow=args.slow, dump=args.dump)
    LOG.critical('{} not found in {} module', args.action, args.module)
    return False
