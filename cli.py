# -*- coding: utf-8 -*-

import argparse
import os.path

from run import main


def sanityCheck(args):

    if not any(
        [args.updatedb, args.bfs, args.dfs, args.stat, args.brute, args.compare]
    ):
        raise AssertionError(
            "select one operation [updatedb, bfs, dfs, stat, brute, compare]..."
        )

    elif args.updatedb:
        if not args.opendrive:
            raise AssertionError("select input file ...")
        elif not os.path.isfile(args.opendrive):
            raise AssertionError(f"{args.opendrive} not found")

    elif args.bfs or args.dfs or args.brute:
        if not args.id:
            raise AssertionError("enter map id to generate tests ...")

    elif args.stat:
        if not args.id:
            raise AssertionError("enter map id to retrieve test stat ...")

    elif args.compare:
        if not args.id:
            raise AssertionError("enter map id to compare ...")
        if not args.delta:
            raise AssertionError("enter delta id to compare ...")

    main(args=args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="command line arguments")

    parser.add_argument(
        "--opendrive", type=str, required=False, help="opendrive file to parse"
    )

    parser.add_argument(
        "--id", type=int, required=False, default=None, help="mapID"
    )

    parser.add_argument(
        "--delta", type=int, required=False, default=None, help="delta mapID"
    )

    parser.add_argument(
        "--time", type=float, required=False, default=None, help="brake time"
    )

    parser.add_argument("--updatedb", action="store_true")

    parser.add_argument("--bfs", action="store_true")

    parser.add_argument("--dfs", action="store_true")

    parser.add_argument("--euler", action="store_true")

    parser.add_argument("--stat", action="store_true")

    parser.add_argument("--brute", action="store_true")

    parser.add_argument("--compare", action="store_true")

    parser.add_argument("--log", action="store_true")

    args = parser.parse_args()
    sanityCheck(args=args)
