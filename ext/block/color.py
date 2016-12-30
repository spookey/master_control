from datetime import datetime, timedelta

from lib.snips.fetch import get_baseurl, make_paths_req, send_get_req


def time_span(now, div):
    seg = 24 / (2 * div)
    slc = timedelta(hours=seg)
    nil = now.replace(hour=0, minute=0, second=0)
    fin = nil + timedelta(hours=24)

    tail, idx = fin, 0
    for idx in range(0, int(24 / seg)):
        head = fin - (idx * slc)
        if now >= head:
            break
        tail = head
    return head, tail, (idx % 2 == 0)


def color_map(val, *, imax, hi, lo, stat=False):
    omin, omax = ((lo, hi) if stat else (hi, lo))
    return int((val * (omax - omin)) / (imax + omin))


def get_color(args):
    now = datetime.now().replace(microsecond=0)
    head, tail, stat = time_span(now, args.divider)
    return '0x{:06x}'.format(color_map(
        (now - head).total_seconds(),
        imax=(tail - head).total_seconds(),
        stat=stat, hi=args.hi, lo=args.lo
    ))


def chroma(args, name):
    with send_get_req(make_paths_req(
        get_baseurl(name), 'light', 'fade', get_color(args)
    )) as resp:
        return resp and resp.status == 200

    return False
