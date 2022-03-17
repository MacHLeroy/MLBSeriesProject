# MLBSeriesProject
Project Exploring MLB Series Win Percentages

**Introduction:**
This project started with what I thought would be a fairly simple question to answer--which teams in MLB history have won the highest percentage of their regular season series? Unfortunately, I was unable to find any sources that tracked regular season series success of MLB teams directly. So, using beautifulsoup, I scraped the result of every baseball game going back to 1900 from Baseball-Reference's website, compiled and cleaned the results, and then wrote a function to calculate each team's regular season series win percentage. Below you can find a notebook walking through my code for scraping, cleaning, and compiling the data, and above you can find a dashboard I built out of the resulting data.

fter scraping the results of every baseball game going back to 1900 and figuring out every teams' regular series win percentage (see project below for more information), I wanted to build a simple way to share the data I had compiled with the world. To me, the clearest way to share data is to make it fun and easy to visualize, so I used streamlit to build an interactive dashboard. I then deployed said dashboard on AWS. 

**Python Scripts:**
Dashboard.py - the file for the actual dashboard. Build on Streamlit, can be deployed locally with -streamlit run Dashboard.py provided all dependencies (including streamlit) have been downloaded and all required files are in working directory (YearlyResultsMaster.csv, LeagueGameResults.csv, PostSeasonStartDates.csv, MasterYearlyResultsWithPlayoffs.csv)

**CSV Files:**

YearlyResultsMaster.csv =  Contains Season Results (Wins, Losses, Series Wins, Series Losses, Series Ties) for all major league teams going back to 1900

LeagueGameResults.csv = Contains the individual game results for all major league baseball games played since 1900

PostSeasonStartDates.csv = Contains the year and postseason start date for each MLB season

MasterYearlyResultsWithPlayoffs.csv = Similar to YearlyResultsMaster but includes playoff results as well. 

**Notebooks:**
These notebooks were used to actually scrape the games from baseballreference and compile the data. Many are working notebooks not in great presentation condition. For a cleaned/compiled version that shows the final thotught process/data generation see the following link: https://colab.research.google.com/drive/199UbuzfVVwhwmNZfiqkorwq0hcC59r57 





