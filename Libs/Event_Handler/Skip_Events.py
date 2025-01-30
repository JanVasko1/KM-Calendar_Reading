# Import Libraries
from pandas import DataFrame
import pandas
import Libs.Defaults_Lists as Defaults_Lists

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Day_Start_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["Start"]
Day_End_Subject = Settings["Event_Handler"]["Events"]["Start_End_Events"]["End"]
HomeOffice_Subject = Settings["Event_Handler"]["Events"]["Special_Events"]["HomeOffice"]["Search_Text"]
Lunch_Subject = Settings["Event_Handler"]["Events"]["Special_Events"]["Lunch"]["Search_Text"]
Private_Subject = Settings["Event_Handler"]["Events"]["Special_Events"]["Private"]["Search_Text"]

Skip_Enabled = Settings["Event_Handler"]["Events"]["Skip"]["Use"]
Skip_Events_regular_list = list(Settings["Event_Handler"]["Events"]["Skip"]["Skip_List"])

# Add to list also special Events which need to be deleted
Skip_Events_special_list = []
Skip_Events_special_list.append(Day_Start_Subject)
Skip_Events_special_list.append(Day_End_Subject)
Skip_Events_special_list.append(HomeOffice_Subject)
Skip_Events_special_list.append(Lunch_Subject)
Skip_Events_special_list.append(Private_Subject)

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Skip_Events(Events: DataFrame, Type: str):
    if Skip_Enabled == True:
        Delete_Index_List = []

        # Iterate over all lines
        for row in Events.iterrows():
            # Define current row as pandas Series
            row_Series = pandas.Series(row[1])
            Event_Subject = row_Series["Subject"]

            if Type == "Regular": 
                Skip_list = Skip_Events_regular_list
            elif Type == "Special":
                Skip_list = Skip_Events_special_list

            for Skip in Skip_list:
                Part_Found = Event_Subject.find(Skip)

                if Part_Found == -1:
                    pass
                else:
                    Delete_Index_List.append(row[0])

        # Delete from Dataframe
        for Index_to_Del in Delete_Index_List:
            Events.drop(labels=[Index_to_Del], axis=0, inplace=True)

        return Events
    else:
        return Events
