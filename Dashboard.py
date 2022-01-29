"""
Dashboard.py
Baseball Dashboard by MacKenzye Leroy

This script allows the user to launch a baseball daushboard by running:

'streamlit run Dashboard.py' 

in the terminal.

Requires: 'YearlyResultsMaster.csv', 'LeagueGameResults.csv', 'PostSeasonStartDates.csv' in the same directory

All of which can be found on GitHub (github.com/MacHLeroy)

"""

# ----Imports------------------------------------
from turtle import title
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import streamlit as st
import plotly.express as px

# ----Set page configurations/defaults--------------
st.set_page_config(layout="wide")
wide_width = 1250
half_width = wide_width/2 -100
plot_height = 450
table_height = 750



#Teams often change names, so we need a unique franchise identifier for each. The dictionary below maps all team names to a unique Franchise ID
#Franchise ID wil be referred to as FranID throughout this script

teams_ID_dictionary= {'Tampa Bay Devil Rays':'TBD', 'Tampa Bay Rays': 'TBD', 'Florida Marlins': 'FLA', 'Miami Marlins':'FLA',
                      'Montreal Expos':'WSN', 'Washington Nationals':'WSN',  'Seattle Pilots':'MIL', 'Milwaukee Brewers':'MIL',
                      'Houston Colt .45s':'HOU', 'Houston Astros':'HOU', 'Washington Senators':'MIN', 'Minnesota Twins': 'MIN',
                      'California Angels':'ANA','Anaheim Angels':'ANA', 'LA Angels of Anaheim':'ANA', 'Los Angeles Angels':'ANA', 
                      'Philadelphia Athletics':'OAK', 'Kansas City Athletics':'OAK', 'Oakland Athletics':'OAK', 'Cleveland Blues':'CLE',
                      'Baltimore Orioles':'BAL','St. Louis Browns':'BAL', 'Cleveland Indians':'CLE', 'Cleveland Naps':'CLE', 
                      'Boston Red Sox':'BOS', 'Boston Americans':'BOS', 'Cincinnati Reds':'CIN','Cincinnati Redlegs':'CIN',
                      'New York Yankees':'NYY', 'New York Highlanders':'NYY', 'Chicago Cubs':'CHC', 'Chicago Orphans':'CHC',
                      'Los Angeles Dodgers':'LAD', 'Brooklyn Superbas':'LAD','Brooklyn Dodgers':'LAD', 'Brooklyn Robins':'LAD',
                      'San Francisco Giants':'SFG', 'New York Giants':'SFG', 'New York Mets':'NYM', 'Atlanta Braves':'ATL', 
                      'Milwaukee Braves':'ATL', 'Boston Braves':'ATL', 'Boston Doves':'ATL', 'Boston Beaneaters':'ATL', 
                      'Boston Bees':'ATL', 'Boston Rustlers':'ATL',  'Pittsburgh Pirates':'PIT', 'Philadelphia Phillies':'PHI',
                      'Chicago White Sox':'CHW', 'Detroit Tigers':'DET', 'Texas Rangers':'TEX', 'Kansas City Royals':'KCR', 
                      'San Diego Padres':'SDP', 'Arizona Diamondbacks':'ARI', 'Seattle Mariners':'SEA',
                      'Toronto Blue Jays':'TOR', 'Colorado Rockies':'COL', 'St. Louis Cardinals':'STL' ,
                      'Baltimore Terrapins':'FedBAL', 'St. Louis Terriers':'FedSTL','Brooklyn Tip-Tops':'FedBRK',
                      'Pittsburgh Rebels': 'FedPIT', 'Kansas City Packers':'FedKCP', 'Indianapolis Hoosiers':'FedINDNEW',
                      'Newark Pepper':'FedINDNEW', 'Buffalo Buffeds':'FedBUF', 'Buffalo Blues':'FedBUF', 'Chicago Whales':'FedCHI',
                      'Chicago Chi-Feds':'FedCHI', 'Cleveland Bronchos':'FedCLE'  
                     }


#current MLB team names
current_teams = ['Cincinnati Reds',  'Pittsburgh Pirates', 'Philadelphia Phillies',
                'Chicago White Sox', 'Detroit Tigers', 'Baltimore Orioles', 
                'Milwaukee Brewers', 'Chicago Cubs',  'Boston Red Sox', 
                'New York Yankees', 'Cleveland Indians', 'San Francisco Giants', 
                'Los Angeles Dodgers', 'Minnesota Twins', 'New York Mets', 
                'Houston Astros',  'Atlanta Braves', 'Oakland Athletics', 
                'Kansas City Royals', 'San Diego Padres', 'Texas Rangers', 
                'Seattle Mariners', 'Toronto Blue Jays',  'Los Angeles Angels',
                'Colorado Rockies',  'Arizona Diamondbacks', 'St. Louis Cardinals',
                'Washington Nationals', 'Tampa Bay Rays', 'Miami Marlins']



#Team colors-Section 2 of the dashboard updates plots to match current team colors. For non-current teams, the following deafult colors are used
default_colors = ['#636EFA', '#BAB0AC', '#EF553B']
color_dictionary =  {'Cincinnati Reds':['#C6011F', '#BAB0AC', '#000000'],  'Pittsburgh Pirates':['#27251F', '#BAB0AC', '#FDB827'], 
                'Philadelphia Phillies':['#E81828', '#BAB0AC', '#002D72'], 'Chicago White Sox':['#27251F', '#FFFFFF', '#C4CED4'], 
                'Detroit Tigers':['#0C2340', '#BAB0AC', '#FA4616'], 'Baltimore Orioles':['#DF4601', '#BAB0AC', '#000000'], 
                'Milwaukee Brewers':['#12284B', '#BAB0AC', '#FFC52F' ], 'Chicago Cubs':['#0E3386', '#BAB0AC', '#CC3433'],  
                'Boston Red Sox':['#BD3039' ,  '#BAB0AC', '#0C2340'], 'New York Yankees':['#0C2340', '#E4002C', '#C4CED3'], 
                'Cleveland Indians':['#0C2340','#BAB0AC', '#E31937' ], 'San Francisco Giants':['#FD5A1E', '#EFD19F', '#27251F'], 
                'Los Angeles Dodgers':['#005A9C', '#A5ACAF', '#EF3E42'], 'Minnesota Twins':['#002B5C', '#B9975B', '#D31145'], 
                'New York Mets':['#002D72', '#BAB0AC', '#FF5910'],  'Houston Astros':['#002D62','#BAB0AC' ,'#EB6E1F'],  
                'Atlanta Braves':['#CE1141', '#EAAA00', '#13274F'], 'Oakland Athletics':['#003831', '#A2AAAD', '#EFB21E'], 
                'Kansas City Royals':['#004687', '#BAB0AC','#BD9B60'], 'San Diego Padres':['#2F241D','#BAB0AC', '#FFC425' ], 
                'Texas Rangers':['#003278','#BAB0AC', '#C0111F' ], 'Seattle Mariners':['#0C2C56', '#C4CED4' ,'#005C5C'], 
                'Toronto Blue Jays':['#134A8E', '#E8291C','#1D2D5C'],  'Los Angeles Angels':['#BA0021' ,'#C4CED4', '#003263'],
                'Colorado Rockies':['#33006F','#C4CED4', '#000000'],  'Arizona Diamondbacks':['#A71930', '#E3D4AD', '#000000'], 
                'St. Louis Cardinals':['#C41E3A', '#FEDB00', '#0C2340'], 'Washington Nationals':['#AB0003', '#BAB0AC', '#14225A' ], 
                'Tampa Bay Rays':['#092C5C', '#F5D130', '#8FBCE6'], 'Miami Marlins':['#00A3E0', '#000000', '#41748D']}


