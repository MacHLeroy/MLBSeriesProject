
#Imports
import numpy as np
import pandas as pd
#import requests
#from bs4 import BeautifulSoup, NavigableString
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator 
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
#import chart_studio
import streamlit as st

st.set_page_config(layout="wide")

#title
st.title('Baseball Dashboard')



#Set up lists/Dictionsaries for queries

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


all_teams = []
federation_teams = []
for key in teams_ID_dictionary:
    all_teams.append(key)
    if teams_ID_dictionary[key][0:3] == 'Fed':
        federation_teams.append(key)

all_teams.sort()
federation_teams.sort()
current_teams.sort()

#Load in Data

@st.cache
def load_data1():
    MasterYearlyResults = pd.read_csv('YearlyResultsMaster.csv')
    MasterYearlyResults['WinPercent'] = MasterYearlyResults ['Wins']/ MasterYearlyResults ['NumberOfGames']
    MasterYearlyResults['SeriesWinPercent'] = MasterYearlyResults ['SeriesWins']/ MasterYearlyResults ['NumberOfSeries']
    MasterYearlyResults['WinPercent'] = MasterYearlyResults ['Wins']/ MasterYearlyResults ['NumberOfGames']
    MasterYearlyResults['SeriesWinPercent'] = MasterYearlyResults ['SeriesWins']/ MasterYearlyResults ['NumberOfSeries']

    return MasterYearlyResults

@st.cache
def load_data2():
    workingdf = pd.read_csv('LeagueGameResults.csv')
    workingdf['Winner'] = np.where(workingdf['Home_Team_Score'] > workingdf['Away_Team_Score'] , workingdf['Home_Team'], workingdf['Away_Team'])
    workingdf['Date'] = pd.to_datetime(workingdf["Date"])
    workingdf['Season'] = pd.DatetimeIndex(workingdf['Date']).year
    return workingdf


@st.cache
def load_data3():
    PostSeasonMarkerDF = pd.read_csv('PostSeasonStartDates.csv')
    PostSeasonMarkerDF = PostSeasonMarkerDF.set_index('Season')
    return PostSeasonMarkerDF


@st.cache
def load_data4():
    WSChampsDF = pd.read_csv('WSChamps.csv')
    return WSChampsDF

@st.cache
def load_data5():
    TeamsAndYears = pd.DataFrame(workingdf.groupby(by=["Home_Team"]).agg({'Season': ['min', 'max']}).to_records())
    TeamsAndYears = TeamsAndYears.rename(columns = {"('Season', 'min')": 'Season_Min',  "('Season', 'max')": 'Season_Max', 'Home_Team': 'Team'})
    return TeamsAndYears

@st.cache
def load_data6():
    TeamsAndYearsFull = pd.DataFrame(workingdf.groupby(by=["Home_Team", "Season"]).agg({'Season': ['max']}).to_records())
    TeamsAndYearsFull = TeamsAndYearsFull.rename(columns={'Home_Team': 'Team'})
    return TeamsAndYearsFull

data_load_state = st.text('Loading data...')
MasterYearlyResults = load_data1()
workingdf = load_data2()
PostSeasonMarkerDF = load_data3()
WSChampsDF = load_data4()
TeamsAndYears = load_data5()
TeamsAndYearsFull = load_data6()
data_load_state.text("Data Loaded!")



