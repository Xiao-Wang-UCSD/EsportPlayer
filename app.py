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
selected_df = line_df.where(line_df['Year']==values)
f = px.line(df, x="Year", y="Sales", title='Yearly Sales')
st.plotly_chart(f)