noPostSeasonList = [1900, 1901, 1902, 1903, 1904, 1994] #Years no postseasons happened

#Get teams lists
all_teams = []
federation_teams = []
for key in teams_ID_dictionary:
    all_teams.append(key)
    if teams_ID_dictionary[key][0:3] == 'Fed':
        federation_teams.append(key)

#sort teams lists
all_teams.sort()
federation_teams.sort()
current_teams.sort()

#Define functions for loading in data. Note all data is cached with @st.cache above function definition

@st.cache
def load_data1():
    """
    Loads YearlyResultsMaster.csv which contains the Season Results for all major league teams going back to 1900

    Returns
    ------
    Dataframe containing the FranID, Team, Year, Number of Games Played, Wins Losses, Number of Series Played, Series Wins,
    Series Losses, Series Ties, Win Percentage and Series Win Percentage for all major league teams separeted out by year going back to 1900
    """
    MasterYearlyResults = pd.read_csv('YearlyResultsMaster.csv')
    MasterYearlyResults['WinPercent'] = MasterYearlyResults ['Wins']/ MasterYearlyResults ['NumberOfGames']
    MasterYearlyResults['SeriesWinPercent'] = MasterYearlyResults ['SeriesWins']/ MasterYearlyResults ['NumberOfSeries']
    MasterYearlyResults['WinPercent'] = MasterYearlyResults ['Wins']/ MasterYearlyResults ['NumberOfGames']
    MasterYearlyResults['SeriesWinPercent'] = MasterYearlyResults ['SeriesWins']/ MasterYearlyResults ['NumberOfSeries']

    return MasterYearlyResults

@st.cache
def load_data2():
    """
    Loads LeagueGameResults.csv which contains the individual game results for all major league baseball games played since 1900

    Returns
    ------
    Dataframe containing the date of each game, the home team name and FranhiseID for each team, the runs scored by each team, and the winner. 
    """
    workingdf = pd.read_csv('LeagueGameResults.csv')
    workingdf['Winner'] = np.where(workingdf['Home_Team_Score'] > workingdf['Away_Team_Score'] , workingdf['Home_Team'], workingdf['Away_Team'])
    workingdf['Date'] = pd.to_datetime(workingdf["Date"])
    workingdf['Season'] = pd.DatetimeIndex(workingdf['Date']).year
    return workingdf


@st.cache
def load_data3():
    """
    Loads 'PostSeasonStartDates.csv' which contains the year and postseason start date for each MLB season

    Returns
    ------
    Dataframe containing the year and postseason start date for each MLB season
    """
    PostSeasonMarkerDF = pd.read_csv('PostSeasonStartDates.csv')
    PostSeasonMarkerDF = PostSeasonMarkerDF.set_index('Season')
    return PostSeasonMarkerDF

@st.cache
def load_data4():
    """
    Loads 'MasterYearlyResultsWithPlayoffs' which contains the year and postseason start date for each MLB season

    Returns
    ------
    Dataframe containing the compiled results plus postseason outcome results for visualization purposes
    """
    MasterYearlyResultsWithPlayoffs = pd.read_csv('MasterYearlyResultsWithPlayoffs.csv')
    return MasterYearlyResultsWithPlayoffs





#Load in Data
data_load_state = st.text('Loading data...')

MasterYearlyResults = load_data1()
workingdf = load_data2()
PostSeasonMarkerDF = load_data3()
MasterYearlyResultsWithPlayoffs = load_data4()

data_load_state.text("")


# ------- Define Functions ----------------------------------------------------------------------------------


