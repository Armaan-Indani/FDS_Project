import pandas as pd

def load_data(path="app/data.csv"):
    return pd.read_csv(path)

def process_data(df):
    # Your custom processing logic
    return df.describe()
