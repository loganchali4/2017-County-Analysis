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
st.subheader('By: Gerry Crepeau, Logan Chalifour, and Riley Demanche')

st.write('On the sidebar, please select one demographic variable of choice and one economic variable of choice. The dashboard will '
         'update to show you interactive choropleth maps of both variables organized by U.S. counties. '
         'Zoom in and out on the map as well as hover over a county to see more information. Below the maps, observe if there is a statistically significant '
         'correlation between the variables you chose and a scatter plot between the two variables to check out the data yourself. '
         'The data was collected during the 2017 American Community Survey.')

link = 'Get the data [HERE](https://www.kaggle.com/muonneutrino/us-census-demographic-data)'
st.markdown(link, unsafe_allow_html=True)
link2 = 'View our GitHub Repository [HERE](https://github.com/gerrycrepeau/Final-Project-App)'
st.markdown(link2, unsafe_allow_html=True)
link3 = 'View our full project report [HERE](./source/2017CountyCorrelations.pdf)'
st.markdown(link3, unsafe_allow_html=True)

st.sidebar.title('Variable Selection')
demo_choice = st.sidebar.selectbox('Select a Demographic Variable:', options=demoList)
st.sidebar.markdown('Note: Population is a not a percentage. It gives the total population in each county')
st.sidebar.markdown('\n\n')
eco_choice = st.sidebar.selectbox('Select an Economic Variable:', options=ecoList)
st.sidebar.markdown('Note: Average Income is measured in USD and Mean Commute is measured in minutes')

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

fig3, ax = plt.subplots(1, 1)
ax.scatter(final_df[demo_choice], final_df[eco_choice], alpha = .1, s = 20, color = 'royalblue')
ax.set_title(f'Scatter Plot of {demo_choice} vs. {eco_choice}')
ax.set_xlabel(demo_choice)
ax.set_ylabel(eco_choice)
st.pyplot(fig3)
