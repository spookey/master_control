from abc import ABC, abstractmethod

from lib.snips.alert import Log, show_pretty
from lib.snips.front import message


class Basic(ABC):
    def __init__(self, ident, *depends, prime=None):
        self.ident = ident
        self.prime = prime if prime else ident
        self.below = []
        self.above = []
        for elem in depends:
            self.below.append(elem)
            elem.above.append(self)
        self.log = Log.get(__name__, self.__class__.__name__)

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
        result = list(_iter())
        self.log.debug('collected chain with {} elements', len(result))
        return result

    def shorter_chain(self, chain):
        result = []
        for elem in chain:
            if elem not in result:
                result.append(elem)
        self.log.debug('cut through {} chain. now {}', len(chain), len(result))
        return result

    def message(self, msg, *txt, lvl=None):
        return message(
            msg, *txt, pkg=self.__class__.__name__, lvl=lvl
        )

    def fire(self, lift, slow=False, dump=False):
        whole = self.recurse_chain(lift=lift)
        short = self.shorter_chain(whole)
        chain = whole if slow else short

        show_pretty(
            'summary', self,
            dict(direction='raise up' if lift else 'put down'),
            dict(chains=dict(
                avail=dict(short=len(short), whole=len(whole)),
                using='whole' if slow else 'short'
            )),
            dict(mode='dump chain' if dump else 'exec chain'),
            chain,
        )
        if dump:
            return True

        for elem in chain:
            func = elem.full if lift else elem.null
            self.log.info('running module: {}', elem)
            if not func():
                self.log.error('module {} failed: abort', elem)
                return False

        return True
