import os
import pandas as pd



sales_data = "my_data.csv"


def data_validation(sales_data):
    if os.path.isfile(sales_data):
        print("The file exists!")
    else:
        print("File not found, did you remember to download the data file?.")
        return
    #reminder, if you want to use this program, don't forget to download my data file. 
    
    df = pd.read_csv(sales_data)
    #reading in from the data file. 
    required_columns = ['Date', 'Region', 'Category', 'Product', 'Revenue', 'UnitsSold']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print("error, column missing, check the file")
        return "not valid"
    else: 
        print("all good!")
    #if it is missing a column then we return an error message.
    '''update: 
            found a better way to validate data, using coerce to check data'''
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if df['Date'].isna().any():
        print("Error: some dates are invalid.")
    else: 
        print("dates are all good!")
    if not pd.api.types.is_string_dtype(df['Region']):
        print("region not valid")
    else:
        print("regions are all valid")
    if not pd.api.types.is_string_dtype(df['Category']):
        print("category not valid")
    else:
        print("category are all valid")
    if not pd.api.types.is_string_dtype(df['Product']):
        print("Product not valid")
    else:
        print("Product are all valid")
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    if df['Revenue'].isna().any():
        print("Error: some revenue entries are invalid.")
    else: 
        print("revenue entries are all good!")
    df['UnitsSold'] = pd.to_numeric(df['UnitsSold'], errors='coerce')
    if df['UnitsSold'].isna().any():
        print("Error: some units sold entries are invalid.")
    else: 
        print("units sold entries are all good!")
    return df
    #returns the data to the app.py 
    """
        version 2.0
        oscar dighton- 26/09/2026
    """