import numpy as np

from CountTableIO import CountTableIO

from RGTools.GenomicElements import GenomicElements
from RGTools.ListFile import ListFile

class CountTableExport:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="export_type")

        top_score_filter_parser = subparsers.add_parser("top_percentile_ge",
                                                        help="Export the top percentile entries in GenomicElements format.", 
                                                        )
        CountTableExport.set_parser_top_percentile_ge(top_score_filter_parser)

        name_replaced_ct_parser = subparsers.add_parser("name_replaced_ct",
                                                        help="Export a count table with replaced index names.",
                                                        )
        CountTableExport.set_parser_name_replaced_ct(name_replaced_ct_parser)

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
    def set_parser_name_replaced_ct(parser):
        parser.add_argument("--inpath", "-I",
                            help="Input path for count table.",
                            required=True,
                            dest="inpath",
                            )

        parser.add_argument("--old_index_list",
                            help="Path to old index list file.",
                            required=True,
                            dest="old_index_list",
                            )

        parser.add_argument("--new_index_list",
                            help="Path to new index list file.",
                            required=True,
                            dest="new_index_list",
                            )

        parser.add_argument("--opath", "-O",
                            help="Output path.",
                            default="stdout",
                            dest="opath",
                            )

    @staticmethod
    def main_name_replaced_ct(args):
        input_df = CountTableIO.read_input_df(args.inpath)

        old_index_file = ListFile()
        old_index_file.read_file(args.old_index_list)
        old_index_names = old_index_file.get_contents(dtype="str")

        new_index_file = ListFile()
        new_index_file.read_file(args.new_index_list)
        new_index_names = new_index_file.get_contents(dtype="str")

        if len(old_index_names) != len(new_index_names):
            raise ValueError("old_index_list and new_index_list must have the same number of entries.")

        replace_map = dict(zip(old_index_names, new_index_names))
        output_df = input_df.copy()
        output_df.index = [replace_map.get(idx, idx) for idx in output_df.index]

        CountTableIO.write_output_df(output_df, args.opath)

    @staticmethod
    def main(args):
        if args.export_type == "top_percentile_ge":
            CountTableExport.main_top_percentile_ge(args)
        elif args.export_type == "name_replaced_ct":
            CountTableExport.main_name_replaced_ct(args)
        else:
            raise ValueError(f"Invalid export type: {args.export_type}")
