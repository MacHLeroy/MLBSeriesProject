# MLBSeriesProject
Project Exploring MLB Series Win Percentages

Introduction:
This project started with what I thought would be a fairly simple question to answer--which teams in MLB history have won the highest percentage of their regular season series? Unfortunately, I was unable to find any sources that tracked regular season series success of MLB teams directly. So, using beautifulsoup, I scraped the result of every baseball game going back to 1900 from Baseball-Reference's website, compiled and cleaned the results, and then wrote a function to calculate each team's regular season series win percentage. Below you can find a notebook walking through my code for scraping, cleaning, and compiling the data, and above you can find a dashboard I built out of the resulting data.

fter scraping the results of every baseball game going back to 1900 and figuring out every teams' regular series win percentage (see project below for more information), I wanted to build a simple way to share the data I had compiled with the world. To me, the clearest way to share data is to make it fun and easy to visualize, so I used streamlit to build an interactive dashboard. I then deployed said dashboard on AWS. 

Files:

