#!/usr/bin/env python

import argparse

from imputate import Imputate
from col_ops import ColOps
from export import CountTableExport

class CountTableTool:
    @staticmethod
    def main(args):
        if args.subcommand == "imputate":
            Imputate.main(args)
        elif args.subcommand == "col_ops":
            ColOps.main(args)
        elif args.subcommand == "export":
            CountTableExport.main(args)
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

        parser_col_ops = subparsers.add_parser(
            "col_ops",
            help="Operate on columns of a count table.",
        )

        ColOps.set_parser(parser_col_ops)

        parser_export = subparsers.add_parser(
            "export",
            help="Export a count table in a different format.",
        )

        CountTableExport.set_parser(parser_export)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Count Table Tool.")

    CountTableTool.set_parser(parser)
    args = parser.parse_args()
    CountTableTool.main(args)

