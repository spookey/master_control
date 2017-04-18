from datetime import datetime, timedelta

from lib.snips.alert import Log, show_pretty
from lib.snips.fetch import get_baseurl, make_paths_req, send_get_req

LOG = Log.get(__name__)


def time_span(curr, points):
    edge = timedelta(hours=(12 / points))
    zero = curr.replace(hour=0, minute=0, second=0, microsecond=0)

    for idx in range(0, (2 * points)):
        head = zero + (idx * edge)
        tail = head + edge
        if curr <= tail and curr >= head:
            rise = (idx % 2 == 0)

            LOG.debug(
                'start {:%H:%M} >= {:%H:%M:%S} [/{}] <= {:%H:%M} end ({})',
                head, curr, points, tail, 'rising' if rise else 'falling'
            )
            return head, tail, rise


def get_color(curr, points, *, c_lo, c_hi):
    head, tail, rise = time_span(curr, points=points)
    value, flank = (curr - head), (tail - head)
    s_val, s_flk = value.total_seconds(), flank.total_seconds()

    LOG.debug(
        'passed ({} == {}) of ({} == {})', value, s_val, flank, s_flk
    )
    color = s_val * (c_hi - c_lo) / (s_flk + c_lo)
    color = int(color if rise else (c_hi - color))
    x_col = '0x{:06x}'.format(color)

    LOG.info(
        'got ({} == {}) for {:%H:%M:%S} [/{}]', x_col, color, curr, points
    )
    return color, x_col


def chroma(hostname, args):
    curr = datetime.now().replace(microsecond=0)
    color, hex_color = get_color(curr, args.points, c_lo=args.lo, c_hi=args.hi)
    request = make_paths_req(get_baseurl(hostname), 'light', 'fade', hex_color)

    if args.dump:
        show_pretty('chroma', dict(
            current=str(curr),
            fade=dict(color=dict(hex=hex_color, raw=color)),
            hostname=hostname,
        ))
        return True

    with send_get_req(request) as resp:
        if resp and resp.status == 200:
            LOG.info('send color {} to {} success!', hex_color, hostname)
            return True

    LOG.error('send to {} failed! sorry!', hostname)
    return False
