import pandas as pd
import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output, State, clientside_callback, ClientsideFunction
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
app.layout = html.Div(id='main-container', className='light-theme', children=[
    dcc.Store(id='theme-store', data='light'),
    html.Div([
        html.H1("Mission Command", className='app-title'),
        html.Button("Toggle Theme", id='theme-btn', className='theme-button')
    ], className='header-container'),
#this is the front end UI, using HTML to create a user interface for the dashboard. from here are three dropdown menus, for region, category, and dates. 
#you can add multiple filters and get specific information and graphs. 
    html.Div([
        html.Div([
            html.Div([
                html.Label("Select Region:", style={'fontWeight': '500', 'fontSize': '13px'}),
                dcc.Dropdown(id='region-dropdown', options=region_options, value='ALL', clearable=False)
            ], style={'width': '32%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Select Date:", style={'fontWeight': '500', 'fontSize': '13px'}),
                dcc.Dropdown(id='date-dropdown', options=date_options, value='ALL', clearable=False)
            ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'} ),
            
            html.Div([
                html.Label("Select Category:", style={'fontWeight': '500', 'fontSize': '13px'}),
                dcc.Dropdown(id='category-dropdown', options=category_options, value='ALL', clearable=False)
            ], style={'width': '32%', 'display': 'inline-block', 'marginLeft': '2%'})
        ])
    ], className='dashboard-card'),
#this displays the data chart based on your filters, or rather lack of filters. 
    html.Div([
        dcc.Graph(id='revenue-chart', config={'displayModeBar': False})
    ], className='dashboard-card')
])
clientside_callback(
    ClientsideFunction(
        namespace='theme_namespace',
        function_name='toggleTheme'
    ),
    [Output('main-container', 'className'),
     Output('theme-store', 'data')],
    Input('theme-btn', 'n_clicks'),
    State('theme-store', 'data'),
    prevent_initial_call=True
)
@app.callback(
    Output('revenue-chart', 'figure'),
    [Input('theme-store', 'data'),
     Input('region-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('category-dropdown', 'value')],
    
)
def update_dashboard(theme,selected_region, selected_date, selected_category):
    chart_template = 'plotly_dark' if theme == 'dark' else 'plotly_white'
    if theme == 'dark':
        paper_bg = '#121212'
        plot_bg = '#121212'
        text_color = '#FFFFFF'
    else:
        paper_bg = '#FFFFFF'
        plot_bg = '#FFFFFF'
        text_color = '#000000'
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
        category_text = "All Categories"
    
    if filtered_df.empty:
        fig = px.bar(title="No data available for this filter combination.")
    else:
        fig = px.bar(
            filtered_df, 
            x='Date', 
            y='Revenue', 
            color='Product',
            title=f'Revenue: {region_text} | {category_text} | Date: {date_text}',
            hover_data=['Category', 'UnitsSold']
        )
        
    fig.update_layout(
        template=chart_template,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={'color': text_color}
    )
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
#this is used for setting up the flask server, which dash uses. this is done to ensure that the server only starts when directly set up on my system. 
    """
    verion 3.1 
    oscar dighton 04/10/2026 
    -added night mode toggle 
    """