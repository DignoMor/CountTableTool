
import pandas as pd

class CountTableIO:
    @staticmethod
    def read_input_df(input_path):
        return pd.read_csv(input_path, 
                           index_col=0, 
                           )

    @staticmethod
    def read_region_info_df(region_info_path):
        return pd.read_csv(region_info_path, 
                           index_col=0, 
                           )

    @staticmethod
    def write_output_df(output_df, opath):
        if opath == "stdout":
            output_df.to_csv(sys.stdout)
        else:
            output_df.to_csv(opath)