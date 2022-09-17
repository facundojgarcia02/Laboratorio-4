import pandas as pd
import datetime

class NotImplementedError(Exception):
    pass

def save_df(df: pd.DataFrame):
    """Save DataFrame as csv.
    
    Params:
    -------
        - df: pandas.DataFrame 
    """
    ct = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = input("Filename: ")
    df.to_csv(filename + f" {ct}.csv", index=False)