def getTeamAndYears(Team, start_year = None, end_year = None, historical_results = True, AsHelperFunction = False):
    
    if historical_results:
        FranID = teams_ID_dictionary[Team]
    
        TeamInQuotes= "'" + FranID + "'"
        query = "FranID == " + TeamInQuotes
        Results = MasterYearlyResults.query(query)
        Results = Results.sort_values(by = 'Year')

    else:
        
        TeamInQuotes= "'" + Team + "'"
        query = "Team == " + TeamInQuotes
        Results = MasterYearlyResults.query(query)

    
    if start_year == None:
        start_year = Results['Year'].iloc[0]
    
    if end_year == None:
        end_year = Results['Year'].iloc[-1]
    
    Results = Results[Results['Year'] >= start_year]
    Results = Results[Results['Year'] <= end_year]

    
    Results = Results.reset_index()
    Results = Results.drop(columns = ['index', 'Unnamed: 0', 'FranID'])
    

    
    total_row = [ 'Total:', '-', Results.NumberOfGames.sum(),  Results.Wins.sum(),  Results.Losses.sum(),
                Results.NumberOfSeries.sum(), Results.SeriesWins.sum(),  Results.SeriesLosses.sum(),
                Results.SeriesTies.sum(), (Results.Wins.sum()/Results.NumberOfGames.sum()),
                (Results.SeriesWins.sum()/Results.NumberOfSeries.sum())]
                


    Results.loc['Total:'] = total_row
    
    Results['WinPercent'] = Results['WinPercent'].round(decimals = 3)
    Results['SeriesWinPercent'] = Results['SeriesWinPercent'].round(decimals = 3) 
    
    
    
    if AsHelperFunction == False:
        table = ff.create_table(Results)
        table.update_layout(width=1450)
        
    
        return table
    
    else:
        return Results


def getTeamAndYearsPlot(Team, start_year = None, end_year = None, historical_results = True, AsHelperFunction = False):

    Results = getTeamAndYears(Team, start_year, end_year, AsHelperFunction=True)

    if start_year != end_year: 
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Results.Year, y=Results.SeriesWinPercent,
                mode='lines',
                name='Series Win Percent'))
        fig.add_trace(go.Scatter(x=Results.Year, y=Results.WinPercent,
                mode='lines',
                name='Win Percent',
                line_color = '#2ca02c'))
        fig.add_hline(y=0.5, line_color = 'Red')
        fig.update_yaxes(range = [.2,.8])  
        fig.update_layout(width=1450)
    return fig
    
def getSeasonHelperFunction(Team, Year):
    TeamInQuotes= "'" + Team + "'"
    query1 = "Home_Team == " + TeamInQuotes + " | Away_Team == " + TeamInQuotes

    df1 = workingdf.query(query1)
    df1 = df1.reset_index()

    query2 = "Season == " + str(Year)
    df1 = df1.query(query2)
    
    return df1


def getOneYearResultsFull(Team, Year, plot = False):
    
    df = getOneYearRegularSeason(Team, Year, Plot=plot, AsHelper = True)
    playoff_df = getOneYearPlayoffs(Team, Year, AsHelper = True)
    
       
    if len(playoff_df) == 0:
        final_row = ['-', '-', 'Did', 'Not', 'Make', 'Playoffs', '-', '-', '-']
        df.loc['-'] = final_row
    else:
        spacer_row = ['Playoff', '-', '-', 'Results', '-', '-', '-', '-', '-']
        df.loc['-'] = spacer_row
        df = pd.concat([df, playoff_df], ignore_index=False)
        
    table = ff.create_table(df)
    table.update_layout(width=1450)
    
    return table



