import Libs.Defaults_Lists as Defaults_Lists
from pandas import DataFrame
from datetime import datetime
import pandas

# ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Personnel_number = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]
Date_Format = Settings["General"]["Formats"]["Date"]
Time_Format = Settings["General"]["Formats"]["Time"]

# ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def DataFrame_WeekDay(row) -> str:
    x_dt = datetime.strptime(row, Date_Format)
    WeekDay = x_dt.strftime("%A")
    return WeekDay

def DataFrame_Week(row) -> str:
    x_dt = datetime.strptime(row, Date_Format)
    ISO_Date = x_dt.isocalendar()

    Week = ISO_Date.week
    Year = ISO_Date.year

    X_Week = f"{Year}-{Week}"
    return X_Week

def Duration_Couter(Time1: str, Time2: str) -> float:
    try:
        # Count duration between 2 strings in fload
        Time2_dt = datetime.strptime(Time2, Time_Format)
        Time1_dt = datetime.strptime(Time1, Time_Format)
        Duration_dt = Time2_dt - Time1_dt
        Duration = Duration_dt.total_seconds() // 60 / 60
    except:
        Duration = 0
    return round(Duration, 2)

# ---------------------------------------------------------- Local Variables ---------------------------------------------------------- #
My_Monday_Start_WH = Settings["General"]["Calendar"]["Monday"]["Work_Hours"]["Start_Time"]
My_Monday_End_WH = Settings["General"]["Calendar"]["Monday"]["Work_Hours"]["End_Time"]
My_Monday_WH = Duration_Couter(Time1=My_Monday_Start_WH, Time2=My_Monday_End_WH)

My_Tuesday_Start_WH = Settings["General"]["Calendar"]["Tuesday"]["Work_Hours"]["Start_Time"]
My_Tuesday_End_WH = Settings["General"]["Calendar"]["Tuesday"]["Work_Hours"]["End_Time"]
My_Tuesday_WH = Duration_Couter(Time1=My_Tuesday_Start_WH, Time2=My_Tuesday_End_WH)

My_Wednesday_Start_WH = Settings["General"]["Calendar"]["Wednesday"]["Work_Hours"]["Start_Time"]
My_Wednesday_End_WH = Settings["General"]["Calendar"]["Wednesday"]["Work_Hours"]["End_Time"]
My_Wednesday_WH = Duration_Couter(Time1=My_Wednesday_Start_WH, Time2=My_Wednesday_End_WH)

My_Thursday_Start_WH = Settings["General"]["Calendar"]["Thursday"]["Work_Hours"]["Start_Time"]
My_Thursday_End_WH = Settings["General"]["Calendar"]["Thursday"]["Work_Hours"]["End_Time"]
My_Thursday_WH = Duration_Couter(Time1=My_Thursday_Start_WH, Time2=My_Thursday_End_WH)

My_Friday_Start_WH = Settings["General"]["Calendar"]["Friday"]["Work_Hours"]["Start_Time"]
My_Friday_End_WH = Settings["General"]["Calendar"]["Friday"]["Work_Hours"]["End_Time"]
My_Friday_WH = Duration_Couter(Time1=My_Friday_Start_WH, Time2=My_Friday_End_WH)

My_Saturday_Start_WH = Settings["General"]["Calendar"]["Saturday"]["Work_Hours"]["Start_Time"]
My_Saturday_End_WH = Settings["General"]["Calendar"]["Saturday"]["Work_Hours"]["End_Time"]
My_Saturday_WH = Duration_Couter(Time1=My_Saturday_Start_WH, Time2=My_Saturday_End_WH)

My_Sunday_Start_WH = Settings["General"]["Calendar"]["Sunday"]["Work_Hours"]["Start_Time"]
My_Sunday_End_WH = Settings["General"]["Calendar"]["Sunday"]["Work_Hours"]["End_Time"]
My_Sunday_WH = Duration_Couter(Time1=My_Sunday_Start_WH, Time2=My_Sunday_End_WH)

My_WH_dict = {
    "Monday": My_Monday_WH,
    "Tuesday": My_Tuesday_WH,
    "Wednesday": My_Wednesday_WH,
    "Thursday": My_Thursday_WH,
    "Friday": My_Friday_WH,
    "Saturday": My_Saturday_WH,
    "Sunday": My_Sunday_WH,
    }

