#!/usr/bin/python                                                                                                                            
import requests
import pandas as pd

''' 
init function takes in season as a string, e.g. "2014-15"
self.player_bio_df is a dataframe of stats from the Player Bio page
self.player_ids is a dictionary with keys as Player Names and values as Player IDs
'''
class PlayerTracking(object):
    def __init__(self, season):
        player_bio_url = 'http://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=' + season + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
        response = requests.get(player_bio_url)
        raw_player_data = response.json()['resultSets'][0]['rowSet']
        headers = response.json()['resultSets'][0]['headers']
        headers = [x.encode('latin-1') for x in headers]
        self.player_bio_df = pd.DataFrame(raw_player_data, columns = headers)
        player_ids_df = self.player_bio_df[['PLAYER_ID', 'PLAYER_NAME']]
        self.player_ids = player_ids_df.set_index('PLAYER_ID').to_dict()['PLAYER_NAME']
        
    # This function returns shot log given a player_id as a data frame
    def get_player_shot_log(self, player_id):
        shot_log_url = 'http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID='+ str(player_id) +'&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='
        response = requests.get(shot_log_url)
        raw_shot_log = response.json()['resultSets'][0]['rowSet']
        headers = response.json()['resultSets'][0]['headers']
        headers = [x.encode('latin-1') for x in headers]
        shot_log_df = pd.DataFrame(raw_shot_log, columns = headers)
        shot_log_df.insert(0, "PLAYER_NAME", self.player_ids[player_id])
        shot_log_df.insert(0, "PLAYER_ID", player_id)
        return shot_log_df
    

