#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import lppn
import sys


def parse():
    parser = argparse.ArgumentParser(
        description=(
            "Print the latest Python patch number of a given major and minor"
            " version"
        )
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Print lppn version"
    )
    parser.add_argument(
        "-f",
        "--full-version",
        action="store_true",
        help="Print full python version",
    )
    parser.add_argument(
        "-g",
        "--get",
        type=int,
        nargs=2,
        metavar=("MAJOR", "MINOR"),
        help="Major and minor python version e.g. 3 12",
    )
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.version:
        print(lppn.version)
        sys.exit(0)

    major, minor = args.get
    patch = lppn.get(major, minor)
    if args.full_version:
        print(f"{major}.{minor}.{patch}")
    else:
        print(patch)
