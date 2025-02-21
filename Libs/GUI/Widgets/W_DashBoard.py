# Import Libraries
import os
from pandas import DataFrame

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

import webview 
from customtkinter import CTk, CTkFrame
from CTkMessagebox import CTkMessagebox

# -------------------------------------------------------------------------------------------------------------------------------------------------- Local Functions -------------------------------------------------------------------------------------------------------------------------------------------------- #
def DashBoard_Project():
    Theme = Defaults_Lists.Get_Current_Theme()
    if Theme == "System":
        Theme = "Dark"
    else:
        pass

    Chart_path = Defaults_Lists.Absolute_path(relative_path=f"Operational\\DashBoard\\DashBoard_Project_{Theme}.html")
    Chart_Exist = os.path.isfile(Chart_path)
    if Chart_Exist == True:
        webview.create_window(title="Project Detail", width=1645, height=428, url=Chart_path, frameless=True, easy_drag=True, resizable=True, shadow=True) 
        webview.start()
    else:
        Error_Message = CTkMessagebox(title="Error", message=f"Chart of Project not available, please download data first.", icon="cancel", fade_in_duration=1)
        Error_Message.get()

def DashBoard_Activity():
    Theme = Defaults_Lists.Get_Current_Theme()
    if Theme == "System":
        Theme = "Dark"
    else:
        pass

    Chart_path = Defaults_Lists.Absolute_path(relative_path=f"Operational\\DashBoard\\DashBoard_Activity_{Theme}.html")
    Chart_Exist = os.path.isfile(Chart_path)
    if Chart_Exist == True:
        webview.create_window(title="Activity Detail", width=1645, height=428, url=Chart_path, frameless=True, easy_drag=True, resizable=True, shadow=True) 
        webview.start()
    else:
        Error_Message = CTkMessagebox(title="Error", message=f"Chart of Activity not available, please download data first.", icon="cancel", fade_in_duration=1)
        Error_Message.get()

def DashBoard_Utilization():
    Theme = Defaults_Lists.Get_Current_Theme()
    if Theme == "System":
        Theme = "Dark"
    else:
        pass

    Chart_path = Defaults_Lists.Absolute_path(relative_path=f"Operational\\DashBoard\\DashBoard_Utilization_{Theme}.html")
    Chart_Exist = os.path.isfile(Chart_path)
    if Chart_Exist == True:
        webview.create_window(title="Utilization Detail", width=1645, height=428, url=Chart_path, frameless=True, easy_drag=True, resizable=True, shadow=True) 
        webview.start()
    else:
        Error_Message = CTkMessagebox(title="Error", message=f"Chart of Utilization not available, please download data first from Sharepoint.", icon="cancel", fade_in_duration=1)
        Error_Message.get()


# -------------------------------------------------------------------------------------------------------------------------------------------------- Dashboard Page Widgets -------------------------------------------------------------------------------------------------------------------------------------------------- #
def DashBoard_Totals_Total_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: float) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="history", Widget_Label_Tooltip="Shows total hours.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Total_Hours_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Total_Hours_text.configure(text=f"{str(Data)}")

    Total_Hours_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Total_Hours_unit_text.configure(text=f"hours")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Total_Hours_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Total_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Average_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: float) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="clock-arrow-up", Widget_Label_Tooltip="Shows Average hours per Event.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Average_Hours_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Average_Hours_text.configure(text=f"{str(Data)}")

    Average_Hours_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Average_Hours_unit_text.configure(text=f"/hours")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Average_Hours_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Average_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Counter_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="arrow-up-1-0", Widget_Label_Tooltip="Shows total counts of Events.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Event_Counter_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Event_Counter_text.configure(text=f"{str(Data)}")

    Event_Counter_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Event_Counter_unit_text.configure(text=f"")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Event_Counter_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Event_Counter_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Report_Period_Util_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="circle-percent", Widget_Label_Tooltip="Shows Utilization of Reporting Period.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Coverage_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Coverage_text.configure(text=f"{str(Data)}")

    Coverage_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Coverage_unit_text.configure(text=f"%")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Active_Day_Util_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="activity", Widget_Label_Tooltip="Shows utilization in relation to my calendar and for active days only.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Day_Average_Coverage_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Day_Average_Coverage_text.configure(text=f"{str(Data)}")

    Day_Average_Coverage_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Day_Average_Coverage_unit_text.configure(text=f"%")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Day_Average_Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Day_Average_Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Totals_Utilization_Surplus_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Data: int) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name="message-square-diff", Widget_Label_Tooltip="Shows hours if Im surplus against KM actual day utilization for Input End Date.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Day_Average_Coverage_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Main", Font_Size="Main")
    Day_Average_Coverage_text.configure(text=f"{str(Data)}")

    Day_Average_Coverage_unit_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Day_Average_Coverage_unit_text.configure(text=f"hours")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Day_Average_Coverage_unit_text.pack(side="right", padx=(0, 20), pady=(15,2))
    Day_Average_Coverage_text.pack(side="right", padx=0, pady=0)

    return Frame_Main


