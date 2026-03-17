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
                "sampleA_2": [11.0, 2.0, 5.1],
                "sampleB_1": [1.0, 10.0, 5.2],
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
            exp_label="A",
            ctrl_label="B",
            tissue_labels="A,A,B,B",
            opath=self.output_path,
        )
        CountTableTool.main(args)

        output_df = CountTableIO.read_input_df(self.output_path)
        self.assertTrue((output_df.columns.values == np.array(["log2FC", "tstat", "pval", "padj"])).all())
        self.assertTrue(output_df.loc["geneA", "log2FC"] > 0)
        self.assertTrue(output_df.loc["geneA", "tstat"] > 0)
        self.assertTrue(np.abs(output_df.loc["geneA", "pval"]) < 0.05)
        self.assertTrue(np.abs(output_df.loc["geneA", "padj"]) < 0.05)
        self.assertTrue(output_df.loc["geneB", "log2FC"] < 0)
        self.assertTrue(output_df.loc["geneB", "tstat"] < 0)
        self.assertTrue(np.abs(output_df.loc["geneB", "pval"]) < 0.05)
        self.assertTrue(np.abs(output_df.loc["geneB", "padj"]) < 0.05)
        self.assertTrue(np.abs(output_df.loc["geneConst", "padj"]) > 0.05)

    def test_de_tstat_nan_raises(self):
        input_with_nan_path = os.path.join(self.__test_path, "input_with_nan.tsv")

        input_with_nan = self.input_df.copy()
        input_with_nan.loc["geneA", "sampleA_1"] = np.nan
        CountTableIO.write_output_df(input_with_nan, input_with_nan_path)

        args = argparse.Namespace(
            subcommand="DE",
            de_method="tstat",
            inpath=input_with_nan_path,
            exp_label="A",
            ctrl_label="B",
            tissue_labels="A,A,B,B",
            opath=self.output_path,
        )
        with self.assertRaises(ValueError):
            CountTableTool.main(args)
