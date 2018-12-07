# GWU_Capstone_NHL_API
Capstone project for GWU on NHL data
## This is my attempt to predict the outcome of NHL Games using machine learning techniques:

  To start I explored the NHL's API at [NHL API here](https://statsapi.web.nhl.com/api/v1), this is an awesome resource
very rich with data back to the start of the league. Like most data sources today the payload comes back in JSON format, which
I was not familiar with, and the NHL's version is heavily nested which proved to be a bit of a challenge. Luckily I found a 
python scraper package that takes the play by play data from a season and wraps it nicely in a csv file for you! That package 
can be found [Harry Shommer's Hockey Scraper](https://github.com/HarryShomer/Hockey-Scraper). The scraper works great but I 
will caution you to have patience, a single season of data is about 2400 games plus the playoffs, and can be on the order of 
650K rows of data per file. It takes a couple of hours for each season so if you use this plan accordingly. 

The play by play data captures every play on the ice, to include an x and y coordinate of the rink! I did not use that feature 
for this project but I plan to revisit and do analysis at a future time. 

I leveraged [this code repository](https://github.com/josh314/nhl) as a starting point, it was designed for a different yet 
similar data source, so with a bit of refactoring I was able to leverage a good bit of this code for my project. In particular I 
agree with his stand on the abbreviations in the dataset and leveraged the clean.py script to run all of the play by play data 
through to fix that issue. All of the cleaned csv files have the year of the season_out.csv format. 

The two aggregation scripts should be your next stop, they will run over the cleaned csvs and are currently set up to run on 
the 2014 - 2019 seasons, and aggregate all of the stats by team by game. I intend to return to this project to get down to the 
player level, because I believe that’s where all the magic is, sadly I did not have time to scope that into this project.

Once you have all of the data run, you can run the visualization scripts, currently set to loop over the afore mentioned 
seasons, the vis are all set up to be plots of the team level stats broken out by the current divisions in the NHL. It is a
lot of png files! and really shows that there is quite a lot of parity in the league currently, at least from a team stats 
standpoint. 

The Machine Learning scripts again leverage the 2014 - 2019 seasons. I used the sklearn library for all of my analysis
Each algorithm was trained on the 2014 and 2018 data, I need to do this to account for the extra column that was the addition 
of Vegas to the league. the rest of the data was run through as test data. Before running the data on the algorithms I pulled 
out all columns that were either Goals, or derived from the goals column, except Shooting percentage. Ultimately I still think 
this gave to much to the computer, as the Logistic Regression performs between 96 and 100 accuracy. 

While the algorithms ability to predict a winner given game data is good, I need to revisit as I would like to leverage past or at least in season data to forecast future games. I need to work through those details but I am confident that it can be achieved.

In closing this was my first real "soup to nuts" project done in python, prior to this I worked more in R, frankly this data would be perfect for an R project, but I learned so much and I am much more confident in my python skills then when I started.
 

A link to a data dictionary to define the statistical terms for the NHL data can be found at [Offside Review](http://offsidereview.com/glossary/)
