# Import Libraries
from customtkinter import CTk, CTkFrame

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_User_Dashboard(Settings: dict, Configuration: dict, Frame: CTk|CTkFrame):
    Members_dict = Settings["0"]["General"]["User"]["Managed_Team"]
    Member_List = Defaults_Lists.List_from_Dict(Dictionary=Members_dict, Key_Argument="User Name")

    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_User_Dashboard_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_User_Dashboard_Work_Detail_Area.grid_propagate(flag=False)

    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_User_Dashboard_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("Totals")
    Tab_Gen.pack_propagate(flag=False)

    if Member_List:
        for member in Member_List:
            member_order = 2    # From 2 as second Tab
            Tab_Cal = TabView.add(f"{member}")
            Tab_Cal.pack_propagate(flag=False)
            Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children[f"!ctkbutton{member_order}"]
            Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Team member dashboard.", ToolTip_Size="Normal")

            # TODO --> Dashboard to each page of each person

            member_order += 1

    TabView.set("Totals")

    # Build look of Widget
    Frame_User_Dashboard_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")
