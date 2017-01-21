from lib.brick.basic import Basic
from lib.snips.mgmnt import management_summary


class State(Basic):
    def __init__(self, *args, command=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = management_summary(command)

    def full(self):
        return True

    def null(self):
        if self.command is not None:
            return self.command(self.prime) is True
        self.log.critical('state command {} unknown', self.prime)
        return False
