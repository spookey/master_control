from lib.parse import arguments, local_collect


def run():
    inst = local_collect()
    args = arguments(inst)
    for instance in [
            insta for ident, prime, insta in inst.get(args.module)
            if any(args.action == act for act in [ident, prime])
    ]:
        return instance.fire(
            lift=args.lift, slow=args.slow, dump=args.dump
        )
    return False
