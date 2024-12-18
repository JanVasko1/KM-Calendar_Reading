# Import Libraries
from pandas import DataFrame
import pandas
from tqdm import tqdm
from datetime import datetime
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Default_Location = Settings["Event_Handler"]["Location"]["Default"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Location_Set(Events: DataFrame):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(Events.shape[0]),desc=f"{now}>> Locations")
    for row in Events.iterrows():
        row_Series = pandas.Series(row[1])

        if row_Series["Location"] == "":
            Events.at[row[0], "Location"] = Default_Location
        else:
            pass
        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()
    return Events