def getOneYearRegularSeason(Team, Year, Plot = True, AsHelper = False):
    
    df = getSeasonHelperFunction(Team, Year)
        
    if len(df) == 0:
        print('Invalid Year for Team Given. Please Try Again')
            
    else: 
    
        Result = getTeamAndYears(Team, Year, Year, AsHelperFunction = True)
    
        Result['SeriesTiePercent'] = Result.SeriesTies/Result.NumberOfSeries
        Result['SeriesLossPercent']= Result.SeriesLosses/Result.NumberOfSeries
        Result['LossPercent'] = Result.Losses/Result.NumberOfGames
    
        noPostSeasonList = [1900, 1901, 1902, 1903, 1904, 1994]
        if Year not in noPostSeasonList:
            postSeasonCheck = PostSeasonMarkerDF.loc[Year][0]
            playoff_df = df[df.Date >= postSeasonCheck]
            df = df[df.Date < postSeasonCheck]
        
     
        df = df.reset_index()    
        df.index = np.arange(1, len(df)+1)
    
            
        df['Team_Winner'] = df['Winner'] == Team
        df['Cumultive_Wins'] = df['Team_Winner'].cumsum()
        df['WinPercent'] = df['Cumultive_Wins']/df.index

    
        df = df.drop(columns = ['index', 'level_0', 'Home_FranID', 'Away_FranID'])
    

        if Plot == True:
            regSeasonBarCharts(Result, Year)
                
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=df.Date, y=df.WinPercent,
                mode='lines',
                name='Win Percent'))
            fig3.add_hline(y=0.5, line_color = 'Red')
            fig3.update_yaxes(range = [.1,.9], title = 'Win Percentage')
            fig3.show()
            
 
            
        df['WinPercent'] = df['WinPercent'].round(decimals = 3)
        df = df.drop(columns = 'Season')
            
            
        df.Date = pd.DatetimeIndex(df.Date).strftime("%m-%d-%Y")
        if AsHelper == False:
            table = ff.create_table(df)
            return table
        else: return df


def getOneYearPlayoffs(Team, Year, AsHelper = False):
    
    playoff_df = getSeasonHelperFunction(Team, Year)
       
    noPostSeasonList = [1900, 1901, 1902, 1903, 1904, 1994]
    if Year not in noPostSeasonList:
        postSeasonCheck = PostSeasonMarkerDF.loc[Year][0]
        playoff_df = playoff_df[playoff_df.Date >= postSeasonCheck]
    else: 
        postSeasonCheck = '2099-01-01'
        playoff_df = playoff_df[playoff_df.Date >= postSeasonCheck]
        return ('No Playoffs in Year Provided')
           
    if len(playoff_df) == 0:
        if AsHelper == True:
            return playoff_df
        else:
            return "Team Did Not Qualify for Playoffs in Year Provided"

    else:
        
        playoff_df = playoff_df.reset_index()    
        playoff_df.index = np.arange(1, len(playoff_df)+1)
    
        playoff_df['Team_Winner'] = playoff_df['Winner'] == Team
        playoff_df['Cumultive_Wins'] = playoff_df['Team_Winner'].cumsum()
        playoff_df['WinPercent'] = playoff_df['Cumultive_Wins']/playoff_df.index
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
            table = ff.create_table(playoff_df)
    
            return table
    
        else:
            return playoff_df


def madePlayoffs(Team, Year):
     
    df = getOneYearPlayoffs(Team, Year, AsHelper = True)
        
    if len(df) != 0:
        return True
    else:
        return False

def wonWorldSeries(Team, Year):
     
    df = getOneYearPlayoffs(Team, Year, AsHelper = True)
        
    if len(df) == 0:
        return False
    elif isinstance(df, str):
        return df
    else:
        if df.Team_Winner.iloc[-2] == True:
            return True
        else:
            return False

def getRecord(Team, Year):
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
    xaxis=dict(title_text="Regular Season Results "),
    yaxis=dict(title_text="Percent"),
    barmode="stack",
    width = 650,
    )
    

    if Team in color_dictionary:
        colors = color_dictionary[Team]
    else:
        colors = default_colors

    for r, c in zip(df2.response.unique(), colors):
        plot_df2 = df2[df2.response == r]
        fig1.add_trace(
        go.Bar(x=[plot_df2.year, plot_df2.layout], y=plot_df2.cnt, name=r , marker_color=c),
            )
        

    return fig1


def getBarChart2(Team, Year):
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
    xaxis=dict(title_text="Regular Season Results "),
    yaxis=dict(title_text="Count"),
    barmode="stack",
    width = 650,
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
    df = getSeasonHelperFunction(Team, Year)
    
    df = df.reset_index()    
    df.index = np.arange(1, len(df)+1)        
    df['Team_Winner'] = df['Winner'] == Team
    df['Cumultive_Wins'] = df['Team_Winner'].cumsum()
    df['WinPercent'] = df['Cumultive_Wins']/df.index
    df = df.drop(columns = ['index', 'level_0'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.Date, y=df.WinPercent, mode='lines', name='Win Percent'))
    fig.add_hline(y=0.5, line_color = 'Red')
    fig.update_yaxes(range = [.1,.9], title = 'Win Percentage')
    fig.update_layout(width = 1450, height = 450)
    return fig