def DashBoard_Project_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Project_DF: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Table_Values = [["Project", "Count", "Total [H]", "Average [H]"]]
    Table_Data_List = Project_DF.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)

    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Shows Projects Details.", Scrollable=True) 
    Frame_Header = Frame_Main.children["!ctkframe"]
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Button --> Projects
    Button_Show_Projects = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Projects.configure(text="Detail", command = lambda:DashBoard_Project())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Projects, message="Shows project chart.", ToolTip_Size="Normal")

    # Table
    Project_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Body, Table_size="Dashboard_Project_Activity", columns=4, rows=Project_DF.shape[0] + 1)
    Project_Table.configure(values=Table_Values)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Projects.pack(side="right")
    Project_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Project_Detail1_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Project_DF: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Project_DF = Project_DF.head(-1)
    Most_Occurrence_ID =  Project_DF["Count"].idxmax()
    Most_Occurrence_Project = Project_DF.iloc[Most_Occurrence_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Most Occurrence", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Count_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Project_Count_text.configure(text=f"{Most_Occurrence_Project}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Count_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Project_Detail2_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Project_DF: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Project_DF = Project_DF.head(-1)
    Most_Hours_ID =  Project_DF["Total[H]"].idxmax()
    Most_Project_Hours = Project_DF.iloc[Most_Hours_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Most Hours", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Hours_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Project_Hours_text.configure(text=f"{Most_Project_Hours}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Project_Detail3_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Project_DF: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Project_DF = Project_DF.head(-1)
    Most_Hours_ID =  Project_DF["Average[H]"].idxmax()
    Most_Project_Avg_Hours = Project_DF.iloc[Most_Hours_ID]["Project"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Projects Average Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Project_Hours_Avg_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Project_Hours_Avg_text.configure(text=f"{Most_Project_Avg_Hours}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Project_Hours_Avg_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Table_Values = [["Activity", "Count", "Total [H]", "Average [H]"]]
    Table_Data_List = Activity_Df.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Shows Activity Details.", Scrollable=True) 
    Frame_Header = Frame_Main.children["!ctkframe"]
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Button --> Activities
    Button_Show_Activities = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Activities.configure(text="Detail", command = lambda:DashBoard_Activity())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Activities, message="Shows activity chart.", ToolTip_Size="Normal")

    # Table
    Activity_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Body, Table_size="Dashboard_Project_Activity", columns=4, rows=Activity_Df.shape[0] + 1)
    Activity_Table.configure(values=Table_Values)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Activities.pack(side="right")
    Activity_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Activity_Detail1_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Occurrence_ID =  Activity_Df["Count"].idxmax()
    Most_Occurrence_Activity = Activity_Df.iloc[Most_Occurrence_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Events Count.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Count_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Activity_Count_text.configure(text=f"{Most_Occurrence_Activity}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Count_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Detail2_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Hours_ID =  Activity_Df["Total[H]"].idxmax()
    Most_Activity_Hours = Activity_Df.iloc[Most_Hours_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Activity Total Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Hours_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Activity_Hours_text.configure(text=f"{Most_Activity_Hours}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Hours_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_Activity_Detail3_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Activity_Df: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Activity_Df = Activity_Df.head(-1)
    Most_Hours_ID =  Activity_Df["Average[H]"].idxmax()
    Most_Activity_Avg_Hours = Activity_Df.iloc[Most_Hours_ID]["Activity"]
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Activity Average Time.", Scrollable=False) 
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Activity_Hours_Avg_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Dashboard_Detail_Value", Font_Size="Field_Label")
    Activity_Hours_Avg_text.configure(text=f"{Most_Activity_Avg_Hours}")

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Activity_Hours_Avg_text.pack(side="right", padx=0, pady=0)

    return Frame_Main

def DashBoard_WeekDays_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, WeekDays_Df: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Table_Values = [["Week Day", "Days Count", "Total Events", "Total [H]", "Average [H]", "My Utilization [%]", "Utilization [%]"]]
    Table_Data_List = WeekDays_Df.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Detail WeekDay Summary.", Scrollable=True) 
    Frame_Header = Frame_Main.children["!ctkframe"]
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Button --> Projects
    Button_Show_Utilization = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Utilization.configure(text="Utilization", command = lambda:DashBoard_Utilization())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Utilization, message="Shows Utilization chart.", ToolTip_Size="Normal")

    # Table
    WeekDays_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Body, Table_size="Dashboard_WeekDays", columns=7, rows=WeekDays_Df.shape[0] + 1)
    WeekDays_Table.configure(values=Table_Values)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Utilization.pack(side="right")
    WeekDays_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Weeks_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Weeks_DF: DataFrame) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Data preparation
    Table_Values = [["Week", "Days", "Days w/o weekend", "Total Events", "Total [H]", "Average [H]", "Week Utilization [%]", "Active Days Utilization [%]"]]
    Table_Data_List = Weeks_DF.values.tolist()
    for data_list in Table_Data_List:
        Table_Values.append(data_list)
    
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Week details.", Scrollable=True) 
    Frame_Header = Frame_Main.children["!ctkframe"]
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Button --> Projects
    Button_Show_Utilization = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Utilization.configure(text="Utilization", command = lambda:DashBoard_Utilization())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Utilization, message="Shows Utilization chart.", ToolTip_Size="Normal")

    # Table
    Week_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Body, Table_size="Dashboard_Weeks", columns=8, rows=Weeks_DF.shape[0] + 1)
    Week_Table.configure(values=Table_Values)

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Utilization.pack(side="right")
    Week_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Main

def DashBoard_Chart_Widget(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str) -> CTkFrame:
    # ------------------------- Main Functions -------------------------#
    # Field - Use
    Frame_Main = Elements_Groups.Get_DashBoard_Widget_Frame(Configuration=Configuration, Frame=Frame, Label=Label, Widget_Line=Widget_Line, Widget_size=Widget_size, Icon_Name=None, Widget_Label_Tooltip="Detail day Project / Activity distribution.", Scrollable=False) 
    Frame_Header = Frame_Main.children["!ctkframe"]
    Frame_Body = Frame_Main.children["!ctkframe2"]

    # Button --> Projects
    Button_Show_Projects = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Projects.configure(text="Projects", command = lambda:DashBoard_Project())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Projects, message="Shows project chart.", ToolTip_Size="Normal")

    # Button --> Activities
    Button_Show_Activities = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Activities.configure(text="Activities", command = lambda:DashBoard_Activity())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Activities, message="Shows activity chart.", ToolTip_Size="Normal")

    # Button --> Activities
    Button_Show_Utilization = Elements.Get_Button_Chart(Configuration=Configuration, Frame=Frame_Header, Button_Size="Chart_Button")
    Button_Show_Utilization.configure(text="Utilization", command = lambda:DashBoard_Utilization())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Show_Utilization, message="Show utilization chart", ToolTip_Size="Normal")

    # TODO --> Finish Dashboard --> Load charts according to button into body of Frame --> potentially not possible

    # Build look of Widget
    Frame_Main.pack(side="top", padx=15, pady=15)
    Button_Show_Utilization.pack(side="right", fill="none", expand=False, padx=5, pady=0)
    Button_Show_Activities.pack(side="right", fill="none", expand=False, padx=5, pady=0)
    Button_Show_Projects.pack(side="right", fill="none", expand=False, padx=5, pady=0)
    
    return Frame_Main
