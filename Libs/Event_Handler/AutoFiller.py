from pandas import DataFrame
import pandas
import json
from tqdm import tqdm
from datetime import datetime

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
File = open(file=f"Libs\\Settings.json", mode="r", encoding="UTF-8", errors="ignore")
Settings = json.load(fp=File)
File.close()

Details_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Details"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def AutoFiller(Events: DataFrame):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    Data_df_TQDM = tqdm(total=int(Events.shape[0]),desc=f"{now}>> AutoFiller")
    for row in Events.iterrows():
        # Define current row as pandas Series
        row_index = row[0]
        row_Series = pandas.Series(row[1])
        Event_Subject = row_Series["Subject"]
        Event_Project = row_Series["Project"]
        Event_Activity = row_Series["Activity"]
        Event_Location = row_Series["Location"]

        for item in Details_dict.items():
            Search_text = item[1][0]
            Part_Found = Event_Subject.find(Search_text)

            if Part_Found == -1:
                pass
            else:
                Project = item[1][1]
                Activity = item[1][2]
                Location = item[1][3]

                # Project
                if (Project != "") and (Project != Event_Project):
                    Events.at[row_index, "Project"] = Project
                else:
                    pass

                # Activity
                if (Activity != "") and (Activity != Event_Activity):
                    Events.at[row_index, "Activity"] = Activity
                else:
                    pass

                # Location
                if (Location != "") and (Location != Event_Location):
                    Events.at[row_index, "Location"] = Location
                else:
                    pass
        Data_df_TQDM.update(1) 
    Data_df_TQDM.close()
        
    return Events

