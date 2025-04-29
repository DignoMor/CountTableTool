
from CountTableIO import CountTableIO

class Imputate:
    @staticmethod
    def get_supported_impuatation_methods():
        return ["min"]


    @staticmethod
    def set_parser(parser):
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
        
        parser.add_argument("--method",
                            help="Imputation method to use. ",
                            choices=Imputate.get_supported_impuatation_methods(),
                            default="min",
                            dest="method",
                            )

    @staticmethod
    def min_imputation(inpath, opath):
        input_df = CountTableIO.read_input_df(inpath)

        input_df.fillna(input_df.min(), inplace=True)

        CountTableIO.write_output_df(input_df, opath)

    @staticmethod
    def main(args):
        if args.method == "min":
            # Call the min imputation function
            Imputate.min_imputation(args.inpath, args.opath)
        else:
            raise ValueError(f"Unsupported imputation method: {args.method}")
