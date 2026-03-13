import argparse
import os
import shutil
import unittest

import numpy as np
import pandas as pd

from CountTableTool import CountTableTool
from CountTableIO import CountTableIO


class DETest(unittest.TestCase):
    def setUp(self):
        self.__test_path = "de_test"
        if not os.path.exists(self.__test_path):
            os.makedirs(self.__test_path)

        self.input_path = os.path.join(self.__test_path, "input.tsv")
        self.output_path = os.path.join(self.__test_path, "output.tsv")

        self.input_df = pd.DataFrame(
            {
                "sampleA_1": [10.0, 1.0, 5.0],
                "sampleA_2": [11.0, 2.0, 5.0],
                "sampleB_1": [1.0, 10.0, 5.0],
                "sampleB_2": [2.0, 11.0, 5.0],
            },
            index=["geneA", "geneB", "geneConst"],
        )
        CountTableIO.write_output_df(self.input_df, self.input_path)

    def tearDown(self):
        if os.path.exists(self.__test_path):
            shutil.rmtree(self.__test_path)

    def test_de_tstat_main(self):
        args = argparse.Namespace(
            subcommand="DE",
            de_method="tstat",
            inpath=self.input_path,
            tissue_labels="A,A,B,B",
            missing="raise",
            opath=self.output_path,
        )
        CountTableTool.main(args)

        output_df = CountTableIO.read_input_df(self.output_path)
        self.assertTrue((output_df.columns.values == np.array(["A", "B"])).all())
        self.assertGreater(output_df.loc["geneA", "A"], 0)
        self.assertLess(output_df.loc["geneA", "B"], 0)
        self.assertLess(output_df.loc["geneB", "A"], 0)
        self.assertGreater(output_df.loc["geneB", "B"], 0)
        self.assertTrue(np.isnan(output_df.loc["geneConst", "A"]))

    def test_de_tstat_missing_drop(self):
        input_with_nan_path = os.path.join(self.__test_path, "input_with_nan.tsv")
        output_with_nan_path = os.path.join(self.__test_path, "output_with_nan.tsv")

        input_with_nan = self.input_df.copy()
        input_with_nan.loc["geneA", "sampleA_1"] = np.nan
        CountTableIO.write_output_df(input_with_nan, input_with_nan_path)

        args = argparse.Namespace(
            subcommand="DE",
            de_method="tstat",
            inpath=input_with_nan_path,
            tissue_labels="A,A,B,B",
            missing="drop",
            opath=output_with_nan_path,
        )
        CountTableTool.main(args)

        output_df = CountTableIO.read_input_df(output_with_nan_path)
        self.assertEqual(output_df.shape, (2, 2))

    def test_de_tstat_missing_raise(self):
        input_with_nan_path = os.path.join(self.__test_path, "input_with_nan.tsv")

        input_with_nan = self.input_df.copy()
        input_with_nan.loc["geneA", "sampleA_1"] = np.nan
        CountTableIO.write_output_df(input_with_nan, input_with_nan_path)

        args = argparse.Namespace(
            subcommand="DE",
            de_method="tstat",
            inpath=input_with_nan_path,
            tissue_labels="A,A,B,B",
            missing="raise",
            opath=self.output_path,
        )
        with self.assertRaises(ValueError):
            CountTableTool.main(args)
