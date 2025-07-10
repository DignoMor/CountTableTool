
import argparse

import pandas as pd
import numpy as np

from CountTableIO import CountTableIO

class ColOps:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="operation")
        parser_concat = subparsers.add_parser("concat",
                                              help="Concatenate count tables.",
                                              )
        ColOps.set_parser_concat(parser_concat)

        parser_filter = subparsers.add_parser("filter",
                                              help="Filter count tables by column.",
                                              )
        ColOps.set_parser_filter(parser_filter)

    @staticmethod
    def set_parser_concat(parser):
        parser.add_argument("--inpath", "-I", 
                            help="Input paths for count tables.", 
                            required=True, 
                            dest="inpaths", 
                            action="append",
                            )
        
        parser.add_argument("--opath", 
                            help="Output path.", 
                            default="stdout", 
                            dest="opath",
                            )

    @staticmethod
    def set_parser_filter(parser):
        parser.add_argument("--inpath", "-I", 
                            help="Input path for count table.", 
                            required=True, 
                            dest="inpath",
                            )

        parser.add_argument("--col", 
                            help="Column to keep.", 
                            required=True, 
                            dest="col",
                            action="append",
                            )

        parser.add_argument("--opath", 
                            help="Output path.", 
                            default="stdout", 
                            dest="opath",
                            )

    @staticmethod
    def main_concat(args):
        input_dfs = [CountTableIO.read_input_df(inpath) for inpath in args.inpaths]
        output_df = pd.concat(input_dfs, axis=1)
        CountTableIO.write_output_df(output_df, 
                                     args.opath, 
                                     )
        
        if not (output_df.shape[0] == input_dfs[0].shape[0]):
            raise ValueError("Index mismatch.")

        return None

    @staticmethod
    def main_filter(args):
        input_df = CountTableIO.read_input_df(args.inpath)

        for col in args.col:
            if not col in input_df.columns:
                raise ValueError(f"Column {col} not found in input count table.")

        output_df = input_df[args.col]
        CountTableIO.write_output_df(output_df, 
                                     args.opath, 
                                     )
        
        return None

    @staticmethod
    def main(args):
        if args.operation == "concat":
            ColOps.main_concat(args)
        elif args.operation == "filter":
            ColOps.main_filter(args)
        else:
            raise ValueError(f"Invalid operation: {args.operation}")
    
