import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output

df=pd.read_csv("my_data.csv")
df['Date'] = pd.to_datetime(df['Date'])
#converting date to datetime is important as pandas reads csv files as strings
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Mission command", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': 'All Regions', 'value': 'ALL'}] + [{'label': region, 'value': region} for region in df['Region'].unique()],
            value='ALL',  # Default selected value
            clearable=False
        )
    ], style={'width': '50%', 'margin': 'auto', 'paddingBottom': '20px'}),
    
    # Graph Container
    dcc.Graph(id='revenue-chart')
])

@app.callback(
    Output('revenue-chart', 'figure'),
    Input('region-dropdown', 'value')
)
def update_dashboard(selected_region):
    if selected_region == 'ALL':
            filtered_df = df
            title_text = 'Revenue by Category (All Regions)'
    else:
    # Filter dataframe based on user dropdown selection
        filtered_df = df[df['Region'] == selected_region]
        title_text = f'Revenue by Category for {selected_region} Region'
    fig= px.bar(
        filtered_df, 
        x='Date', 
        y='Revenue', 
        color='Category',
        title=f'Revenue by Category for {selected_region} Region',
        hover_data=['UnitsSold']
    )
   
    fig.update_layout(
   
        template='plotly_white' 
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)