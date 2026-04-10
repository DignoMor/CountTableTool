import pandas as pd

from CountTableIO import CountTableIO


class CountTableImport:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="import_type")
        parser_rsem = subparsers.add_parser(
            "rsem",
            help="Import count table data from RSEM outputs.",
        )
        CountTableImport.set_parser_rsem(parser_rsem)

    @staticmethod
    def set_parser_rsem(parser):
        parser.add_argument("--sample",
                            help="Name of the sample.",
                            dest="sample",
                            action="append",
                            required=True,
                            )

        parser.add_argument("--rsem_output",
                            help="Path to the RSEM output.",
                            dest="rsem_output",
                            action="append",
                            required=True,
                            )

        parser.add_argument("--gene_id_list",
                            help="A file containing gene IDs, one per line.",
                            dest="gene_id_list",
                            required=True,
                            )

        parser.add_argument("--count_type",
                            help="Type of count to import from RSEM outputs.",
                            dest="count_type",
                            default="expected_count",
                            )

        parser.add_argument("--opath", "-O",
                            help="Output path for imported count table.",
                            dest="opath",
                            required=True,
                            )

    @staticmethod
    def main_rsem(args):
        if len(args.sample) != len(args.rsem_output):
            raise ValueError("Number of --sample and --rsem_output arguments must match.")

        gene_ids = pd.read_csv(args.gene_id_list, sep="\t", header=None).iloc[:, 0].astype(str).tolist()

        sample_series = {}
        for sample_name, rsem_output_path in zip(args.sample, args.rsem_output):
            rsem_df = pd.read_csv(rsem_output_path, sep="\t", index_col=0)
            if args.count_type not in rsem_df.columns:
                raise ValueError(f"Count type '{args.count_type}' not found in RSEM output: {rsem_output_path}")

            sample_series[sample_name] = rsem_df[args.count_type].reindex(gene_ids)

        output_df = pd.DataFrame(sample_series, index=gene_ids)
        CountTableIO.write_output_df(output_df, args.opath)

    @staticmethod
    def main(args):
        if args.import_type == "rsem":
            CountTableImport.main_rsem(args)
        else:
            raise NotImplementedError(f"Unsupported import type: {args.import_type}")
