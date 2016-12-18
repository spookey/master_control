from abc import ABC, abstractmethod

from m_c.snips.front import message


class Basic(ABC):
    def __init__(self, ident, *depends, prime=None):
        self.ident = ident
        self.prime = prime if prime else ident
        self.below = []
        self.above = []
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
        return '<{name} \'{ident}\'{prime}>'.format(
            ident=self.ident,
            name=self.__class__.__name__,
            prime=(' ({prime})'.format(
                prime=self.prime
            ) if self.prime != self.ident else '')
        )

    def recurse_chain(self, lift=True):
        def _iter():
            for chain in self.below if lift else self.above:
                for elem in chain.recurse_chain(lift=lift):
                    yield elem
            yield self
        return list(_iter())

    @staticmethod
    def shorter_chain(chain):
        result = []
        for elem in chain:
            if elem not in result:
                result.append(elem)
        return result

    def message(self, msg, *txt, lvl=None):
        return message(
            msg, *txt, pkg=self.__class__.__name__, lvl=lvl
        )

    def fire(self, lift, slow=False, dump=False):
        whole = self.recurse_chain(lift=lift)
        short = self.shorter_chain(whole)
        chain = whole if slow else short

        self.message(
            'raise up' if lift else 'put down',
            ('path', dict(
                _now_=len(chain), short=len(short), whole=len(whole)
            )),
            chain, lvl=None,
        )
        for elem in chain:
            func = elem.full if lift else elem.null
            self.message(
                '{}running module'.format('not ' if dump else ''),
                elem, lvl=None
            )
            if dump:
                continue
            if not func():
                self.message('module error', elem, lvl='fatal')
                return False
        return True
