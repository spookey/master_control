from os import makedirs, path

from lib.snips.alert import Log

LOG = Log.get(__name__)


def join_loc(*parts):
    return path.abspath(path.join(*(path.expanduser(p) for p in parts)))


def base_loc(*parts):
    return join_loc(path.dirname(path.dirname(path.dirname(__file__))), *parts)


def check_loc(location, folder=False):
    func = path.isdir if folder else path.isfile
    return path.exists(location) and func(location)


def make_dir(location):
    location = join_loc(location)
    if not check_loc(location, folder=True):
        LOG.info('creating directory {}', location)
        makedirs(location)
    return location


def sure_loc(location):
    location = join_loc(location)
    make_dir(path.dirname(location))
    return location
