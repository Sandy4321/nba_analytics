#!/usr/bin/python                                                                                                                            
import requests
import pandas as pd
from os import path

DATA_DIR = '/Users/tdliu/nba_analytics/data'
SEASON = '2013-14'
SHOT_LOGS_FILENAME = 'shot_logs.csv'
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
        self.season = season
        self.player_bio_df = pd.DataFrame(raw_player_data, columns = headers)
        player_ids_df = self.player_bio_df[['PLAYER_ID', 'PLAYER_NAME']]
        self.player_ids = player_ids_df.set_index('PLAYER_ID').to_dict()['PLAYER_NAME']
        
    # This function returns shot log given a player_id as a data frame
    def get_player_shot_log(self, player_id):
        shot_log_url = 'http://stats.nba.com/stats/playerdashptshotlog?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID='+ str(player_id) +'&Season=' + self.season + '&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision='
        response = requests.get(shot_log_url)
        raw_shot_log = response.json()['resultSets'][0]['rowSet']
        if not raw_shot_log:
            print "No data available for " + self.player_ids[player_id]
            return None
        headers = response.json()['resultSets'][0]['headers']
        headers = [x.encode('latin-1') for x in headers]
        shot_log_df = pd.DataFrame(raw_shot_log, columns = headers)
        shot_log_df.insert(0, "PLAYER_NAME", self.player_ids[player_id])
        shot_log_df.insert(0, "PLAYER_ID", player_id)
        shot_log_df.sort(["GAME_ID", "SHOT_NUMBER"], ascending = [1,1], inplace=True)
        return shot_log_df

    def get_player_shot_chart(self, player_id):
        shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=' + season + '&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=' + str(player_id) +'&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'
        response = requests.get(shot_chart_url)
        raw_shot_chart = response.json()['resultSets'][0]['rowSet']
        headers = response.json()['resultSets'][0]['headers']
        shot_chart_df = pd.DataFrame(raw_shot_chart, columns = headers)
        shot_chart_df.sort(["GAME_ID", "PERIOD", "MINUTES_REMAINING", "SECONDS_REMAINING"], ascending = [1,1,0,0], inplace=True)
        return shot_chart_df

# This function takes in PlayerTracking object and returns a data frame with shot logs for all players    
def get_all_player_shot_logs(player_tracking):
    player_ids = player_tracking.player_ids
    frames = []
    for player_id in player_ids:
        player_shot_log = player_tracking.get_player_shot_log(player_id)
        if player_shot_log is None:
            continue
        frames.append(player_shot_log)
    return pd.concat(frames)
        
def main():
    player_tracking = PlayerTracking(SEASON)
    shot_logs_df = get_all_player_shot_logs(player_tracking)
    shot_logs_df.to_csv(path.join(DATA_DIR, '_'.join([SEASON, SHOT_LOGS_FILENAME])), index = False)

if __name__ == "__main__": main()
