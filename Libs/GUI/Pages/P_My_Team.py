# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_User_Dashboard(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTk|CTkFrame):
    Members_dict = Settings["0"]["General"]["User"]["Managed_Team"]
    Member_List = Defaults_Lists.List_from_Dict(Dictionary=Members_dict, Key_Argument="User Name")

    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_User_Dashboard_Work_Main_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Main", GUI_Level_ID=0)

    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_User_Dashboard_Work_Main_Area, Tab_size="Normal", GUI_Level_ID=1)
    Tab_Gen = TabView.add("Totals")

    if Member_List:
        for member in Member_List:
            member_order = 2    # From 2 as second Tab
            Tab_Cal = TabView.add(f"{member}")
            Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children[f"!ctkbutton{member_order}"]
            Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Team member dashboard.", ToolTip_Size="Normal", GUI_Level_ID=1)

            # TODO --> Dashboard to each page of each person

            member_order += 1

    TabView.set("Totals")

    # Build look of Widget
    Frame_User_Dashboard_Work_Main_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)
