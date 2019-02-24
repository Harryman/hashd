from typing import List
import argparse

from commands.init import init


def parse(args_str: List[str]) -> None:
    parser = argparse.ArgumentParser(prog="hashd")
    parser.set_defaults(func=lambda a: parser.print_help())

    subparsers = parser.add_subparsers(help="Sub-commands:")

    init_subparser = subparsers.add_parser(
        "init",
        help="Generates and stores a local private key and provides the mnemonic",
    )
    init_subparser.set_defaults(func=init)

    args = parser.parse_args(args_str)
    args.func(args)