def getTeamAndYears(Team, start_year = None, end_year = None, historical_results = True, AsHelperFunction = False):

    """
    Parameters
    ----------
    Team: string
        Team of interest
    start_year : integer, optional
        first year of data to pull. If none provided, the lowest year in team existence is set
    end_year :integer, optional
        last year of data to pull. If none provided, the lowest year in team existence is set
    historical_results : boolean, optional
        Whether or not to include all results from a franchise or just the results tied to the exact name selected. 
        For exmaple, include New York Highlanders Results for New York Yankees or not? Default is True.
    AsHelperFunction : boolean, optional
        Whether or not to return a plotly table or dataframe. Default is false which returns a plotly table,
        while true would return a dataframe


    Returns
    -------
    Either a dataframe or a plotly table of the results. 

    Columns of final dtaframe/table: Team, Year, Number of Games Played, Wins Losses, Number of Series Played, 
    Series Wins, Series Losses, Series Ties, Win Percentage and Series Win Percentage for each year of interest.
    """
    
    #If including historical results, we need to use the unique identifier for the franchise associated with the team (FranID)
    if historical_results:
        FranID = teams_ID_dictionary[Team]
    
        TeamInQuotes= "'" + FranID + "'"
        query = "FranID == " + TeamInQuotes
        Results = MasterYearlyResults.query(query)
        Results = Results.sort_values(by = 'Year')

    #If not including historical results, we can query for just the exact team name provided
    else:
        
        TeamInQuotes= "'" + Team + "'"
        query = "Team == " + TeamInQuotes
        Results = MasterYearlyResults.query(query)

    #If no start_year provided, default to minumum
    if start_year == None:
        start_year = Results['Year'].iloc[0]
    
    #If no end_year provided, default to maximum
    if end_year == None:
        end_year = Results['Year'].iloc[-1]


    #filter results for range provided by start_year and end_year
    Results = Results[Results['Year'] >= start_year]
    Results = Results[Results['Year'] <= end_year]

    
    Results = Results.reset_index()
    Results = Results.drop(columns = ['index', 'Unnamed: 0', 'FranID'])
    

    #Creat and add final row with compiled results
    total_row = [ 'Total:', '-', Results.NumberOfGames.sum(),  Results.Wins.sum(),  Results.Losses.sum(),
                Results.NumberOfSeries.sum(), Results.SeriesWins.sum(),  Results.SeriesLosses.sum(),
                Results.SeriesTies.sum(), (Results.Wins.sum()/Results.NumberOfGames.sum()),
                (Results.SeriesWins.sum()/Results.NumberOfSeries.sum())]     
    Results.loc['Total:'] = total_row


    #Round Win and Series win percentages for readability
    Results['WinPercent'] = Results['WinPercent'].round(decimals = 3)
    Results['SeriesWinPercent'] = Results['SeriesWinPercent'].round(decimals = 3) 
    
    
    
    #If not being used as a helper function, default is to build and return a table of results
    if AsHelperFunction == False:
        Results = Results.rename(columns = {'NumberOfSeries':'Number of Series', 'NumberOfGames':'Number of Games', 'SeriesWins': 'Series Wins', 'SeriesLosses':'Series Losses',
                            'SeriesTies': 'Series Ties', 'WinPercent':'Win Percent', 'SeriesWinPercent':'Series Win Percent' })

        table = go.Figure(data=[go.Table(
            header=dict(values=list(Results.columns), 
                        font=dict(color='black')),
            cells=dict(values=[Results['Team'], Results['Year'], Results['Number of Games'], Results['Wins'],
                                Results['Losses'], Results['Number of Series'], Results['Series Wins'], Results['Series Losses'],
                                Results['Series Ties'], Results['Win Percent'], Results['Series Win Percent']], 
                        font=dict(color='black')))

])
       
        table.update_layout(width=wide_width, height = table_height)
    
        return table
    
    #If being used as a helper function, return the dataframe itself
    else:
        return Results

        

    


def getTeamAndYearsPlot(Team, start_year = None, end_year = None, historical_results = True, AsHelperFunction = False):

    """
    Parameters
    ----------
    Team: string
        Team of interest
    start_year : integer, optional
        first year of data to pull. The default is the None, which will default to first 
        year of team existence when getTeamdAndYears is called
    end_year :integer, optional
        last year of data to pull. The default is the None, which will default to last year 
        of team existence when getTeamdAndYears is called

    Returns
    -------
    Plotly figure showing the teams win percentage and series win percantage for selected team over years of interest
    """

    #call getTeamAndYears as helperfunction to get dataframe to draw data from
    Results = getTeamAndYears(Team, start_year, end_year, AsHelperFunction=True)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Results.Year, y=Results.SeriesWinPercent,
            mode='lines',
            name='Series Win Percent'))
    fig.add_trace(go.Scatter(x=Results.Year, y=Results.WinPercent,
            mode='lines',
            name='Win Percent',
            line_color = '#2ca02c'))
    fig.add_hline(y=0.5, line_color = 'Red')
    fig.update_yaxes(range = [.2,.8], title="Win Percent") 
    fig.update_xaxes(title="Year") 
    fig.update_layout(width=wide_width, title = "Overall Win Percent and Series Win Percent by Year")
    return fig

    
def getSeasonHelperFunction(Team, Year):

    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer, optional
        year to pull data from

    Returns
    -------
    Dataframe for all games played by team of interest in year of interest including postseason
    Dataframe columns: Home Team, Home Team Score, Away Team, Away Team Score, Date, Winner, 
    Home Team FranID, Away Team FranID

    Used by
    -------
    getOneYearRegularSeason
    getOneYearPlayoffs
    """


    #Set up query string for team of interest
    TeamInQuotes= "'" + Team + "'"
    query1 = "Home_Team == " + TeamInQuotes + " | Away_Team == " + TeamInQuotes

    #query workingdf for all games matching team of interest
    df1 = workingdf.query(query1)
    df1 = df1.reset_index()

    #filter dataframe
    query2 = "Season == " + str(Year)
    df1 = df1.query(query2)
    
    #return resulting dataframe
    return df1


def getOneYearResultsFull(Team, Year):

    
    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer, optional
        year to pull data from

    Returns
    -------
    Plotly table of full season results (regular season and playoffs). 
    Dataframe columns: Home Team, Home Team Score, Away Team, Away Team Score, Date, Winner, 
    Team Winner (Did team of interest win), Cumulative Wins, Win Percentage to date

    """
    
    #Get regular season results
    df = getOneYearRegularSeason(Team, Year, AsHelper = True)

    #Get playoff results
    playoff_df = getOneYearPlayoffs(Team, Year, AsHelper = True)
    
    #If did not make playoffs add a row stating that   
    if len(playoff_df) == 0:
        final_row = ['-', '-', 'Did', 'Not', 'Make', 'Playoffs', '-', '-', '-']
        df.loc['-'] = final_row

    #If team did make playoffs add spacer row then playoff results
    else:
        spacer_row = ['Playoff', '-', '-', 'Results', '-', '-', '-', '-', '-']
        df.loc['-'] = spacer_row
        df = pd.concat([df, playoff_df], ignore_index=False)
    
    #create table
    df = df.rename(columns = {'Home_Team': 'Home Team', 'Home_Team_Score': 'Home Team Score', 'Away_Team': 'Away Team', 'WinPercent': 'Win Percent',
                            'Away_Team_Score': 'Away Team Score', 'Team_Winner': 'Result', 'Cumulative_Wins':'Cumulative Wins'})
    df= df.replace({'Result': {True: 'Win', False: 'Loss'}})

    table = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    font=dict(color='black')),

        cells=dict(values=[df['Home Team'], df['Home Team Score'], df['Away Team'], df['Away Team Score'],
                                df['Date'], df['Winner'], df['Result'], df['Cumulative Wins'], df['Win Percent']],
                    font=dict(color='black')))])

    #update table size (defaults declared at top)   
    table.update_layout(width=wide_width, height = table_height)
    
    #return table
    return table



