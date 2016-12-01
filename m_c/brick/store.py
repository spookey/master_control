from m_c.brick.basic import Basic
from m_c.snips.shell import launch, launch_repeat, repeating


class Store(Basic):
    def mounted(self):
        code, out, _ = launch('mount')
        if not code and out:
            for line in out:
                if 'on /{prefix}/{disk}'.format(
                        prefix=self.conf['prefix'].strip('/'),
                        disk=self.conf['prime']
                ) in line:
                    return True
            return False

    def _disk_info(self):
        def _pull():
            code, out, err = launch('diskutil', 'info', self.conf['prime'])
            if code:
                self.message('disk is unknown', code, out, err, lvl='error')
            return [(k.strip(), v.strip()) for k, v in [
                ln.split(':') for ln in out if ln
            ]]
        uuid, node = None, None
        for key, val in _pull():
            if key == 'Disk / Partition UUID':
                uuid = val
            if key == 'Device Node':
                node = val
        return uuid, node

    def _disk_password(self):
        code, out, err = launch(
            'security', 'find-generic-password', '-ga', self.conf['prime']
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

    def wait_auto(self):
        for step, finished in repeating(
                self.mounted, times=self.conf['power_delay'], patience=1
        ):
            if finished:
                return True
            self.message('disk autmount wait #{:02}'.format(step), lvl='delay')
        self.message('disk autmount failed', 'giving up', lvl='error')
        return False

    def exec_hard(self):
        d_uuid, d_node = self._disk_info()
        if not all([d_uuid, d_node]):
            self.message('disk info not present', d_node, d_uuid, lvl='fatal')
            return False

        passwd = self._disk_password()
        if not passwd:
            self.message('disk password not present', lvl='fatal')
            return False

        return self._disk_unlock(d_uuid, passwd) and self._disk_mount(d_node)

    def full(self):
        for func in [self.mounted, self.wait_auto, self.exec_hard]:
            if func():
                return True
        return False

    def null(self):
        if not self.mounted():
            return True

        for step, (code, out, err) in launch_repeat(
                'diskutil', 'unmount', self.conf['prime'],
                times=self.conf['eject_retry'],
                patience=self.conf['eject_wait'],
        ):
            if not code:
                return True
            self.message(
                'disk unmount try #{:02}'.format(step),
                code, out, err, lvl='error'
            )

        self.message('disk unmount failed', 'giving up', lvl='fatal')
        return False
