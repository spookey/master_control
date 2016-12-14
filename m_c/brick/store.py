from m_c.brick.basic import Basic
from m_c.snips.shell import launch, launch_repeat, repeating


class Store(Basic):
    def __init__(
            self, *args,
            eject_retry=3, eject_wait=5, power_delay=30, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.eject_retry = eject_retry
        self.eject_wait = eject_wait
        self.power_delay = power_delay

    def _disk_info(self):
        code, out, err = launch('diskutil', 'info', self.prime)
        if code:
            self.message('disk unknown', code, out, err, lvl='error')
        return dict((k.strip(), v.strip()) for k, v in [
            ln.split(':') for ln in out if ln
        ])

    def mounted(self):
        return self._disk_info().get('Mounted') == 'Yes'

    def wait_disk(self):
        if not any(obj.__class__.__name__ == 'Power' for obj in self.below):
            return False

        for step, finished in repeating(
                self.mounted, times=self.power_delay, patience=1
        ):
            if finished:
                return True
            if not step % 3:
                self.message(
                    'disk autmount wait #{:02}'.format(step), lvl='delay'
                )
        self.message('disk autmount failed', 'giving up', lvl='error')
        return False

    def _fetch_password(self):
        code, out, err = launch(
            'security', 'find-generic-password', '-ga', self.prime
        )
        if code:
            self.message('disk password error', code, out, err, lvl='error')
        if not code and err:
            _, _, passwd = err[-1].rpartition(': "')
            return passwd.rstrip('"')

    def _disk_unlock(self, uuid, passwd):
        code, out, err = launch(
            'diskutil', 'corestorage', 'unlockvolume', uuid,
            '-stdinpassphrase', stdin=passwd
        )
        if not code:
            return True
        self.message('disk unlock error', code, out, err, lvl='error')
        if err and 'already unlocked and is attached' in err[0]:
            return True
        return False

    def _disk_mount(self, node):
        code, out, err = launch('diskutil', 'mount', node)
        if not code:
            return True
        self.message('disk mount error', code, out, err, lvl='error')
        return False

    def mount_manually(self):
        info = self._disk_info()
        d_uuid = info.get('Disk / Partition UUID')
        d_node = info.get('Device Node')
        if not all([d_uuid, d_node]):
            self.message('disk info not present', d_node, d_uuid, lvl='fatal')
            return False

        passwd = self._fetch_password()
        if not passwd:
            self.message('disk password not present', lvl='fatal')
            return False

        return self._disk_unlock(d_uuid, passwd) and self._disk_mount(d_node)

    def full(self):
        for func in [self.mounted, self.wait_disk, self.mount_manually]:
            if func():
                return True
        return False

    def null(self):
        if not self.mounted():
            return True

        for step, (code, out, err) in launch_repeat(
                'diskutil', 'unmount', self.prime,
                times=self.eject_retry, patience=self.eject_wait
        ):
            if not code:
                return True
            self.message(
                'disk unmount try #{:02}'.format(step),
                code, out, err, lvl='error'
            )

        self.message('disk unmount failed', 'giving up', lvl='fatal')
        return False