def getOneYearRegularSeason(Team, Year, AsHelper = False):

    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year to pull data from

    AsHelperFunction : boolean, optional
        Whether or not to return a plotly table or dataframe. Default is false which returns a plotly table,
        while true would return a dataframe

    Returns
    -------
    Dataframe or plotly table for all games played by team of interest in year of interest during regular season. 
    Dataframe/Table Columns: Dataframe columns: Home Team, Home Team Score, Away Team, Away Team Score, Date, Winner, 
    Team Winner (Did team of interest win), Cumulative Wins, Win Percentage to date


    Called in
    -------
    getOneYearResultsFull
    """
    
    #Call getSeasonHelperFunction to get results for team and year of interest
    df = getSeasonHelperFunction(Team, Year)
        
    #Check df is not empty
    if len(df) == 0:
        print('Invalid Year for Team Given. Please Try Again')
            
    else: 
        if Year not in noPostSeasonList:
            postSeasonCheck = PostSeasonMarkerDF.loc[Year][0]
            playoff_df = df[df.Date >= postSeasonCheck]
            df = df[df.Date < postSeasonCheck]
        
     
        df = df.reset_index()    
        df.index = np.arange(1, len(df)+1)
    
        #Add columns for Team Winner (whether or not team of interest won), Cumulative Wins, and WinPercent (both to date)
        df['Team_Winner'] = df['Winner'] == Team
        df['Cumulative_Wins'] = df['Team_Winner'].cumsum()
        df['WinPercent'] = df['Cumulative_Wins']/df.index

        #drop unnessary columns
        df = df.drop(columns = ['index', 'level_0', 'Home_FranID', 'Away_FranID'])
            
        #round off for readability
        df['WinPercent'] = df['WinPercent'].round(decimals = 3)
        df = df.drop(columns = 'Season')
            
        #convert to date
        df.Date = pd.DatetimeIndex(df.Date).strftime("%m-%d-%Y")

        #If not being used as a helper function, default is to build and return a table of results
        if AsHelper == False:
            df = df.rename(columns = {'Home_Team': 'Home Team', 'Home_Team_Score': 'Home Team Score', 'Away_Team': 'Away Team', 'WinPercent': 'Win Percent',
                            'Away_Team_Score': 'Away Team Score', 'Team_Winner': 'Result', 'Cumulative_Wins':'Cumulative Wins'})
            df= df.replace({'Result': {True: 'Win', False: 'Loss'}})

            table = go.Figure(data=[go.Table(
                    header=dict(values=list(df.columns),
                            font=dict(color='black')),

                    cells=dict(values=[df['Home Team'], df['Home Team Score'], df['Away Team'], df['Away Team Score'],
                                df['Date'], df['Winner'], df['Result'], df['Cumulative Wins'], df['Win Percent']],
                            font=dict(color='black')))])
       
            table.update_layout(width=wide_width, height = table_height)
            return table
        #if being used as a helper function, return a dataframe
        else: return df


def getOneYearPlayoffs(Team, Year, AsHelper = False):

    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year to pull data from

    AsHelperFunction : boolean, optional
        Whether or not to return a plotly table or dataframe. Default is false which returns a plotly table,
        while true would return a dataframe

    Returns
    -------
    Dataframe or plotly table for all games played by team of interest in year of interest during postseason. 
    Dataframe/Table Columns: Dataframe columns: Home Team, Home Team Score, Away Team, Away Team Score, Date, Winner, 
    Team Winner (Did team of interest win), Cumulative Wins, Win Percentage to date


    Called in
    -------
    getOneYearResultsFull
    """
    
    #Call getSeasonHelperFunction to get results for team and year of interest
    playoff_df = getSeasonHelperFunction(Team, Year)
       
    #check valid playoff year
    if Year not in noPostSeasonList:
        postSeasonCheck = PostSeasonMarkerDF.loc[Year][0]
        playoff_df = playoff_df[playoff_df.Date >= postSeasonCheck]
    else: 
        postSeasonCheck = '2099-01-01'
        playoff_df = playoff_df[playoff_df.Date >= postSeasonCheck]
    
    #check df is not empty
    if len(playoff_df) == 0:
        if AsHelper == True:
            return playoff_df
        else:
            return "Team Did Not Qualify for Playoffs in Year Provided"

    else:
        
        playoff_df = playoff_df.reset_index()    
        playoff_df.index = np.arange(1, len(playoff_df)+1)
    
        playoff_df['Team_Winner'] = playoff_df['Winner'] == Team
        playoff_df['Cumulative_Wins'] = playoff_df['Team_Winner'].cumsum()
        playoff_df['WinPercent'] = playoff_df['Cumulative_Wins']/playoff_df.index


        playoff_df.Date = pd.DatetimeIndex(playoff_df.Date).strftime("%m-%d-%Y")
        
        playoff_df['WinPercent'] = playoff_df['WinPercent'].round(decimals = 3)
        playoff_df = playoff_df.drop(columns = ['index', 'level_0', 'Season', 'Home_FranID', 'Away_FranID'])
    
        if playoff_df.Team_Winner.iloc[-1] == True:
                
            final_row = ['-', '-', 'Won', 'World', 'Series', '!', '!', '-', '-']
        else: 
            final_row = ['-', 'Elimainated', 'in', 'Playoffs','by', playoff_df.Winner.iloc[-1], '-', '-', '-']
        playoff_df.loc['--'] = final_row
        
        #playoff_df.Date = pd.DatetimeIndex(playoff_df.Date).strftime("%m-%d-%Y")
        

        if AsHelper == False:
            playoff_df = playoff_df.rename(columns = {'Home_Team': 'Home Team', 'Home_Team_Score': 'Home Team Score', 'Away_Team': 'Away Team', 'WinPercent': 'Win Percent',
                            'Away_Team_Score': 'Away Team Score', 'Team_Winner': 'Result', 'Cumulative_Wins':'Cumulative Wins'})
            playoff_df= playoff_df.replace({'Result': {True: 'Win', False: 'Loss'}})

            table = go.Figure(data=[go.Table(
                    header=dict(values=list(playoff_df.columns),
                            font=dict(color='black')),

                    cells=dict(values=[playoff_df['Home Team'], playoff_df['Home Team Score'], playoff_df['Away Team'], playoff_df['Away Team Score'],
                                playoff_df['Date'], playoff_df['Winner'], playoff_df['Result'], playoff_df['Cumulative Wins'], playoff_df['Win Percent']],
                            font=dict(color='black')))])
       
            table.update_layout(width=wide_width, height = table_height)
            return table
    
        else:
            return playoff_df


