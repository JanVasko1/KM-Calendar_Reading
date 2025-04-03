# Import Libraries
import json

from customtkinter import CTk, CTkFrame, CTkButton
import pywinstyles

import Libs.GUI.Widgets.W_Settings as W_Settings
import Libs.GUI.Elements as Elements

def Page_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["0"]["General"]["User"]["User_Type"]

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    Tab_Gen = TabView.add("General")
    Tab_Cal = TabView.add("Calendar")
    Tab_E_G = TabView.add("Events - General")
    Tab_E_Spec = TabView.add("Events - Special")
    Tab_E_E = TabView.add("Events - Empty")
    Tab_E_A = TabView.add("Events - Rules")
    if User_Type == "Manager":
        Tab_Team = TabView.add("My Team")

        Tab_Team_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton7"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="MY Team base setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    else:
        pass
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Cal_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_E_G_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Tab_E_Spec_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton4"]
    Tab_E_E_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton5"]
    Tab_E_A_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton6"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Cal_ToolTip_But, message="Base calendar From/To + Day Starting and Ending Event setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_G_ToolTip_But, message="Multiple general setup related to Events.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_Spec_ToolTip_But, message="Special Events which needs special treatment.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_E_ToolTip_But, message="Filling Empty time Tool and Split too long Empty place.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_A_ToolTip_But, message="Rule base Event Handling tools setup.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- General ---------- #
    Frame_Tab_Gen_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_A.pack_propagate(flag=False)
    Frame_Tab_Gen_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_B.pack_propagate(flag=False)
    Frame_Tab_Gen_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_C.pack_propagate(flag=False)

    Appearance_Widget = W_Settings.Settings_General_Appearance(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_A, GUI_Level_ID=2)
    User_Widget = W_Settings.Settings_User_Widget(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_A, GUI_Level_ID=2)
    Sharepoint_Widget = W_Settings.Settings_General_Sharepoint(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)
    Exchange_Widget = W_Settings.Settings_General_Exchange(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)
    Formats_Widget = W_Settings.Settings_General_Formats(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_C, GUI_Level_ID=2)

    # ---------- Calendar Page ---------- #
    Frame_Tab_Cal_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_A.pack_propagate(flag=False)
    Frame_Tab_Cal_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_B.pack_propagate(flag=False)
    Frame_Tab_Cal_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_C.pack_propagate(flag=False)

    My_Calendar_Widget = W_Settings.Settings_Calendar_Working_Hours(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_A, GUI_Level_ID=2)
    KM_Calendar_Widget = W_Settings.Settings_Calendar_Vacation(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_B, GUI_Level_ID=2)
    Calendar_Start_End_Widget = W_Settings.Settings_Calendar_Start_End_Time(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_C, GUI_Level_ID=2)

    # ---------- Event-General Page ---------- #
    Frame_Tab_E_G_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_G_Column_A.pack_propagate(flag=False)
    Frame_Tab_E_G_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_G_Column_B.pack_propagate(flag=False)
    Frame_Tab_E_G_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_G_Column_C.pack_propagate(flag=False)

    Skip_General_Widget = W_Settings.Settings_Events_General_Skip(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_G_Column_A, GUI_Level_ID=2)
    Join_Widget = W_Settings.Settings_Join_events(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_G_Column_B, GUI_Level_ID=2)
    Splitting_Widget = W_Settings.Settings_Events_Split(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_G_Column_B, GUI_Level_ID=2)
    Parallel_Widget = W_Settings.Settings_Parallel_events(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_G_Column_C, GUI_Level_ID=2)

    # ---------- Event-Special Page ---------- #
    Frame_Tab_E_Spec_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_Spec_Column_A.pack_propagate(flag=False)
    Frame_Tab_E_Spec_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_Spec_Column_B.pack_propagate(flag=False)
    Frame_Tab_E_Spec_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_Spec_Column_C.pack_propagate(flag=False)

    Lunch_Widget = W_Settings.Settings_Events_General_Lunch(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_Spec_Column_A, GUI_Level_ID=2)
    Vacation_Widget = W_Settings.Settings_Events_General_Vacation(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_Spec_Column_A, GUI_Level_ID=2)
    SickDay_Widget = W_Settings.Settings_Events_General_SickDay(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_Spec_Column_B, GUI_Level_ID=2)
    HomeOffice_Widget = W_Settings.Settings_Events_General_HomeOffice(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_Spec_Column_B, GUI_Level_ID=2)
    Private_Widget = W_Settings.Settings_Events_General_Private(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_Spec_Column_C, GUI_Level_ID=2)

    # ---------- Event-Empty Page ---------- #
    Frame_Tab_E_E_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_E, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_Empty_General_Widget = W_Settings.Settings_Events_Empty_Generally(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_E_Column_A, GUI_Level_ID=2)
    Event_Scheduler_Widget = W_Settings.Settings_Events_Empty_Schedule(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_E_Column_A, GUI_Level_ID=2)

    # ---------- Event-AutoFill Page ---------- #
    Frame_Tab_E_A_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_A, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_AutoFiller_Widget = W_Settings.Settings_Events_AutoFill(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_A_Column_A, GUI_Level_ID=2)
    Event_Activity_Correction_Widget = W_Settings.Settings_Events_Activity_Correction(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_E_A_Column_A, GUI_Level_ID=2)

    if User_Type == "Manager":
        # ---------- Managed Team ---------- #
        Frame_Tab_Team_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Team, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

        Managed_Team_Widget = W_Settings.Settings_My_Team(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Team_Column_A, GUI_Level_ID=2)
    else:
        pass
    
    # Build look of Widget
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Tab_Gen_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Gen_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Gen_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Appearance_Widget.Show()
    User_Widget.Show()
    Sharepoint_Widget.Show()
    Exchange_Widget.Show()
    Formats_Widget.Show()

    Frame_Tab_Cal_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Cal_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Cal_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    My_Calendar_Widget.Show()
    KM_Calendar_Widget.Show()
    Calendar_Start_End_Widget.Show()

    Frame_Tab_E_G_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_G_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_G_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Skip_General_Widget.Show()
    Join_Widget.Show()
    Splitting_Widget.Show()
    Parallel_Widget.Show()

    Frame_Tab_E_Spec_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_Spec_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_Spec_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Lunch_Widget.Show()
    Vacation_Widget.Show()
    SickDay_Widget.Show()
    HomeOffice_Widget.Show()
    Private_Widget.Show()

    Frame_Tab_E_E_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Event_Empty_General_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Scheduler_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_E_A_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Event_AutoFiller_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Activity_Correction_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    if User_Type == "Manager":
        # Managed Team
        Frame_Tab_Team_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        Managed_Team_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    else:
        pass
