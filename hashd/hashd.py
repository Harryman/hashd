from typing import List
import argparse

from commands import init, add_work, hash_bench

def parse(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser(prog="hashd")
    parser.set_defaults(func=lambda a: parser.print_help())

    subparsers = parser.add_subparsers(help="Sub-commands:")

    init_subparser = subparsers.add_parser(
        "init",
        help="Generates and stores a local private key and provides the mnemonic",
    )
    init_subparser.set_defaults(func=init.init)

    add_work_subparser = subparsers.add_parser(
        "add-work",
        help="Adds PoW to a block signature",
    )
    add_work_subparser.add_argument("signature")
    add_work_subparser.set_defaults(func=add_work.add_work)

    hash_bench_subparser = subparsers.add_parser(
        "hash-bench",
        help="Benchmark to show lowest hash after 1, 10, and 100 seconds",
    )
    hash_bench_subparser.set_defaults(func=hash_bench.hash_bench)

    args = parser.parse_args(args_str)
    args.func(args)