def madePlayoffs(Team, Year):

    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year to pull data from


    Returns
    -------
    Boolean: True if the team played in the postseason for the year of interest, False otherwise
    """
    #Call getOneYearPlayoffs to get playoff results for team/year of interest
    df = getOneYearPlayoffs(Team, Year, AsHelper = True)
    
    #If df not empty, team made postseason
    if len(df) != 0:
        return True
    else:
        return False

def wonWorldSeries(Team, Year):

    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year to pull data from


    Returns
    -------
    Boolean: True if the team of interest won the World Series for the year of interest, False otherwise
    """
    

    #Call getOneYearPlayoffs to get playoff results for team/year of interest
    df = getOneYearPlayoffs(Team, Year, AsHelper = True)
    
    #see if team has postseason results and if they won final game of result
    if len(df) == 0:
        return False
    elif Team in federation_teams:
        return False
    elif isinstance(df, str):
        return df
    else:
        if df.Team_Winner.iloc[-2] == True:
            return True
        else:
            return False



def getRecord(Team, Year):
    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year to pull data from

    Returns
    -------
    A list contain information about the team for that season in the following format
    [Wins (integer), Losses (integer), WinPercent (Float), playoff_winner (string)]

    playoff_winner = who won the final series in that teams playoff result. Used to 
    determine who elimanted the team if they did not win the World Series. 

    """


    TeamInQuotes= "'" + Team + "'"
    query = "Team == " + TeamInQuotes
    Results = MasterYearlyResults.query(query)
    Results = Results[Results.Year == Year]
    Wins = Results.Wins.iloc[0]
    Losses = Results.Losses.iloc[0]
    WinPercent = round(Results.WinPercent.iloc[0], 3)
    playoff_winner = np.NaN
    if madePlayoffs(Team, Year):
        playoff_df = getOneYearPlayoffs(Team, Year, AsHelper=True)
        if playoff_df.Team_Winner.iloc[-2] != True:
            playoff_winner = playoff_df.Winner.iloc[-2]
    Record = [Wins, Losses, WinPercent, playoff_winner]
    return Record

def getBarChart1(Team, Year):
    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year of interest
    
    Returns
    -------
    Plotly bar chart with two bars- one showing win percent and loss percent stacked and 
    series win percent, series tie percent, and series loss percent stacked

    
    """

    df = getTeamAndYears(Team, Year, Year, AsHelperFunction = True)
    
    df['SeriesTiePercent'] = df.SeriesTies/df.NumberOfSeries
    df['SeriesLossPercent']= df.SeriesLosses/df.NumberOfSeries
    df['LossPercent'] = df.Losses/df.NumberOfGames
    
    df2 = pd.DataFrame(
    dict(
        year=[Year, Year] * 3,
        layout=["Record", "Series Record"] * 3,
        response=["Win Percent", "Tie Percent", 'Loss Percent'] * 2,
        cnt=[df.WinPercent.iloc[-1], df.SeriesTiePercent.iloc[-1], df.LossPercent.iloc[-1],
        df.SeriesWinPercent.iloc[-1], 0, df.SeriesLossPercent.iloc[-1] ],
        response2=["Wins", "Ties", 'Losses'] * 2,
        cnt2=[df.Wins.iloc[-1], df.SeriesTies.iloc[-1], df.Losses.iloc[-1],
        df.SeriesWins.iloc[-1], 0, df.SeriesLosses.iloc[-1] ]
        ))  
      
    fig1 = go.Figure()
    
    
    fig1.update_layout(
    template="simple_white",
    xaxis=dict(title_text="Percent of Games Won/Lost (Left) and Percent of Series Won, Lost, and Tied (Right)"),
    yaxis=dict(title_text="Percent"),
    title = "Regular Season Results (Percentages)" ,
    barmode="stack",
    width = half_width,
    )
    

    if Team in color_dictionary:
        colors = color_dictionary[Team]
    else:
        colors = default_colors

    for r, c in zip(df2.response.unique(), colors):
        plot_df2 = df2[df2.response == r]
        fig1.add_trace(
        go.Bar(x=[plot_df2.year, plot_df2.layout], y=plot_df2.cnt, name=r , marker_color=c) ,
            )
        

    return fig1


