# Import Libraries
from pandas import DataFrame, concat
from datetime import datetime, timedelta
from holidays import country_holidays

import Libs.Data_Functions as Data_Functions
import Libs.File_Manipulation as File_Manipulation
import Libs.GUI.Charts as Charts

from customtkinter import CTk

def Generate_Summary(Settings: dict, Configuration: dict, window: CTk|None, Calculation_source: str, Events: DataFrame, Report_Period_Active_Days: int|None, Report_Period_Start: datetime|None, Report_Period_End: datetime|None, Team_Member_ID: str|None) -> None:
    # ------------------------------------------------------------ Defaults ------------------------------------------------------------ #
    File_Sub_Path = "DashBoard"
    if Calculation_source == "Team":
        File_Sub_Path = f"My_Team\\{Team_Member_ID}"
    else:
        pass

    Date_Format = Settings["0"]["General"]["Formats"]["Date"]
    Time_Format = Settings["0"]["General"]["Formats"]["Time"]
    
    My_Monday_WH = int(Settings["0"]["General"]["Calendar"]["Monday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Tuesday_WH = int(Settings["0"]["General"]["Calendar"]["Tuesday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Wednesday_WH = int(Settings["0"]["General"]["Calendar"]["Wednesday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Thursday_WH = int(Settings["0"]["General"]["Calendar"]["Thursday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Friday_WH = int(Settings["0"]["General"]["Calendar"]["Friday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Saturday_WH = int(Settings["0"]["General"]["Calendar"]["Saturday"]["Work_Hours"]["Day_Duration"]) / 60
    My_Sunday_WH = int(Settings["0"]["General"]["Calendar"]["Sunday"]["Work_Hours"]["Day_Duration"]) / 60

    My_WH_dict = {
        "Monday": My_Monday_WH,
        "Tuesday": My_Tuesday_WH,
        "Wednesday": My_Wednesday_WH,
        "Thursday": My_Thursday_WH,
        "Friday": My_Friday_WH,
        "Saturday": My_Saturday_WH,
        "Sunday": My_Sunday_WH,
        }

    KM_Monday_WH = int(Settings["0"]["General"]["Calendar"]["Monday"]["Vacation"]["Day_Duration"]) / 60
    KM_Tuesday_WH = int(Settings["0"]["General"]["Calendar"]["Tuesday"]["Vacation"]["Day_Duration"]) / 60
    KM_Wednesday_WH = int(Settings["0"]["General"]["Calendar"]["Wednesday"]["Vacation"]["Day_Duration"]) / 60
    KM_Thursday_WH = int(Settings["0"]["General"]["Calendar"]["Thursday"]["Vacation"]["Day_Duration"]) / 60
    KM_Friday_WH = int(Settings["0"]["General"]["Calendar"]["Friday"]["Vacation"]["Day_Duration"]) / 60
    KM_Saturday_WH = int(Settings["0"]["General"]["Calendar"]["Saturday"]["Vacation"]["Day_Duration"]) / 60
    KM_Sunday_WH = int(Settings["0"]["General"]["Calendar"]["Sunday"]["Vacation"]["Day_Duration"]) / 60

    KM_WH_dict = {
        "Monday": KM_Monday_WH,
        "Tuesday": KM_Tuesday_WH,
        "Wednesday": KM_Wednesday_WH,
        "Thursday": KM_Thursday_WH,
        "Friday": KM_Friday_WH,
        "Saturday": KM_Saturday_WH,
        "Sunday": KM_Sunday_WH,
        }

    # ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #

    def DataFrame_WeekDay(row) -> str:
        x_dt = datetime.strptime(row, Date_Format)
        WeekDay = x_dt.strftime("%A")
        return WeekDay

    def Define_Event_Duration(row) -> int:
        Start_Time = row["Start Time"]
        End_Time = row["End Time"]
        Start_Time_dt = datetime.strptime(Start_Time, Time_Format)
        End_Time_dt = datetime.strptime(End_Time, Time_Format)
        Duration_dt = End_Time_dt - Start_Time_dt
        Duration = Duration_dt.seconds // 60
        return Duration

    def DataFrame_Week(row) -> str:
        x_dt = datetime.strptime(row, Date_Format)
        ISO_Date = x_dt.isocalendar()

        Week = ISO_Date.week
        Year = ISO_Date.year

        X_Week = f"{Year}-{Week}"
        return X_Week

    def Get_Utilization_Calendar(Events: DataFrame, Utilization_Start_Date_dt: datetime, Utilization_End_Date_dt: datetime, Date_Format: str) -> DataFrame:
        Czech_Holidays = country_holidays("CZ")
        Utilization_Calendar_df = DataFrame(columns=["Working_day", "KM_Cumulative_Utilization", "Day_Total_Time", "Reported_Cumulative_Time"])
        KM_Cumulative_Utilization = 0
        Day_Total_Time = 0
        Reported_Cumulative_Time = 0

        # Dataframe preparation
        Events_Date_GR = Events.loc[:, ["Date", "Duration_H"]]
        Events_Date_Sum = Events_Date_GR.groupby(["Date"]).sum()
        Events_Date_Sum["Cumulated_H"] = Events_Date_Sum["Duration_H"].cumsum()
        
        while True:
            Check_Date_str = Utilization_Start_Date_dt.strftime(format=Date_Format)
            Working_day = True

            # Working Day
            Holiday_day = Czech_Holidays.get(key=Check_Date_str)
            if Holiday_day == None:
                Weekend_Day = Utilization_Start_Date_dt.weekday()
                if Weekend_Day < 5:
                    pass
                else:
                    Working_day = False
            else:
                Working_day = False

            # Cumulated KM Utilization
            if Working_day == True:
                KM_Cumulative_Utilization = KM_Cumulative_Utilization + 8
            else: 
                KM_Cumulative_Utilization = KM_Cumulative_Utilization

            # Day Total Time
            try:
                Day_Total_Time = Events_Date_Sum.loc[f"{Check_Date_str}"]["Duration_H"]
            except:
                Day_Total_Time = Day_Total_Time


            # Reported Cumulative Utilization
            try:
                Reported_Cumulative_Time = Events_Date_Sum.loc[f"{Check_Date_str}"]["Cumulated_H"]
            except:
                Reported_Cumulative_Time = Reported_Cumulative_Time
            
            # Add to calendar
            Utilization_Calendar_df.loc[f"{Check_Date_str}"] = [Working_day, KM_Cumulative_Utilization, Day_Total_Time, Reported_Cumulative_Time]

            # Check End of Report Period
            if Utilization_Start_Date_dt == Utilization_End_Date_dt:
                break
            else:
                Utilization_Start_Date_dt += timedelta(days=1)
        
        return Utilization_Calendar_df  

    # ---------------------------------------------------------------------------------- Preparation ---------------------------------------------------------------------------------- #
    # Update Events Dataframe - PreProcessing
    Events = Events.reset_index().rename(columns={"Network Description": "Project"})	
    Events["Duration"] = Events.apply(Define_Event_Duration, axis = 1)
    Events["Duration_H"] = Events["Duration"].map(lambda x: round(x/60, 2))

    # Deletion
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Project.csv"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Activity.csv"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_WeekDays.csv"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Weeks.csv"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Totals.csv"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Project_Light.html"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Project_Dark.html"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Activity_Light.html"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Activity_Dark.html"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Utilization_Light.html"))
    File_Manipulation.Delete_File(Configuration=Configuration, window=window, file_path=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\DashBoard_Utilization_Dark.html"))

    # ---------------------------------------------------------------------------------- Projects ---------------------------------------------------------------------------------- #
    # Calculation
    Events_Project_GR = Events.loc[:, ["Project", "Duration_H"]]
    Events_Project_Sum = Events_Project_GR.groupby(["Project"]).sum()
    Events_Project_Sum.rename(columns={"Duration_H": "Total[H]"}, inplace=True)
    Events_Project_Sum["Total[H]"] = Events_Project_Sum["Total[H]"].map(lambda x: round(x, 2))
    Events_Project_Mean = Events_Project_GR.groupby(["Project"]).mean()
    Events_Project_Mean.rename(columns={"Duration_H": "Average[H]"}, inplace=True)
    Events_Project_Mean["Average[H]"] = Events_Project_Mean["Average[H]"].map(lambda x: round(x, 2))
    Events_Project_Count = Events_Project_GR.groupby(["Project"]).count()
    Events_Project_Count.rename(columns={"Duration_H": "Count"}, inplace=True)
    Events_Project_Concat = concat(objs=[Events_Project_Count, Events_Project_Sum, Events_Project_Mean], axis=1, join="inner")

    # Summary line
    Project_Count_Summary = Events_Project_Concat["Count"].sum()
    Project_TotalH_Summary = round(Events_Project_Concat["Total[H]"].sum(), 2)
    Project_AverageH_Summary = round(Project_TotalH_Summary / Project_Count_Summary, 2)
    Events_Project_Concat.loc["Summary"] = [Project_Count_Summary, Project_TotalH_Summary, Project_AverageH_Summary]
    Events_Project_Concat["Count"] = Events_Project_Concat["Count"].astype(int)
    Events_Project_Concat = Events_Project_Concat.reset_index().rename(columns={"index": "Project"})		

    # ---------------------------------------------------------------------------------- Activity ---------------------------------------------------------------------------------- #
    # Calculation
    Events_Activity_GR = Events.loc[:, ["Activity", "Duration_H"]]
    Events_Activity_Sum = Events_Activity_GR.groupby(["Activity"]).sum()
    Events_Activity_Sum.rename(columns={"Duration_H": "Total[H]"}, inplace=True)
    Events_Activity_Sum["Total[H]"] = Events_Activity_Sum["Total[H]"].map(lambda x: round(x, 2))
    Events_Activity_Mean = Events_Activity_GR.groupby(["Activity"]).mean()
    Events_Activity_Mean.rename(columns={"Duration_H": "Average[H]"}, inplace=True)
    Events_Activity_Mean["Average[H]"] = Events_Activity_Mean["Average[H]"].map(lambda x: round(x, 2))
    Events_Activity_Count = Events_Activity_GR.groupby(["Activity"]).count()
    Events_Activity_Count.rename(columns={"Duration_H": "Count"}, inplace=True)
    Events_Activity_Concat = concat(objs=[Events_Activity_Count, Events_Activity_Sum, Events_Activity_Mean], axis=1, join="inner")

    # Summary line
    Activity_Count_Summary = Events_Activity_Concat["Count"].sum()
    Activity_TotalH_Summary = round(Events_Activity_Concat["Total[H]"].sum(), 2)
    Activity_AverageH_Summary = round(Activity_TotalH_Summary / Activity_Count_Summary, 2)
    Events_Activity_Concat.loc["Summary"] = [Activity_Count_Summary, Activity_TotalH_Summary, Activity_AverageH_Summary]
    Events_Activity_Concat["Count"] = Events_Activity_Concat["Count"].astype(int)
    Events_Activity_Concat = Events_Activity_Concat.reset_index().rename(columns={"index": "Activity"})		

    # ---------------------------------------------------------------------------------- Weekday ---------------------------------------------------------------------------------- #
    # Calculation
    WeekDays_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    Events_WeekDays = DataFrame(index=WeekDays_list, columns=["Days Count", "Total Events", "Total[H]", "Average[H]", "My Utilization[%]", "Utilization[%]"])
    Events_WeekDays_GR = Events.loc[:, ["Date", "Project", "Activity", "Duration_H"]]
    Events_WeekDays_GR["WeekDay"] =  Events_WeekDays_GR["Date"].apply(DataFrame_WeekDay)
    Used_Days = 0
    Used_Days_wo = 0

    for WeekDay in WeekDays_list:
        WeekDay_dates_count = 0
        Total_Count = 0
        Total_Hours = 0
        Average_Hours = 0
        My_Day_Utilization = 0
        KM_Day_Utilization = 0

        mask =  Events_WeekDays_GR["WeekDay"] == WeekDay
        Filtered_Df = DataFrame(Events_WeekDays_GR[mask])

        if Filtered_Df.empty:
            pass
        else:
            Used_Days += 1  # Number of path because of utilization
            if (WeekDay == "Saturday") or (WeekDay == "Sunday"):
                pass
            else:
                Used_Days_wo += 1

            WeekDay_dates_list = list(set(Filtered_Df["Date"]))
            WeekDay_dates_count = len(WeekDay_dates_list)
            Filtered_Df.drop(labels=["Date"], axis=1, inplace=True)

            Events_Totals_GR = Filtered_Df.loc[:, ["Project", "Duration_H"]]

            # WeekDay Totals
            Total_Count = round(Events_Totals_GR["Project"].count(), 0)
            Total_Hours = round(Events_Totals_GR["Duration_H"].sum(), 2)
            Average_Hours = round(Total_Hours / WeekDay_dates_count, 2)

            # WeekDay Utilization
            if My_WH_dict[WeekDay] != 0:
                My_Day_Utilization = round(Average_Hours / My_WH_dict[WeekDay] * 100, 2)
            else:
                # Because of nonworking day
                My_Day_Utilization = round(100, 2)

            if KM_WH_dict[WeekDay] != 0:
                KM_Day_Utilization = round(Average_Hours / KM_WH_dict[WeekDay] * 100, 2)
            else:
                # Because of nonworking day
                KM_Day_Utilization = round(100, 2)
        
        # Update
        Events_WeekDays.at[WeekDay, "Days Count"] = WeekDay_dates_count
        Events_WeekDays.at[WeekDay, "Total Events"] = Total_Count
        Events_WeekDays.at[WeekDay, "Total[H]"] = Total_Hours
        Events_WeekDays.at[WeekDay, "Average[H]"] = Average_Hours
        Events_WeekDays.at[WeekDay, "My Utilization[%]"] = My_Day_Utilization
        Events_WeekDays.at[WeekDay, "Utilization[%]"] = KM_Day_Utilization
        
        del Filtered_Df
    
    # Summary Lines
    if Used_Days_wo > 5:
        # Dont want to count with Saturday and Sunday
        Used_Days_wo = 5
    else:
        pass
    Total_Days_w = round(Events_WeekDays["Days Count"].sum(), 0)
    Total_Events_w = round(Events_WeekDays["Total Events"].sum(), 0)
    TotalH_w = round(Events_WeekDays["Total[H]"].sum(), 2)
    AverageH_w = round(TotalH_w / Used_Days, 2)
    My_Day_Utilization_w = round((Events_WeekDays["My Utilization[%]"].sum()) / Used_Days, 2)
    KM_Day_Utilization_w = round((Events_WeekDays["Utilization[%]"].sum()) / Used_Days, 2)
    
    Total_Days_wo = round(Events_WeekDays.loc["Monday":"Friday", "Days Count"].sum(), 0)
    Total_Events_wo = round(Events_WeekDays.loc["Monday":"Friday", "Total Events"].sum(), 0)
    TotalH_wo = round(Events_WeekDays.loc["Monday":"Friday", "Total[H]"].sum(), 2)
    if Used_Days_wo > 0:
        AverageH_wo = round(TotalH_wo / Used_Days_wo, 2)
        My_Day_Utilization_wo = round((Events_WeekDays.loc["Monday":"Friday", "My Utilization[%]"].sum()) / Used_Days_wo, 2)
        KM_Day_Utilization_wo = round((Events_WeekDays.loc["Monday":"Friday", "Utilization[%]"].sum()) / Used_Days_wo, 2)
    else:
        AverageH_wo = 0
        My_Day_Utilization_wo = 0
        KM_Day_Utilization_wo = 0
    

    Events_WeekDays.loc["Summary w weekend"] = [Total_Days_w, Total_Events_w, TotalH_w, AverageH_w, My_Day_Utilization_w, KM_Day_Utilization_w]
    Events_WeekDays.loc["Summary w/o weekend"] = [Total_Days_wo, Total_Events_wo, TotalH_wo, AverageH_wo, My_Day_Utilization_wo, KM_Day_Utilization_wo]
    Events_WeekDays["Days Count"] = Events_WeekDays["Days Count"].astype(int)
    Events_WeekDays["Total Events"] = Events_WeekDays["Total Events"].astype(int)
    Events_WeekDays = Events_WeekDays.reset_index().rename(columns={"index": "Week Day"})		

    # ---------------------------------------------------------------------------------- Weeks ---------------------------------------------------------------------------------- #
     # Calculation
    Events_Weeks_GR = Events.loc[:, ["Date", "Project", "Duration_H"]]
    Events_Weeks_GR["Week"] =  Events_Weeks_GR["Date"].apply(DataFrame_Week)
    Events_Weeks_GR["WeekDay"] =  Events_Weeks_GR["Date"].apply(DataFrame_WeekDay)
    Weeks_list = list(set(Events_Weeks_GR["Week"]))
    Weeks_list.sort()
    Events_Weeks = DataFrame(index=Weeks_list, columns=["Days", "Days w/o weekend", "Total Events", "Total[H]", "Average[H]", "Week Utilization[%]", "Active Days Utilization[%]"])

    for Week in Weeks_list:
        Week_days_count = 0
        Week_days_count_wo = 0
        Total_Count = 0
        Total_Hours = 0
        Average_Hours = 0
        Week_Utilization = 0

        mask1 =  Events_Weeks_GR["Week"] == Week
        mask2 =  Events_Weeks_GR["WeekDay"] != "Saturday"
        mask3 =  Events_Weeks_GR["WeekDay"] != "Sunday"
        Filtered_Df = DataFrame(Events_Weeks_GR[mask1])

        if Filtered_Df.empty:
            pass
        else:
            Week_days_list = list(set(Filtered_Df["Date"]))
            Week_days_count = len(Week_days_list)

            # Weekdays without weekend
            Filtered_Df_wo = Events_Weeks_GR[mask1 & mask2 & mask3]
            Week_days_list_wo = list(set(Filtered_Df_wo["Date"]))
            Week_days_count_wo = len(Week_days_list_wo)
            Active_days_Hours = Week_days_count * 8

            Total_Count = round(Filtered_Df["Project"].count(), 0)
            Total_Hours = round(Filtered_Df["Duration_H"].sum(), 2)
            Average_Hours = round(Total_Hours / Week_days_count_wo, 2)
            Week_Utilization = round(Total_Hours / 40 * 100, 2)
            Active_Days_Utilization = round(Total_Hours / Active_days_Hours * 100, 2)

        # Update
        Events_Weeks.at[Week, "Days"] = Week_days_count
        Events_Weeks.at[Week, "Days w/o weekend"] = Week_days_count_wo
        Events_Weeks.at[Week, "Total Events"] = Total_Count
        Events_Weeks.at[Week, "Total[H]"] = Total_Hours
        Events_Weeks.at[Week, "Average[H]"] = Average_Hours
        Events_Weeks.at[Week, "Week Utilization[%]"] = Week_Utilization
        Events_Weeks.at[Week, "Active Days Utilization[%]"] = Active_Days_Utilization

        del Filtered_Df

    Events_Weeks["Days"] = Events_Weeks["Days"].astype(int)
    Events_Weeks["Total Events"] = Events_Weeks["Total Events"].astype(int)
    Events_Weeks = Events_Weeks.reset_index().rename(columns={"index": "Week"})	   

    # ---------------------------------------------------------------------------------- Day Charts ---------------------------------------------------------------------------------- #
    # Generate charts - Project And Activity
    Charts.Gen_Chart_Project_Activity(Settings=Settings, Configuration=Configuration, window=window, Calculation_source=Calculation_source, Category="Project", theme="Dark", Events=Events, Report_Period_End=Report_Period_End, File_Sub_Path=File_Sub_Path)
    Charts.Gen_Chart_Project_Activity(Settings=Settings, Configuration=Configuration, window=window, Calculation_source=Calculation_source, Category="Project", theme="Light", Events=Events, Report_Period_End=Report_Period_End, File_Sub_Path=File_Sub_Path)
    Charts.Gen_Chart_Project_Activity(Settings=Settings, Configuration=Configuration, window=window, Calculation_source=Calculation_source, Category="Activity", theme="Dark", Events=Events, Report_Period_End=Report_Period_End, File_Sub_Path=File_Sub_Path)
    Charts.Gen_Chart_Project_Activity(Settings=Settings, Configuration=Configuration, window=window, Calculation_source=Calculation_source, Category="Activity", theme="Light", Events=Events, Report_Period_End=Report_Period_End, File_Sub_Path=File_Sub_Path)

    # Utilization
    Utilization_Start_Date = min(Events["Date"])
    Utilization_Start_Date_dt = datetime.strptime(Utilization_Start_Date, Date_Format)
    Utilization_End_Date = max(Events["Date"])
    Utilization_End_Date_dt = datetime.strptime(Utilization_End_Date, Date_Format)
    Utilization_Event_Calendar_df = Get_Utilization_Calendar(Events=Events, Utilization_Start_Date_dt=Utilization_Start_Date_dt, Utilization_End_Date_dt=Utilization_End_Date_dt, Date_Format=Date_Format)

    # Utilization surplus --> for Totals
    Utilization_Surplus_hours = None    # Must be as default value
    Input_End_Date_str = Utilization_End_Date_dt.strftime(format=Date_Format)
    KM_Cumulative_Util_by_Date = Utilization_Event_Calendar_df.loc[f"{Input_End_Date_str}"]["KM_Cumulative_Utilization"]
    Reported_Cumulative_Time_by_Date = Utilization_Event_Calendar_df.loc[f"{Input_End_Date_str}"]["Reported_Cumulative_Time"]
    Utilization_Surplus_hours = float(round(number=Reported_Cumulative_Time_by_Date - KM_Cumulative_Util_by_Date, ndigits=2))

    # Prevents chart to crash interpolation
    if Total_Days_w > 1:
        Charts.Gen_Chart_Calendar_Utilization(Settings=Settings, Configuration=Configuration, window=window, theme="Dark", Utilization_Calendar_df=Utilization_Event_Calendar_df, File_Sub_Path=File_Sub_Path)
        Charts.Gen_Chart_Calendar_Utilization(Settings=Settings, Configuration=Configuration, window=window, theme="Light", Utilization_Calendar_df=Utilization_Event_Calendar_df, File_Sub_Path=File_Sub_Path)
    else:
        pass

    # ---------------------------------------------------------------------------------- Totals ---------------------------------------------------------------------------------- #
    # Calculation
    Total_Duration_hours = round(Events["Duration_H"].sum(), 2)
    Mean_Duration_hours = round(Events["Duration_H"].mean(), 2)
    Event_counts = Events.shape[0]
    
    # Reporting Period Utilization
    if type(Report_Period_Active_Days) is int:
        Period_Utilization = Report_Period_Active_Days * 8

        # Load already registered Events to sum with totals
        Reporting_Period_Utilization = round(number=round(number=Total_Duration_hours, ndigits=0) / (Period_Utilization) * 100, ndigits=2)
    else:
        # Cannot divide by 0
        Reporting_Period_Utilization = None
    My_Calendar_Utilization = My_Day_Utilization_w

    Totals_dict = {
        "Total_Duration_hours": Total_Duration_hours,
        "Mean_Duration_hours": Mean_Duration_hours,
        "Event_counts": Event_counts,
        "My_Calendar_Utilization": My_Calendar_Utilization,
        "Reporting_Period_Utilization": Reporting_Period_Utilization,
        "Utilization_Surplus_hours": Utilization_Surplus_hours}
    
    Totals_df = DataFrame(data=Totals_dict, columns=list(Totals_dict.keys()), index=[0])

    # ---------------------------------------------------------------------------------- PostProcessing ---------------------------------------------------------------------------------- #
    # Save Files
    Events_Project_Concat.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Project.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")
    Events_Activity_Concat.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Activity.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")
    Events_WeekDays.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_WeekDays.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")
    Events_Weeks.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Weeks.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")
    Totals_df.to_csv(path_or_buf=Data_Functions.Absolute_path(relative_path=f"Operational\\{File_Sub_Path}\\Events_Totals.csv"), index=False, sep=";", header=True, encoding="utf-8-sig")