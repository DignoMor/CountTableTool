#!/usr/bin/env python

import argparse

from imputate import Imputate

class CountTableTool:
    @staticmethod
    def main(args):
        if args.subcommand == "imputate":
            Imputate.main(args)
        else:
            raise ValueError("Invalid subcommand.")
    
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="subcommand")

        parser_imputate = subparsers.add_parser(
            "imputate",
            help="Impute missing values in a count table.",
        )

        Imputate.set_parser(parser_imputate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Count Table Tool.")

    CountTableTool.set_parser(parser)
    args = parser.parse_args()
    CountTableTool.main(args)

