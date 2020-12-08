import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from urllib.request import urlopen
import json
import streamlit as st
from scipy.stats import pearsonr

@st.cache
def load_county_data():
    return pd.read_pickle("final_df.pkl")

final_df = load_county_data()

columnList = final_df.columns.values.tolist()

demoList = ['Population', '% Men', '% Women', '% White', '% Black', '% Hispanic', '% Asian', '% Native', '% Pacific']

ecoList = ['Average Income', 'Poverty Rate', 'Unemployment Rate', '% Self-Employed', '% Work at Home', 'Mean Commute']


st.title('2017 U.S. County Correlation Dashboard')
st.sidebar.title('Variable Selection')
st.write('Find the data [HERE](www.kaggle.com/muonneutrino/us-census-demographic-data)')


demo_choice = st.sidebar.selectbox('Select a Demographic Variable:', options=demoList)
eco_choice = st.sidebar.selectbox('Select an Economic Variable:', options=ecoList)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

def make_map(var):
    fig = px.choropleth(final_df, geojson=counties, locations='County FIPS', color=var,
                           color_continuous_scale="dense",
                           scope="usa",
                           hover_name = 'County',
                           hover_data = ['State'])

    fig.update_traces(marker_line_width=.1, marker_opacity=1)

    fig.update_layout(title_text = f'{var} by County')

    st.plotly_chart(fig)

make_map(demo_choice)
make_map(eco_choice)

corr_coef, pvalue = pearsonr(final_df[demo_choice], final_df[eco_choice])

if pvalue <= .05:
    st.write(f'There is a statistically significant correlation between {demo_choice} and {eco_choice} for counties in the USA.')
    st.write(f'The correlation coefficient between {demo_choice} and {eco_choice} is {corr_coef:.3f}.')
    if corr_coef > 0:
        st.write(f'This means that {demo_choice} and {eco_choice} are positively correlated.')
    elif corr_coef < 0:
        st.write(f'This means that {demo_choice} and {eco_choice} are inversely correlated.')
elif pvalue > .05:
    st.write(f'We cannot conclude a statistically significant correlation between {demo_choice} and {eco_choice}.')

plt.scatter(final_df[demo_choice], final_df[eco_choice], alpha = .1, s = 20, color = 'royalblue')
plt.title(f'Scatter Plot of {demo_choice} vs. {eco_choice}')
plt.xlabel(demo_choice)
plt.ylabel(eco_choice)
st.pyplot()
