from contextlib import closing
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def get_remote(url, **data):
    request = Request('{}/?{}'.format(
        url.rstrip('/'), urlencode(data)
    ))

    try:
        with closing(urlopen(request)) as response:
            return response, None
    except URLError as ex:
        return None, ex
