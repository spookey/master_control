from m_c.brick.basic import Basic
from m_c.snips.fetch import get_remote


class Power(Basic):
    def do_fire(self, lift=True):
        rsp, err = get_remote(
            self.conf['url'].format(hostname=self.conf['hostname']),
            power=''.join([self.conf['family'], self.conf['prime']]),
            state='full' if lift else 'null',
        )
        if err:
            self.message('full power error', err, lvl='error')
            return False
        return rsp and rsp.status == 200

    def full(self):
        return self.do_fire(lift=True)

    def null(self):
        return self.do_fire(lift=False)
