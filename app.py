import pandas as pd
import streamlit as st
import plotly.express as px

st.title("If you want to be an esport player")

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
full_df = get_data('full')
st.header("Overview")
st.write(full_df)

# Show the market chart


xaxis_config = {
        'tickmode':'linear'
        }
yaxis_config = {
        "title":'Revenue(MM)'
        }

market_df = get_data('market')[['Revenue','Year']]
st.header("Market Chart")
selected_df = market_df
selected_df = selected_df.dropna()
f = px.bar(selected_df, x="Year", y = 'Revenue',title = 'Total Market Pool')
f.update_layout(
    title=title_config,
    xaxis=xaxis_config,
    yaxis=yaxis_config
    )
st.plotly_chart(f)

# Show the pie chart

legend_config = {
        'x':0.8,
        'y':-0.4,
        'traceorder':"normal",
        'font':{
            'size':15
            }
        }

pie_df = get_data('pie')
st.header("Pie Chart")
years = tuple(pie_df['Year'].unique()) 
values = st.selectbox("Year",years)
selected_df = pie_df.where(pie_df['Year']==values)
selected_df = selected_df.dropna()
f = px.pie(selected_df, values='Players', names='Name', title='Player Population')
f.update_layout(
    title=title_config,
    legend=legend_config
    )

colors = None#['gold', 'yellow', 'lightblue', 'lightgreen']
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

# Show the line chart
line_df = get_data('line')[['Name','Tournaments#','Year']]
st.header("Line Chart")
game = ['All']
game += list(line_df['Name'].unique())
values = st.selectbox("Select a Game",game)

if values != 'All':
    selected_df = line_df.where(line_df['Name']==values)
    selected_df = selected_df.dropna()
else:
    selected_df = line_df
    selected_df = selected_df.dropna()

f = px.line(selected_df, x="Year", y="Tournaments#",title='Yearly Tournament',color='Name')
f.update_layout(
    title=title_config,
    xaxis=xaxis_config,
    yaxis={
        "title":'Tournaments'
        #'range':[20,180]
        #,'rangemode':"tozero"
    },
    legend_title_text='',
    legend = {'x':1.05,'y':1.03}
    )
st.plotly_chart(f)

# Show the chart for total prize


xaxis_config = {
        'title':'Game'
        }

st.write(get_data('prize'))
prize_df = get_data('prize')[['Name','Total Prize Poll#2016','Year']]
st.header("Prize Chart")
values = st.selectbox("Year ",years)
selected_df = prize_df.where(prize_df['Year']==str(values))
selected_df = selected_df.dropna()
f = px.bar(selected_df, x="Name", y = 'Total Prize Poll',title = 'Total Prize Pool')
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
radar_df = get_data('radar')
st.header("Radar Chart")
game = tuple(radar_df['Name'].unique())
values = st.selectbox("Game ",game)
selected_df = radar_df.where(radar_df['Name']==values)
selected_df = selected_df.dropna().drop(columns=['Name'])
selected_df = selected_df.T.reset_index(drop=False)
selected_df.columns = ['feature','value']
st.write(selected_df)

f = px.line_polar(selected_df, r='value', theta='feature', line_close=True)
f.update_layout(
    title=title_config)
f.update_traces(fill='toself')
st.plotly_chart(f)

q1_str = "Do you like to participate in many small competitions or just a few big ones?"
q1_selection = ['Many small ones','A good mixture','A few big ones']
q1 = st.slider(q1_str,q1_selection)


