import pandas as pd

def load_noon_report(file):
    df = pd.read_excel(file)

    # clean column names
    df.columns = df.columns.str.strip()

    return df