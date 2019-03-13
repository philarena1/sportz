import glob
import pandas as pd
import os
from datetime import datetime
import re

# get all csv files in folders
path = r'venv/daily_lines'                     # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

# read all csv and make 1 df
df_from_each_file = (pd.read_csv(f,index_col=False ) for f in all_files)
all_lines_df = pd.concat(df_from_each_file, ignore_index=True,sort=False)

def process_data(all_lines_df):
    # get date from file name
    all_lines_df['day'] = all_lines_df.file_name.str.split("_").str[2]

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

    # get pitcher arm
    def getPitcher(s):
        if bool(re.search('(R)', s, re.IGNORECASE)) == True:
            return 'right'
        elif bool(re.search('(L)', s, re.IGNORECASE)) == True:
            return 'left'

        return ''

    def getWeekday(day):
        day = datetime.strptime(day,'%m-%d-%Y')
        weekday = day.weekday()
        return weekday

    def remove_sign(s):
        s = str(s)
        num = s.rstrip("%")
        return num

    # get streak type
    def getStreakType(s):
        if bool(re.search('L', s, re.IGNORECASE)) == True:
            return 'lose'
        elif bool(re.search('W', s, re.IGNORECASE)) == True:
            return 'win'
        return ''

    def get_num(s):
        try:
            streak_num = re.search(r'\d+', s).group()
        except:
            streak_num = 0
        return streak_num

    def winner(s):
        if s == True:
            game = 'winner'
        else:
            game = 'loser'
        return game

    def to_num(s):
        if s.isdigit():
            run = int(s)
        else:
            run = 0
        return run

    all_lines_df['team_name'] = all_lines_df.team.apply(getTeamName)
    all_lines_df['pitcher_arm'] = all_lines_df.pitcher.apply(getPitcher)
    all_lines_df['day_of_week'] = all_lines_df.day.apply(getWeekday)
    all_lines_df['run'] = all_lines_df.run.apply(remove_sign)
    all_lines_df['money'] = all_lines_df.money.apply(remove_sign)
    all_lines_df['O_U_3'] = all_lines_df.O_U_3.apply(remove_sign)
    all_lines_df['streak_type'] = all_lines_df.streak.apply(getStreakType)
    all_lines_df['streak_num'] = all_lines_df.streak.apply(get_num)

    all_lines_df['line_change_perc'] = (all_lines_df['ML_2'] - all_lines_df['ML'] )/ all_lines_df['ML']

    all_lines_df['run'] = all_lines_df.run.apply(to_num)
    all_lines_df['money'] = all_lines_df.money.apply(to_num)
    all_lines_df['O_U_3'] = all_lines_df.O_U_3.apply(to_num)

    # did they win
    all_lines_df['win'] = all_lines_df.team.str.contains('«',regex=True)
    all_lines_df['win'] = all_lines_df.win.apply(winner)


    return all_lines_df


def format_for_model(test_df):
    # dummy variable for teams
    team_dummy = pd.get_dummies(test_df.team_name,prefix=['team_name'], drop_first=True).iloc[:, 1:]
    df = pd.concat([test_df, team_dummy], axis=1)
    df = df.drop('team_name', 1)

    # dummy for pitcher_arm
    pitcher_arm_dummy = pd.get_dummies(test_df.pitcher_arm,prefix=['pitcher_arm'], drop_first=True).iloc[:, 1:]
    df = pd.concat([df, pitcher_arm_dummy], axis=1)
    df = df.drop('pitcher_arm', 1)

    # dummy for streak
    win_streak_dummy = pd.get_dummies(test_df.streak_type,prefix=['streak_type'], drop_first=True).iloc[:, 1:]
    df = pd.concat([df, win_streak_dummy], axis=1)
    df = df.drop('streak_type', 1)

    # dummy for predictor- winning
    win_dummy = pd.get_dummies(test_df.win, drop_first=True)
    df = pd.concat([df, win_dummy], axis=1)
    df = df.drop('win', 1)

    # delete unnecessary
    columns = ['team','pitcher','win_loss','streak','ATS','file_name','day','day_of_week']
    df.drop(columns, inplace=True, axis=1)

    df = df.fillna(0)
    cols_to_norm = ['ML', 'O_U', 'ML_2', 'O_U_2', 'run', 'money', 'O_U_3']
    df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    return df


test_df = process_data(all_lines_df)

model_df = format_for_model(test_df)


# normalize columns

#cols_to_norm = ['ML','O_U','ML_2','O_U_2','run','money','O_U_3']
#model_df[cols_to_norm] = model_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))


#### Logistic regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# separate x and y
X = model_df.drop('winner',1)
y = model_df['winner']
y = y.astype('int')

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.09,random_state = 42)

logreg = LogisticRegression()
logreg.fit(X_train,y_train)
score = logreg.score(X_train, y_train)
score2 = logreg.score(X_test,y_test)

print('Training set accurate %s' % (score))
print('test set accurate %s' % (score2))



#######  neural net
# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Part 2 - Now let's make the ANN!

# Importing the Keras libraries and packages
import keras
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 45, kernel_initializer = 'uniform', activation = 'relu', input_dim = 40))

# Adding the second hidden layer
classifier.add(Dense(units = 45, kernel_initializer = 'uniform', activation = 'relu'))

# Adding the second hidden layer
classifier.add(Dense(units = 45, kernel_initializer = 'uniform', activation = 'relu'))


# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(X_train, y_train, batch_size = 32, epochs = 1500)

# Part 3 - Making predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.45) # choose %, or maybe compare to actual implied odd

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)



# run entire original df through model

X_df = sc.fit_transform(X)
y_df = classifier.predict(X_df)
y_df = (y_df > 0.50)
cm = confusion_matrix(y, y_df)

df_pred = pd.DataFrame(y_df, columns=['prediction'])
model_df_pred = model_df.join(df_pred)

test_df_pred = test_df.join(df_pred)



## predict
f = 'venv/lines_03-12-2019.csv'
df_predict = pd.read_csv(f, index_col=False )

num_predict = len(df_predict)
df_with_total = test_df.append(df_predict) # need all values for dummy

process_predict = process_data(df_with_total)
predict_df = format_for_model(process_predict)

predict_df = predict_df.tail(num_predict)

X = predict_df.drop('winner',1)
y = model_df['winner']
y = y.astype('int')

X_df = sc.fit_transform(X)
y_df = classifier.predict(X_df)

predict_output = pd.DataFrame(y_df, columns=['win_likelihood'])

df_predict_with_predictions = df_predict.join(predict_output)