from bs4 import BeautifulSoup
from tqdm import tqdm
from single_game_scrape import get_game_stats
import random
import numpy as np
import re
import time
import csv
import requests

# Open CSV file to write  webscraped data
csv_file = open('nfl_scrape_test.csv', 'w')
csv_writer = csv.writer(csv_file)

# Boolean for if labels still need to be added to the csv
labels_needed = True

start_year = 2010
end_year = 2012
# Loop through the year range specified
for y in tqdm(range(start_year, end_year + 1)):

    # Make year a string for column and for link
    year = str(y)

    #Loop through first 16 weeks of the season
    #Exclude week 17 because starters sit and such
    for i in tqdm(range(16)):
        week = str(i+1)

        # Find each game in the week
        source_link = 'https://www.espn.com/nfl/schedule/_/week/' + week + '/year/' + year + '/seasontype/2'
        source = requests.get(source_link).text
        soup = BeautifulSoup(source, 'lxml')
        games = soup.find_all('td', class_ = 'teams__col Table__TD')

        # Loop through each game 
        for j, game in enumerate(games):
            score = game.a.text
            score = score.split(' ')

            #Use try and except to get past weird situations like postponement
            try:
                home_team = score[0]
                home_score = score[1][:-1]
                away_team = score[2]
                away_score = score[3]
                game_id = game.a['href'].split('=')[1]
            except Exception as e:
                continue

            game_link = 'https://www.espn.com/nfl/matchup/_/gameId/' + game_id

            # Call game stats function on each game link
            try:
                game_stats = get_nfl_game_stats(game_link)
            except Exception as e:
                continue

            # Write labels on first iteration
            if labels_needed:
                statistic_list = list(game_stats.keys())
                labels_list = ['year', 'week', 'home_team', 'home_score', 'away_team', 'away_score', 'game_id']
                labels_list.extend(statistic_list)
                csv_writer.writerow(labels_list)
                labels_needed=False
            
            # Add random wait time to prevent too many hits to website
            if random.choice([True, False]):
                wait_time = np.random.uniform(0.3,0.6)
                time.sleep(wait_time)

            #Store and write stats
            write_stats = [year, week, home_team, home_score, away_team, away_score, game_id]
            write_stats.extend(list(game_stats.values()))
            csv_writer.writerow(write_stats)
    
