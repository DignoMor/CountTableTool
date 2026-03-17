import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels.stats.multitest import multipletests

from CountTableIO import CountTableIO


class DE:
    @staticmethod
    def set_parser(parser):
        subparsers = parser.add_subparsers(dest="de_method")
        parser_tstat = subparsers.add_parser(
            "tstat",
            help="Compute t-statistics for tissue specificity.",
        )
        DE.set_parser_tstat(parser_tstat)

    @staticmethod
    def set_parser_tstat(parser):
        parser.add_argument("--inpath", "-I",
                            help="Input path for count table.",
                            required=True,
                            dest="inpath",
                            )

        parser.add_argument("--exp_label",
                            help="Label for experiment samples.",
                            required=True,
                            dest="exp_label",
                            )

        parser.add_argument("--ctrl_label",
                            help="Control label(s) as a comma-separated string. "
                                 "If omitted, all non-experiment labels are used.",
                            default=None,
                            dest="ctrl_label",
                            )

        parser.add_argument("--tissue_labels",
                            help="Tissue labels for each sample as a comma-separated string. "
                                 "If omitted, column names will be used.",
                            default=None,
                            dest="tissue_labels",
                            )

        parser.add_argument("--opath",
                            help="Output path for t-stat table.",
                            default="stdout",
                            dest="opath",
                            )

    @staticmethod
    def _compute_stats_one_elem(x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if np.any(np.isnan(y)):
            raise ValueError("Missing values found in Y.")

        x_df = pd.DataFrame(x, columns=["X1"])
        x_df = sm.add_constant(x_df["X1"])

        if np.linalg.matrix_rank(x_df) <= 1:
            raise ValueError("Singular design matrix.")

        model = sm.OLS(y, x_df, missing="raise").fit()
        tstat = model.tvalues["X1"]
        pval = model.pvalues["X1"]
        if not np.isfinite(tstat):
            tstat = np.nan
        if not np.isfinite(pval):
            pval = np.nan

        exp_vals = y[x == 1]
        ctrl_vals = y[x == -1]
        if len(exp_vals) == 0 or len(ctrl_vals) == 0:
            raise ValueError("At least one experiment and one control sample are required.")

        # Use a pseudocount to keep log2FC defined when mean is zero.
        log2fc = np.log2((np.mean(exp_vals) + 1.0) / (np.mean(ctrl_vals) + 1.0))
        return log2fc, tstat, pval

    @staticmethod
    def main_tstat(args):
        input_df = CountTableIO.read_input_df(args.inpath)

        if np.any(np.isnan(input_df.values)):
            raise ValueError("Missing values found in input table.")

        if args.tissue_labels is None:
            tissue_labels = np.array(input_df.columns, dtype=str)
        else:
            tissue_labels = np.array(args.tissue_labels.split(","), dtype=str)

        if len(tissue_labels) != input_df.shape[1]:
            raise ValueError("Number of tissue labels must match the number of columns in input table.")

        exp_labels = str(args.exp_label).split(",")
        exp_mask = np.array([label in exp_labels for label in tissue_labels])
        if not np.any(exp_mask):
            raise ValueError(f"Experiment label not found: {', '.join(exp_labels)}")

        if args.ctrl_label is None:
            ctrl_mask = ~exp_mask
        else:
            ctrl_labels = [label.strip() for label in str(args.ctrl_label).split(",")]
            ctrl_labels = [label for label in ctrl_labels if label != ""]
            ctrl_mask = np.array([label not in exp_labels for label in tissue_labels])

            if not np.any(ctrl_mask):
                raise ValueError(f"Control label not found: {', '.join(ctrl_labels)}")

        if np.any(exp_mask & ctrl_mask):
            raise ValueError("Experiment and control sets must be disjoint.")

        x = exp_mask.astype(int) - ctrl_mask.astype(int)
        use_mask = (x != 0.0)

        output_df = pd.DataFrame(index=input_df.index, 
                                 columns=["log2FC", "tstat", "pval"],
                                 dtype=float,
                                 )

        for elem_ind, elem_info in input_df.iterrows():
            y = elem_info.values[use_mask]
            x = x[use_mask]
            log2fc, tstat, pval = DE._compute_stats_one_elem(x, y)
            output_df.loc[elem_ind, "log2FC"] = log2fc
            output_df.loc[elem_ind, "tstat"] = tstat
            output_df.loc[elem_ind, "pval"] = pval

        output_df["padj"] = multipletests(output_df["pval"].values, 
                                          method="fdr_bh", 
                                          )[1]
        CountTableIO.write_output_df(output_df, args.opath)

    @staticmethod
    def main(args):
        if args.de_method == "tstat":
            DE.main_tstat(args)
        else:
            raise ValueError(f"Invalid DE method: {args.de_method}")
