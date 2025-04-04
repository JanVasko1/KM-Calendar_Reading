# Import Libraries
from pandas import DataFrame, Series

# ---------------------------------------------------------- Main Function ---------------------------------------------------------- #
def Join_Events(Settings: dict, Events: DataFrame) -> DataFrame:
    Join_method_dict = Settings["0"]["Event_Handler"]["Events"]["Join_method"]
    Join_Events_Enabled = Join_method_dict["Use"]

    if Join_Events_Enabled == True:
        Cumulated_Events = DataFrame(columns=list(Events.columns))
        
        Pre_Index = ""
        Pre_Date = ""
        Pre_Project = ""
        Pre_Activity = ""
        Pre_Event_End_time = ""
        Pre_Busy_Status = ""

        for row in Events.iterrows():
            # Define current row as pandas Series
            row_Series = Series(row[1])

            Current_Date = row_Series["Start_Date"]
            Current_Subject = row_Series["Subject"]
            Current_Project = row_Series["Project"] 
            Current_Activity = row_Series["Activity"]
            Current_Event_Start_time = row_Series["Start_Time"]
            Current_Event_End_time = row_Series["End_Time"]
            Current_Busy_Status = row_Series["Busy_Status"]

            if Current_Date == Pre_Date:
                if Current_Subject == Pre_Subject:
                    if Current_Project == Pre_Project:
                        if Current_Activity == Pre_Activity:
                            if Current_Event_Start_time == Pre_Event_End_time:
                                if Current_Busy_Status == Pre_Busy_Status:
                                    if Join_method_dict[Current_Busy_Status] == "Join":
                                        # Change End date of previously inserted 
                                        Cumulated_Events.iloc[Pre_Index]["End_Time"] = Current_Event_End_time
                                        
                                        # Change Duration
                                        Current_Duration = int(row_Series["Duration"])
                                        Pre_Duration = int(Cumulated_Events.iloc[Pre_Index]["Duration"])
                                        Cumulated_Events.iloc[Pre_Index]["Duration"] = Pre_Duration + Current_Duration
                                    elif Join_method_dict[Current_Busy_Status] == "Keep separate":
                                        Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                                    else:
                                        Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                                else:
                                    Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                            else:
                                Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                        else:
                            Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                    else:
                        Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
                else:
                    Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series
            else:
                Cumulated_Events.loc[len(Cumulated_Events.index)] = row_Series

            # Get maximal Index
            Cumulated_Events_Indexes = Cumulated_Events.index
            Pre_Index = Cumulated_Events_Indexes.max()

            Pre_Date = Current_Date
            Pre_Subject = Current_Subject
            Pre_Project = Current_Project
            Pre_Activity = Current_Activity
            Pre_Event_End_time = Current_Event_End_time
            Pre_Busy_Status = Current_Busy_Status

        return Cumulated_Events
    else: 
        return Events