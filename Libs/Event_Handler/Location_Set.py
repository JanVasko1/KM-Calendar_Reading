# Import Libraries
from pandas import DataFrame
import pandas
from datetime import datetime
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Default_Location = Settings["Event_Handler"]["Location"]["Default"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Location_Set(Events: DataFrame):
    for row in Events.iterrows():
        row_Series = pandas.Series(row[1])

        if row_Series["Location"] == "":
            Events.at[row[0], "Location"] = Default_Location
        else:
            pass
    return Events

