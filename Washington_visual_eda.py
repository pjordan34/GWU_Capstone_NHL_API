import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dfs = []
files =  ['data/2014agg_regular_season_so.csv', 'data/2015agg_regular_season_so.csv', 'data/2016agg_regular_season_so.csv','data/2017agg_regular_season_so.csv','data/2018agg_regular_season_so.csv','data/2019agg_regular_season_so.csv']
for file in files:
    dfs.append(pd.read_csv(file))
big_frame = pd.concat(dfs, ignore_index=True)

dfs2 = []
filenames = ['data/2014agg_playoffs.csv', 'data/2015agg_playoffs.csv', 'data/2016agg_playoffs.csv', 'data/2017agg_playoffs.csv', 'data/2018agg_playoffs.csv']
for filename in filenames:
    dfs2.append(pd.read_csv(filename))
playoffs = pd.concat(dfs2, ignore_index=True)

big_frame = big_frame.set_index(['Ev_Team'])
wsh = big_frame.loc['WSH']

wshbySeason = wsh.groupby(['Season'])
wshWins = wshbySeason.Win.sum()

playoffs = playoffs.set_index(['Ev_Team'])
wshPlayoffs = playoffs.loc['WSH']
wshPlayoffsbySeason = wshPlayoffs.groupby(['Season'])
wshPlayoffWins = wshPlayoffsbySeason.Win.sum()

fig = plt.figure(figsize=(35,35))
plt.suptitle('Stats by Season by Game for Washington', fontsize=24)
plt.subplot(8,2,1)
sns.boxplot(x='Season', y='Goals_for', data=wsh)
# Label the axes
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goals Scored per Game', fontsize=18)
plt.xticks(rotation = 60)
plt.yticks([0,2,4,5,7,10])

plt.subplot(8,2,2)
sns.boxplot(x='Season', y='Goals_A', data=wsh)
# Label the axes
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goals Allowed per Game', fontsize=18)
plt.xticks(rotation = 60)
plt.yticks([0,2,4,5,7,10])

plt.subplot(8,2,3)
sns.boxplot(x='Season', y='Blocks_for', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Blocks_for per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,4)
sns.boxplot(x='Season', y='Blocks_A', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Blocks Against per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,5)
sns.boxplot(x='Season', y='wshF', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('WSH for per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,6)
sns.boxplot(x='Season', y='wshA', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('WSH Against per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,7)
sns.boxplot(x='Season', y='Sv%', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Save Percentage per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,8)
sns.boxplot(x='Season', y='SOG_A', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('SOG Against per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,9)
sns.boxplot(x='Season', y='SOG_for', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('SOG for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,10)
sns.boxplot(x='Season', y='Shot_Percentage_for', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Shot% for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,11)
sns.boxplot(x='Season', y='Goals_for%', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goal% for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,12)
wshWins.plot(kind='bar')
plt.xlabel('Season', fontsize=18)
plt.ylabel('# of Wins', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,13)
sns.boxplot(x='Season', y='Hits_for', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Hits for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,14)
sns.boxplot(x='Season', y='Hits_A', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Hits Against per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,15)
sns.boxplot(x='Season', y='Miss%', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Miss% per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,16)
sns.boxplot(x='Season', y='Saves', data=wsh)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Saves per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.tight_layout(pad=8.0,w_pad=2.0, h_pad=2.0)
plt.savefig('data/WSH_Stats_by_Season.png', bbox_inches='tight', pad_inches=0.5)
#plt.show()
plt.clf()

# WSH playoff stats by season
fig = plt.figure(figsize=(35,35))
plt.suptitle('Playoff Stats by Season for Washington', fontsize=24)
plt.subplot(8,2,1)
sns.boxplot(x='Season', y='Goals_for', data=wshPlayoffs)
# Label the axes
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goals Scored per Game', fontsize=18)
plt.xticks(rotation = 60)
plt.yticks([0,2,4,5,7,10])

plt.subplot(8,2,2)
sns.boxplot(x='Season', y='Goals_A', data=wshPlayoffs)
# Label the axes
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goals Allowed per Game', fontsize=18)
plt.xticks(rotation = 60)
plt.yticks([0,2,4,5,7,10])

plt.subplot(8,2,3)
sns.boxplot(x='Season', y='Blocks_for', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Blocks_for per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,4)
sns.boxplot(x='Season', y='Blocks_A', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Blocks Against per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,5)
sns.boxplot(x='Season', y='wshF', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('WSH for per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,6)
sns.boxplot(x='Season', y='wshA', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('WSH Against per Game', fontsize=18)
plt.xticks(rotation = 60)


plt.subplot(8,2,7)
sns.boxplot(x='Season', y='Sv%', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Save Percentage per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,8)
sns.boxplot(x='Season', y='SOG_A', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('SOG Against per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,9)
sns.boxplot(x='Season', y='SOG_for', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('SOG for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,10)
sns.boxplot(x='Season', y='Shot_Percentage_for', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Shot% for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,11)
sns.boxplot(x='Season', y='Goals_for%', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Goal% for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,12)
wshPlayoffWins.plot(kind='bar')
plt.xlabel('Season', fontsize=18)
plt.ylabel('# of Wins', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,13)
sns.boxplot(x='Season', y='Hits_for', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Hits for per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,14)
sns.boxplot(x='Season', y='Hits_A', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Hits Against per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,15)
sns.boxplot(x='Season', y='Miss%', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Miss% per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.subplot(8,2,16)
sns.boxplot(x='Season', y='Saves', data=wshPlayoffs)
plt.xlabel('Season', fontsize=18)
plt.ylabel('Saves per Game', fontsize=18)
plt.xticks(rotation = 60)

plt.tight_layout(pad=8.0,w_pad=2.0, h_pad=2.0)
plt.savefig('data/WSH_Playoff_Stats_by_Season.png', bbox_inches='tight', pad_inches=0.5)
#plt.show()
plt.clf()



