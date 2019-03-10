import glob
import pandas as pd
import os

# get all csv files in folders
path = r'venv/daily_lines'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

# read all csv and make 1 df
df_from_each_file = (pd.read_csv(f,index_col=False ) for f in all_files)
all_lines_df = pd.concat(df_from_each_file, ignore_index=True,sort=False)

# get date from file name
all_lines_df['day'] = all_lines_df.file_name.str.split("_").str[2]