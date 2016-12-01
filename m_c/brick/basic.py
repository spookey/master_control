from abc import ABC, abstractmethod

from m_c.snips.front import message


class Basic(ABC):
    def __init__(self, ident, *depends, **conf):
        self.ident = ident
        self.below = []
        self.above = []
        self.conf = conf
        for elem in depends:
            self.below.append(elem)
            elem.above.append(self)

    @abstractmethod
    def full(self):
        pass

    @abstractmethod
    def null(self):
        pass

    def __repr__(self):
        prime = self.conf.get('prime', self.ident)
        prime = prime if prime != self.ident else None
        return '<{name} \'{ident}\'{prime}>'.format(
            ident=self.ident,
            name=self.__class__.__name__,
            prime=' ({p})'.format(p=prime) if prime else ''
        )

    def pull_chain(self, lift=True):
        return self.below if lift else self.above

    def pull_meths(self, lift=True, elem=None):
        elem = (elem if elem else self)
        return elem.full if lift else elem.null

    def path_whole(self, lift=True):
        def _iter():
            for chain in self.pull_chain(lift=lift):
                for elem in chain.path_whole(lift=lift):
                    yield elem
            yield self
        return list(_iter())

    def path_short(self, lift=True):
        result = []
        for elem in self.path_whole(lift=lift):
            if elem not in result:
                result.append(elem)
        return result

    def message(self, msg, *txt, lvl=None):
        return message(
            msg, self, *txt, pkg=self.__class__.__name__, lvl=lvl
        )

    def fire(self, lift, fast=True, dump=False):
        whole = self.path_whole(lift=lift)
        short = self.path_short(lift=lift)
        chain = short if fast else whole

        self.message(
            'raise up' if lift else 'put down',
            ('path', dict(
                _now_=len(chain), short=len(short), whole=len(whole)
            )),
            chain, lvl='basic',
        )
        for elem in chain:
            func = elem.pull_meths(lift=lift)
            self.message('running module', elem, lvl='basic')
            if dump:
                continue
            if not func():
                self.message('module error', elem, lvl='fatal')
                return False
        return True
