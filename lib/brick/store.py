from lib.brick.basic import Basic
from lib.snips.shell import launch, launch_repeat, repeating


class Store(Basic):
    def __init__(
            self, *args, eject_retry=3, eject_wait=5, power_delay=30, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.eject_retry = eject_retry
        self.eject_wait = eject_wait
        self.power_delay = power_delay

    def _disk_info(self):
        code, out, _ = launch('diskutil', 'info', self.prime)
        if code != 0:
            self.log.warning('disk unknown: {}', ' '.join(out))
        return dict((k.strip(), v.strip()) for k, v in [
            ln.split(':') for ln in out if ln
        ])

    def mounted(self):
        return self._disk_info().get('Mounted') == 'Yes'

    def wait_disk(self):
        if not any(obj.__class__.__name__ == 'Power' for obj in self.below):
            self.log.debug('disk wait for {} useless, no power', self.prime)
            return False

        for _, finished in repeating(
                self.mounted, times=self.power_delay, patience=1
        ):
            if finished:
                return True
        self.log.error('disk autmount failed for {}', self.prime)
        return False

    def _fetch_password(self):
        code, _, err = launch(
            'security', 'find-generic-password', '-ga', self.prime, e_hide=True
        )
        if code == 0:
            _, _, passwd = err[-1].rpartition(': "')
            return passwd.rstrip('"')

        self.log.error('disk password failed: {}', ' '.join(err))
        return False

    def _disk_unlock(self, uuid, passwd):
        code, _, err = launch(
            'diskutil', 'corestorage', 'unlockvolume', uuid,
            '-stdinpassphrase', stdin=passwd
        )
        if code == 0:
            return True
        if err and 'already unlocked and is attached' in err[0]:
            self.log.info('disk {} was already unlocked', self.prime)
            return True
        self.log.error('disk unlock failed', ' '.join(err))
        return False

    def _disk_mount(self, node):
        code, _, err = launch('diskutil', 'mount', node)
        if code == 0:
            return True
        self.log.error('disk mount failed: {}', ' '.join(err))
        return False

    def mount_manually(self):
        info = self._disk_info()
        d_uuid = info.get('Disk / Partition UUID')
        d_node = info.get('Device Node')
        if not all([d_uuid, d_node]):
            self.log.error('disk info missing "{}" "{}"', d_node, d_uuid)
            return False

        passwd = self._fetch_password()
        if not passwd:
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

        for _, (code, _, _) in launch_repeat(
                'diskutil', 'unmount', self.prime,
                times=self.eject_retry, patience=self.eject_wait
        ):
            if code == 0:
                return True
        return False
