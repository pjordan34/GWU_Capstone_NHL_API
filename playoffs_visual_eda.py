import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# pull in the files you want from the aggregation script, after comparing results I chose to keep shootouts as they gave a more accurate win count

files = ['data/2014agg_playoffs.csv', 'data/2015agg_playoffs.csv', 'data/2016agg_playoffs.csv', 'data/2017agg_playoffs.csv', 'data/2018agg_playoffs.csv']
season = 2014

for file in files:
    df = pd.read_csv(file)
    df = df.set_index(['Ev_Team', 'Game_Id']).sort_index()
# filter the data by division and conference
    metro = ['CAR', 'CBJ', 'NJD', 'WSH', 'NYR', 'NYI', 'PHI', 'PIT']
    atlantic = ['BOS', 'TOR', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL']
    central = ['CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'WPG']
    pacific = ['ANA', 'ARI', 'CGY', 'EDM', 'LAK', 'SJS', 'VAN', 'VGK']
    eastern_conference = metro + atlantic
    western_conference = central + pacific

    metroDf = df.loc[metro]
    atlanticDf = df.loc[atlantic]
    centralDf = df.loc[central]
    pacificDf = df.loc[pacific]
    eastern_conferenceDf = df.loc[eastern_conference]
    western_conferenceDf = df.loc[western_conference]
# reset the index for visualizations
    metroDf.reset_index(inplace=True)
    atlanticDf.reset_index(inplace=True)
    centralDf.reset_index(inplace=True)
    pacificDf.reset_index(inplace=True)
    eastern_conferenceDf.reset_index(inplace=True)
    western_conferenceDf.reset_index(inplace=True)
# print a correlation matrix to look for relationships in the data
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(corr, linewidths=.5, ax=ax,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values)
    plt.xticks(rotation=60)
    # show and save off the graph
    plt.savefig('data/'+str(season)+'corrPlot.png', bbox_inches='tight',pad_inches=0.5)
    #plt.show()
    plt.clf()
# boxplots by season of goals for and goals against
    fig = plt.figure(figsize=(12, 12))
    plt.suptitle('Goals Scored vs. Goals Allowed per Game by Division'+''+str(season)+''+'Playoffs', fontsize=14)

    plt.subplot(4, 2, 1)
    sns.boxplot(x='Ev_Team', y='Goals_for', data=metroDf)
    plt.xlabel('Metro Divison')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 2)
    sns.boxplot(x='Ev_Team', y='Goals_A', data=metroDf)
    plt.xlabel('Metro Divison')
    plt.ylabel('Goals Allowed')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 3)
    sns.boxplot(x='Ev_Team', y='Goals_for', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 4)
    sns.boxplot(x='Ev_Team', y='Goals_A', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Goals Allowed')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 5)
    sns.boxplot(x='Ev_Team', y='Goals_for', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 6)
    sns.boxplot(x='Ev_Team', y='Goals_A', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Goals Allowed')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 7)
    sns.boxplot(x='Ev_Team', y='Goals_for', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    plt.subplot(4, 2, 8)
    sns.boxplot(x='Ev_Team', y='Goals_A', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Goals Allowed')
    plt.xticks(rotation=60)
    plt.yticks([0, 2, 4, 5, 7, 10])

    # save off the graph
    plt.tight_layout(pad=3.0, w_pad=1.0, h_pad=1.0)
    plt.savefig('data/'+str(season)+'playoffs_goalsFA.png', bbox_inches='tight',pad_inches=0.5)
    #plt.show()
    plt.clf()
# violin plots of Save percentage and Shots on Goal Against
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Save% vs Shots on Goal Against per Game by Division'+''+str(season)+''+'Playoffs', fontsize=14)


    plt.subplot(4, 2, 1)
    sns.violinplot(x='Ev_Team', y='Sv%', data=metroDf)
    plt.xlabel('Metro Divison')
    plt.ylabel('Save Percentage')
    plt.xticks(rotation=60)
    plt.yticks([60, 70, 80, 90, 100])

    plt.subplot(4, 2, 2)
    sns.violinplot(x='Ev_Team', y='SOG_A', data=metroDf)
    plt.xlabel('Metro Divison')
    plt.ylabel('Shots on Goal Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 3)
    sns.violinplot(x='Ev_Team', y='Sv%', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Save Percentage')
    plt.xticks(rotation=60)
    plt.yticks([60, 70, 80, 90, 100])

    plt.subplot(4, 2, 4)
    sns.violinplot(x='Ev_Team', y='SOG_A', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Shots on Goal Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 5)
    sns.violinplot(x='Ev_Team', y='Sv%', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Save Percentage')
    plt.xticks(rotation=60)
    plt.yticks([60, 70, 80, 90, 100])

    plt.subplot(4, 2, 6)
    sns.violinplot(x='Ev_Team', y='SOG_A', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Shots on Goal Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 7)
    sns.violinplot(x='Ev_Team', y='Sv%', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Save Percentage')
    plt.xticks(rotation=60)
    plt.yticks([60, 70, 80, 90, 100])

    plt.subplot(4, 2, 8)
    sns.violinplot(x='Ev_Team', y='SOG_A', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Shots on Goal Against')
    plt.xticks(rotation=60)
    # show and save off the graph
    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Playoffs_Save_perc_SOGA.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# swarm plots on blocks for and against
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Blocks Against vs Blocks for per Game by Division'+''+str(season)+''+'Playoffs', fontsize=14)

    plt.subplot(4, 2, 1)
    sns.swarmplot(x='Ev_Team', y='Blocks_A', data=metroDf)
    # Label the axes
    plt.xlabel('Metro Divison')
    plt.ylabel('Blocks Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 2)
    sns.swarmplot(x='Ev_Team', y='Blocks_for', data=metroDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Blocks for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 3)
    sns.swarmplot(x='Ev_Team', y='Blocks_A', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Blocks Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 4)
    sns.swarmplot(x='Ev_Team', y='Blocks_for', data=atlanticDf)
    plt.xlabel('Atlantic Divison')
    plt.ylabel('Blocks for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 5)
    sns.swarmplot(x='Ev_Team', y='Blocks_A', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Blocks Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 6)
    sns.swarmplot(x='Ev_Team', y='Blocks_for', data=centralDf)
    plt.xlabel('Central Divison')
    plt.ylabel('Blocks for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 7)
    sns.swarmplot(x='Ev_Team', y='Blocks_A', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Blocks Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 8)
    sns.swarmplot(x='Ev_Team', y='Blocks_for', data=pacificDf)
    plt.xlabel('Pacific Divison')
    plt.ylabel('Blocks for')
    plt.xticks(rotation=60)
    # show and save off the graph
    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Playoffs_Blocks_for_A.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# swarm plots of weighted shots for and against
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Weighted Shots for vs Against per Game by Division'+''+str(season)+''+'Playoffs', fontsize=14)

    plt.subplot(4, 2, 1)
    sns.swarmplot(x='Ev_Team', y='wshF', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Wieghted Shots for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 2)
    sns.swarmplot(x='Ev_Team', y='wshA', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Wieghted Shots Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 3)
    sns.swarmplot(x='Ev_Team', y='wshF', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Wieghted Shots for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 4)
    sns.swarmplot(x='Ev_Team', y='wshA', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Wieghted Shots Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 5)
    sns.swarmplot(x='Ev_Team', y='wshF', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Wieghted Shots for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 6)
    sns.swarmplot(x='Ev_Team', y='wshA', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Wieghted Shots Against')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 7)
    sns.swarmplot(x='Ev_Team', y='wshF', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Wieghted Shots for')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 8)
    sns.swarmplot(x='Ev_Team', y='wshA', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Wieghted Shots Against')
    plt.xticks(rotation=60)

    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    # show and save off the graph
    plt.savefig('data/' + str(season) + 'Playoffs_WeightedShots_for_A.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# boxplots of Shot percentage and SOG for by season
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Shot Percentage vs Shots on Goal_for per Game by Division'+''+str(season)+''+'Playoffs', fontsize=14)

    plt.subplot(4, 2, 1)
    sns.boxplot(x='Ev_Team', y='Shot_Percentage_for', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Shot%')
    plt.yticks([0, 10, 20, 30, 40])

    plt.subplot(4, 2, 2)
    sns.boxplot(x='Ev_Team', y='SOG_for', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Shots on Goal')

    plt.subplot(4, 2, 3)
    sns.boxplot(x='Ev_Team', y='Shot_Percentage_for', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Shot%')
    plt.yticks([0, 10, 20, 30, 40])

    plt.subplot(4, 2, 4)
    sns.boxplot(x='Ev_Team', y='SOG_for', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Shots on Goal')

    plt.subplot(4, 2, 5)
    sns.boxplot(x='Ev_Team', y='Shot_Percentage_for', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Shot%')
    plt.yticks([0, 10, 20, 30, 40])

    plt.subplot(4, 2, 6)
    sns.boxplot(x='Ev_Team', y='SOG_for', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Shots on Goal')

    plt.subplot(4, 2, 7)
    sns.boxplot(x='Ev_Team', y='Shot_Percentage_for', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Shot%')
    plt.yticks([0, 10, 20, 30, 40])

    plt.subplot(4, 2, 8)
    sns.boxplot(x='Ev_Team', y='SOG_for', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Shots on Goal')

    # show and save off the graph
    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Playoffs_Shot_Perc_SOG_for.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# calculate total wins
    metrobyTeam = metroDf.groupby(['Ev_Team'])
    metroWins = metrobyTeam.Win.sum()
    atlanticbyTeam = atlanticDf.groupby(['Ev_Team'])
    atlanticWins = atlanticbyTeam.Win.sum()
    pacificbyTeam = pacificDf.groupby(['Ev_Team'])
    pacificWins = pacificbyTeam.Win.sum()
    centralbyTeam = centralDf.groupby(['Ev_Team'])
    centralWins = centralbyTeam.Win.sum()
# boxplots for goals for percentage and bar plots for total wins per season
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Goals for Percentage per Game vs Team Wins by Division'+''+str(season)+''+'Playoffs', fontsize=14)

    plt.subplot(4, 2, 1)
    sns.boxplot(x='Ev_Team', y='Goals_for%', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Goals for %')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 2)
    metroWins.plot(kind='bar')
    plt.ylabel('Wins')
    plt.xlabel('Metro Division')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 3)
    sns.boxplot(x='Ev_Team', y='Goals_for%', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Goals for %')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 4)
    atlanticWins.plot(kind='bar')
    plt.ylabel('Wins')
    plt.xlabel('Atlantic Division')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 5)
    sns.boxplot(x='Ev_Team', y='Goals_for%', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Goals for %')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 6)
    centralWins.plot(kind='bar')
    plt.ylabel('Wins')
    plt.xlabel('Central Division')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 7)
    sns.boxplot(x='Ev_Team', y='Goals_for%', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Goals for %')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 8)
    pacificWins.plot(kind='bar')
    plt.ylabel('Wins')
    plt.xlabel('Pacific Division')
    plt.xticks(rotation=60)
# show and save off the graph
    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Playoff_Goals_for_Percentage_Wins.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# plot miss% and Saves per game
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Miss Percentage per Game & Saves per Game by Division'+''+str(season), fontsize=14)

    plt.subplot(4, 2, 1)
    sns.boxplot(x='Ev_Team', y='Miss%', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Miss Percentage')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 2)
    sns.swarmplot(x='Ev_Team', y='Saves', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Saves per Game')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 3)
    sns.boxplot(x='Ev_Team', y='Miss%', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Miss Percentage')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 4)
    sns.swarmplot(x='Ev_Team', y='Saves', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Saves per Game')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 5)
    sns.boxplot(x='Ev_Team', y='Miss%', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Miss Percentage')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 6)
    sns.swarmplot(x='Ev_Team', y='Saves', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Saves per Game')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 7)
    sns.boxplot(x='Ev_Team', y='Miss%', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Miss Percentage')
    plt.xticks(rotation=60)

    plt.subplot(4, 2, 8)
    sns.swarmplot(x='Ev_Team', y='Saves', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Saves per Game')
    plt.xticks(rotation=60)

    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Miss_Percentage_Saves.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()
# plots for Hits for and Hits Against per game
    fig = plt.figure(figsize=(12, 12))
    fig.suptitle('Hits for per Game vs Hits Against per Game by Division' + '' + str(season), fontsize=14)

    plt.subplot(4,2,1)
    sns.violinplot(x='Ev_Team', y='Hits_for', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Hits for per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,2)
    sns.violinplot(x='Ev_Team', y='Hits_A', data=metroDf)
    plt.xlabel('Metro Division')
    plt.ylabel('Hits Against per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,3)
    sns.violinplot(x='Ev_Team', y='Hits_for', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Hits for per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,4)
    sns.violinplot(x='Ev_Team', y='Hits_A', data=atlanticDf)
    plt.xlabel('Atlantic Division')
    plt.ylabel('Hits Against per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,5)
    sns.violinplot(x='Ev_Team', y='Hits_for', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Hits for per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,6)
    sns.violinplot(x='Ev_Team', y='Hits_A', data=centralDf)
    plt.xlabel('Central Division')
    plt.ylabel('Hits Against per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,7)
    sns.violinplot(x='Ev_Team', y='Hits_for', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Hits for per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.subplot(4,2,8)
    sns.violinplot(x='Ev_Team', y='Hits_A', data=pacificDf)
    plt.xlabel('Pacific Division')
    plt.ylabel('Hits Against per Game')
    plt.xticks(rotation = 60)
    plt.yticks([0,20,40,60])

    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=2.0)
    plt.savefig('data/' + str(season) + 'Hits_for_A.png', bbox_inches='tight', pad_inches=0.5)
    #plt.show()
    plt.clf()

    #increment the season and run through it again
    season = season + 1
