from contextlib import closing, contextmanager
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from lib.snips.alert import Log

LOG = Log.get(__name__)


def make_param_req(url, **data):
    return Request('{}/?{}'.format(url.rstrip('/'), urlencode(data)))


def make_paths_req(url, *parts):
    return Request('{}/{}'.format(url.rstrip('/'), '/'.join(parts)))


@contextmanager
def send_get_req(request):
    try:
        with closing(urlopen(request)) as response:
            yield response
    except URLError as ex:
        LOG.error('{r.type} connection to {r.host} failed: {}', ex, r=request)
        yield None