st.write('Introduction')

st.subheader('Season Over Season Results')

st.write("""This widget allows you to look up the year over year results for any major league team in baseball history within a selected range.
            A table with the results as well as a plot showing the team's win percentage and series win percentage during the span selected. 
            will be automatically generated. You can also choose whether or not to include historical teams that may fall under this team's name. 
            For example, the New York Yankes are probably the most well known team in baseball history. But what many don't know is that 
            they were originally founded as the Baltimore Orioles in 1901 and then changed names to the New York Highlanders from 1904 until
            1913 before ultimately landing on the world famous New York Yankees. Use the first dropdown to select whether or not you want to included these results. 
            """)

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

Team_option_1 = st.selectbox(
    'Select a Team:',
    team_dropdown)



#historical_results_check = st.checkbox('Include historical results under other names?')

if historical_results_check:
    Franchise = teams_ID_dictionary[Team_option_1]
    Year_list1 = MasterYearlyResults[MasterYearlyResults['FranID'] == Franchise].Year
else:
    Year_list1 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_1].Year

#historical_results_check = st.checkbox('Include historical results under other names?')

year_slider = st.slider("Years of Interest:", 1900, 2021, value=[min(Year_list1), max(Year_list1)])

st.plotly_chart(getTeamAndYearsPlot(Team_option_1, start_year = year_slider[0], end_year=year_slider[1], historical_results = historical_results_check))

st.plotly_chart(getTeamAndYears(Team_option_1, start_year = year_slider[0], end_year=year_slider[1], historical_results = historical_results_check))

st.subheader('Single Season Results')

st.write("""This widget allows you to look up a single season for any given team in Major League Baseball History. By default the full regular season and playoff 
            schedule/results are returned as well as serveral plots and a quick season summary. 
            """)

results_type = st.selectbox(
    'Type Of Results',
    ['Full', 'Regular Season', 'Playoff'])



plots_2 = st.checkbox('Include plots?', value = True)

results_2 = st.checkbox('Include Game Results?', value = True)

Team_option_2 = st.selectbox(
    'Select a Team: ',
    all_teams)

Year_list2 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_2].Year
Year_list2 = Year_list2.iloc[::-1]

year_option = st.selectbox(
    'Select a Year:',
    Year_list2
     )


if results_type == 'Playoff':
    
    section_two_result = getOneYearPlayoffs(Team_option_2, year_option)
    
elif results_type == 'Regular Season':
    section_two_result = getOneYearRegularSeason(Team_option_2, year_option)
else:
    section_two_result = getOneYearResultsFull(Team_option_2, year_option)

    
record = getRecord(Team_option_2, year_option)

playoffs = madePlayoffs(Team_option_2, year_option)


if playoffs:
    playoff_sentence = "qualified for the postseason"
    worldseries = wonWorldSeries(Team_option_2, year_option)
    if worldseries:
        worldseries_sentence = "and ultimately won the World Series!"
    else:
        worldseries_sentence =f"but were eliminated by the {record[3]}."
else:
    playoff_sentence = 'did not qualify for the postseason'
    worldseries_sentence = '.'



Info = f"In {year_option} the {Team_option_2} won {record[0]} games and lost {record[1]} for an overall win percentage of {record[2]}. They {playoff_sentence} {worldseries_sentence}"

st.write(Info)

if plots_2:

    st.plotly_chart(getOneYearPlot(Team_option_2, year_option))

    col1, col2 = st.columns(2)

    col1.plotly_chart(getBarChart1(Team_option_2, year_option))

    col2.plotly_chart(getBarChart2(Team_option_2, year_option))

if results_2:
    st.plotly_chart(section_two_result)


