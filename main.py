
# Import Libraries
import os
import time
import pandas
import markdown
from pandas import DataFrame
from datetime import datetime

import customtkinter
from customtkinter import CTk, CTkFrame, StringVar, CTkProgressBar, CTkEntry, CTkLabel, CTkOptionMenu, CTkLabel
from CTkMessagebox import CTkMessagebox
from CTkTable import CTkTable
import pywinstyles
from tkhtmlview import HTMLLabel

import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Process as Process
import Libs.Defaults_Lists as Defaults_Lists

# ------------------------------------------------------------------------------------------------------------------------------------ Local Functions ------------------------------------------------------------------------------------------------------------------------------------ #
def Dialog_Window_Request(title: str, text: str, Dialog_Type: str) -> str|None:
    # Password required
    dialog = Elements.Get_DialogWindow(Configuration=Configuration, title=title, text=text, Dialog_Type=Dialog_Type)
    SP_Password = dialog.get_input()
    return SP_Password

def Get_Current_Theme() -> str:
    Current_Theme = customtkinter.get_appearance_mode()
    return Current_Theme
# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    User_Name = Settings["General"]["Default"]["Name"]
    User_ID = Settings["General"]["Default"]["Code"]
    User_Email = Settings["General"]["Default"]["Email"]

    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = Get_Current_Theme() 
        if Current_Theme == "Dark":
            customtkinter.set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            customtkinter.set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            customtkinter.set_appearance_mode(mode_string="dark")
        else:
            customtkinter.set_appearance_mode(mode_string="system")

    # ------------------------- Main Functions -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Set="lucide", Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal")

    # Account Mail
    Frame_User_Email = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Email.configure(text=User_Email)
    Frame_User_Email.pack_propagate(flag=False)

    # Account ID
    Frame_User_ID = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_ID.configure(text=User_ID)
    Frame_User_ID.pack_propagate(flag=False)

    # Account Name
    Frame_User_Name = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Name.configure(text=User_Name)
    Frame_User_Name.pack_propagate(flag=False)

    # Build look of Widget
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Email.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

