import pandas as pd


def extract_value(df, keyword):
    """
    Search keyword in entire dataframe and return value from next column
    """

    for index, row in df.iterrows():

        row_values = [str(x).upper() for x in row.values]

        for i, cell in enumerate(row_values):

            if keyword.upper() in cell:

                try:
                    value = row.iloc[i + 1]

                    if pd.isna(value):
                        return None

                    return value

                except:
                    return None

    return None


def calculate_kpis(df):

    kpis = {}

    # =========================
    # VOYAGE KPIs
    # =========================

    kpis["distance_sailed"] = extract_value(df, "DISTANCE SAILED")

    kpis["cp_speed"] = extract_value(df, "ALLOWED CP SPEED")

    kpis["wind_speed"] = extract_value(df, "WIND SPEED")

    kpis["avg_speed"] = extract_value(df, "AVG SPEED")

    # =========================
    # FUEL
    # =========================

    kpis["hsfo_consumption"] = extract_value(df, "HSFO")

    kpis["lsfo_consumption"] = extract_value(df, "LSFO")

    # =========================
    # ROB
    # =========================

    kpis["rob_hsfo"] = extract_value(df, "ROB HSFO")

    kpis["rob_lsfo"] = extract_value(df, "ROB LSFO")

    return kpis