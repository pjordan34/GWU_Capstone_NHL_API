import pandas as pd
import sys
import requests
import matplotlib.pyplot as plt
import json
from pandas.io.json import json_normalize

# Assign URL to variable: url
url = 'https://statsapi.web.nhl.com/api/v1/teams/15/?expand=team.roster&season=20172018'

# Package the request, send the request and catch the response: r
r = requests.get(url)

# Decode the JSON data into a dictionary: json_data
json_data = r.json()

# Print each key-value pair in json_data
for k in json_data.keys():
    print(k + ': ', json_data[k])

df = pd.DataFrame(json_data)
teams = json_normalize(df['teams'])
print(teams.columns)

team = teams[['abbreviation', 'conference.id', 'conference.link',
       'conference.name', 'division.id',
       'division.link', 'division.name', 'id', 'link',
       'name', 'officialSiteUrl', 'roster.link', 'teamName','venue.name']].drop_duplicates()
print(team.head())

teams_roster = pd.DataFrame(json_normalize(teams['roster.roster'][0]))
print(teams_roster.columns)
