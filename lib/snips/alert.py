from inspect import signature
from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, LoggerAdapter, StreamHandler,
    getLogger
)
from logging.handlers import RotatingFileHandler
from pprint import pformat
from textwrap import indent as t_indent

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


def text_pretty(*txt, indent=' ' * 2):
    for elem in txt:
        yield t_indent(pformat(elem), indent)


def show_pretty(msg, *txt):
    print(t_indent(msg.upper(), ' ' * 2))
    for elem in text_pretty(*txt, indent=' ' * 4):
        print(elem)


def make_bucket(level, location, size=1024 * 64, count=9):
    bucket = RotatingFileHandler(location, maxBytes=size, backupCount=count)
    bucket.setFormatter(Formatter('''
{levelname:9s}{asctime:25s}{name}.{funcName}() [{pathname}:{lineno:d}]
  {message}'''.strip(), style='{'))
    bucket.setLevel(level)
    return bucket


def make_stream(level):
    stream = StreamHandler(stream=None)
    stream.setFormatter(Formatter('''
{levelname:9s}{name}.{funcName}()
  {message}'''.strip(), style='{'))
    stream.setLevel(level)
    return stream
