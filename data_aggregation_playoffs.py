import numpy as np
import pandas as pd
from event_filter import playoffs


# pull in all Clean play by play files
files = ['data/2013_2014out.csv', 'data/2014_2015out.csv', 'data/2015_2016out.csv', 'data/2016_2017out.csv','data/2017_2018out.csv']
season = 2014
# Read in the csv after it has run through the clean script in a loop
for file in files:
    df = pd.read_csv(file)
# filter so only playoff  games are present, we will do a seperate but similar model for playoffsplayDf = playular_season(df)
    playDf = playoffs(df)

# drop columns that are not needed for team aggrigations
    playDf.drop(['Description', 'Time_Elapsed',
            'Seconds_Elapsed', 'Strength', 'Ev_Zone', 'Type',
            'Home_Zone', 'p1_name', 'p1_ID', 'p2_name',
            'p2_ID', 'p3_name', 'p3_ID', 'awayPlayer1', 'awayPlayer1_id',
            'awayPlayer2', 'awayPlayer2_id', 'awayPlayer3', 'awayPlayer3_id',
            'awayPlayer4', 'awayPlayer4_id', 'awayPlayer5', 'awayPlayer5_id',
            'awayPlayer6', 'awayPlayer6_id', 'homePlayer1', 'homePlayer1_id',
            'homePlayer2', 'homePlayer2_id', 'homePlayer3', 'homePlayer3_id',
            'homePlayer4', 'homePlayer4_id', 'homePlayer5', 'homePlayer5_id',
            'homePlayer6', 'homePlayer6_id', 'Away_Players', 'Home_Players', 'Away_Goalie', 'Away_Goalie_Id',
            'Home_Goalie',
            'Home_Goalie_Id', 'xC', 'yC', 'Home_Coach', 'Away_Coach'], axis=1, inplace=True)
# create filters to reduce the amount of rows you have to compute on.
    playDfShotAtt = playDf[playDf.Event.isin(['SHOT', 'GOAL', 'MISS', 'BLOCK'])]
    playDfMiss = playDf[playDf.Event.isin(['MISS'])]
    playDfSOG = playDf[playDf.Event.isin(['SHOT', 'GOAL'])]
# This one will create a off row df from the others, so we will merge this back in last
    playDfGoal = playDf[playDf.Event.isin(['GOAL'])]
    playDfHit = playDf[playDf.Event.isin(['HIT'])]
    playDfBlock = playDf[playDf.Event.isin(['BLOCK'])]
# set a MultiIndex to start your filtering
    playDf.set_index(['Game_Id', 'Ev_Team'], inplace=True)
