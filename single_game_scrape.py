from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import re
import time
import csv
import requests

def get_nfl_game_stats(game_link):

    #Get webpage
    source = requests.get(game_link).text
    soup = BeautifulSoup(source, 'lxml')

    #Find table with all nfl stats
    table = soup.find('section', class_ = 'Card TeamStatsTable')
    stats = table.find_all('tr', class_ = 'Table__TR Table__TR--sm Table__even')
    ret_stats = {}

    #Deinfe home and away stats for each game
    for stat in stats:
        columns = stat.find_all('td', class_ = 'Table__TD')
        cat = columns[0].text
        away_stat = columns[1].text
        home_stat = columns[2].text
        ret_stats['home_' + cat] = home_stat
        ret_stats['away_' + cat] = away_stat

    #Get betting lines
    try:
        bet_table = soup.find('div', class_ = 'betting-details-with-logo')
        line = bet_table.find('div', class_ = 'n8 GameInfo__BettingItem flex-expand line').text
        line_split = line.split(" ")
        try:
            ret_stats['favorite'] = line_split[1]
            ret_stats['line'] = line_split[2]
        except Exception as e:
            ret_stats['favorite'] = None
            ret_stats['line'] = 0

        #Get over/under lines
        o_u = bet_table.find('div', class_ = 'n8 GameInfo__BettingItem flex-expand ou').text
        o_u_split = o_u.split(" ")
        ret_stats['over/under'] = o_u_split[1]

    #Return none if lines are not available
    except Exception as e:
        ret_stats['favorite'] = None
        ret_stats['line'] = None
        ret_stats['over/under'] = None

    return ret_stats