# ------------------------------------------------------------------------------------------------------------------------------------ Side Bar ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame) -> CTkFrame:
    User_Type = Settings["General"]["Default"]["User_Type"]

    global Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady, Icon_Default_pady, Logo_Height, Logo_width, Side_Bar_Frame_Height, Icon_Button_Height, Logo_pady
    
    if User_Type == "User":
        Icon_count = 6
    elif User_Type == "Manager":
        Icon_count = 7

    Icon_Default_pady = 10
    Logo_Height = 40
    Logo_width = 70
    Logo_pady = 20
    
    Side_Bar_Frame_Height = Side_Bar_Frame._current_height
    Icon_Button_Height = Configuration["Buttons"]["Picture_SideBar"]["height"]

    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()
            window.update_idletasks()

    def Show_Download_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        Page_Download(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Dashboard(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Team_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_User_Dashboard(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Data_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Data(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Information(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        Page_Settings(Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Define_Icons_Top_Bottom_indent(Frame_Height: int, Icon_count: int, Icon_Button_Height: int, Icon_Default_pady: int, Logo_height: int, Logo_pady: int) -> list[int, int]:
        Total_Logo_Height = Logo_height + (2 * Logo_pady)
        Total_Icons_Height = Icon_count * (Icon_Button_Height + (2 * Icon_Default_pady))
        Side_Bar_Middle_point = Frame_Height // 2
        Side_Bar_Icon_top_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2)
        Side_Bar_Icon_Bottom_pady = Side_Bar_Middle_point - (Total_Icons_Height // 2) - Total_Logo_Height - Logo_pady

        return Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="download", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Download_Row = 0
    elif User_Type == "Manager":
        Download_Row = 0
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=Download_Row))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Download new data.", ToolTip_Size="Normal")

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="layout-dashboard", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Dashboard_Row = 1
    elif User_Type == "Manager":
        Dashboard_Row = 1
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Dashboard_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Dashboard, message="My dashboard page.", ToolTip_Size="Normal")

    # Page - Users Dashboard
    if User_Type == "User":
        pass
    elif User_Type == "Manager":
        Team_Row = 2
        Icon_Frame_Users_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="users", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
        Icon_Frame_Users_Dashboard.configure(command = lambda: Show_Team_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Team_Row))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Users_Dashboard, message="My Team page.", ToolTip_Size="Normal")

    # Page - Data
    Icon_Frame_Data = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="file-spreadsheet", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Data_Row = 2
    elif User_Type == "Manager":
        Data_Row = 3
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page(Active_Window = Active_Window, Side_Bar_Row=Data_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Data, message="Data to export page.", ToolTip_Size="Normal")

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Information_Row = 3
    elif User_Type == "Manager":
        Information_Row = 4
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=Information_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Information, message="Application information page.", ToolTip_Size="Normal")

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Settings_Row = 4
    elif User_Type == "Manager":
        Settings_Row = 5
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=Settings_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal")

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_SideBar")
    Icon_Frame_Close.configure(command = lambda: window.quit())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Close, message="Close application.", ToolTip_Size="Normal")

    Konica_Logo = Elements.Get_Background_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=Logo_width, heigh=Logo_Height)

    # Define intend
    Side_Bar_Icon_top_pady, Side_Bar_Icon_Bottom_pady = Define_Icons_Top_Bottom_indent(Frame_Height=Side_Bar_Frame_Height, Icon_count=Icon_count, Icon_Button_Height=Icon_Button_Height, Icon_Default_pady=Icon_Default_pady, Logo_height=Logo_Height, Logo_pady=Logo_pady)

    # Build look of Widget
    Active_Window.grid(row=1, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
    if User_Type == "User":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=5, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Konica_Logo.grid(row=6, column=0, padx=(0, 0), pady=Logo_pady, sticky="", columnspan=2)
    elif User_Type == "Manager":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Users_Dashboard.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=5, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=6, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Konica_Logo.grid(row=7, column=0, padx=(0, 0), pady=Logo_pady, sticky="", columnspan=2)

# ------------------------------------------------------------------------------------------------------------------------------------ Download Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Download(Frame: CTk|CTkFrame):
    User_Type = Settings["General"]["Default"]["User_Type"]

    import Libs.GUI.Widgets.Download as Download
    # ------------------------- Local Functions -------------------------#
    def Change_Download_Data_Source(Download_Data_Source: StringVar, Exchange_Password_Var: CTkEntry):
        if Download_Data_Source.get() == "Exchange":
            Exchange_Password_Var.focus()
            Exchange_Password_Var.configure(state="normal")
        elif Download_Data_Source.get() == "Outlook_Client":
            Exchange_Password_Var.delete(first_index=0, last_index=1000)
            Exchange_Password_Var.configure(state="disabled")
        else:
            pass

    def Change_Download_Date_Range_Source(Download_Date_Range_Source: StringVar, Manual_Date_From_Var: CTkEntry, Manual_Date_To_Var: CTkEntry, Sharepoint_Password_Var: CTkEntry, Sharepoint_Date_From_Option_Var: CTkOptionMenu, Sharepoint_Date_To_Option_Var: CTkOptionMenu, Sharepoint_Man_Date_To_Var: CTkEntry) -> None:
        if Download_Date_Range_Source.get() == "Manual":
            Manual_Date_From_Var.focus()
            Manual_Date_From_Var.configure(state="normal")
            Manual_Date_To_Var.configure(state="normal")

            Sharepoint_Password_Var.delete(first_index=0, last_index=1000)
            Sharepoint_Password_Var.configure(state="disabled")
            Sharepoint_Date_From_Option_Var.configure(state="disabled")
            Sharepoint_Date_To_Option_Var.configure(state="disabled")
            Sharepoint_Man_Date_To_Var.configure(state="disabled")
        elif Download_Date_Range_Source.get() == "Sharepoint":
            Sharepoint_Password_Var.focus()
            Sharepoint_Password_Var.configure(state="normal")
            Sharepoint_Date_From_Option_Var.configure(state="normal")
            Sharepoint_Date_To_Option_Var.configure(state="normal")
            Sharepoint_Man_Date_To_Var.configure(state="normal")

            Manual_Date_From_Var.delete(first_index=0, last_index=1000)
            Manual_Date_From_Var.configure(placeholder_text="Date From")
            Manual_Date_From_Var.configure(state="disabled")
            Manual_Date_To_Var.delete(first_index=0, last_index=1000)
            Manual_Date_To_Var.configure(placeholder_text="Date To")
            Manual_Date_To_Var.configure(state="disabled")
        else:
            pass

    def Download_Data(Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: StringVar, Download_Data_Source: StringVar, Sharepoint_Widget: CTkFrame, Manual_Widget: CTkFrame, Exchange_Widget: CTkFrame):
        Format_Date = Settings["General"]["Formats"]["Date"]
        Can_Download = True

        # -------------- Actual Values  -------------- #
        Download_Date_Range_Source = Download_Date_Range_Source.get()
        Download_Data_Source = Download_Data_Source.get()

        # Sharepoint
        SP_Date_From_Method = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        SP_Date_To_Method = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe5"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        SP_Man_Date_To = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe6"].children["!ctkframe3"].children["!ctkentry"].get()
        SP_Password = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe7"].children["!ctkframe3"].children["!ctkentry"].get()

        # Manual
        Input_Start_Date = Manual_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        Input_End_Date = Manual_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()
        Input_Start_Date = Input_Start_Date.upper()
        Input_End_Date = Input_End_Date.upper()
        
        # Exchange
        Exchange_Password = Exchange_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

        # -------------- Missing Data handler  -------------- #
        # Date Range Source
        if Download_Date_Range_Source == "Sharepoint":
            if SP_Password == "":
                Can_Download = False
                CTkMessagebox(title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1)
            else:
                Input_Start_Date = None
                Input_End_Date = None

        elif Download_Date_Range_Source == "Manual":
            SP_Password = None
            try:
                # Test if Today is selected 
                if Input_Start_Date == "T":
                    Input_Start_Date = datetime.now()
                    Input_Start_Date = Input_Start_Date.strftime(Format_Date)
                else:
                    pass

                if Input_End_Date == "T":
                    Input_End_Date = datetime.now()
                    Input_End_Date = Input_End_Date.strftime(Format_Date)
                else:
                    pass
                datetime.strptime(Input_Start_Date, Format_Date)
                datetime.strptime(Input_End_Date, Format_Date)
            except:
                Can_Download = False
                CTkMessagebox(title="Error", message=f"Date format is not supported date format, should be {Format_Date}", icon="cancel", fade_in_duration=1)
        else:
            Can_Download = False
            CTkMessagebox(title="Error", message=f"Download Date Range Source: {Download_Date_Range_Source} is not supported. Must be Sharepoint/Manual", icon="cancel", fade_in_duration=1)

        # Data source
        if Can_Download == True:
            if Download_Data_Source == "Exchange":
                if Exchange_Password == "":
                    Can_Download = False
                    CTkMessagebox(title="Error", message="You forgot to insert Exchange password.", icon="cancel", fade_in_duration=1)
                else:
                    pass
            elif Download_Data_Source == "Outlook_Client":
                Exchange_Password = None
            else:
                Can_Download = False
                CTkMessagebox(title="Error", message=f"Download Data Source: {Download_Data_Source} is not supported. Must be Exchange/Outlook_Client", icon="cancel", fade_in_duration=1)
        else:
            pass

        # -------------- Download  -------------- #
        if Can_Download == True:
            Process.Download_and_Process(Settings=Settings, window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Date_From_Method=SP_Date_From_Method, SP_Date_To_Method=SP_Date_To_Method, SP_Man_Date_To=SP_Man_Date_To, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
            
            # Save into Settings --> to be displayed on Dashboard later 
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Creation_Date"], Information=Today_str)
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Data_Period"], Information="Current")
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
        else:
            CTkMessagebox(title="Error", message="Not possible to download and process data", icon="cancel", fade_in_duration=1)

    def Pre_Download_Data(Previous_Period_Def_Widget: CTkFrame, Previous_Sharepoint_Widget: CTkFrame) -> None:
        def get_year_month_list(start_date: datetime, end_date: datetime):
            year_month_list = []
            current = start_date
            while current <= end_date:
                year_month_list.append((current.year, current.month))
                # Move to the next month
                if current.month == 12:
                    current = datetime(current.year + 1, 1, 1)
                else:
                    current = datetime(current.year, current.month + 1, 1)
            return year_month_list
        
        Can_Download = True

        # Sharepoint
        SP_Password = Previous_Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

        # History Period definition and checks
        From_Month = Previous_Period_Def_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        From_Year = Previous_Period_Def_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        From_DateTime =datetime(year=From_Year, month=From_Month, day=1)
        To_Month = Previous_Period_Def_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        To_Year = Previous_Period_Def_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        To_DateTime =datetime(year=To_Year, month=To_Month, day=1)

        # Check filled password
        if Download_Date_Range_Source == "Sharepoint":
            if SP_Password == "":
                Can_Download = False
                CTkMessagebox(title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1)
            else:
                pass

        if From_DateTime <= To_DateTime:
            Download_Periods = get_year_month_list(start_date=From_DateTime, end_date=To_DateTime)
        else:
            Can_Download = False
            CTkMessagebox(title="Error", message=f"Cannot download as From Period is sooner To Period, please check.", icon="cancel", fade_in_duration=1)

        # -------------- Download  -------------- #
        if Can_Download == True:
            Process.Pre_Periods_Download_and_Process(Settings=Settings, window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, SP_Password=SP_Password, Download_Periods=Download_Periods)

            # Save into Settings --> to be displayed on Dashboard later 
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Creation_Date"], Information=Today_str)
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Data_Period"], Information="Past")
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
        else:
            pass


    def My_Team_Download_Data() -> None:
        print("My_Team_Download_Data")
        # TODO --> Finish and prepare downloader, prepare also utilization in one chart for all team mebers --> to see 
        
        pass


    # ------------------------- Main Functions -------------------------#
    # Default
    Download_Date_Range_Source = StringVar(master=Frame, value="Sharepoint", name="Download_Date_Range_Source")
    Download_Data_Source = StringVar(master=Frame, value="Exchange", name="Download_Data_Source")

    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_State_Area.pack_propagate(flag=False)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Download_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_New = TabView.add("New")
    Tab_New.pack_propagate(flag=False)
    Tab_Pre = TabView.add("Past")
    Tab_Pre.pack_propagate(flag=False)
    if User_Type == "Manager":
        Tab_Team = TabView.add("My Team")
        Tab_Team.pack_propagate(flag=False)

        Tab_Team_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="Used to download data from my team wit current reporting period.", ToolTip_Size="Normal")
    else:
        pass
    TabView.set("New")

    Tab_New_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Pre_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_New_ToolTip_But, message="Used to download new data to be registered, or Current Period checking.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Pre_ToolTip_But, message="Used to download already registered date in Time Sheets --> download from Sharepoint previous periods.", ToolTip_Size="Normal")

    # ---------- New Download ---------- #
    # Download Method
    Method_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_New, Label_Size="H1", Font_Size="H1")
    Method_Text.configure(text="Step 1 - Date Range Source")

    Sharepoint_Widget = Download.Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Date_Range_Source=Download_Date_Range_Source)
    Sharepoint_Usage_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Sharepoint_Date_From_Option_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkoptionmenu"]
    Sharepoint_Date_To_Option_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe5"].children["!ctkframe3"].children["!ctkoptionmenu"]
    Sharepoint_Man_Date_To_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe6"].children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_Password_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe7"].children["!ctkframe3"].children["!ctkentry"]
    
    Manual_Widget = Download.Download_Manual(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Date_Range_Source=Download_Date_Range_Source)
    Manual_Usage_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Manual_Date_From_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"]
    Manual_Date_To_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"]
    Manual_Date_From_Var.configure(state="disabled")
    Manual_Date_To_Var.configure(state="disabled")

    # Disabling fields --> Download_Date_Range_Source
    Sharepoint_Usage_Var.configure(command = lambda:Change_Download_Date_Range_Source(Download_Date_Range_Source=Download_Date_Range_Source, Manual_Date_From_Var=Manual_Date_From_Var, Manual_Date_To_Var=Manual_Date_To_Var, Sharepoint_Password_Var=Sharepoint_Password_Var, Sharepoint_Date_From_Option_Var=Sharepoint_Date_From_Option_Var, Sharepoint_Date_To_Option_Var=Sharepoint_Date_To_Option_Var, Sharepoint_Man_Date_To_Var=Sharepoint_Man_Date_To_Var))
    Manual_Usage_Var.configure(command = lambda:Change_Download_Date_Range_Source(Download_Date_Range_Source=Download_Date_Range_Source, Manual_Date_From_Var=Manual_Date_From_Var, Manual_Date_To_Var=Manual_Date_To_Var, Sharepoint_Password_Var=Sharepoint_Password_Var, Sharepoint_Date_From_Option_Var=Sharepoint_Date_From_Option_Var, Sharepoint_Date_To_Option_Var=Sharepoint_Date_To_Option_Var, Sharepoint_Man_Date_To_Var=Sharepoint_Man_Date_To_Var))

    # Download Source
    Source_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_New, Label_Size="H1", Font_Size="H1")
    Source_Text.configure(text="Step 2 - Download Data Source")

    Exchange_Widget = Download.Download_Exchange(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Data_Source=Download_Data_Source)
    Exchange_Usage_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Exchange_Password_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"]

    Outlook_Widget = Download.Download_Outlook(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Data_Source=Download_Data_Source)
    Outlook_Usage_Var = Outlook_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]

    # Disabling fields --> Download_Data_Source
    Exchange_Usage_Var.configure(command = lambda:Change_Download_Data_Source(Download_Data_Source=Download_Data_Source, Exchange_Password_Var=Exchange_Password_Var))
    Outlook_Usage_Var.configure(command = lambda:Change_Download_Data_Source(Download_Data_Source=Download_Data_Source, Exchange_Password_Var=Exchange_Password_Var))

    # Download button
    Download_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_New, Label_Size="H1", Font_Size="H1")
    Download_Text.configure(text="Step 3 - Download and process")

    Button_Download = Elements.Get_Button(Configuration=Configuration, Frame=Tab_New, Button_Size="Normal")
    Button_Download.configure(text="Download", command = lambda:Download_Data(Progress_Bar=Progress_Bar, Progress_text=Progress_text, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, Sharepoint_Widget=Sharepoint_Widget, Manual_Widget=Manual_Widget, Exchange_Widget=Exchange_Widget))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download, message="Initiate Download and Process data.", ToolTip_Size="Normal")
    
    # ---------- Previous periods ---------- #
    Previous_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Pre, Label_Size="H1", Font_Size="H1")
    Previous_Text.configure(text="Step 1 - Define previous periods")

    Previous_Period_Def_Widget = Download.Per_Period_Selection(Settings=Settings, Configuration=Configuration, Frame=Tab_Pre)

    Pre_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Pre, Label_Size="H1", Font_Size="H1")
    Pre_Sharepoint_Text.configure(text="Step 2 - Sharepoint credential")

    Previous_Sharepoint_Widget = Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_Pre)

    # Download button
    Pre_Download_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Pre, Label_Size="H1", Font_Size="H1")
    Pre_Download_Text.configure(text="Step 2 - Download and process")

    Pre_Button_Download = Elements.Get_Button(Configuration=Configuration, Frame=Tab_Pre, Button_Size="Normal")
    Pre_Button_Download.configure(text="Download", command = lambda:Pre_Download_Data(Previous_Period_Def_Widget=Previous_Period_Def_Widget, Previous_Sharepoint_Widget=Previous_Sharepoint_Widget))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download, message="Initiate Download, then check Dashboard.", ToolTip_Size="Normal")
    
    # ---------- Previous periods ---------- #
    if User_Type == "Manager":
        Team_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Team, Label_Size="H1", Font_Size="H1")
        Team_Sharepoint_Text.configure(text="Step 1 - Sharepoint credential")

        My_Team_Sharepoint_Widget = Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_Team) # Can most probably by identical as downloads needs to connect same ways as in Pre

        # Download button
        Team_Download_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Team, Label_Size="H1", Font_Size="H1")
        Team_Download_Text.configure(text="Step 2 - Download and process")

        Team_Button_Download = Elements.Get_Button(Configuration=Configuration, Frame=Tab_Team, Button_Size="Normal")
        Team_Button_Download.configure(text="Download", command = lambda:My_Team_Download_Data())
        Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download, message="Initiate Download, then check My Team Dashboard.", ToolTip_Size="Normal")
    else:
        pass

    # ------------------------- State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Frame_Download_State_Area, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)

    Progress_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Progress_text.configure(text=f"Download progress", width=200)


    # Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")
    
    Method_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Sharepoint_Widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="n")
    Manual_Widget.grid(row=1, column=1, padx=20, pady=(5, 20), sticky="n")
    Source_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    Exchange_Widget.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="n")
    Outlook_Widget.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="n")
    Download_Text.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    Button_Download.grid(row=5, column=0, padx=5, pady=15, sticky="nw")
    
    Previous_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Previous_Period_Def_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    Pre_Sharepoint_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    Previous_Sharepoint_Widget.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    Pre_Download_Text.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    Pre_Button_Download.grid(row=5, column=0, padx=5, pady=15, sticky="nw")

    if User_Type == "Manager":
        Team_Sharepoint_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        My_Team_Sharepoint_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        Team_Download_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        Team_Button_Download.grid(row=3, column=0, padx=5, pady=15, sticky="nw")
    else:
        pass

    Progress_text.grid(row=0, column=1, padx=5, pady=15, sticky="w")
    Progress_Bar.grid(row=0, column=2, padx=5, pady=15, sticky="w")
    
