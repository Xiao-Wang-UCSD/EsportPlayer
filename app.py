import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

st.title("If You Want to be an Esports Player")

@st.cache
def get_data(name):
    if name == 'market':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/market-chart-data.csv")
    if name == 'pie':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/pie-chart-data.csv")
    if name == 'line':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/line-chart-data.csv")
    if name == 'radar':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/radar-chart-data.csv")
    if name == 'prize':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/prize-chart-data.csv")
    if name == 'full':
        return pd.read_csv("https://raw.githubusercontent.com/Xiao-Wang-UCSD/EsportPlayer/master/data/full-chart-data.csv")

# Config
title_config = {
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        }


# Show the full dataframe
raw_data_button = st.checkbox('Show Raw Data')
show=st.checkbox('Show Script')
full_df = get_data('full')
if raw_data_button:
    st.header("Overview")
    st.write(full_df)

# Show the market chart

legend_config = {
        'traceorder':"normal",
        'font':{
            'size':14
            }
        }

xaxis_config = {
        'tickmode':'linear',
        'title':'Year'
        }
yaxis_config = {
        "title":'Revenue(MM)'
        }
if show:
    st.header("Story Background")
    st.write('')
    
    st.write('Background: Hank has been a pro player in many games since high school. He saw esports is booming and he wants to be a professional player. His best friend, Sean, will help him decide which game to play using data visualization.')
    st.write('Here begins the conversation...')
    st.write("Hank: Bro, you know me. I always enjoy playing games and my dream is to make a living on it. A lot of pro gamers became famous in esports and started to make a lot of money. I am jealous. So, how’s the market? Is it really growing fast? ")
    st.write("Sean: Oh, man, it’s booming and it’s going to keep rapidly growing in the next few years. Look at the chart and see how crazy it is growing? ")
market_df = get_data('market')[['Revenue','Year']]

st.markdown('---')
st.header("Understand the Market")
selected_df = market_df
selected_df = selected_df.dropna()

poly = PolynomialFeatures(degree=2)
X_ = poly.fit_transform(np.array(selected_df['Year']).reshape(-1,1))
reg = LinearRegression().fit(X_,np.array(selected_df['Revenue']))
predict = reg.predict(X_)

fig=go.Figure()
fig.add_trace(go.Bar(name='Total Market Size', x=selected_df['Year'], y=selected_df['Revenue']))
fig.add_trace(go.Scatter(name='2nd Polynomial Line', x=selected_df['Year'], y=predict))



fig.update_layout(
    title=title_config,
    xaxis=xaxis_config,
    yaxis=yaxis_config,
    legend=legend_config
    )
st.plotly_chart(fig)

# Show the pie chart
if show:
    st.write("Hank: Wow, that’s great. What a great opportunity for me to start a career in esports! But what game should I focus on?")
    st.write("Sean: That really depends on what you are good at. But I will walk you through the most popular ones and you can probably make a choice after.")
    st.write("Hank: Thanks, bro. You are really helping me a lot. ")
    st.write("Sean: Look at the first pie chart. It shows the player population. The larger the area is, the more popular the game is.")
legend_config = {
        'x':0.8,
        'y':-0.4,
        'traceorder':"normal",
        'font':{
            'size':14
            }
        }

pie_df = get_data('pie')
st.markdown('---')
st.header("Which Game is the Most Popular?")
years = tuple(pie_df['Year'].unique()) 
values = st.selectbox("Select Year",years)
selected_df = pie_df.where(pie_df['Year']==values)
selected_df = selected_df.dropna()
f = px.pie(selected_df, values='Players', names='Name', title='Player Population')
f.update_layout(
    title=title_config,
    legend=legend_config
    )

colors = None#['rgb(100,113,242)', 'rgb(222,96,70)', 'rgb(92,201,154)', 'rgb(161,107,242)']
f.update_traces(
    hoverinfo='label+percent',
    textfont_size=14,
    textfont_color='white',
    marker={
        'colors':colors, 
        'line':{
            'color':'white',
            'width':1
            }
            },
    textposition='inside'
    )
