import argparse
import unittest
import shutil
import os

import pandas as pd
import numpy as np

from RGTools.BedTable import BedTable3
from RGTools.GenomicElements import GenomicElements
from RGTools.ListFile import ListFile

from export import CountTableExport
from CountTableIO import CountTableIO

class ExportTest(unittest.TestCase):
    def setUp(self):
        self.__test_path = "export_test"
        if not os.path.exists(self.__test_path):
            os.makedirs(self.__test_path)

        self.__test_count_table_path = os.path.join(self.__test_path, "test_count_table.tsv")
        self.__test_region_path = os.path.join(self.__test_path, "test_region.bed3")
        self.__old_index_list_path = os.path.join(self.__test_path, "old_index_list.txt")
        self.__new_index_list_path = os.path.join(self.__test_path, "new_index_list.txt")

        test_region = pd.DataFrame({
            "chrom": ["chr1"] * 100,
            "start": np.arange(1, 10000, 100),
            "end": np.arange(100, 10100, 100),
        })

        self.test_bt = BedTable3()
        self.test_bt.load_from_dataframe(test_region)
        self.test_bt.write(self.__test_region_path)

        test_count_table = pd.DataFrame(
            index = ["{r[chrom]}:{r[start]}-{r[end]}".format(r=r) for r in self.test_bt.iter_regions()],
            data={"ascending": np.arange(100),
                  "descending": np.arange(100, 0, -1), 
                  },
        )
        self.test_count_table = test_count_table

        CountTableIO.write_output_df(test_count_table, self.__test_count_table_path)

        old_index_names = test_count_table.index.tolist()
        new_index_names = [f"renamed_{idx}" for idx in old_index_names]
        ListFile.write_list_to_file(old_index_names, self.__old_index_list_path)
        ListFile.write_list_to_file(new_index_names, self.__new_index_list_path)

    def tearDown(self):
        if os.path.exists(self.__test_path):
            shutil.rmtree(self.__test_path)
        
        super().tearDown()

    def test_main_top_percentile_ge(self):
        args = argparse.Namespace(
            subcommand="export",
            export_type="top_percentile_ge",
            inpath=self.__test_count_table_path,
            percentile=10,
            filter_by="ascending",
            region_file_path=self.__test_region_path,
            region_file_type="bed3",
            opath=os.path.join(self.__test_path, "output_ge.bed3"),
        )
        CountTableExport.main(args)
        output_ge = GenomicElements(region_file_path=args.opath,
                                    region_file_type="bed3",
                                    fasta_path=None, 
                                    )
        output_bt = output_ge.get_region_bed_table()

        self.assertTrue((output_bt.to_dataframe().values == self.test_bt.to_dataframe().iloc[-10:].values).all())

        args.filter_by = "descending"
        CountTableExport.main(args)
        output_ge = GenomicElements(region_file_path=args.opath,
                                    region_file_type="bed3",
                                    fasta_path=None, 
                                    )
        output_bt = output_ge.get_region_bed_table()
        self.assertTrue((output_bt.to_dataframe().values == self.test_bt.to_dataframe().iloc[:10].values).all())

    def test_main_name_replaced_ct(self):
        output_path = os.path.join(self.__test_path, "name_replaced_output.csv")
        args = argparse.Namespace(
            subcommand="export",
            export_type="name_replaced_ct",
            inpath=self.__test_count_table_path,
            old_index_list=self.__old_index_list_path,
            new_index_list=self.__new_index_list_path,
            opath=output_path,
        )

        CountTableExport.main(args)

        output_df = CountTableIO.read_input_df(output_path)
        
        self.assertEqual(output_df.index[12], 'renamed_' + self.test_count_table.index[12])


