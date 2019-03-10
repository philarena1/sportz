#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 11:49:30 2019

@author: philiparena
"""
import requests
from bs4 import BeautifulSoup

def get_lines(day):
    day = day
    url = "http://www.vegasinsider.com/mlb/matchups/matchups.cfm/date/" + day
    page = requests.get(url)
    page.text
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

t = get_lines('09-17-18')