# Import Libraries
import pandas
from pandas import DataFrame

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Location_Set(Settings: dict, Events: DataFrame):
    Default_Location = Settings["Event_Handler"]["Location"]["Default"]

    for row in Events.iterrows():
        row_Series = pandas.Series(row[1])

        if row_Series["Location"] == "":
            Events.at[row[0], "Location"] = Default_Location
        else:
            pass
    return Events

