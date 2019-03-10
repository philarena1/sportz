import glob
import pandas as pd
import os

path = r'venv/daily_lines'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = (pd.read_csv(f,index_col=False ) for f in all_files)
all_lines_df   = pd.concat(df_from_each_file, ignore_index=True,sort=False)