KM_Monday_Start_WH = Settings["General"]["Calendar"]["Monday"]["Vacation"]["Start_Time"]
KM_Monday_End_WH = Settings["General"]["Calendar"]["Monday"]["Vacation"]["End_Time"]
KM_Monday_WH = Duration_Couter(Time1=KM_Monday_Start_WH, Time2=KM_Monday_End_WH)

KM_Tuesday_Start_WH = Settings["General"]["Calendar"]["Tuesday"]["Vacation"]["Start_Time"]
KM_Tuesday_End_WH = Settings["General"]["Calendar"]["Tuesday"]["Vacation"]["End_Time"]
KM_Tuesday_WH = Duration_Couter(Time1=KM_Tuesday_Start_WH, Time2=KM_Tuesday_End_WH)

KM_Wednesday_Start_WH = Settings["General"]["Calendar"]["Wednesday"]["Vacation"]["Start_Time"]
KM_Wednesday_End_WH = Settings["General"]["Calendar"]["Wednesday"]["Vacation"]["End_Time"]
KM_Wednesday_WH = Duration_Couter(Time1=KM_Wednesday_Start_WH, Time2=KM_Wednesday_End_WH)

KM_Thursday_Start_WH = Settings["General"]["Calendar"]["Thursday"]["Vacation"]["Start_Time"]
KM_Thursday_End_WH = Settings["General"]["Calendar"]["Thursday"]["Vacation"]["End_Time"]
KM_Thursday_WH = Duration_Couter(Time1=KM_Thursday_Start_WH, Time2=KM_Thursday_End_WH)

KM_Friday_Start_WH = Settings["General"]["Calendar"]["Friday"]["Vacation"]["Start_Time"]
KM_Friday_End_WH = Settings["General"]["Calendar"]["Friday"]["Vacation"]["End_Time"]
KM_Friday_WH = Duration_Couter(Time1=KM_Friday_Start_WH, Time2=KM_Friday_End_WH)

KM_Saturday_Start_WH = Settings["General"]["Calendar"]["Saturday"]["Vacation"]["Start_Time"]
KM_Saturday_End_WH = Settings["General"]["Calendar"]["Saturday"]["Vacation"]["End_Time"]
KM_Saturday_WH = Duration_Couter(Time1=KM_Saturday_Start_WH, Time2=KM_Saturday_End_WH)

KM_Sunday_Start_WH = Settings["General"]["Calendar"]["Sunday"]["Vacation"]["Start_Time"]
KM_Sunday_End_WH = Settings["General"]["Calendar"]["Sunday"]["Vacation"]["End_Time"]
KM_Sunday_WH = Duration_Couter(Time1=KM_Sunday_Start_WH, Time2=KM_Sunday_End_WH)

KM_WH_dict = {
    "Monday": KM_Monday_WH,
    "Tuesday": KM_Tuesday_WH,
    "Wednesday": KM_Wednesday_WH,
    "Thursday": KM_Thursday_WH,
    "Friday": KM_Friday_WH,
    "Saturday": KM_Saturday_WH,
    "Sunday": KM_Sunday_WH,
    }

# ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
def Generate_Summary(Events: DataFrame) -> DataFrame:
    #Update Events Dataframe
    Events["Personnel number"] = Personnel_number
    Events["Start_Time"] = Events["Start_Time"].astype(str)
    Events["End_Time"] = Events["End_Time"].astype(str)
    Events[["Start_Date_Del", "Start_Time"]] = Events["Start_Time"].str.split(" ", expand=True)
    Events[["End_Date_Del", "End_Time"]] = Events["End_Time"].str.split(" ", expand=True)
    Events["Start_Time"] = Events["Start_Time"].map(lambda x: x[:])
    Events["End_Time"] = Events["End_Time"].map(lambda x: x[:])
    Events["Duration_H"] = Events["Duration"].map(lambda x: round(x/60, 2))
    
    # ------------------------------ Statistics ------------------------------ #
    # ---------------------------------------------------------------------------------- Totals ---------------------------------------------------------------------------------- #
    Total_Duration_hours = round(Events["Duration_H"].sum(), 2)
    Mean_Duration_hours = round(Events["Duration_H"].mean(), 2)
    Event_counts = Events.shape[0]
    Total_Coverage = 0          #! Dodělat --> spočítat coverage (někde už to spočítany je) spočítat i ostatní main statistiky!!! a vrátit je zpátky do hlavního programu
    Day_Average_Coverage = 0    #! Dodělat --> spočítat coverage (někde už to spočítany je) spočítat i ostatní main statistiky!!! a vrátit je zpátky do hlavního programu

    Totals_dict = {
        "Total_Duration_hours": Total_Duration_hours,
        "Mean_Duration_hours": Mean_Duration_hours,
        "Event_counts": Event_counts,
        "Total_Coverage": Total_Coverage,
        "Day_Average_Coverage": Day_Average_Coverage}
    
    Totals_df = DataFrame(data=Totals_dict, columns=list(Totals_dict.keys()), index=[0])
    Totals_df.to_csv(path_or_buf=f"Operational\\Events_Totals.csv", index=False, sep=";", header=True, encoding="utf-8-sig")


    # ---------------------------------------------------------------------------------- Projects ---------------------------------------------------------------------------------- #
    Events_Project_GR = Events.loc[:, ["Project", "Duration_H"]]
    Events_Project_Sum = Events_Project_GR.groupby(["Project"]).sum()
    Events_Project_Sum.rename(columns={"Duration_H": "Total[H]"}, inplace=True)
    Events_Project_Mean = Events_Project_GR.groupby(["Project"]).mean()
    Events_Project_Mean.rename(columns={"Duration_H": "Average[H]"}, inplace=True)
    Events_Project_Mean["Average[H]"] = Events_Project_Mean["Average[H]"].map(lambda x: round(x, 2))
    Events_Project_Count = Events_Project_GR.groupby(["Project"]).count()
    Events_Project_Count.rename(columns={"Duration_H": "Count"}, inplace=True)
    Events_Project_Concanet = pandas.concat(objs=[Events_Project_Count, Events_Project_Sum, Events_Project_Mean], axis=1, join="inner")

    # Summary line
    Project_Count_Sumary = Events_Project_Concanet["Count"].sum()
    Project_TotalH_Sumary = Events_Project_Concanet["Total[H]"].sum()
    Project_AverageH_Sumary = round(Project_TotalH_Sumary / Project_Count_Sumary, 2)
    Events_Project_Concanet.loc["Summary"] = [Project_Count_Sumary, Project_TotalH_Sumary, Project_AverageH_Sumary]
    Events_Project_Concanet["Count"] = Events_Project_Concanet["Count"].astype(int)
    Events_Project_Concanet = Events_Project_Concanet.reset_index().rename(columns={"index": "Project"})		
    Events_Project_Concanet.to_csv(path_or_buf=f"Operational\\Events_Project.csv", index=False, sep=";", header=True, encoding="utf-8-sig")

    # ---------------------------------------------------------------------------------- Activity ---------------------------------------------------------------------------------- #
    Events_Activity_GR = Events.loc[:, ["Activity", "Duration_H"]]
    Events_Activity_Sum = Events_Activity_GR.groupby(["Activity"]).sum()
    Events_Activity_Sum.rename(columns={"Duration_H": "Total[H]"}, inplace=True)
    Events_Activity_Mean = Events_Activity_GR.groupby(["Activity"]).mean()
    Events_Activity_Mean.rename(columns={"Duration_H": "Average[H]"}, inplace=True)
    Events_Activity_Mean["Average[H]"] = Events_Activity_Mean["Average[H]"].map(lambda x: round(x, 2))
    Events_Activity_Count = Events_Activity_GR.groupby(["Activity"]).count()
    Events_Activity_Count.rename(columns={"Duration_H": "Count"}, inplace=True)
    Events_Activity_Concanet = pandas.concat(objs=[Events_Activity_Count, Events_Activity_Sum, Events_Activity_Mean], axis=1, join="inner")

    # Summary line
    Activity_Count_Sumary = Events_Activity_Concanet["Count"].sum()
    Activity_TotalH_Sumary = Events_Activity_Concanet["Total[H]"].sum()
    Activity_AverageH_Sumary = round(Activity_TotalH_Sumary / Activity_Count_Sumary, 2)
    Events_Activity_Concanet.loc["Summary"] = [Activity_Count_Sumary, Activity_TotalH_Sumary, Activity_AverageH_Sumary]
    Events_Activity_Concanet["Count"] = Events_Activity_Concanet["Count"].astype(int)
    Events_Activity_Concanet = Events_Activity_Concanet.reset_index().rename(columns={"index": "Activity"})		
    Events_Activity_Concanet.to_csv(path_or_buf=f"Operational\\Events_Activity.csv", index=False, sep=";", header=True, encoding="utf-8-sig")


    # ---------------------------------------------------------------------------------- Weekday ---------------------------------------------------------------------------------- #
    WeekDays_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    Events_WeekDays = pandas.DataFrame(index=WeekDays_list, columns=["Days Count", "Total Events", "Total[H]", "Average[H]", "My Utilization[%]", "Utilization[%]"])
    Events_WeekDays_GR = Events.loc[:, ["Start_Date", "Project", "Activity", "Duration_H"]]
    Events_WeekDays_GR["WeekDay"] =  Events_WeekDays_GR["Start_Date"].apply(DataFrame_WeekDay)
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
        Filtered_Df = Events_WeekDays_GR[mask]

        if Filtered_Df.empty:
            pass
        else:
            Used_Days += 1  # Počet průchodů --> kvůli Utilization
            if (WeekDay == "Saturday") or (WeekDay == "Sunday"):
                pass
            else:
                Used_Days_wo += 1

            WeekDay_dates_list = list(set(Filtered_Df["Start_Date"]))
            WeekDay_dates_count = len(WeekDay_dates_list)
            Filtered_Df.drop(labels=["Start_Date"], axis=1, inplace=True)

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
    Events_WeekDays.to_csv(path_or_buf=f"Operational\\Events_WeekDays.csv", index=False, sep=";", header=True, encoding="utf-8-sig")

    # ---------------------------------------------------------------------------------- Weeks ---------------------------------------------------------------------------------- #
    Events_Weeks_GR = Events.loc[:, ["Start_Date", "Project", "Duration_H"]]
    Events_Weeks_GR["Week"] =  Events_Weeks_GR["Start_Date"].apply(DataFrame_Week)
    Events_Weeks_GR["WeekDay"] =  Events_Weeks_GR["Start_Date"].apply(DataFrame_WeekDay)
    Weeks_list = list(set(Events_Weeks_GR["Week"]))
    Weeks_list.sort()
    Events_Weeks = pandas.DataFrame(index=Weeks_list, columns=["Days", "Days w/o weekend", "Total Events", "Total[H]", "Average[H]", "Week Utilization[%]", "Active Days Utilization[%]"])

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
        Filtered_Df = Events_Weeks_GR[mask1]

        if Filtered_Df.empty:
            pass
        else:
            Week_days_list = list(set(Filtered_Df["Start_Date"]))
            Week_days_count = len(Week_days_list)

            # Weekdays without weekend
            Filtered_Df_wo = Events_Weeks_GR[mask1 & mask2 & mask3]
            Week_days_list_wo = list(set(Filtered_Df_wo["Start_Date"]))
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
    Events_Weeks.to_csv(path_or_buf=f"Operational\\Events_Weeks.csv", index=False, sep=";", header=True, encoding="utf-8-sig")
    
    # ---------------------------------------------------------------------------------- TimeSheet ----------------------------------------------------------------------------------
    Events.drop(labels=["End_Date", "Recurring", "Meeting_Room", "All_Day_Event", "Event_Empty_Insert", "Within_Working_Hours", "Start_Date_Del", "End_Date_Del"], axis=1, inplace=True)
    Events.rename(columns={"Start_Date": "Date", "Project": "Network Description", "Subject": "Activity description", "Start_Time": "Start Time", "End_Time": "End Time", "": ""}, inplace=True)
    Events = Events[["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location", "Duration", "Busy_Status"]]

    Events = Defaults_Lists.Dataframe_sort(Sort_Dataframe=Events, Columns_list=["Date", "Start Time"], Accenting_list=[True, True]) 
    pandas.set_option("display.max_rows", None)
    Events.drop(labels=["Duration", "Busy_Status"], axis=1, inplace=True)
    Events.to_csv(path_or_buf=f"Operational\\Events.csv", index=False, sep=";", header=True, encoding="utf-8-sig")
