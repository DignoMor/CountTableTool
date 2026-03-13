import numpy as np
import pandas as pd
import statsmodels.api as sm

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

        parser.add_argument("--tissue_labels",
                            help="Tissue labels for each sample as a comma-separated string. "
                                 "If omitted, column names will be used.",
                            default=None,
                            dest="tissue_labels",
                            )

        parser.add_argument("--missing",
                            help="Method for handling missing values.",
                            default="raise",
                            choices=["raise", "drop"],
                            )

        parser.add_argument("--opath",
                            help="Output path for t-stat table.",
                            default="stdout",
                            dest="opath",
                            )

    @staticmethod
    def _compute_tstat_one_elem(x, y, missing="raise"):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if missing == "raise" and np.any(np.isnan(y)):
            raise ValueError("Missing values found in Y with missing='raise'.")

        if np.all(np.isnan(y)):
            raise ValueError("All values in Y are missing.")

        x_df = pd.DataFrame(x, columns=["X1"])
        x_df = sm.add_constant(x_df["X1"])

        # Return np.nan if the design is singular after removing NaNs.
        keep = ~np.isnan(y)
        if np.linalg.matrix_rank(x_df.loc[keep]) <= 1:
            raise ValueError("Singular design matrix.")

        model = sm.OLS(y, x_df, missing=missing).fit()
        tstat = model.tvalues["X1"]
        if not np.isfinite(tstat):
            return np.nan
        return tstat

    @staticmethod
    def main_tstat(args):
        input_df = CountTableIO.read_input_df(args.inpath)

        if args.missing == "raise" and np.any(np.isnan(input_df.values)):
            raise ValueError("Missing values found in input table with missing='raise'.")

        if args.missing == 'drop':
            input_df = input_df.dropna(axis=0)

        if args.tissue_labels is None:
            tissue_labels = np.array(input_df.columns, dtype=str)
        else:
            tissue_labels = np.array(args.tissue_labels.split(","), dtype=str)

        if len(tissue_labels) != input_df.shape[1]:
            raise ValueError("Number of tissue labels must match the number of columns in input table.")

        unique_tissues = np.unique(tissue_labels)

        output_array = np.zeros((input_df.shape[0], len(unique_tissues)))

        for tissue_ind, tissue in enumerate(unique_tissues):
            x = np.array([1 if label == tissue else -1 for label in tissue_labels])

            for elem_ind, (_, elem_info) in enumerate(input_df.iterrows()):
                y = elem_info.values
                tstat = DE._compute_tstat_one_elem(x, y, missing=args.missing)
                output_array[elem_ind, tissue_ind] = tstat

        output_df = pd.DataFrame(output_array,
                                 index=input_df.index,
                                 columns=unique_tissues,
                                 )
        CountTableIO.write_output_df(output_df, args.opath)

    @staticmethod
    def main(args):
        if args.de_method == "tstat":
            DE.main_tstat(args)
        else:
            raise ValueError(f"Invalid DE method: {args.de_method}")
