from lib.snips.alert import Log
from lib.snips.files import sure_loc

LOG = Log.get(__name__)


def write_file(location, content):
    length = len(content)
    with open(sure_loc(location), 'w') as file:
        LOG.debug('writing {} bytes to file {}', length, location)
        return file.write(content) == length
    LOG.error('writing failed to file {}', location)
