import pandas as pd
import plotly.express as px


df = pd.read_csv("my_data.csv")




fig = px.bar(
    df, 
    x='Date', 
    y='Revenue', 
    color='Region',          
    title='Daily Revenue by region',
    hover_data=['Region', 'UnitsSold'] 
)


fig.update_layout(
    xaxis_title='Date of Sale',
    yaxis_title='Revenue ($)',
    template='plotly_white'      
)


fig.show()