def getBarChart2(Team, Year):
    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year of interest
    
    Returns
    -------
    Plotly bar chart with two bars- one showing absolute number of wins and losses stacked and 
    one showing absolute number of series wins, series ties, and series losses stacked
    """
    df = getTeamAndYears(Team, Year, Year, AsHelperFunction = True)
    
    df['SeriesTiePercent'] = df.SeriesTies/df.NumberOfSeries
    df['SeriesLossPercent']= df.SeriesLosses/df.NumberOfSeries
    df['LossPercent'] = df.Losses/df.NumberOfGames
    
    df2 = pd.DataFrame(
    dict(
        year=[Year, Year] * 3,
        layout=["Record", "Series Record"] * 3,
        response=["Win Percent", "Tie Percent", 'Loss Percent'] * 2,
        cnt=[df.WinPercent.iloc[-1], df.SeriesTiePercent.iloc[-1], df.LossPercent.iloc[-1],
        df.SeriesWinPercent.iloc[-1], 0, df.SeriesLossPercent.iloc[-1] ],
        response2=["Wins", "Ties", 'Losses'] * 2,
        cnt2=[df.Wins.iloc[-1], df.SeriesTies.iloc[-1], df.Losses.iloc[-1],
        df.SeriesWins.iloc[-1], 0, df.SeriesLosses.iloc[-1] ]
        ))
    
    fig = go.Figure()
    
    fig.update_layout(
    template="simple_white",
    xaxis=dict(title_text="Number of Games Won/Lost (Left) and Number of Series Won, Lost, and Tied (Right)"),
    yaxis=dict(title_text="Count"),
    title = "Regular Season Results (Absolute Count)",
    barmode="stack",
    width = half_width,
    )
    
    if Team in color_dictionary:
        colors = color_dictionary[Team]
    else:
        colors = default_colors
        
    for r, c in zip(df2.response2.unique(), colors):
        plot_df2 = df2[df2.response2 == r]
        fig.add_trace(
        go.Bar(x=[plot_df2.year, plot_df2.layout], y=plot_df2.cnt2, name=r , marker_color=c),
            )
    
    return fig


def getOneYearPlot(Team, Year):
    """
    Parameters
    ----------
    Team: string
        team of interest
    Year : integer
        year of interest
    
    Returns
    -------
    Plotly line chart with win and series win percent plotted against date in season.  
    """

    df = getSeasonHelperFunction(Team, Year)
    
    df = df.reset_index()    
    df.index = np.arange(1, len(df)+1)        
    df['Team_Winner'] = df['Winner'] == Team
    df['Cumulative_Wins'] = df['Team_Winner'].cumsum()
    df['WinPercent'] = df['Cumulative_Wins']/df.index
    df = df.drop(columns = ['index', 'level_0'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.Date, y=df.WinPercent, mode='lines', name='Win Percent'))
    fig.add_hline(y=0.5, line_color = 'Red')
    fig.update_yaxes(range = [.1,.9], title = 'Win Percentage')
    fig.update_layout(width = wide_width, 
                      height = plot_height, 
                      title = "Win Percentage by Date")
    return fig


#Streamlit Section

#title
st.title("Series-ly, You Have to Win Them")

st.subheader("by [MacKenzye Leroy](https://mackenzye-leroy.com)")

sidebar_selectbox = st.sidebar.radio(
    "",
    ("Home", "All-Time Results Visualized",
    "Season Over Season Results",
     "Single Season Results", "Top/Bottom 10 All-Time", 
     "Biggest Overachievers and Underachievers")
)





#Home page:


if sidebar_selectbox == "Home":

    #Introduction to whole dashboard
    st.write("""Welcome! This dashboard is the result of a fairly simple question I wasn't able to find an answer to online--which MLB teams in history won
                the highest percentage of their regular season series (as opposed to games), and was a higher series win percentage indicative of playoff success? 
                When I realized there was no easy source of data to answer this question, I got to work making my own from other sources. I began by scraping the results of 
                all MLB games going back to 1900, cleaned the data up, and then calculated how many series each team played for each season
                and how many of those they won. If you're interested in my work collecting or cleaning the data, or my more rigorous statistical analysis of whether or
                not regular series win percentage was indicative of playoff success, check out my website [mackenzye-leroy.com](https://mackenzye-leroy.com), where I cover a lot of that work.
                If you're simply interested in playing around with some of the results, you're in the right place! Use the navigation bar on the left to navigate 
                to different widgets I built with the data. Each one is briefly described below.
                """)


    st.subheader('All-Time Results Visualized')

    st.write("""
            This widget plots the winning percentage and series winning percentage of all teams since 1900, as well as which teams made the playoffs and won 
            the World Series. You can filter by year, team, whether or not a team made the playoffs, and whether or not a team won the World Series. Click 
            "All-Time Results Visualized" in the navigation bar on the left to learn more!
            """)

    st.subheader('Season Over Season Results')

    st.write("""
            This widget allows you to look up the year-over-year results for any Major League team in baseball history from 1900 to 2021. 
            Click "Season Over Season Results" in the navigation bar on the left to learn more!
            """)

    st.subheader('Single Season Results')

    st.write("""
            This widget allows you to look up a single season of game results for any given team in Major League Baseball history.
            Click "Single Season Results" in the navigation bar on the left to learn more!
            """)

    st.subheader('Top/Bottom 10 All-Time')

    st.write("""
            This widget allows you to check out the best and worst teams in MLB history in terms of regular season win percentage. 
            Click "Top/Bottom 10 All-Time" in the navigation bar on the left to learn more!
            """)

    st.subheader('Biggest Overachievers and Underachievers')

    st.write("""
            This widget allows you to check out which teams have most overperformed and underperformed their win/loss record in terms of 
            series win percentage. Click "Biggest Overachievers and Underachievers" in the navigation bar on the left to learn more!
            """)


elif sidebar_selectbox == "All-Time Results Visualized":

    


    
    teams_default = st.radio("Clear/Select Teams:", ('Select Current Teams', 'Select All Teams', 'Clear All Teams'))

    if teams_default == 'Select Current Teams':
        teams_default_result = current_teams
    elif teams_default == 'Select All Teams':
        teams_default_result = all_teams
    
    elif teams_default == 'Clear All Teams':
        teams_default_result = None

    
        
    team_input = st.multiselect("Teams", options = all_teams, default = teams_default_result)

    year_slider = st.slider("Years of Interest:", 1900, 2021, value=[1900, 2021])

    
    filteredResults = MasterYearlyResultsWithPlayoffs[MasterYearlyResultsWithPlayoffs['Year'] > year_slider[0]]
    
    WSIndex = filteredResults[filteredResults.WonWorldSeries == True]['MadePostSeason'].index
    filteredResults['MadePostSeason'] = filteredResults['MadePostSeason'] .astype('string')

    for x in WSIndex:
        filteredResults.at[x, 'MadePostSeason'] = 'True and Won World Series'

    filteredResults = filteredResults[filteredResults['Year']<year_slider[1]]
    filteredResults = filteredResults[filteredResults['Team'].isin(team_input)]
    filteredResults["WinPercent"] = filteredResults["WinPercent"].round(decimals = 3)
    filteredResults["SeriesWinPercent"] = filteredResults["SeriesWinPercent"].round(decimals = 3)
    filteredResults = filteredResults.rename(columns = {'MadePostSeason': 'Made Postseason?', 'WinPercent': 'Win Percent', 'SeriesWinPercent': 'Series Win Percent'})

    symbols = ['circle', 'diamond', 'star']
    color_sequence = ['#636EFA', '#EECA3B', '#EF553B']

    fig = px.scatter(filteredResults, x="Win Percent", y="Series Win Percent", color = "Made Postseason?", symbol = 'Made Postseason?',
                    width = 1200, height =850,
                    symbol_sequence = symbols,
                    color_discrete_sequence = color_sequence,
                    hover_data=["Team", "Year"])

    st.plotly_chart(fig)

    st.write("""
    The above graphic shows the regular season win percentage versus the regular season series win percentage of all MLB teams going back to 1900. 
    Teams represented as red diamonds made the postseason, and teams represented as gold stars won the World Series. Teams further to the right won a higher percentage of their 
    regular season games and teams higher up won a higher percentage of their regular season series. Obviously, those values are highly correlated (a team can't 
    win a lot of series without winning a lot of games), but there are still some interesting outliers. For example, the 1947 New York Yankees won over 63 percent
    of their games and ultimately won the World Series, but only about 47 percent of their regular season series. If you're interested in more outliers check out the "Biggest 
    Overachievers and Underachievers" tab on the left. We also see that while many World Series winning teams had both high win percentages and series 
    win percentages, plenty of teams with only slightly above average win percentages and series win percentages won the World Series. You can use the slider 
    above to filter years of interest and the box above to filter teams.
    \n
    
    Note: Results here include all teams since 1900 including some teams that have changed names, and some teams that no longer exist. If you're interested in learning 
    more about some of these historical teams, check out the "Season Over Season Results" tab on the left then the "Single Season Results" tab.
    """)

    


elif sidebar_selectbox == 'Season Over Season Results':

    #Title of Top Section
    st.subheader('Season Over Season Results')

    #Intro to top section
    st.write("""This widget allows you to look up the year-over-year results for any Major League team in baseball history within a selected range.
            A table with the results as well as a plot showing the team's win percentage and series win percentage during the span selected 
            will be automatically generated. You can also choose whether or not to include historical teams that may fall under this team's name. 
            For example, the New York Yankees are probably the most well-known team in baseball history. What many don't know though is that 
            they were originally founded as the Baltimore Orioles in 1901 and then changed names to the New York Highlanders from 1904 until
            1913 before ultimately landing on the world famous New York Yankees. Use the first dropdown to select whether or not you want to 
            include these historical results or not. You can also explore the results of the short-lived Federation League, 
            which existed from 1914-1915 by selecting "Federation League Teams." 
            """)

    #Team type dropdown
    Team_dropdown_type = (st.selectbox(
    'Types of Teams', 
    ['Current Teams (historical results under other names included)', 
    'Current Teams (historical results under other names excluded)',
    'All Teams', 'Federation League Teams']))

    if Team_dropdown_type == 'Current Teams (historical results under other names included)':
        team_dropdown = current_teams
        historical_results_check = True

    elif Team_dropdown_type ==  'Current Teams (historical results under other names excluded)':
        team_dropdown = current_teams
        historical_results_check = False

    elif Team_dropdown_type == 'Federation League Teams':
        team_dropdown = federation_teams
        historical_results_check = True
    
    else: 
        team_dropdown = all_teams
        historical_results_check = False

    #Select from given teams (updated when Team_dropdown_type is updated)
    Team_option_1 = st.selectbox(
        'Select a Team:',
        team_dropdown)



#include Historical results?
    if historical_results_check:
        Franchise = teams_ID_dictionary[Team_option_1]
        Year_list1 = MasterYearlyResults[MasterYearlyResults['FranID'] == Franchise].Year
    else:
        Year_list1 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_1].Year


    #Year span selecter. Updates to reflect the max/min of whaichever team is selected above
    year_slider = st.slider("Years of Interest:", 1900, 2021, value=[min(Year_list1), max(Year_list1)])

    #only return plot if more than one year selected/available
    if year_slider[0] != year_slider[1]:

        st.plotly_chart(getTeamAndYearsPlot(Team_option_1, start_year = year_slider[0], end_year=year_slider[1], historical_results = historical_results_check))

    #return table of reseults for years selected
    st.plotly_chart(getTeamAndYears(Team_option_1, start_year = year_slider[0], end_year=year_slider[1], historical_results = historical_results_check))

elif sidebar_selectbox == 'Single Season Results':

    #Single Season Results Section Section
    st.subheader('Single Season Results')

    #Introduction
    st.write("""This widget allows you to look up a single season of game results for any given team in Major League Baseball history. By default, the full regular season and playoff 
                schedule/results are returned as well as several plots. The first plot shows the win percentage of the team of interest over the course of the season. 
                The plot below on the left shows final win and loss percentage of the team in the given year as well as their final series win, loss, and tie percentage. 
                The final plot shows the final absolute count of wins and losses as well as series wins, ties, and losses for the season selected. If you are only interested 
                in playoff or regular season results, you can use the drop down below to select those. If you're only interested in the table of results or the plots, you
                can disable one or both of them with the checkboxes below. 
            """)

    #Type of Results
    results_type = st.selectbox(
        'Type Of Results',
        ['Full', 'Regular Season', 'Playoff'])


    #Include Plots? Default is True
    plots_2 = st.checkbox('Include plots?', value = True)

    #Include Table of results? Default is True
    results_2 = st.checkbox('Include game results?', value = True)

    #Select Team
    Team_option_2 = st.selectbox(
        'Select a Team: ',
        all_teams)

    #Find valid years for team selected
    Year_list2 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_2].Year
    Year_list2 = Year_list2.iloc[::-1]

    #Select Year. Only provides valid years for team selected above
    year_option = st.selectbox(
        'Select a Year:',
        Year_list2
        )

    #Check if team made playoffs for year selected
    playoffs = madePlayoffs(Team_option_2, year_option)

    if results_type == 'Playoff':
        #If team amde playoffs, allow user to look up just playoff results for year. 
        if playoffs:
            section_two_result = getOneYearPlayoffs(Team_option_2, year_option)
        else:
            section_two_result = None


    elif results_type == 'Regular Season':
        section_two_result = getOneYearRegularSeason(Team_option_2, year_option)
    else:
        section_two_result = getOneYearResultsFull(Team_option_2, year_option)

    #Get team Record list for year selected   
    record = getRecord(Team_option_2, year_option)



    #Construct results string bases on whether team made playoffs/won world series
    if playoffs:
        playoff_sentence = "qualified for the postseason"
        worldseries = wonWorldSeries(Team_option_2, year_option)
        if worldseries:
            worldseries_sentence = "and ultimately won the World Series!"
        else:
            worldseries_sentence =f"but were eliminated by the {record[3]}."
    else:
        playoff_sentence = 'did not qualify for the postseason.'
        worldseries_sentence = ''


    #Write result string
    Info = f"In {year_option}, the {Team_option_2} won {record[0]} games and lost {record[1]} for an overall win percentage of {record[2]}. They {playoff_sentence} {worldseries_sentence}"

    #Return result string
    st.subheader(Info)

    #If plots box checked, generate win percentage plot and both bar charts
    if plots_2:

        st.plotly_chart(getOneYearPlot(Team_option_2, year_option))

        col1, col2 = st.columns(2)

        col1.plotly_chart(getBarChart1(Team_option_2, year_option))

        col2.plotly_chart(getBarChart2(Team_option_2, year_option))

    #If results table box checked, return result (if valid)
    if results_2:
        if section_two_result != None:
            st.plotly_chart(section_two_result)


elif sidebar_selectbox == "Top/Bottom 10 All-Time":

    st.write("""Since this project started with the simple question of which teams in baseball won the highest percentage of their regular season series,
    it seems right to dedicate a section to those teams. The top table below shows the top 10 teams in MLB history in terms of series win percentage and 
    the bottom chart shows the bottom 10 (the teams with the worst series win percentages in MLB history). If you're interested in learning more about
    one or more of these incredible (or pitiful) seasons, be sure to make a note of the team name and year then head over to the "Singe Season Results" tab, 
    where you can look up those respective seasons and learn more.""")

    st.subheader('Top 10 All-Time')

    top10 = MasterYearlyResultsWithPlayoffs.sort_values(by = ['SeriesWinPercent'], ascending = False).head(10)
    top10 = top10.drop(columns = ['Unnamed: 0', 'LossPercent', 'SeriesLossPercent', 'SeriesTiePercent', 'LossDifference', 'FranID', 'Difference'])
    top10 = top10.rename(columns = {'NumberOfGames': 'Number Of Games', 'NumberOfSeries': 'Number Of Series', 'SeriesWins': 'Series Wins', 
                                                        'SeriesLosses': 'Series Losses', 'SeriesTies': 'Series Ties', 'WinPercent': 'Win Percent', 
                                                        'SeriesWinPercent': 'Series Win Percent', 'MadePostSeason': 'Made Postseason?', 'WonWorldSeries': 'Won World Series?'})
    top10 = top10.reset_index(drop=True)
    top10.index = np.arange(1,len(top10)+1)


    st.table(top10)

    st.subheader('Bottom 10 All-Time')

    bottom10 = MasterYearlyResultsWithPlayoffs.sort_values(by = ['SeriesWinPercent'], ascending = True).head(10)
    bottom10 = bottom10.drop(columns = ['Unnamed: 0', 'LossPercent', 'SeriesLossPercent', 'SeriesTiePercent', 'LossDifference', 'FranID', 'Difference'])
    bottom10= bottom10.rename(columns = {'NumberOfGames': 'Number Of Games', 'NumberOfSeries': 'Number Of Series', 'SeriesWins': 'Series Wins', 
                                                        'SeriesLosses': 'Series Losses', 'SeriesTies': 'Series Ties', 'WinPercent': 'Win Percent', 
                                                        'SeriesWinPercent': 'Series Win Percent', 'MadePostSeason': 'Made Postseason?', 'WonWorldSeries': 'Won World Series?'})
    bottom10 = bottom10.reset_index(drop=True)
    bottom10.index = np.arange(1,len(bottom10)+1)

    st.table(bottom10)

elif sidebar_selectbox == 'Biggest Overachievers and Underachievers':

    st.write("""The following charts are all about outliers or teams that had unusually large differences in their  win percentages and their 
    series win percentages (regular season). I classified an overachiever as a team that won a higher percentage of their regular season series than their regular season games. 
    In all of MLB history, there have only been 172 such teams (out of over 2500 total teams!). Among that already select group, the top chart below shows the 10 teams with 
    the biggest differences in series win percentage and win percentage. I've crowned these teams as the biggest overachievers in MLB history. These teams were abnormally good at winning 
    series given their overall record. On the flip side, the bottom chart shows the 10 teams in MLB history with the largest difference in win percentage 
    and series win percenatge in the other direction--teams that won a much higher percentage of their games than their series. If you're interested in learning more about
    one or more of these unusual seasons, be sure to make a note of the team name and year then head over to the "Singe Season Results" tab, where you can look up those
    respective seasons and learn more.""")

    st.subheader('Biggest Overachievers')

    overAchievers = MasterYearlyResultsWithPlayoffs.sort_values(by = ['Difference'], ascending = False).head(10)
    overAchievers = overAchievers.drop(columns = ['Unnamed: 0', 'LossPercent', 'SeriesLossPercent', 'SeriesTiePercent', 'LossDifference', 'FranID'])
    overAchievers = overAchievers.rename(columns = {'NumberOfGames': 'Number Of Games', 'NumberOfSeries': 'Number Of Series', 'SeriesWins': 'Series Wins', 
                                                        'SeriesLosses': 'Series Losses', 'SeriesTies': 'Series Ties', 'WinPercent': 'Win Percent', 
                                                        'SeriesWinPercent': 'Series Win Percent', 'MadePostSeason': 'Made Postseason?', 'WonWorldSeries': 'Won World Series?'})
    overAchievers = overAchievers.reset_index(drop=True)
    overAchievers.index = np.arange(1,len(overAchievers)+1)
    st.table(overAchievers)

    st.subheader('Biggest Underachievers')

    underAchievers = MasterYearlyResultsWithPlayoffs.sort_values(by = ['Difference'], ascending = True).head(10)
    underAchievers = underAchievers.drop(columns = ['Unnamed: 0', 'LossPercent', 'SeriesLossPercent', 'SeriesTiePercent', 'LossDifference', 'FranID'])
    underAchievers = underAchievers.rename(columns = {'NumberOfGames': 'Number Of Games', 'NumberOfSeries': 'Number Of Series', 'SeriesWins': 'Series Wins', 
                                                        'SeriesLosses': 'Series Losses', 'SeriesTies': 'Series Ties', 'WinPercent': 'Win Percent', 
                                                        'SeriesWinPercent': 'Series Win Percent', 'MadePostSeason': 'Made Postseason?', 'WonWorldSeries': 'Won World Series?'})
    underAchievers = underAchievers.reset_index(drop=True)
    underAchievers.index = np.arange(1,len(underAchievers)+1)
    st.table(underAchievers)



#final contact note
st.write('')
st.write('Have a question? Reach out to me! You can find contact info on my website [mackenzye-leroy.com](https://mackenzye-leroy.com)')



