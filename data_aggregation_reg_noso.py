import pandas as pd

import numpy as np


from event_filter import regular_season, remove_shootouts


# pull in all Clean play by play files
files = ['data/2013_2014out.csv', 'data/2014_2015out.csv', 'data/2015_2016out.csv', 'data/2016_2017out.csv','data/2017_2018out.csv','data/2018_2019out.csv']
season = 2014
# Read in the csv after it has run through the clean script in a loop
for file in files:
    df = pd.read_csv(file)
# filter so only regular season games are present, we will do a seperate but similar model for playoffsregDf = regular_season(df)
    regDf = regular_season(df)
# filter out shootouts but we may revisit this to see if it affects the model's accuracy
    regDf = remove_shootouts(regDf)
    regDf2 = regDf
# drop columns that are not needed for team aggrigations
    regDf.drop(['Description', 'Time_Elapsed',
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
    regDfShotAtt = regDf[regDf.Event.isin(['SHOT', 'GOAL', 'MISS', 'BLOCK'])]
    regDfMiss = regDf[regDf.Event.isin(['MISS'])]
    regDfSOG = regDf[regDf.Event.isin(['SHOT', 'GOAL'])]
# This one will create a off row df from the others, so we will merge this back in last
    regDfGoal = regDf[regDf.Event.isin(['GOAL'])]
    regDfHit = regDf[regDf.Event.isin(['HIT'])]
    regDfBlock = regDf[regDf.Event.isin(['BLOCK'])]
# set a MultiIndex to start your filtering
    regDf.set_index(['Game_Id', 'Ev_Team'], inplace=True)
# Aggregations by game, and a concatonate at the end
    regDfShotAtt = (regDfShotAtt.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfShotAtt.rename(columns={'Event': 'Shot_Att'}, inplace=True)
    regDfSOG = (regDfSOG.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfSOG.rename(columns={'Event': 'SOG_for'}, inplace=True)
    regDfHit = (regDfHit.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfHit.rename(columns={'Event': 'Hits_for'}, inplace=True)
    regDfGoal = (regDfGoal.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfGoal.rename(columns={'Event': 'Goals_for'}, inplace=True)
    regDfblocks = (regDfBlock.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfblocks.rename(columns={'Event': 'Blocks_A'}, inplace=True)
    regDfMiss = (regDfMiss.groupby(['Game_Id', 'Ev_Team'])['Event'].size().reset_index())
    regDfMiss.rename(columns={'Event': 'Misses'}, inplace=True)
    regDfO = pd.concat([regDfShotAtt, regDfMiss['Misses'], regDfSOG['SOG_for'], regDfHit['Hits_for'], regDfblocks['Blocks_A']], axis=1)
# at this point we need the 'Against' metrics which are really the opposite of the calculations we have already made, so we make a loop to do that.
# this is very repetiative and there may be a better way about it, but this is what I came up with
    games_list = list(regDfO.Game_Id.unique())

    regDfO['Blocks_for'] = 0
    j = 1
    for i in range(len(games_list)):
           regDfO['Blocks_for'][i * 2] = regDfO['Blocks_A'][i + j]
           regDfO['Blocks_for'][i + j] = regDfO['Blocks_A'][i * 2]
           j = j + 1

    regDfO['Shot_Att_A'] = 0
    j = 1
    for i in range(len(games_list)):
           regDfO['Shot_Att_A'][i * 2] = regDfO['Shot_Att'][i + j]
           regDfO['Shot_Att_A'][i + j] = regDfO['Shot_Att'][i * 2]
           j = j + 1

    regDfO['SOG_A'] = 0
    j = 1
    for i in range(len(games_list)):
           regDfO['SOG_A'][i * 2] = regDfO['SOG_for'][i + j]
           regDfO['SOG_A'][i + j] = regDfO['SOG_for'][i * 2]
           j = j + 1

    regDfO['Hits_A'] = 0
    j = 1
    for i in range(len(games_list)):
           regDfO['Hits_A'][i * 2] = regDfO['Hits_for'][i + j]
           regDfO['Hits_A'][i + j] = regDfO['Hits_for'][i * 2]
           j = j + 1

# Now merge in the Goals_For column
    regDfcomplete = regDfO.merge(right=regDfGoal, left_on=['Game_Id', 'Ev_Team'], right_on=['Game_Id', 'Ev_Team'],
                                    how='left')
# and fill in the NaN values with 0
    regDfcomplete.fillna(0, inplace=True)

# one more loop to bring in Goals_A
    regDfcomplete['Goals_A'] = 0
    j = 1
    for i in range(len(games_list)):
           regDfcomplete['Goals_A'][i * 2] = regDfcomplete['Goals_for'][i + j]
           regDfcomplete['Goals_A'][i + j] = regDfcomplete['Goals_for'][i * 2]
           j = j + 1

# now we can calculate Saves

    regDfcomplete['Saves'] = regDfcomplete['SOG_A'] - regDfcomplete['Goals_A']
# add in stats and fancy stats
    regDfcomplete['Shot_Percentage_for'] = round((regDfcomplete['Goals_for'] / regDfcomplete['SOG_for']) * 100, 2)
    regDfcomplete['Fenwick_for'] = regDfcomplete['SOG_for'] + regDfcomplete['Misses']
    regDfcomplete['Corsi_for'] = regDfcomplete['Shot_Att']
    regDfcomplete['Corsi_A'] = regDfcomplete['Shot_Att_A']
    regDfcomplete['Fenwick_A'] = regDfcomplete['Shot_Att_A'] - regDfcomplete['Blocks_for']
    regDfcomplete['FSH%'] = round((regDfcomplete['Goals_for'] / regDfcomplete['Fenwick_for']) * 100, 2)
    regDfcomplete['Miss%'] = round((regDfcomplete['Misses'] / regDfcomplete['Fenwick_for']) * 100, 2)
    regDfcomplete['wshF'] = round(
        (regDfcomplete['Goals_for'] + (0.2 * (regDfcomplete['Corsi_for'] - regDfcomplete['Goals_for']))), 2)
    regDfcomplete['wshA'] = round(
        (regDfcomplete['Goals_A'] + (0.2 * (regDfcomplete['Corsi_A'] - regDfcomplete['Goals_A']))), 2)
    regDfcomplete['Goals_for%'] = round(
        (regDfcomplete['Goals_for'] / (regDfcomplete['Goals_for'] + regDfcomplete['Goals_A'])) * 100, 2)
    regDfcomplete['Fenwick_for%'] = round(
        (regDfcomplete['Fenwick_for'] / (regDfcomplete['Fenwick_for'] + regDfcomplete['Fenwick_A'])) * 100, 2)
    regDfcomplete['Corsi_for%'] = round(
        (regDfcomplete['Corsi_for'] / (regDfcomplete['Corsi_for'] + regDfcomplete['Corsi_A'])) * 100, 2)
    regDfcomplete['wshF%'] = round((regDfcomplete['wshF'] / (regDfcomplete['wshF'] + regDfcomplete['wshA'])) * 100, 2)
    regDfcomplete['Sv%'] = round((regDfcomplete['Saves'] / regDfcomplete['SOG_A']) * 100, 2)

    # and finally to calculate wins. I am going to count ties as a win for now since both teams get a standings point. if it negativly affects the model I'll adjust
    regDfcomplete['Win'] = np.where(np.logical_or(regDfcomplete['Goals_for'] > regDfcomplete['Goals_A'],
                                                  regDfcomplete['Goals_for'] == regDfcomplete['Goals_A']), 1, 0)
# Add a Season column just for reference
    regDfcomplete['Season'] = season
# write the new df out to csv
    regDfcomplete.to_csv('data/'+ str(season) + 'agg_regular_season.csv')
    season = season + 1