# ------------------------------------------------------------------------------------------------------------------------------------ Dashboard Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Dashboard(Frame: CTk|CTkFrame):
    import Libs.GUI.Widgets.DashBoard as DashBoard
    # ------------------------- Main Functions -------------------------#
    # Define Frames
    Frame_Dashboard_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Dashboard_Work_Detail_Area.grid_propagate(flag=False)

    Frame_DashBoard_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Work_Detail_Area, Frame_Size="Triple_size")

    # ------------------------- Dashboard work Area -------------------------#
    try:
        Totals_Summary_Df = pandas.read_csv(f"Operational\\nts\\Events_Totals.csv", sep=";")
        Project_DF = pandas.read_csv(f"Operational\\DashBoard\\Events_Project.csv", sep=";")
        Activity_Df = pandas.read_csv(f"Operational\\DashBoard\\Events_Activity.csv", sep=";")
        WeekDays_Df = pandas.read_csv(f"Operational\\DashBoard\\Events_WeekDays.csv", sep=";")
        Weeks_DF = pandas.read_csv(f"Operational\\DashBoard\\Events_Weeks.csv", sep=";")

        # Total Line
        Total_Duration_hours = float(Totals_Summary_Df.iloc[0]["Total_Duration_hours"])
        Mean_Duration_hours = float(Totals_Summary_Df.iloc[0]["Mean_Duration_hours"])
        Event_counts = int(Totals_Summary_Df.iloc[0]["Event_counts"])
        Reporting_Period_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["Reporting_Period_Utilization"], ndigits=2))
        My_Calendar_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["My_Calendar_Utilization"], ndigits=2))
        Utilization_Surplus_hours = float(Totals_Summary_Df.iloc[0]["Utilization_Surplus_hours"])

        Creation_Date = Settings["General"]["DashBoard"]["Creation_Date"]
        Data_Period = Settings["General"]["DashBoard"]["Data_Period"]
        Data_Source = Settings["General"]["DashBoard"]["Data_Source"]
        DashBoard_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
        DashBoard_text_Additional.configure(text=f"""Generated on: {Creation_Date} -- Period: {Data_Period} -- Dates Source: {Data_Source}.""")

        Frame_Dashboard_Total_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Totals_Line")
        Frame_Dashboard_Total_Line.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Counter = DashBoard.DashBoard_Totals_Counter_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Count", Widget_Line="Totals_Line", Widget_size="Normal", Data=Event_counts)
        Frame_DashBoard_Totals_Counter.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Total = DashBoard.DashBoard_Totals_Total_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Total", Widget_Line="Totals_Line", Widget_size="Normal", Data=Total_Duration_hours)
        Frame_DashBoard_Totals_Total.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Average = DashBoard.DashBoard_Totals_Average_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Average", Widget_Line="Totals_Line", Widget_size="Normal", Data=Mean_Duration_hours)
        Frame_DashBoard_Totals_Average.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Report_Per_Util = DashBoard.DashBoard_Totals_Report_Period_Util_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Reported Period Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=Reporting_Period_Utilization)
        Frame_DashBoard_Totals_Report_Per_Util.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Active_Day_Util = DashBoard.DashBoard_Totals_Active_Day_Util_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="My Active Days Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=My_Calendar_Utilization)
        Frame_DashBoard_Totals_Active_Day_Util.pack_propagate(flag=False)
        Frame_DashBoard_Totals_Util_by_today_surplus = DashBoard.DashBoard_Totals_Utilization_Surplus_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Total_Line, Label="Util. surplus by Input End Date", Widget_Line="Totals_Line", Widget_size="Normal", Data=Utilization_Surplus_hours)
        Frame_DashBoard_Totals_Util_by_today_surplus.pack_propagate(flag=False)

        # Project Activity Line
        Frame_Dashboard_Project_Activity_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Project_Activity_Line")
        Frame_Dashboard_Project_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section")
        Frame_Dashboard_Project_Detail_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Detail_Section")
        Frame_DashBoard_Project_Frame = DashBoard.DashBoard_Project_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Detail_Section, Label="Projects", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Project_DF=Project_DF)
        Frame_Dashboard_Project_Side_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Side_Section")
        Frame_DashBoard_Project_Detail1_Frame = DashBoard.DashBoard_Project_Detail1_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Most Occurrence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF)
        Frame_DashBoard_Project_Detail1_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Project_Detail2_Frame = DashBoard.DashBoard_Project_Detail2_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF)
        Frame_DashBoard_Project_Detail2_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Project_Detail3_Frame = DashBoard.DashBoard_Project_Detail3_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Project_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Project_DF=Project_DF)
        Frame_DashBoard_Project_Detail3_Frame.pack_propagate(flag=False)

        Frame_Dashboard_Activity_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section")
        Frame_Dashboard_Activity_Detail_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Detail_Section")
        Frame_DashBoard_Activity_Frame = DashBoard.DashBoard_Activity_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Detail_Section, Label="Activity", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Activity_Df=Activity_Df)
        Frame_Dashboard_Activity_Side_Section = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Side_Section")
        Frame_DashBoard_Activity_Detail1_Frame = DashBoard.DashBoard_Activity_Detail1_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Occurrence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
        Frame_DashBoard_Activity_Detail1_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Activity_Detail2_Frame = DashBoard.DashBoard_Activity_Detail2_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
        Frame_DashBoard_Activity_Detail2_Frame.pack_propagate(flag=False)
        Frame_DashBoard_Activity_Detail3_Frame = DashBoard.DashBoard_Activity_Detail3_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Activity_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
        Frame_DashBoard_Activity_Detail3_Frame.pack_propagate(flag=False)

        # WeekDay and Weeks Line
        Frame_Dashboard_WeekDay_Weeks_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="WeekDay_Weeks_Line")
        Frame_DashBoard_WeekDays_Frame = DashBoard.DashBoard_WeekDays_Widget(Configuration=Configuration, Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="WeekDays", Widget_Line="WeekDay_Weeks", Widget_size="Normal", WeekDays_Df=WeekDays_Df)
        Frame_DashBoard_Weeks_Frame = DashBoard.DashBoard_Weeks_Widget(Configuration=Configuration, Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="Weeks", Widget_Line="WeekDay_Weeks", Widget_size="Normal", Weeks_DF=Weeks_DF)

        # Day Chart Line
        Frame_Dashboard_Day_Chart_Line = Elements.Get_Dashboards_Frame(Configuration=Configuration, Frame=Frame_DashBoard_Scrollable_Area, Frame_Size="Day_Chart_Line")
        Frame_DashBoard_Chart_Frame = DashBoard.DashBoard_Chart_Widget(Configuration=Configuration, Frame=Frame_Dashboard_Day_Chart_Line, Label="Charts", Widget_Line="WeekChart", Widget_size="Normal")
        Frame_DashBoard_Chart_Frame.pack_propagate(flag=False)

        # Build look of Widget
        Frame_Dashboard_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        Frame_DashBoard_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        DashBoard_text_Additional.pack(side="top", fill="none", expand=True, padx=(1250, 20), pady=(0, 0))

        Frame_Dashboard_Total_Line.pack(side="top", fill="x", expand=True, padx=0, pady=(10, 0))
        Frame_DashBoard_Totals_Counter.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Total.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Average.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Report_Per_Util.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Active_Day_Util.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_DashBoard_Totals_Util_by_today_surplus.pack(side="left", fill="none", expand=True, padx=0, pady=0)

        Frame_Dashboard_Project_Activity_Line.pack(side="top", fill="x", expand=True, padx=5, pady=(10, 0))
        Frame_Dashboard_Project_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Project_Detail_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_DashBoard_Project_Frame.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_Dashboard_Project_Side_Section.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail1_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail2_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
        Frame_DashBoard_Project_Detail3_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)

        Frame_Dashboard_Activity_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_Dashboard_Activity_Detail_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_DashBoard_Activity_Frame.pack(side="left", fill="none", expand=True, padx=0, pady=0)
        Frame_Dashboard_Activity_Side_Section.pack(side="left", fill="x", expand=True, padx=0, pady=0)
        Frame_DashBoard_Activity_Detail1_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
        Frame_DashBoard_Activity_Detail2_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
        Frame_DashBoard_Activity_Detail3_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)

        Frame_Dashboard_WeekDay_Weeks_Line.pack(side="top", fill="x", expand=True, padx=5, pady=(10, 0))
        Frame_DashBoard_WeekDays_Frame.pack(side="left", fill="none", expand=True, padx=5, pady=5)
        Frame_DashBoard_Weeks_Frame.pack(side="left", fill="none", expand=True, padx=5, pady=5)

        Frame_Dashboard_Day_Chart_Line.pack(side="top", fill="x", expand=True, padx=0, pady=(10, 0))
        Frame_DashBoard_Chart_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
    except:
        CTkMessagebox(title="Error", message=f"Dashboard not all data available, please run Downloader first.", icon="cancel", fade_in_duration=1)

