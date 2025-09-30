
import unittest
import argparse
import shutil
import os

import pandas as pd
import numpy as np

from normalization import Normalization
from CountTableIO import CountTableIO

class NormalizationTest(unittest.TestCase):
    def setUp(self):
        self.__test_path = "normalization_test"
        if not os.path.exists(self.__test_path):
            os.makedirs(self.__test_path)

        self.__test_count_table_path = os.path.join(self.__test_path, "test_count_table.tsv")
        
        self.test_count_table = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [4, 5, 6],
            "C": [7, 8, 9],
        })

        CountTableIO.write_output_df(self.test_count_table, self.__test_count_table_path)

    def tearDown(self):
        if os.path.exists(self.__test_path):
            shutil.rmtree(self.__test_path)

    def test_per_million_normalization(self):
        args = argparse.Namespace(
            subcommand="normalization",
            normalization_type="per_million",
            inpath=self.__test_count_table_path,
            opath=os.path.join(self.__test_path, "test_per_million_normalization.tsv"),
        )
        Normalization.main(args)

        output_df = CountTableIO.read_input_df(args.opath)
        self.assertTrue((output_df.sum(axis=0).values == np.array([1000000, 1000000, 1000000])).all())
