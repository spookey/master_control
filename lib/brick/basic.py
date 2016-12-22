from abc import ABC, abstractmethod

from lib.snips.alert import Log, show_pretty


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

    def batch(self, *, lift):
        for chain in self.below if lift else self.above:
            for elem in chain.batch(lift=lift):
                yield elem
        yield self

    def recurse_batch(self, lift=True):
        result = list(self.batch(lift=lift))
        self.log.debug('collected batch with {} elements', len(result))
        return result

    def shorter_batch(self, batch):
        result = []
        for elem in batch:
            if elem not in result:
                result.append(elem)
        self.log.debug('cut through {} batch. new {}', len(batch), len(result))
        return result

    def fire(self, lift, slow=False, dump=False):
        whole = self.recurse_batch(lift=lift)
        short = self.shorter_batch(whole)
        batch = whole if slow else short

        show_pretty(
            'summary', self,
            dict(direction='raise up' if lift else 'put down'),
            dict(batches=dict(
                avail=dict(short=len(short), whole=len(whole)),
                using='whole' if slow else 'short'
            )),
            dict(mode='dump batch' if dump else 'exec batch'),
            batch,
        )
        if dump:
            return True

        for elem in batch:
            func = elem.full if lift else elem.null
            self.log.info('running module: {}', elem)
            if not func():
                self.log.error('module {} failed: end', elem)
                return False
            else:
                self.log.info('module {} success', elem)

        return True