# Aggregations by game, and a concatonate at the end
    playDfShotAtt = (playDfShotAtt.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfShotAtt.rename(columns={'Event': 'Shot_Att'}, inplace=True)
    playDfSOG = (playDfSOG.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfSOG.rename(columns={'Event': 'SOG_for'}, inplace=True)
    playDfHit = (playDfHit.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfHit.rename(columns={'Event': 'Hits_for'}, inplace=True)
    playDfGoal = (playDfGoal.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfGoal.rename(columns={'Event': 'Goals_for'}, inplace=True)
    playDfblocks = (playDfBlock.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfblocks.rename(columns={'Event': 'Blocks_A'}, inplace=True)
    playDfMiss = (playDfMiss.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    playDfMiss.rename(columns={'Event': 'Misses'}, inplace=True)
    playDfO = pd.concat([playDfShotAtt, playDfMiss['Misses'], playDfSOG['SOG_for'], playDfHit['Hits_for'], playDfblocks['Blocks_A']], axis=1)
# at this point we need the 'Against' metrics which are really the opposite of the calculations we have already made, so we make a loop to do that.
# this is very repetiative and there may be a better way about it, but this is what I came up with
    games_list = list(playDfO.Game_Id.unique())

    playDfO['Blocks_for'] = 0
    j = 1
    for i in range(len(games_list)):
           playDfO['Blocks_for'][i * 2] = playDfO['Blocks_A'][i + j]
           playDfO['Blocks_for'][i + j] = playDfO['Blocks_A'][i * 2]
           j = j + 1

    playDfO['Shot_Att_A'] = 0
    j = 1
    for i in range(len(games_list)):
           playDfO['Shot_Att_A'][i * 2] = playDfO['Shot_Att'][i + j]
           playDfO['Shot_Att_A'][i + j] = playDfO['Shot_Att'][i * 2]
           j = j + 1

    playDfO['SOG_A'] = 0
    j = 1
    for i in range(len(games_list)):
           playDfO['SOG_A'][i * 2] = playDfO['SOG_for'][i + j]
           playDfO['SOG_A'][i + j] = playDfO['SOG_for'][i * 2]
           j = j + 1

    playDfO['Hits_A'] = 0
    j = 1
    for i in range(len(games_list)):
           playDfO['Hits_A'][i * 2] = playDfO['Hits_for'][i + j]
           playDfO['Hits_A'][i + j] = playDfO['Hits_for'][i * 2]
           j = j + 1

# Now merge in the Goals_For column
    playDfcomplete = playDfO.merge(right=playDfGoal, left_on=['Game_Id', 'Ev_Team'], right_on=['Game_Id', 'Ev_Team'],
                                    how='left')
# and fill in the NaN values with 0
    playDfcomplete.fillna(0, inplace=True)

# one more loop to bring in Goals_A
    playDfcomplete['Goals_A'] = 0
    j = 1
    for i in range(len(games_list)):
           playDfcomplete['Goals_A'][i * 2] = playDfcomplete['Goals_for'][i + j]
           playDfcomplete['Goals_A'][i + j] = playDfcomplete['Goals_for'][i * 2]
           j = j + 1

# now we can calculate Saves

    playDfcomplete['Saves'] = playDfcomplete['SOG_A'] - playDfcomplete['Goals_A']
# add in stats and fancy stats
    playDfcomplete['Shot_Percentage_for'] = round((playDfcomplete['Goals_for'] / playDfcomplete['SOG_for']) * 100, 2)
    playDfcomplete['Fenwick_for'] = playDfcomplete['SOG_for'] + playDfcomplete['Misses']
    playDfcomplete['Corsi_for'] = playDfcomplete['Shot_Att']
    playDfcomplete['Corsi_A'] = playDfcomplete['Shot_Att_A']
    playDfcomplete['Fenwick_A'] = playDfcomplete['Shot_Att_A'] - playDfcomplete['Blocks_for']
    playDfcomplete['FSH%'] = round((playDfcomplete['Goals_for'] / playDfcomplete['Fenwick_for']) * 100, 2)
    playDfcomplete['Miss%'] = round((playDfcomplete['Misses'] / playDfcomplete['Fenwick_for']) * 100, 2)
    playDfcomplete['wshF'] = round(
        (playDfcomplete['Goals_for'] + (0.2 * (playDfcomplete['Corsi_for'] - playDfcomplete['Goals_for']))), 2)
    playDfcomplete['wshA'] = round(
        (playDfcomplete['Goals_A'] + (0.2 * (playDfcomplete['Corsi_A'] - playDfcomplete['Goals_A']))), 2)
    playDfcomplete['Goals_for%'] = round(
        (playDfcomplete['Goals_for'] / (playDfcomplete['Goals_for'] + playDfcomplete['Goals_A'])) * 100, 2)
    playDfcomplete['Fenwick_for%'] = round(
        (playDfcomplete['Fenwick_for'] / (playDfcomplete['Fenwick_for'] + playDfcomplete['Fenwick_A'])) * 100, 2)
    playDfcomplete['Corsi_for%'] = round(
        (playDfcomplete['Corsi_for'] / (playDfcomplete['Corsi_for'] + playDfcomplete['Corsi_A'])) * 100, 2)
    playDfcomplete['wshF%'] = round((playDfcomplete['wshF'] / (playDfcomplete['wshF'] + playDfcomplete['wshA'])) * 100, 2)
    playDfcomplete['Sv%'] = round((playDfcomplete['Saves'] / playDfcomplete['SOG_A']) * 100, 2)

    # and finally to calculate wins. I am going to count ties as a win for now since both teams get a standings point. if it negativly affects the model I'll adjust
    playDfcomplete['Win'] = np.where(np.logical_or(playDfcomplete['Goals_for'] > playDfcomplete['Goals_A'],
                                                  playDfcomplete['Goals_for'] == playDfcomplete['Goals_A']), 1, 0)
# Add a Season column just for reference
    playDfcomplete['Season'] = season
# write the new df out to csv
    playDfcomplete.to_csv('data/' + str(season) + 'agg_playoffs.csv')
    season = season + 1