# ------------------------------------------------------------------------------------------------------------------------------------ Dashboard Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_User_Dashboard(Frame: CTk|CTkFrame):
    Members_dict = Settings["General"]["Default"]["Managed_Team"]
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

            # TODO --> Finish fill dashboard to each page of each person

            member_order += 1

    TabView.set("Totals")

    # Build look of Widget
    Frame_User_Dashboard_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")

# ------------------------------------------------------------------------------------------------------------------------------------ Data Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Data(Frame: CTk|CTkFrame):
    # ------------------------- Local Functions -------------------------#
    global Info_current_row, Info_Table_Rows, Events_List_Header
    Info_current_row = 0
    Info_Table_Rows = 20
    Events_List_Header = ["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]

    def change_first(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row > Info_Table_Rows:
            Info_current_row = Info_Table_Rows
            Showed_events = Events_List[0 : Info_Table_Rows]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{0} / {Info_Table_Rows} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_left(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row > Info_Table_Rows:
            Info_current_row -= Info_Table_Rows
            Start_interval = Info_current_row - Info_Table_Rows
            End_interval = Info_current_row

            if Start_interval < 0:
                Start_interval = 0
                End_interval = Info_Table_Rows
            else:
                pass

            Showed_events = Events_List[Start_interval : End_interval]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Start_interval} / {End_interval} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_right(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row < Events_list_len:
            Info_current_row += Info_Table_Rows
            Start_interval = Info_current_row - Info_Table_Rows
            End_interval = Info_current_row
            Showed_events = Events_List[Start_interval : Info_current_row]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Start_interval} / {End_interval} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def change_last(Table: CTkTable, Current_Rows: CTkLabel, Events_list_len: int) -> None:
        global Info_current_row
        if Info_current_row < Events_list_len:
            Info_current_row = Events_list_len
            Showed_events = Events_List[Events_list_len - Info_Table_Rows : Events_list_len]
            Showed_events.insert(0, Events_List_Header)
            Table.update_values(Showed_events)
            Current_Rows.configure(text=f"{Events_list_len - Info_Table_Rows} / {Events_list_len} ({Events_list_len})")
            window.update_idletasks()
        else:
            pass

    def Data_Excel():
        import subprocess
        subprocess.run('start excel "Operational\\Downloads\\Events.csv"', shell=True, capture_output=False, text=False)

    def Data_Upload(Events: DataFrame):
        SP_Password = Dialog_Window_Request(title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        if SP_Password == None:
            CTkMessagebox(title="Error", message="Cannot upload, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Upload(Events=Events, SP_Password=SP_Password)
            CTkMessagebox(title="Success", message="Successfully uploaded to Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)

    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Data_Button_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Data_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Data_Work_Detail_Area.grid_propagate(flag=False)

    Events = pandas.read_csv(f"Operational\\Downloads\\Events.csv", sep=";")

    # ------------------------- Buttons Area -------------------------#
    # Download Button
    Button_Upload = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Upload.configure(text="Upload", command = lambda:Data_Upload(Events=Events))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Upload, message="Upload processed data directly to Sharepoint TimeSheets.", ToolTip_Size="Normal")

    # Download Button
    Button_Excel = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Excel.configure(text="Excel", command = lambda:Data_Excel())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Excel, message="Show generated Excel file.", ToolTip_Size="Normal")

    # ------------------------- Work Area -------------------------#
    # Current Page text
    Page_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Label_Size="H1", Font_Size="H1")

    # Data table
    Events_List = []
    for row in Events.iterrows():
        Events_List.append(row[1].to_list())
    Events_list_len = len(Events_List)

    Frame_Events_Table = Elements_Groups.Get_Table_Frame(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Table_Values=None, Table_Size="Triple_size", Table_Columns=8, Table_Rows=Info_Table_Rows + 1)
    Frame_Events_Table_Var = Frame_Events_Table.children["!ctktable"]
    Frame_Events_Table_Var.configure(wraplength=180)
    # Init values in table
    change_right(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len)

    # Beginning Button
    Button_First = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_First.configure(text="<<", command = lambda: change_first(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_First, message="First page", ToolTip_Size="Normal")

    # Pre Button
    Button_Pre = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Pre.configure(text="<", command = lambda: change_left(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Pre, message="Previous page", ToolTip_Size="Normal")

    # next Button
    Button_Next = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Next.configure(text=">", command = lambda: change_right(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Next, message="Next page", ToolTip_Size="Normal")

    # End Button
    Button_Last = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Data_Work_Detail_Area, Button_Size="Small")
    Button_Last.configure(text=">>", command = lambda: change_last(Table=Frame_Events_Table_Var, Current_Rows=Page_text, Events_list_len=Events_list_len))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Last, message="Last page", ToolTip_Size="Normal")


    # Build look of Widget
    Frame_Data_Button_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Data_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    Button_Upload.grid(row=0, column=0, padx=5, pady=15, sticky="e")
    Button_Excel.grid(row=0, column=1, padx=5, pady=15, sticky="e")

    Frame_Events_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Button_First.pack(side="left", expand=True, padx=(600,10), pady=10)
    Button_Pre.pack(side="left", expand=True, padx=(10,10), pady=10)
    Page_text.pack(side="left", expand=True, pady=10)
    Button_Next.pack(side="left", expand=True, padx=(10,10), pady=10)
    Button_Last.pack(side="left", expand=True, padx=(10,600), pady=10)



# ------------------------------------------------------------------------------------------------------------------------------------ Information Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Information(Frame: CTk|CTkFrame):
    Work_Area_Detail_Background = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"]["Triple_size"]["fg_color"]
    
    Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]

    # ------------------------- Main Functions -------------------------#
    Frame_Information_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Information_Work_Detail_Area.grid_propagate(flag=False)

    # Get Theme --> because of background color
    Current_Theme = Get_Current_Theme() 

    if Current_Theme == "Dark":
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]
    elif Current_Theme == "Light":
        HTML_Background_Color = Work_Area_Detail_Background[0]
        HTML_Font_Color = Work_Area_Detail_Font[0]
    elif Current_Theme == "System":
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]
    else:
        HTML_Background_Color = Work_Area_Detail_Background[1]
        HTML_Font_Color = Work_Area_Detail_Font[1]

    # ------------------------- Info Text Area -------------------------#
    # Description
    Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Information_Work_Detail_Area, Frame_Size="Triple_size")

    with open("Libs\\GUI\\Information.md", "r", encoding="UTF-8") as file:
        html_markdown=markdown.markdown( file.read())
    file.close()

    Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=f"{html_markdown}", background=HTML_Background_Color, font="Roboto", fg=HTML_Font_Color)
    Information_html.configure(height=700)

    # Build look of Widget
    Frame_Information_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_Information_Scrollable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    Information_html.pack(side="top", fill="both", expand=True, padx=10, pady=10)



