from inspect import signature
from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, LoggerAdapter, StreamHandler,
    getLogger
)
from logging.handlers import RotatingFileHandler

LEVELS = [DEBUG, INFO, WARNING, ERROR]
ROOT_LOGGER = getLogger()
ROOT_LOGGER.setLevel(LEVELS[0])


class Log(LoggerAdapter):
    @classmethod
    def get(cls, *names, extra=None):
        return cls(getLogger('.'.join(names)), extra)

    def log(self, level, msg, *args, **kwargs):
        if not self.isEnabledFor(level):
            return

        func = self.logger._log  # pylint: disable=W0212
        proc = dict((key, val) for key, val in [
            (pk, kwargs.get(pk)) for pk in signature(func).parameters.keys()
        ] if val)
        func(level, str(msg).format(*args, **kwargs), (), **proc)


def make_bucket(level, location, size=1024 * 8, count=9):
    bucket = RotatingFileHandler(location, maxBytes=size, backupCount=count)
    bucket.setFormatter(Formatter('''
{levelname:9s}{asctime:25s}{name}.{funcName}() [{pathname}:{lineno:d}]
\t{message}'''.strip(), style='{'))
    bucket.setLevel(level)
    return bucket


def make_stream(level):
    stream = StreamHandler(stream=None)
    stream.setFormatter(Formatter('''
{levelname:9s}{name}.{funcName}()
\t{message}'''.strip(), style='{'))
    stream.setLevel(level)
    return stream
