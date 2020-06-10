import pandas as pd
import streamlit as st
import plotly.express as px

st.title("If you want to be an esport player")

@st.cache
def get_data(name):
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

full_df = get_data('full')
st.header("Overview")
st.write(full_df)

pie_df = get_data('pie')
st.header("Pie Chart")
years = tuple(pie_df['Year'].unique())
values = st.selectbox("Year",years)
selected_df = pie_df.where(pie_df['Year']==values)
f = px.pie(selected_df, values='Players', names='Name', title='Player Population')
st.plotly_chart(f)

line_df = get_data('line')
st.header("Line Chart")
game = tuple(line_df['Name'].unique())
values = st.selectbox("Game",game)
selected_df = line_df.where(line_df['Name']==values)
f = px.line(selected_df, x="Year", y="Number", title='Yearly Tournament')
st.plotly_chart(f)

prize_df = get_data('prize')
st.header("prize Chart")
year = tuple(prize_df['Year'].unique())
values = st.selectbox("Year",year)
selected_df = prize_df.where(prize_df['Year']==values)
f = px.histogram(selected_df, x="Name", y = 'Prize',title = 'Total Prize Pool')
st.plotly_chart(f)

radar_df = get_data('radar')
st.header("Radar Chart")
game = tuple(radar_df['Name'].unique())
values = st.selectbox("Game",game)
selected_df = radar_df.where(radar_df['Name']==values)
selected_df = selected_df.dropna().drop(columns=['Name'])
selected_df = selected_df.T.reset_index(drop=False)
selected_df.columns = ['feature','value']
st.write(selected_df)

f = px.line_polar(selected_df, r='value', theta='feature', line_close=True)
f.update_traces(fill='toself')
st.plotly_chart(f)


