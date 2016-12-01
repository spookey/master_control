from m_c.parse import arguments, local_actions


def run():
    acts = local_actions()
    args = arguments(acts)
    prog = acts.get(args.pkg, {}).get(args.mod)
    if prog:
        return prog.fire(lift=args.lift, fast=(not args.slow), dump=args.dump)
