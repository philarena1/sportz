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

# did they win

all_lines_df['win'] = all_lines_df.team.str.contains('«',regex=True)

# get team abbreviation
def getTeamName(s):
    if bool(re.search('Arizona', s, re.IGNORECASE)) == True:
        return 'ARI'
    elif bool(re.search('Atlanta', s, re.IGNORECASE)) == True:
        return 'ATL'
    elif bool(re.search('Baltimore', s, re.IGNORECASE)) == True:
        return 'BAL'
    elif bool(re.search('Boston', s, re.IGNORECASE)) == True:
        return 'BOS'
    elif bool(re.search('Chi. Cubs', s, re.IGNORECASE)) == True:
        return 'CHC'
    elif bool(re.search('Chi. White Sox', s, re.IGNORECASE)) == True:
        return 'CWS'
    elif bool(re.search('Cincinnati', s, re.IGNORECASE)) == True:
        return 'CIN'
    elif bool(re.search('Cleveland', s, re.IGNORECASE)) == True:
        return 'CLE'
    elif bool(re.search('Colorado', s, re.IGNORECASE)) == True:
        return 'COL'
    elif bool(re.search('Detroit', s, re.IGNORECASE)) == True:
        return 'DET'
    elif bool(re.search('Houston', s, re.IGNORECASE)) == True:
        return 'HOU'
    elif bool(re.search('Kansas City', s, re.IGNORECASE)) == True:
        return 'KC'
    elif bool(re.search('L.A. Angels', s, re.IGNORECASE)) == True:
        return 'LAA'
    elif bool(re.search('L.A. Dodgers', s, re.IGNORECASE)) == True:
        return 'LAD'
    elif bool(re.search('Miami', s, re.IGNORECASE)) == True:
        return 'MIA'
    elif bool(re.search('Milwaukee', s, re.IGNORECASE)) == True:
        return 'MIL'
    elif bool(re.search('Minnesota', s, re.IGNORECASE)) == True:
        return 'MIN'
    elif bool(re.search('N.Y. Mets', s, re.IGNORECASE)) == True:
        return 'NYM'
    elif bool(re.search('N.Y. Yankees', s, re.IGNORECASE)) == True:
        return 'NYY'
    elif bool(re.search('Oakland', s, re.IGNORECASE)) == True:
        return 'OAK'
    elif bool(re.search('Philadelphia', s, re.IGNORECASE)) == True:
        return 'PHI'
    elif bool(re.search('Pittsburgh', s, re.IGNORECASE)) == True:
        return 'PIT'
    elif bool(re.search('San Diego', s, re.IGNORECASE)) == True:
        return 'SD'
    elif bool(re.search('San Francisco', s, re.IGNORECASE)) == True:
        return 'SF'
    elif bool(re.search('Seattle', s, re.IGNORECASE)) == True:
        return 'SEA'
    elif bool(re.search('St. Louis', s, re.IGNORECASE)) == True:
        return 'STL'
    elif bool(re.search('Tampa Bay', s, re.IGNORECASE)) == True:
        return 'TB'
    elif bool(re.search('Texas', s, re.IGNORECASE)) == True:
        return 'TEX'
    elif bool(re.search('Toronto', s, re.IGNORECASE)) == True:
        return 'TOR'
    elif bool(re.search('Washington', s, re.IGNORECASE)) == True:
        return 'WSH'

    return ''


all_lines_df['team_name'] = all_lines_df.team.apply(getTeamName)