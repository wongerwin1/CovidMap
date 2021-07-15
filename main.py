# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# read the data from covid_19_data.csv
df = pd.read_csv('covid_19_data.csv')

# Rename the columns
df = df.rename(columns={'Country/Region':'Country'})
df = df.rename(columns={'ObservationDate':'Date'})
print(df.head())

# Manipulate DataFrame
df_countries = df.groupby(['Country',"Date"]).sum().reset_index().sort_values("Date",
                ascending=False)
df_countries = df_countries.drop_duplicates(subset = ['Country'])
df_countries = df_countries[df_countries["Confirmed"]>0]

# Create the Choropleth
fig = go.Figure(data = go.Choropleth(
    locations=df_countries['Country'],
    locationmode='country names',
    z = df_countries['Confirmed'],
    colorscale= 'Reds',
    marker_line_color = 'black',
    marker_line_width = 0.5,
))
fig.update_layout(
    title_text = 'Confirmed Cases as of March 28, 2020',
    title_x = 1,
    geo= dict(
        showframe = True,
        showcoastlines = False,
        projection_type = 'equirectangular'
    )
)

# Manipulating the original dataframe
df_countrydate = df[df['Confirmed'] > 0]
df_countrydate = df_countrydate.groupby(['Date', 'Country']).sum().reset_index()

# Creating the visualization
fig = px.choropleth(df_countrydate,
                    locations="Country",
                    locationmode="country names",
                    color="Confirmed",
                    hover_name="Country",
                    animation_frame="Date"
                    )
fig.update_layout(
    title_text='Global Spread of Coronavirus',
    title_x=0.5,
    geo=dict(
        showframe=True,
        showcoastlines=True,
    ),
# Create a source for the data
annotations = [dict(
    x=0.55,
    y=0.1,
    xref='paper',
    yref='paper',
    text='Data Source: <a href = "https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset">\
               World Health Organization<br> Corona Virus 2019</a>',
    showarrow=False
)]
)
# Display the map
fig.show()
fig.write_html("fileName.html")