# ------------------------------------------------------------------------------------------------------------------------------------ Settings Page ------------------------------------------------------------------------------------------------------------------------------------ #
def Page_Settings(Frame: CTk|CTkFrame):
    User_Type = Settings["General"]["Default"]["User_Type"]

    import Libs.GUI.Widgets.Settings as Settings_Widgets
    # ------------------------- Local Functions -------------------------#
    def Download_Project_Activities():
        SP_Password = Dialog_Window_Request(title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        
        if SP_Password == None:
            CTkMessagebox(title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Get_Project_and_Activity(Settings=Settings, SP_Password=SP_Password)
            CTkMessagebox(title="warning", message="Project and Activity downloaded from Sharepoint. Restart app!!", icon="check", option_1="Thanks", fade_in_duration=1)

    def Upload_Project_Activities():
        Exchange_Password = Dialog_Window_Request(title="Exchange Login", text="Write your password", Dialog_Type="Password")
        
        if Exchange_Password == None:
            CTkMessagebox(title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Download.Exchange as Exchange
            Exchange.Push_Project(Settings=Settings, Exchange_Password=Exchange_Password)
            Exchange.Push_Activity(Settings=Settings, Exchange_Password=Exchange_Password)
            CTkMessagebox(title="warning", message="Project and Activity uploaded to Exchange. Give MS time to upload changes and restart Outlook.", icon="check", option_1="Thanks", fade_in_duration=1)

    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Settings_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- State Area -------------------------#
    # Button - Download New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Download_Pro_Act.configure(text="Get Project/Activity", command = lambda:Download_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download_Pro_Act, message="Actualize the list of Projects and Activities inside the app from actual Sharepoint.", ToolTip_Size="Normal")

    # Button - Download New Project and Activities
    Button_Upload_Pro_Act = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Upload_Pro_Act.configure(text="Upload Project/Activity", command = lambda:Upload_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Upload_Pro_Act, message="Upload the list of Projects and Activities into Exchange.", ToolTip_Size="Normal")

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("General")
    Tab_Gen.pack_propagate(flag=False)
    Tab_Dat = TabView.add("Data Source")
    Tab_Dat.pack_propagate(flag=False)
    Tab_Cal = TabView.add("Calendar")
    Tab_Cal.pack_propagate(flag=False)
    Tab_E_G = TabView.add("Events - General")
    Tab_E_G.pack_propagate(flag=False)
    Tab_E_Spec = TabView.add("Events - Special")
    Tab_E_Spec.pack_propagate(flag=False)
    Tab_E_E = TabView.add("Events - Empty")
    Tab_E_E.pack_propagate(flag=False)
    Tab_E_S = TabView.add("Events - Empty Scheduler")
    Tab_E_S.pack_propagate(flag=False)
    Tab_E_A = TabView.add("Events - Rules")
    Tab_E_A.pack_propagate(flag=False)
    if User_Type == "Manager":
        Tab_Team = TabView.add("My Team")
        Tab_Team.pack_propagate(flag=False)

        Tab_Team_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton9"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="MY Team base setup.", ToolTip_Size="Normal")
    else:
        pass
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Dat_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_Cal_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Tab_E_G_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton4"]
    Tab_E_Spec_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton5"]
    Tab_E_E_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton6"]
    Tab_E_S_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton7"]
    Tab_E_A_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton8"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Dat_ToolTip_But, message="Setup related to Downloading date.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Cal_ToolTip_But, message="Base calendar From/To + Day Starting and Ending Event setup.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_G_ToolTip_But, message="Multiple general setup related to Events.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_Spec_ToolTip_But, message="Special Events which needs special treatment.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_E_ToolTip_But, message="Filling Empty time Tool and Split too long Empty place.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_S_ToolTip_But, message="Basic Scheduler setup.", ToolTip_Size="Normal")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_A_ToolTip_But, message="Rule base Event Handling tools setup.", ToolTip_Size="Normal")

    # General
    Theme_Widget = Settings_Widgets.Settings_General_Theme(Settings=Settings, Configuration=Configuration, Frame=Tab_Gen, window=window)
    Color_Palette_Widget = Settings_Widgets.Settings_General_Color(Settings=Settings, Configuration=Configuration, Frame=Tab_Gen)
    Program_User_Type_Widget = Settings_Widgets.Settings_User_Widget(Settings=Settings, Configuration=Configuration, Frame=Tab_Gen)

    # General Page
    Sharepoint_Widget = Settings_Widgets.Settings_General_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_Dat)
    Exchange_Widget = Settings_Widgets.Settings_General_Exchange(Settings=Settings, Configuration=Configuration, Frame=Tab_Dat)
    Outlook_Widget = Settings_Widgets.Settings_General_Outlook(Settings=Settings, Configuration=Configuration, Frame=Tab_Dat)
    Formats_Widget = Settings_Widgets.Settings_General_Formats(Settings=Settings, Configuration=Configuration, Frame=Tab_Dat)

    # Calendar Page
    Calendar_Working_Widget = Settings_Widgets.Settings_Calendar_Working_Hours(Settings=Settings, Configuration=Configuration, Frame=Tab_Cal)
    Calendar_Vacation_Widget = Settings_Widgets.Settings_Calendar_Vacation(Settings=Settings, Configuration=Configuration, Frame=Tab_Cal)
    Calendar_Start_End_Widget = Settings_Widgets.Settings_Calendar_Start_End_Time(Settings=Settings, Configuration=Configuration, Frame=Tab_Cal)

    # Event-General Page
    Event_Skip_Widget = Settings_Widgets.Settings_Events_General_Skip(Settings=Settings, Configuration=Configuration, Frame=Tab_E_G)
    Event_Join_Widget = Settings_Widgets.Settings_Join_events(Settings=Settings, Configuration=Configuration, Frame=Tab_E_G)
    Event_Parallel_Widget = Settings_Widgets.Settings_Parallel_events(Settings=Settings, Configuration=Configuration, Frame=Tab_E_G)

    # Event-Special Page
    Event_Lunch_Widget = Settings_Widgets.Settings_Events_General_Lunch(Settings=Settings, Configuration=Configuration, Frame=Tab_E_Spec)
    Event_Vacation_Widget = Settings_Widgets.Settings_Events_General_Vacation(Settings=Settings, Configuration=Configuration, Frame=Tab_E_Spec)
    Event_SickDay_Widget = Settings_Widgets.Settings_Events_General_SickDay(Settings=Settings, Configuration=Configuration, Frame=Tab_E_Spec)
    Event_HomeOffice_Widget = Settings_Widgets.Settings_Events_General_HomeOffice(Settings=Settings, Configuration=Configuration, Frame=Tab_E_Spec)
    Event_Private_Widget = Settings_Widgets.Settings_Events_General_Private(Settings=Settings, Configuration=Configuration, Frame=Tab_E_Spec)

    # Event-Empty Page
    Event_Empty_General_Widget = Settings_Widgets.Settings_Events_Empty_Generally(Settings=Settings, Configuration=Configuration, Frame=Tab_E_E)
    Event_Split_Widget = Settings_Widgets.Settings_Events_Split(Settings=Settings, Configuration=Configuration, Frame=Tab_E_E)

    # Event-Empty Splitting Page
    Event_Scheduler_Widget = Settings_Widgets.Settings_Events_Empty_Schedule(Settings=Settings, Configuration=Configuration, Frame=Tab_E_S)

    # Event-AutoFill Page
    Event_AutoFiller_Widget = Settings_Widgets.Settings_Events_AutoFill(Settings=Settings, Configuration=Configuration, Frame=Tab_E_A)
    Event_Activity_Correction_Widget = Settings_Widgets.Settings_Events_Activity_Correction(Settings=Settings, Configuration=Configuration, Frame=Tab_E_A)

    if User_Type == "Manager":
        # Managed Team
        Managed_Team_Widget = Settings_Widgets.Settings_My_Team(Settings=Settings, Configuration=Configuration, Frame=Tab_Team)
    else:
        pass
    
    # Build look of Widget
    Frame_Settings_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Button_Download_Pro_Act.grid(row=0, column=0, padx=5, pady=15, sticky="e")
    Button_Upload_Pro_Act.grid(row=0, column=1, padx=5, pady=15, sticky="e")

    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")

    Theme_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Color_Palette_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Program_User_Type_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Sharepoint_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Exchange_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Outlook_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
    Formats_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    Calendar_Working_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Calendar_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Calendar_Start_End_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Event_Skip_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Join_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Event_Parallel_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Event_Lunch_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Event_SickDay_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
    Event_HomeOffice_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    Event_Private_Widget.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

    Event_Empty_General_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Split_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    Event_Scheduler_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Event_AutoFiller_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Activity_Correction_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    if User_Type == "Manager":
        # Managed Team
        Managed_Team_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    else:
        pass


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheets")
        super().iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self,event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self,event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

