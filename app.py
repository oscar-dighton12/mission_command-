import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output
import os 
from validator import data_validation
sales_data = "my_data.csv"
#checking to ensure that my data has been downloaded, unfortunately this program currently only works with this specific file, in a later update it will be improved so that you can use a custom file
"""if os.path.isfile(sales_data):
    print("The file exists!")
else:
    print("File not found, did you remember to download the data file?.")"""
#note this code is redudant

"""

df = pd.read_csv(sales_data)
"""
#redundant code 
#this loads the csv file into pandas 
#checking to ensure that my data has been downloaded, unfortunately this program currently only works with this specific file, in a later update it will be improved so that you can use a custom file
df=data_validation(sales_data)
df['Date'] = pd.to_datetime(df['Date'])
#converts from static to datetime objects 
app = Dash(__name__)
#initializes dash, which uses flask. 

region_options = [{'label': 'All Regions', 'value': 'ALL'}] + [
    {'label': r, 'value': r} for r in df['Region'].unique()
]
#this the selection for the regions you can choose. 

unique_dates = df['Date'].dt.strftime('%Y-%m-%d').unique()
date_options = [{'label': 'All Dates', 'value': 'ALL'}] + [
    {'label': d, 'value': d} for d in sorted(unique_dates)
]
#this is different from the more simple regional selection, as we need to do this to ensure that the date format is converted back into strings for html dropdowns
category_options = [{'label': 'All Categories', 'value': 'ALL'}] + [
    {'label': c, 'value': c} for c in df['Category'].unique()
]
#likewise this covers the categories of products 
app.layout = html.Div([
    html.H1("Mission Command", style={'textAlign': 'center'}),
#this is the front end UI, using HTML to create a user interface for the dashboard. from here are three dropdown menus, for region, category, and dates. 
#you can add multiple filters and get specific information and graphs. 
    html.Div([
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=region_options,
                value='ALL',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
        
        html.Div([
            html.Label("Select Date:"),
            dcc.Dropdown(
                id='date-dropdown',
                options=date_options,
                value='ALL',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '3%'}),
        
        html.Div([
            html.Label("Select Category:"),
            dcc.Dropdown(
                id='category-dropdown',
                options=category_options,
                value='ALL',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'width': '85%', 'margin': 'auto', 'paddingBottom': '20px'}),
#this displays the data chart based on your filters, or rather lack of filters. 
    dcc.Graph(id='revenue-chart')
])
#this is the backend section for the app 
@app.callback(
    Output('revenue-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
#the app callback is a decorator that registers the relationship, when one of the inputs get updated and changed by user input it, it will change the output based on the input.
def update_dashboard(selected_region, selected_date, selected_category):
    filtered_df = df.copy()
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
        region_text = f'{selected_region} Region'
    else:
        region_text = 'All Regions'
    if selected_date != 'ALL':
        target_date = pd.to_datetime(selected_date)
        filtered_df = filtered_df[filtered_df['Date'] == target_date]
        date_text = selected_date
    else:
        date_text = 'All Dates'
        
    if selected_category != 'ALL':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        category_text = selected_category
    else:
        category_text="All Categories"
    
    if filtered_df.empty:
        fig = px.bar(title="No data available for this filter combination.")
        fig.update_layout(template='plotly_white')
        return fig
    else:
        fig = px.bar(
            filtered_df, 
            x='Date', 
            y='Revenue', 
            color='Product',
            title=f'Revenue: {region_text} | {category_text} | Date: {date_text}',
            hover_data=['Category', 'UnitsSold']
        )
    fig.update_layout(template='plotly_white')
    return fig

if __name__ == '__main__':
    app.run(debug=True)

    """
    verion 3.0 
    oscar dighton 27/09/2026 
    """