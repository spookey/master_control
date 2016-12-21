from lib.brick.basic import Basic
from lib.snips.mgmnt import management_summary
from lib.snips.shell import launch


class State(Basic):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        acts = management_summary(self.do_func)
        self.command = acts.get(command)

    def full(self):
        return True

    def do_func(self, cmd):
        code, _, err = launch(*cmd)
        if code == 0:
            return True
        self.log.error('command {} failed: {}', self.prime, ' '.join(err))
        return False

    def null(self):
        if self.command:
            return self.command() is True
        self.log.critical('state command {} unknown', self.prime)
        return False
