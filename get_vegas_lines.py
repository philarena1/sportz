#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 11:49:30 2019

@author: philiparena
"""
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta
import datetime
from time import sleep
from tqdm import tqdm

def get_lines(day):
    day = day
    url = "http://www.vegasinsider.com/mlb/matchups/matchups.cfm/date/" + day
    page = requests.get(url)
    # page.text
    soup = BeautifulSoup(page.text, 'html.parser')

    ls = []
    for x in soup.findAll(class_='viBodyBorderNorm'):
        for row in x.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 12:
                ls.append(cells)

    game_info = {}
    i = 0
    for x in soup.findAll(class_='viBodyBorderNorm'):
        for row in x.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 12:
                ls = []
                for result in cells:
                    result = result.text
                    # print(result)
                    ls.append(result)
                game_info[i] = ls
                i = i + 1

    team_info = {}
    i = 0
    x = 0
    while i < len(game_info):

        if game_info[i][0] == 'Teams':
            pass
        else:
            game_day_info = {}
            team = game_info[i][0]
            pitcher = game_info[i][1]
            win_loss = game_info[i][2]
            streak = game_info[i][3]
            ML = game_info[i][4]
            O_U = game_info[i][5]
            ML_2 = game_info[i][6]
            O_U_2 = game_info[i][7]
            run = game_info[i][8]
            money = game_info[i][9]
            O_U_3 = game_info[i][10]
            ATS = game_info[i][11]

            team = ''.join([i for i in team if not i.isdigit()])
            game_day_info['team'] = team.strip()
            game_day_info['pitcher'] = pitcher.strip()
            game_day_info['win_loss'] = win_loss.strip()
            game_day_info['streak'] = streak.strip()
            game_day_info['ML'] = ML.strip()
            game_day_info['O_U'] = O_U.strip()
            game_day_info['ML_2'] = ML_2.strip()
            game_day_info['O_U_2'] = O_U_2.strip()
            game_day_info['run'] = run.strip()
            game_day_info['money'] = money.strip()
            game_day_info['O_U_3'] = O_U_3.strip()
            game_day_info['ATS'] = ATS.strip()

            team_info[x] = game_day_info
            x = x + 1
        i = i + 1
    return team_info

def write_record_csv(file_name, data):
    with open(file_name+'.csv','w') as file:
        # headers
        file.write('team,pitcher,win_loss,streak,ML,O_U,ML_2,O_U_2,run,money,O_U_3,ATS')
        file.write('\n')
        for row in data:
            record = str(data[row]['team'] + "," + \
                         data[row]['pitcher']  + "," + \
                         data[row]['win_loss'] + "," + \
                         data[row]['streak'] + "," + \
                         data[row]['ML'] + "," + \
                         data[row]['O_U'] + "," + \
                         data[row]['ML_2'] + "," + \
                         data[row]['O_U_2'] + "," + \
                         data[row]['run'] + "," + \
                         data[row]['money'] + "," + \
                         data[row]['O_U_3'] + "," + \
                         data[row]['ATS'])
            file.write(record)
            file.write('\n')



def get_list_dates_in_range(start, end):
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    delta = end_date - start_date
    list_of_days = []
    for i in range(delta.days + 1):
        list_of_days.append(start_date + timedelta(i))
    return list_of_days








#day = '03-06-19'
#lines = get_lines(day)
#files = folder_name+'/lines_'+day
#write_record_csv(file_name= files,data= lines)



def main():
    # keep files organized- if 'daily_lines' does not exist, create it
    import os
    folder_name = 'daily_lines'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    days = get_list_dates_in_range('2019-03-07','2019-03-10')
    for day in tqdm(days):
        day = day.strftime('%m-%d-%Y')
        lines = get_lines(day)
        files = folder_name + '/lines_' + day
        write_record_csv(file_name=files, data=lines)
        sleep(5)


if __name__ == main():
    main()