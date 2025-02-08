from pandas import DataFrame
import pandas

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def AutoFiller(Settings: dict, Events: DataFrame):
    AutoFiller_Enabled = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Use"]
    AutoFiller_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Search_Text"]["Dictionary"]

    if AutoFiller_Enabled == True:
        for row in Events.iterrows():
            # Define current row as pandas Series
            row_index = row[0]
            row_Series = pandas.Series(row[1])
            Event_Subject = row_Series["Subject"]
            Event_Project = row_Series["Project"]
            Event_Activity = row_Series["Activity"]
            Event_Location = row_Series["Location"]

            for item in AutoFiller_dict.items():
                Search_text = item[1]["Search Text"]
                Part_Found = Event_Subject.find(Search_text)

                if Part_Found == -1:
                    pass
                else:
                    Project = item[1]["Project"]
                    Activity = item[1]["Activity"]
                    Location = item[1]["Location"]

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
        return Events
    else:
        return Events

def Auto_Activity_Corrections(Settings: dict, Events: DataFrame):
    Activity_Correction_Enabled = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Use"]
    Activity_Correction_dict = Settings["Event_Handler"]["Events"]["Auto_Filler"]["Activity_Correction"]["Dictionary"]

    if Activity_Correction_Enabled == True:
        for row in Events.iterrows():
            # Define current row as pandas Series
            row_index = row[0]
            row_Series = pandas.Series(row[1])
            Event_Project = row_Series["Project"]
            Event_Activity = row_Series["Activity"]

            for item in Activity_Correction_dict.items():
                Check_Project = item[1]["Project"]
                Check_Activity = item[1]["Wrong Activity"]

                if (Event_Project == Check_Project) and (Event_Activity == Check_Activity):
                    New_Activity = Check_Activity = item[1]["Correct Activity"]
                    Events.at[row_index, "Activity"] = New_Activity
                else:
                    pass

        return Events
    else:
        return Events
