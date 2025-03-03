# Import Libraries
from pandas import read_csv

from customtkinter import CTk, CTkFrame

import Libs.Data_Functions as Data_Functions
import Libs.GUI.Widgets.W_DashBoard as W_DashBoard
import Libs.GUI.Elements as Elements

def Page_Dashboard(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_DashBoard_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Triple_size", GUI_Level_ID=1)

    # ------------------------- Dashboard work Area -------------------------#
    try:
        Totals_Summary_Df = read_csv(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\Events_Totals.csv"), sep=";")
        Project_DF = read_csv(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\Events_Project.csv"), sep=";")
        Activity_Df = read_csv(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\Events_Activity.csv"), sep=";")
        WeekDays_Df = read_csv(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\Events_WeekDays.csv"), sep=";")
        Weeks_DF = read_csv(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\Events_Weeks.csv"), sep=";")

        # Total Line
        Total_Duration_hours = float(Totals_Summary_Df.iloc[0]["Total_Duration_hours"])
        Mean_Duration_hours = float(Totals_Summary_Df.iloc[0]["Mean_Duration_hours"])
        Event_counts = int(Totals_Summary_Df.iloc[0]["Event_counts"])
        Reporting_Period_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["Reporting_Period_Utilization"], ndigits=2))
        My_Calendar_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["My_Calendar_Utilization"], ndigits=2))
        Utilization_Surplus_hours = float(Totals_Summary_Df.iloc[0]["Utilization_Surplus_hours"])

        Creation_Date = Settings["0"]["General"]["DashBoard"]["DashBoard"]["Creation_Date"]
        Data_Period = Settings["0"]["General"]["DashBoard"]["DashBoard"]["Data_Period"]
        Data_Source = Settings["0"]["General"]["DashBoard"]["DashBoard"]["Data_Source"]
        DashBoard_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
        DashBoard_text_Additional.configure(text=f"""Generated on: {Creation_Date} -- Period: {Data_Period} -- Dates Source: {Data_Source}.""")

        Frame_Dashboard_Total_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Totals_Line", GUI_Level_ID=1)
        Frame_Dashboard_Total_Line.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Counter = W_DashBoard.DashBoard_Totals_Counter_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Count", Widget_Line="Totals_Line", Widget_size="Normal", Data=Event_counts, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Counter.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Total = W_DashBoard.DashBoard_Totals_Total_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Total", Widget_Line="Totals_Line", Widget_size="Normal", Data=Total_Duration_hours, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Total.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Average = W_DashBoard.DashBoard_Totals_Average_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Average", Widget_Line="Totals_Line", Widget_size="Normal", Data=Mean_Duration_hours, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Average.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Active_Day_Util = W_DashBoard.DashBoard_Totals_Active_Day_Util_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="My Active Days Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=My_Calendar_Utilization, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Active_Day_Util.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Util_by_today_surplus = W_DashBoard.DashBoard_Totals_Utilization_Surplus_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Displayed period surplus", Widget_Line="Totals_Line", Widget_size="Normal", Data=Utilization_Surplus_hours, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Util_by_today_surplus.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Report_Per_Util = W_DashBoard.DashBoard_Totals_Report_Period_Util_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Reported Period Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=Reporting_Period_Utilization, GUI_Level_ID=2)
        Frame_DashBoard_Totals_Report_Per_Util.pack_propagate(flag=False)

        # Project Activity Line
        Frame_Dashboard_Project_Activity_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Project_Activity_Line", GUI_Level_ID=1)
        Frame_Dashboard_Project_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section", GUI_Level_ID=1)
        Frame_Dashboard_Project_Detail_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Detail_Section", GUI_Level_ID=1)
        Frame_DashBoard_Project_Frame = W_DashBoard.DashBoard_Project_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Detail_Section, Label="Projects", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Project_DF=Project_DF, GUI_Level_ID=2)
        Frame_Dashboard_Project_Side_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Side_Section", GUI_Level_ID=1)
        Frame_DashBoard_Project_Detail1_Frame = W_DashBoard.DashBoard_Project_Detail1_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Most Occurrence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF, GUI_Level_ID=2)
        Frame_DashBoard_Project_Detail1_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Project_Detail2_Frame = W_DashBoard.DashBoard_Project_Detail2_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF, GUI_Level_ID=2)
        Frame_DashBoard_Project_Detail2_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Project_Detail3_Frame = W_DashBoard.DashBoard_Project_Detail3_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF, GUI_Level_ID=2)
        Frame_DashBoard_Project_Detail3_Frame.pack_propagate(flag=False)

        Frame_Dashboard_Activity_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section", GUI_Level_ID=1)
        Frame_Dashboard_Activity_Detail_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Detail_Section", GUI_Level_ID=1)
        Frame_DashBoard_Activity_Frame = W_DashBoard.DashBoard_Activity_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Detail_Section, Label="Activity", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Activity_Df=Activity_Df, GUI_Level_ID=2)
        Frame_Dashboard_Activity_Side_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Side_Section", GUI_Level_ID=1)
        Frame_DashBoard_Activity_Detail1_Frame = W_DashBoard.DashBoard_Activity_Detail1_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Occurrence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df, GUI_Level_ID=2)
        Frame_DashBoard_Activity_Detail1_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Activity_Detail2_Frame = W_DashBoard.DashBoard_Activity_Detail2_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df, GUI_Level_ID=2)
        Frame_DashBoard_Activity_Detail2_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Activity_Detail3_Frame = W_DashBoard.DashBoard_Activity_Detail3_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df, GUI_Level_ID=2)
        Frame_DashBoard_Activity_Detail3_Frame.pack_propagate(flag=False)

        # WeekDay and Weeks Line
        Frame_Dashboard_WeekDay_Weeks_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="WeekDay_Weeks_Line", GUI_Level_ID=1)
        Frame_DashBoard_WeekDays_Frame = W_DashBoard.DashBoard_WeekDays_Widget(Configuration=Configuration, Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="WeekDays", Widget_Line="WeekDay_Weeks", Widget_size="Normal", WeekDays_Df=WeekDays_Df, GUI_Level_ID=2)
        Frame_DashBoard_Weeks_Frame = W_DashBoard.DashBoard_Weeks_Widget(Configuration=Configuration, Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="Weeks", Widget_Line="WeekDay_Weeks", Widget_size="Normal", Weeks_DF=Weeks_DF, GUI_Level_ID=2)

        # Day Chart Line
        Frame_Dashboard_Day_Chart_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Day_Chart_Line", GUI_Level_ID=1)
        Frame_DashBoard_Chart_Frame = W_DashBoard.DashBoard_Chart_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Day_Chart_Line, Label="Charts", Widget_Line="WeekChart", Widget_size="Normal", GUI_Level_ID=2)
        Frame_DashBoard_Chart_Frame.pack_propagate(flag=False)

        # Build look of Widget
        Frame_DashBoard_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        DashBoard_text_Additional.pack(side="top", fill="none", expand=False, padx=(1250, 20), pady=(0, 0))

        Frame_Dashboard_Total_Line.pack(side="top", fill="both", expand=True, padx=0, pady=(10, 0))
        Frame_DashBoard_Totals_Counter.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Total.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Average.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Active_Day_Util.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Util_by_today_surplus.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Report_Per_Util.pack(side="left", fill="none", expand=True, padx=0, pady=0)

        Frame_Dashboard_Project_Activity_Line.pack(side="top", fill="x", expand=True, padx=5, pady=(10, 0))
        Frame_Dashboard_Project_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Project_Detail_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_DashBoard_Project_Frame.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Project_Side_Section.pack(side="left", fill="y", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail1_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail2_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail3_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)

        Frame_Dashboard_Activity_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Activity_Detail_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_DashBoard_Activity_Frame.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Activity_Side_Section.pack(side="left", fill="y", expand=True, padx=0, pady=0)
        Frame_DashBoard_Activity_Detail1_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)
        Frame_DashBoard_Activity_Detail2_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)
        Frame_DashBoard_Activity_Detail3_Frame.pack(side="top", fill="y", expand=True, padx=5, pady=5)

        Frame_Dashboard_WeekDay_Weeks_Line.pack(side="top", fill="x", expand=True, padx=5, pady=(10, 0))
        Frame_DashBoard_WeekDays_Frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        Frame_DashBoard_Weeks_Frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        Frame_Dashboard_Day_Chart_Line.pack(side="top", fill="x", expand=True, padx=0, pady=(10, 0))
        Frame_DashBoard_Chart_Frame.pack(side="top", fill="x", expand=False, padx=5, pady=5)
    except:
        Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="Dashboard not all data available, please run Downloader first.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
