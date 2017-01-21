from subprocess import PIPE, Popen, TimeoutExpired
from time import sleep

from lib.snips.alert import Log

LOG = Log.get(__name__)


def launch(*commands, cwd=None, stdin=None, timeout=15, e_hide=False):
    with Popen(
        list(commands), universal_newlines=True,
        cwd=cwd, stdout=PIPE, stderr=PIPE, stdin=PIPE
    ) as proc:
        LOG.debug('command run ->\n{}', ' '.join(proc.args))
        try:
            out, err = proc.communicate(input=stdin, timeout=timeout)
        except TimeoutExpired as ex:
            LOG.error('command timeout: {}', ex)
            proc.kill()
            out, err = proc.communicate()

        if out:
            LOG.debug('command out ->\n{}', out)
        if err and not e_hide:
            LOG.debug('command err ->\n{}', err)
        LOG.info('command returncode: {}', proc.returncode)
        return proc.returncode, out.splitlines(), err.splitlines()


def repeating(func, *args, times=1, patience=0, **kwargs):
    times = abs(times) if times else 1
    patience = abs(patience) if patience else None
    for step in range(1, times + 1):
        result = func(*args, **kwargs)
        LOG.info('repeating #{} of {} got ->\n{}', step, times, result)
        yield step, result
        if patience and step < times:
            LOG.debug('waiting {} seconds before repeating', patience)
            sleep(patience)


def launch_repeat(*args, times=1, patience=0, **kwargs):
    for step, (code, out, err) in repeating(
            launch, *args, times=times, patience=patience, **kwargs
    ):
        yield step, (code, out, err)
        if code == 0:
            break
