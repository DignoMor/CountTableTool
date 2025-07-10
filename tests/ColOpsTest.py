
import argparse
import unittest
import shutil
import os

import pandas as pd
import numpy as np

from col_ops import ColOps
from CountTableIO import CountTableIO

class ColOpsTest(unittest.TestCase):
    def setUp(self):
        self.__test_path = "col_ops_test"

        if not os.path.exists(self.__test_path):
            os.makedirs(self.__test_path)

        self.input_df_path_1 = os.path.join(self.__test_path, "input_df_1.tsv")
        self.input_df_path_2 = os.path.join(self.__test_path, "input_df_2.tsv")

        self.input_df_1 = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9],
        })

        self.input_df_2 = pd.DataFrame({
            "D": [1, 2, 3],
            "E": [4, 5, 6],
            "F": [7, 8, 9],
        })

        CountTableIO.write_output_df(self.input_df_1, self.input_df_path_1)
        CountTableIO.write_output_df(self.input_df_2, self.input_df_path_2)

    def test_concat(self):
        args = argparse.Namespace(
            subcommand="col_ops",
            operation="concat",
            inpaths=[self.input_df_path_1, self.input_df_path_2],
            opath=os.path.join(self.__test_path, "output_df_concat.tsv"),
        )
        ColOps.main(args)

        output_df = CountTableIO.read_input_df(args.opath)
        self.assertTrue((output_df.columns == np.array(["A", "B", "C", "D", "E", "F"])).all())

    def test_filter(self):
        args = argparse.Namespace(
            subcommand="col_ops",
            operation="filter",
            inpath=self.input_df_path_1,
            col=["A", "B"],
            opath=os.path.join(self.__test_path, "output_df_filter.tsv"),
        )
        ColOps.main(args)

        output_df = CountTableIO.read_input_df(args.opath)
        self.assertTrue((output_df.columns == np.array(["A", "B"])).all())

    def tearDown(self):
        if os.path.exists(self.__test_path):
            shutil.rmtree(self.__test_path)

