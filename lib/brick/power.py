from lib.brick.basic import Basic
from lib.snips.fetch import make_param_req, send_get_req


class Power(Basic):
    def __init__(self, *args, url=None, hostname=None, family=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = url.format(hostname=hostname)
        self.family = family

    def do_fire(self, lift=True):
        with send_get_req(make_param_req(
            self.base_url,
            power=''.join([self.family, self.prime]),
            state='full' if lift else 'null',
        )) as rsp:
            return rsp and rsp.status == 200

        self.log.error('connection error [{}]', self.base_url)
        return False

    def full(self):
        return self.do_fire(lift=True)

    def null(self):
        return self.do_fire(lift=False)
