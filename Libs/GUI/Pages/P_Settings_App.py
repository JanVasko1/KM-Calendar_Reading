# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Widgets.W_Settings_App as W_Settings_App
import Libs.GUI.Elements as Elements

def Page_App_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["0"]["General"]["User"]["User_Type"]

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    Tab_Gen = TabView.add("General")
    Tab_Cal = TabView.add("Calendar")
    if User_Type == "Manager":
        Tab_Team = TabView.add("My Team")

        Tab_Team_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="MY Team base setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    else:
        pass
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Cal_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Cal_ToolTip_But, message="Base calendar From/To + Day Starting and Ending Event setup.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- General ---------- #
    Frame_Tab_Gen_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_A.pack_propagate(flag=False)
    Frame_Tab_Gen_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_B.pack_propagate(flag=False)
    Frame_Tab_Gen_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_C.pack_propagate(flag=False)

    Appearance_Widget = W_Settings_App.Settings_General_Appearance(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_A, GUI_Level_ID=2)
    User_Widget = W_Settings_App.Settings_User_Widget(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_A, GUI_Level_ID=2)
    Sharepoint_Widget = W_Settings_App.Settings_General_Sharepoint(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)
    Exchange_Widget = W_Settings_App.Settings_General_Exchange(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)
    Formats_Widget = W_Settings_App.Settings_General_Formats(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Gen_Column_C, GUI_Level_ID=2)

    # ---------- Calendar Page ---------- #
    Frame_Tab_Cal_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_A.pack_propagate(flag=False)
    Frame_Tab_Cal_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_B.pack_propagate(flag=False)
    Frame_Tab_Cal_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_C.pack_propagate(flag=False)

    My_Calendar_Widget = W_Settings_App.Settings_Calendar_Working_Hours(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_A, GUI_Level_ID=2)
    KM_Calendar_Widget = W_Settings_App.Settings_Calendar_Vacation(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_B, GUI_Level_ID=2)
    Calendar_Start_End_Widget = W_Settings_App.Settings_Calendar_Start_End_Time(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Cal_Column_C, GUI_Level_ID=2)

    if User_Type == "Manager":
        # ---------- Managed Team ---------- #
        Frame_Tab_Team_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Team, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

        Managed_Team_Widget = W_Settings_App.Settings_My_Team(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Team_Column_A, GUI_Level_ID=2)
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

    if User_Type == "Manager":
        # Managed Team
        Frame_Tab_Team_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        Managed_Team_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    else:
        pass
