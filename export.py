import numpy as np

from CountTableIO import CountTableIO

from RGTools.GenomicElements import GenomicElements

class CountTableExport:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="export_type")

        top_score_filter_parser = subparsers.add_parser("top_percentile_ge",
                                                        help="Export the top percentile entries in GenomicElements format.", 
                                                        )
        CountTableExport.set_parser_top_percentile_ge(top_score_filter_parser)

    @staticmethod
    def set_parser_top_percentile_ge(parser):
        GenomicElements.set_parser_genomic_element_region(parser)
        
        parser.add_argument("--inpath", "-I", 
                            help="Input path for count table.", 
                            required=True, 
                            dest="inpath", 
                            )
        
        parser.add_argument("--percentile",
                            help="Top percentile to export.", 
                            required=True, 
                            dest="percentile", 
                            type=int,
                            )
        
        parser.add_argument("--filter_by",
                            help="Column name to filter by.", 
                            required=True, 
                            dest="filter_by", 
                            )
        
        parser.add_argument("--opath", "-O", 
                            help="Output path.", 
                            default="stdout", 
                            dest="opath", 
                            )

    @staticmethod
    def main_top_percentile_ge(args):
        input_df = CountTableIO.read_input_df(args.inpath)
        filter_values = input_df[args.filter_by].values
        cutoff = np.percentile(filter_values[~np.isnan(filter_values)], 
                               100 - args.percentile, 
                               )
        filter_logical = filter_values >= cutoff
        input_ge = GenomicElements(region_file_path=args.region_file_path,
                                   region_file_type=args.region_file_type,
                                   fasta_path=None, 
                                   )
        output_ge = input_ge.apply_logical_filter(filter_logical, args.opath)

    @staticmethod
    def main(args):
        if args.export_type == "top_percentile_ge":
            CountTableExport.main_top_percentile_ge(args)
        else:
            raise ValueError(f"Invalid export type: {args.export_type}")