st.plotly_chart(f)

if show:
    st.write("Hank: Wow. I have never realized that LOL is way more popular than the rest. With these many players, there must be a lot of tournaments I can show off at. Since LOL is the most popular, I guess it has the most tournament opportunities, right?")
    st.write("Sean: Not really. Look at this chart. It shows the number of tournaments each game has every year.")

# Show the line chart
line_df = get_data('line')[['Name','Tournaments#','Year']]
st.markdown('---')
st.header("Opportunities")
game = ['All']
game += list(line_df['Name'].unique())
values = st.selectbox("Select Game",game)

if values != 'All':
    selected_df = line_df.where(line_df['Name']==values)
    selected_df = selected_df.dropna()
else:
    selected_df = line_df
    selected_df = selected_df.dropna()

f = px.line(selected_df, x="Year", y="Tournaments#",title='Tournament per Year',color='Name')
f.update_layout(
    title=title_config,
    xaxis=xaxis_config,
    yaxis={
        "title":'Tournaments'
        #'range':[20,180]
        #,'rangemode':"tozero"
    },
    legend_title_text='',
    legend = {'x':1.05,'y':1.03,'font':{
            'size':14
            }
        }
    )
st.plotly_chart(f)

# Show the chart for total prize
if show:
    st.write("Hank: Interesting. It looks like CS: GO has the most tournaments. And it is also the least popular?")
    st.write("Sean: Yeah that is big data man. CS:GO actually has the best esports environment so it has many competitions. There are so many opportunities for young gamers like you.")
    st.write("Hank: That really makes sense. Thank you a lot bro! I think I can simply choose CS:GO as the start of my career since I can win tons of money from these tournaments.")
    st.write("Sean: Not so hurry boi. If you are interested in money, then let’s talk about the sexiest. Look at this chart, it shows the actual prize pool each game has every year. Dota2 is the most generous and they gave out over 30M dollars!")


xaxis_config = {
        'title':'Game'
        }


prize_df = get_data('prize')[['Name','Total Prize Pool','Year']]
st.markdown('---')
st.header("Let the Money Talk")
values = st.selectbox("Select Year ",years)
selected_df = prize_df.where(prize_df['Year']==str(values))
selected_df = selected_df.dropna()
f = px.bar(selected_df, x="Name", y = 'Total Prize Pool',title = 'Total Prize Pool',color='Name')
f.update_layout(
    title=title_config,
    yaxis={
        "title":'Total Prize',
        'rangemode':"tozero"
    },
    xaxis=xaxis_config,
    )
st.plotly_chart(f)

# Show the radar chart
if show:
    st.write("Hank: Wow! No wonder why professional Dota gamers like Puppey are so rich! But, wait, this is really confusing. Dota2 has the least tournaments but it has the largest rewards? Should I be a professional Dota2 player then?")
    st.write("Sean: Well, that also means it can be quite competitive. To really make the best decision, we need a bigger picture! Let’s look at this radar chart I made for you! So this radar chart has five aspects, Player growth, Average earning, Professional rate(It’s basically how hard it is to become a professional player), Total prize each year, and Total tournaments. The larger the number, the better for you.")
    st.write("Hank: Wow. This chart really helps me a lot. But I still need to spend more time considering my option. ")

title_config = {
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'text':'ok'
        }

legend_config = {
        'x':0.8,
        'y':-0.4,
        'traceorder':"normal",
        'font':{
            'size':14
            }
        }

def show_radar_all(selected_df):
    selected_df = selected_df.copy()
    fig = go.Figure()
    for i in selected_df['Name'].unique():
        temp = selected_df.where(selected_df['Name']==i)
        temp = temp.dropna().drop(columns=['Name'])
        temp = temp.T.reset_index(drop=False)
        temp.columns = ['feature','value']
        fig.add_trace(go.Scatterpolar(
            r=temp['value'],
            theta=temp['feature'],
            fill='toself',
            name=i
        ))

    fig.update_layout(
        title=title_config,
        polar=dict(
            radialaxis=dict(
            range=[0, 5]
            )),
        legend=legend_config    
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig)


