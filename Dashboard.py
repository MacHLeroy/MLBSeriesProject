
#Imports
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup, NavigableString
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator 
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import chart_studio
import streamlit as st

st.set_page_config(layout="wide")

#title
st.title('Fucking Around with Baseball Nonsense')

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
    Results = Results.drop(columns = ['index', 'Unnamed: 0'])
    

    
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
        spacer_row = ['-', '-', 'Playoff', '-', 'Results', '-', '-', '-', '-']
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

    
        df = df.drop(columns = ['index', 'level_0'])
    

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
        print('No Playoffs in year selected')
           
    if len(playoff_df) == 0:
        if AsHelper == True:
            return playoff_df
        else:
            print("Team Did Not Qualify for Playoffs in Year Provided")

    else:
        
        playoff_df = playoff_df.reset_index()    
        playoff_df.index = np.arange(1, len(playoff_df)+1)
    
        playoff_df['Team_Winner'] = playoff_df['Winner'] == Team
        playoff_df['Cumultive_Wins'] = playoff_df['Team_Winner'].cumsum()
        playoff_df['WinPercent'] = playoff_df['Cumultive_Wins']/playoff_df.index
        playoff_df.Date = pd.DatetimeIndex(playoff_df.Date).strftime("%m-%d-%Y")
        
        playoff_df['WinPercent'] = playoff_df['WinPercent'].round(decimals = 3)
        playoff_df = playoff_df.drop(columns = ['index', 'level_0', 'Season'])
    
        if playoff_df.Team_Winner.iloc[-1] == True:
                
            final_row = ['-', '-', 'Won', 'World', 'Series', '!', '!', '!', '-']
        else: 
            final_row = ['Elimainated', 'in', 'Playoffs','-', '-', '-', '-', '-', '-']
        playoff_df.loc['--'] = final_row
        
        #playoff_df.Date = pd.DatetimeIndex(playoff_df.Date).strftime("%m-%d-%Y")
        
        if AsHelper == False:
            table = ff.create_table(playoff_df)
    
            return table
    
        else:
            return playoff_df

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
    

    
    colors = ["#636EFA", '#BAB0AC', "#EF553B" ]
    
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
    
    colors = ["#636EFA", '#BAB0AC', "#EF553B" ]
        
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
    fig.update_layout(width = 1450)
    return fig



st.subheader('Season Over Season Results')

st.write('Instructions')

Team_option_1 = st.selectbox(
    'Select a Team:',
    pd.Series(MasterYearlyResults.Team.unique())
     )

Year_list1 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_1].Year

year_slider = st.slider("Double ended slider", 1900, 2021, value=[min(Year_list1), max(Year_list1)])

st.plotly_chart(getTeamAndYearsPlot(Team_option_1, start_year = year_slider[0], end_year=year_slider[1]))

st.plotly_chart(getTeamAndYears(Team_option_1, start_year = year_slider[0], end_year=year_slider[1]))

Team_option_2 = st.selectbox(
    'Select a Team: ',
    TeamsAndYears.Team)

st.subheader('Single Season Results')

st.write('Add Instructions/explanation')

Year_list2 = MasterYearlyResults[MasterYearlyResults['Team'] == Team_option_2].Year

year_option = st.selectbox(
    'Select a Year:',
    Year_list2
     )

st.plotly_chart(getOneYearPlot(Team_option_2, year_option))

col1, col2 = st.columns(2)

col1.plotly_chart(getBarChart1(Team_option_2, year_option))

col2.plotly_chart(getBarChart2(Team_option_2, year_option))

st.plotly_chart(getOneYearResultsFull(Team_option_2, year_option))