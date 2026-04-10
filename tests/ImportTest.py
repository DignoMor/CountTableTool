import argparse
import os
import shutil
import unittest

import numpy as np
import pandas as pd

from CountTableTool import CountTableTool


class ImportTest(unittest.TestCase):
    def setUp(self):
        self.__test_path = "import_test"
        if not os.path.exists(self.__test_path):
            os.makedirs(self.__test_path)

        self.__rsem_a_path = os.path.join(self.__test_path, "sample_A.genes.results")
        self.__rsem_b_path = os.path.join(self.__test_path, "sample_B.genes.results")
        self.__gene_id_list_path = os.path.join(self.__test_path, "gene_ids.txt")
        self.__subset_gene_id_list_path = os.path.join(self.__test_path, "gene_ids_subset.txt")
        self.__output_path = os.path.join(self.__test_path, "output_count_table.tsv")
        self.__subset_output_path = os.path.join(self.__test_path, "output_count_table_subset.tsv")

        # Fake RSEM-like dataset following the column pattern of genes.results
        rsem_a_df = pd.DataFrame(
            {
                "gene_id": ["GENE0001", "GENE0002", "GENE0003", "GENE0004", "GENE0005", "GENE0006"],
                "transcript_id(s)": ["TX0001", "TX0002", "TX0003", "TX0004", "TX0005", "TX0006"],
                "length": [1000, 1100, 1200, 1300, 1400, 1500],
                "effective_length": [800, 900, 950, 1000, 1100, 1200],
                "expected_count": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
                "TPM": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
                "FPKM": [1.2, 2.4, 3.6, 4.8, 6.0, 7.2],
            }
        )
        rsem_b_df = pd.DataFrame(
            {
                "gene_id": ["GENE0001", "GENE0002", "GENE0003", "GENE0004", "GENE0005", "GENE0006"],
                "transcript_id(s)": ["TX0001", "TX0002", "TX0003", "TX0004", "TX0005", "TX0006"],
                "length": [1000, 1100, 1200, 1300, 1400, 1500],
                "effective_length": [800, 900, 950, 1000, 1100, 1200],
                "expected_count": [11.0, 21.0, 31.0, 41.0, 51.0, 61.0],
                "TPM": [2.1, 4.1, 6.1, 8.1, 10.1, 12.1],
                "FPKM": [1.3, 2.5, 3.7, 4.9, 6.1, 7.3],
            }
        )
        gene_id_list_df = pd.DataFrame(
            {"gene_id": ["GENE0001", "GENE0002", "GENE0003", "GENE0004", "GENE0005", "GENE0006", "GENE9999"]}
        )
        subset_gene_id_list_df = pd.DataFrame(
            {"gene_id": ["GENE0001", "GENE0002", "GENE0003", "GENE0004", "GENE0005"]}
        )

        rsem_a_df.to_csv(self.__rsem_a_path, sep="\t", index=False)
        rsem_b_df.to_csv(self.__rsem_b_path, sep="\t", index=False)
        gene_id_list_df.to_csv(self.__gene_id_list_path, sep="\t", index=False, header=False)
        subset_gene_id_list_df.to_csv(self.__subset_gene_id_list_path, sep="\t", index=False, header=False)

    def tearDown(self):
        if os.path.exists(self.__test_path):
            shutil.rmtree(self.__test_path)

    def test_import_rsem_main(self):
        args = argparse.Namespace(
            subcommand="import",
            import_type="rsem",
            sample=["sample_A", "sample_B"],
            rsem_output=[self.__rsem_a_path, self.__rsem_b_path],
            gene_id_list=self.__gene_id_list_path,
            count_type="expected_count",
            opath=self.__output_path,
        )

        CountTableTool.main(args)

        output_df = pd.read_csv(self.__output_path, index_col=0)

        self.assertTrue((output_df.index.values == np.array([
            "GENE0001",
            "GENE0002",
            "GENE0003",
            "GENE0004",
            "GENE0005",
            "GENE0006",
            "GENE9999",
        ])).all())
        self.assertTrue((output_df.columns.values == np.array(["sample_A", "sample_B"])).all())

        self.assertTrue(np.isclose(output_df.loc["GENE0001", "sample_A"], 10.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0002", "sample_A"], 20.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0003", "sample_A"], 30.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0004", "sample_A"], 40.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0005", "sample_A"], 50.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0006", "sample_A"], 60.0))

        self.assertTrue(np.isclose(output_df.loc["GENE0001", "sample_B"], 11.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0002", "sample_B"], 21.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0003", "sample_B"], 31.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0004", "sample_B"], 41.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0005", "sample_B"], 51.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0006", "sample_B"], 61.0))

        self.assertTrue(np.isnan(output_df.loc["GENE9999", "sample_A"]))
        self.assertTrue(np.isnan(output_df.loc["GENE9999", "sample_B"]))

    def test_import_rsem_main_subset_genes(self):
        args = argparse.Namespace(
            subcommand="import",
            import_type="rsem",
            sample=["sample_A", "sample_B"],
            rsem_output=[self.__rsem_a_path, self.__rsem_b_path],
            gene_id_list=self.__subset_gene_id_list_path,
            count_type="expected_count",
            opath=self.__subset_output_path,
        )

        CountTableTool.main(args)

        output_df = pd.read_csv(self.__subset_output_path, index_col=0)
        self.assertTrue((output_df.index.values == np.array([
            "GENE0001",
            "GENE0002",
            "GENE0003",
            "GENE0004",
            "GENE0005",
        ])).all())

        self.assertTrue(np.isclose(output_df.loc["GENE0001", "sample_A"], 10.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0005", "sample_A"], 50.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0001", "sample_B"], 11.0))
        self.assertTrue(np.isclose(output_df.loc["GENE0005", "sample_B"], 51.0))

        with self.assertRaises(KeyError):
            _ = output_df.loc["GENE0006"]

