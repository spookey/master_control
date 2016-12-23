from lib.brick.basic import Basic
from lib.snips.fetch import get_baseurl, make_paths_req, send_get_req


class Power(Basic):
    def __init__(self, *args, hostname=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hostname = hostname

    def do_fire(self, lift=True):
        with send_get_req(make_paths_req(
            get_baseurl(self.hostname), 'power',
            'full' if lift else 'null', self.prime
        )) as resp:
            return resp and resp.status == 200

        self.log.error('connection error [{}]', self.hostname)
        return False

    def full(self):
        return self.do_fire(lift=True)

    def null(self):
        return self.do_fire(lift=False)
