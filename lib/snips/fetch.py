from contextlib import closing, contextmanager
from urllib.error import URLError
from urllib.request import Request, urlopen

from lib.snips.alert import Log

LOG = Log.get(__name__)


def get_baseurl(hostname):
    return 'http://{hostname}.local'.format(hostname=hostname)


def make_paths_req(url, *parts):
    return Request('{}/{}'.format(url.rstrip('/'), '/'.join(parts)))


@contextmanager
def send_get_req(request):
    try:
        with closing(urlopen(request)) as response:
            yield response
    except URLError as ex:
        LOG.error('{r.type} connection to {r.host} failed: {}', ex, r=request)
        yield