radar_df = get_data('radar')
st.markdown('---')
st.header("Make a Better Decision")
game = ['All']
game+=list(radar_df['Name'].unique())
values = st.selectbox("Select Game ",game)

title_config['text'] = values

if values=='All':
    show_radar_all(radar_df)
else:
    selected_df = radar_df.where(radar_df['Name']==values)
    selected_df = selected_df.dropna()
    show_radar_all(selected_df)

if show:
    st.write("Sean: Dude, I made a small recommendation system for you. Just answer the questions and I will recommend to you which game you should play professionally.")
    
# Survey section
st.markdown('---')
st.header("Mini Recommendation System")

q4_str = "Do you like to participate in many small competitions or just a few big ones?"
q4_selection = {'Many small ones':0,'A good mixture':1,'A few big ones':2}

q2_str = "What if esports is your only income source?"
q2_selection = {"No, that is too risky":0,'Not sure':1,'Sure, I am all-in':2}

q3_str = "Do you care about playing a trendy game?"
q3_selection = {"Absolutely, if it's not trendy, I won't play":0,'I dont care':1}

q1_str = "Are you very good at FPS game?"
q1_selection = {'I am born for it':0,'Very good':1,'Not where my best is at':2}


q1 = st.radio(q1_str,list(q1_selection))
q2 = st.radio(q2_str,list(q2_selection))
q3 = st.radio(q3_str,list(q3_selection))
q4 = st.radio(q4_str,list(q4_selection))

def calculate_score(q1_value,q2_value,q3_value,q4_value):

    game_dic = {'Dota2':0,'CS:GO':0,'LOL':0,'Overwatch':0}

    if q1_selection[q1_value]==0:
        game_dic['CS:GO']+=2
        #game_dic['LOL']+=1
        game_dic['Overwatch']+=2
    elif q1_selection[q1_value]==1:
        game_dic['CS:GO']+=1
        game_dic['LOL']+=1
        game_dic['Overwatch']+=1
        game_dic['Dota2']+=1
    else:
        game_dic['Dota2']+=2
        game_dic['LOL']+=2

    if q2_selection[q2_value]==0:
        game_dic['CS:GO']+=2
        game_dic['LOL']+=1
        game_dic['Overwatch']+=1
    elif q2_selection[q2_value]==1:
        game_dic['LOL']+=1
        game_dic['Overwatch']+=1
        game_dic['CS:GO']+=1
    else:
        game_dic['Dota2']+=2

    if q3_selection[q3_value]==0:
        game_dic['LOL']+=0.5
        game_dic['CS:GO']+=0.25
        game_dic['Overwatch']-=0.5
        game_dic['Dota2']-=0.5
    elif q3_selection[q3_value]==1:
        game_dic['LOL']+=1
        game_dic['Overwatch']+=1
        game_dic['CS:GO']+=1
        game_dic['Dota2']+=1
    if q4_selection[q4_value]==0:
        game_dic['CS:GO']+=2
        #game_dic['LOL']+=1
        #game_dic['Overwatch']+=1
    elif q4_selection[q4_value]==1:
        game_dic['CS:GO']+=1
        game_dic['LOL']+=2
        game_dic['Overwatch']+=2
        game_dic['Dota2']+=1
    else:
        game_dic['Dota2']+=2
    return max(game_dic, key=game_dic.get)

recommended = calculate_score(q1,q2,q3,q4)

recommend_msg = "You should play "

recommend_button = st.button('Recommend for me')
if recommend_button:
    st.success(recommend_msg+recommended+'!')

reference_data_button = st.checkbox('Show Reference')
if reference_data_button:
    st.markdown('---')
    st.header('Reference')
    st.write('https://steamcharts.com/app/570#All')
    st.write('https://www.statista.com/statistics/618035/number-gamers-overwatch-worldwide/')
    st.write('https://www.statista.com/topics/4266/league-of-legends/')
    st.write('https://www.statista.com/statistics/607472/dota2-users-number/')
    st.write('https://www.statista.com/statistics/808922/csgo-users-number/')

