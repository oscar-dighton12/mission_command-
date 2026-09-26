import pandas as pd
import plotly.express as px 
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("my_data.csv")
df['Date'] = pd.to_datetime(df['Date'])
app = Dash(__name__)

region_options = [{'label': 'All Regions', 'value': 'ALL'}] + [
    {'label': r, 'value': r} for r in df['Region'].unique()
]

unique_dates = df['Date'].dt.strftime('%Y-%m-%d').unique()
date_options = [{'label': 'All Dates', 'value': 'ALL'}] + [
    {'label': d, 'value': d} for d in sorted(unique_dates)
]

category_options = [{'label': 'All Categories', 'value': 'ALL'}] + [
    {'label': c, 'value': c} for c in df['Category'].unique()
]

app.layout = html.Div([
    html.H1("Mission Command", style={'textAlign': 'center'}),
    
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
    
    dcc.Graph(id='revenue-chart')
])

@app.callback(
    Output('revenue-chart', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('date-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_dashboard(selected_region, selected_date, selected_category):
    filtered_df = df.copy()
    region_text = 'All Regions'
    date_text = 'All Dates'
    category_text = 'All Categories'
    
    if selected_region != 'ALL':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
        region_text = f'{selected_region} Region'
        
    # 2. Filter by Date
    if selected_date != 'ALL':
        target_date = pd.to_datetime(selected_date)
        filtered_df = filtered_df[filtered_df['Date'] == target_date]
        date_text = selected_date
        
    # 3. Filter by Category (Chained safely onto the filtered dataframe)
    if selected_category != 'ALL':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        category_text = selected_category

    # Build dynamic title
    title_text = f'Revenue for {region_text} | Category: {category_text} | Date: {date_text}'
        
    # Handle empty states defensively
    if filtered_df.empty:
        fig = px.bar(title="No data available for this filter combination.")
        fig.update_layout(template='plotly_white')
        return fig

    # 4. Create chart
    fig = px.bar(
        filtered_df, 
        x='Date', 
        y='Revenue', 
        color='Product',
        title=title_text,
        hover_data=['Category', 'UnitsSold']
    )
   
    fig.update_layout(template='plotly_white')
    return fig

if __name__ == '__main__':
    app.run(debug=True)