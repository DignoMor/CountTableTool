
from CountTableIO import CountTableIO

class Normalization:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="normalization_type")
        parser_per_million = subparsers.add_parser("per_million",
                                                   help="Per million normalization.",
                                                   )
        Normalization.set_parser_per_million(parser_per_million)

    @staticmethod
    def set_parser_per_million(parser):
        parser.add_argument("--inpath", "-I", 
                            help="Input path for count table.", 
                            required=True, 
                            dest="inpath", 
                            )

        parser.add_argument("--opath", "-O", 
                            help="Output path.", 
                            default="stdout", 
                            dest="opath", 
                            )

    @staticmethod
    def per_million_normalization_main(args):
        input_df = CountTableIO.read_input_df(args.inpath)
        output_df = input_df / input_df.sum(axis=0) * 1e6
        CountTableIO.write_output_df(output_df, args.opath)
        return None
    
    @staticmethod
    def main(args):
        if args.normalization_type == "per_million":
            Normalization.per_million_normalization_main(args)
        else:
            raise ValueError(f"Invalid normalization type: {args.normalization_type}")
