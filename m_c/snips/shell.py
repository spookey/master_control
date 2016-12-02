from subprocess import PIPE, Popen, TimeoutExpired
from time import sleep


def launch(*commands, cwd=None, stdin=None, timeout=15):
    with Popen(
        list(commands), universal_newlines=True,
        cwd=cwd, stdout=PIPE, stderr=PIPE, stdin=PIPE
    ) as proc:
        try:
            out, err = proc.communicate(input=stdin, timeout=timeout)
        except TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()
        return proc.returncode, out.splitlines(), err.splitlines()


def repeating(func, *args, times=1, patience=0, **kwargs):
    times = abs(times) if times else 1
    patience = abs(patience) if patience else None
    for step in range(1, times + 1):
        result = func(*args, **kwargs)
        yield step, result
        if patience and step < times:
            sleep(patience)


def launch_repeat(*args, times=1, patience=0, **kwargs):
    for step, (code, out, err) in repeating(
            launch, *args, times=times, patience=patience, **kwargs
    ):
        yield step, (code, out, err)
        if code == 0:
            break