if __name__ == "__main__":
    Settings = Defaults_Lists.Load_Settings()
    Configuration = Defaults_Lists.Load_Configuration() 

    Date_format = Settings["General"]["Formats"]["Date"]
    Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

    Today = datetime.now()
    Today_str = Today.strftime(Date_format)

    # Create folders if do not exists
    try:
        os.mkdir(f"Operational\\")
        os.mkdir(f"Operational\\DashBoard\\")
        os.mkdir(f"Operational\\Downloads\\")
        os.mkdir(f"Operational\\My_Team_Members\\")
        os.mkdir(f"Operational\\SP_History\\")
    except:
        pass

    window = Win()
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    Window_Frame_width = 1800
    Window_Frame_height = 900
    left_position = int(display_width // 2 - Window_Frame_width // 2)
    top_position = int(display_height // 2 - Window_Frame_height // 2)
    window.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

    # Rounded corners 
    window.config(background="#000001")
    window.attributes("-transparentcolor", "#000001")

    # Base Windows style setup --> always keep normal before change
    customtkinter.set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")
    pywinstyles.apply_style(window=window, style=Win_Style_Actual)

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Configuration=Configuration, Frame=window, Frame_Size="Background")
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="Work_Area")
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Header")
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Detail = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
    Frame_Work_Area_Detail.pack_propagate(flag=False)
    Frame_Work_Area_Detail.pack(side="left", fill="none", expand=False)

    Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar)
    Get_Header(Frame=Frame_Header)
    Page_Dashboard(Frame=Frame_Work_Area_Detail)

    # run
    window.mainloop()