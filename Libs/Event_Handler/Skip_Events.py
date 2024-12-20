# Import Libraries
from pandas import DataFrame
import pandas
from datetime import datetime
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Day_Start_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
Day_End_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]
Skip_Events_list = Settings["Event_Handler"]["Events"]["Skip"]
Skip_Events_list.append(Day_Start_Subject)
Skip_Events_list.append(Day_End_Subject)

Columns = ["Subject", 
        "Start_Date", 
        "End_Date",
        "Start_Time", 
        "End_Time",
        "Duration",
        "Project",
        "Activity",
        "Recurring",
        "Busy_Status",
        "Meeting_Room",
        "All_Day_Event",
        "Event_Empty_Insert",
        "Within_Working_Hours",
        "Location"]

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Skip_Events(Events: DataFrame):
    Cumulated_Events = pandas.DataFrame(columns=Columns)
    for row in Events.iterrows():
        # Define current row as pandas Series
        row_Series = pandas.Series(row[1])
        Event_Subject = row_Series["Subject"]

        for Skip in Skip_Events_list:
            Part_Found = Event_Subject.find(Skip)

            if Part_Found == -1:
                pass
            else:
                break

        if Part_Found == -1:
            Cumulated_Events.loc[Cumulated_Events.shape[0]] = row_Series
        else:
            pass

    return Cumulated_Events
