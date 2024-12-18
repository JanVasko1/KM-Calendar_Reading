# Import Libraries
import time
import customtkinter
from customtkinter import CTk, CTkFrame, IntVar, StringVar, CTkProgressBar

import Libs.GUI.Widgets as Widgets
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements

import Libs.Defaults_Lists as Defaults_Lists
import pywinstyles

#! ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Account_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]
Account_Name = Settings["General"]["Person"]["Name"]
Account_ID = Settings["General"]["Person"]["Code"]

#! ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Theme_Change():
    Current_Theme = customtkinter.get_appearance_mode()
    if Current_Theme == "Dark":
        customtkinter.set_appearance_mode("light")
    elif Current_Theme == "Light":
        customtkinter.set_appearance_mode("dark")
    elif Current_Theme == "System":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("system")

#? ----------------------------------------------------- Buttong ----------------------------------------------------- #
# -------------------------------------------- Page Listing -------------------------------------------- #
def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
    # Find
    for widget in Pre_Working_Frame.winfo_children():
        widget.destroy()

def Show_Download_Page() -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Download(Frame=Frame_Work_Area_Detail)

def Show_Dashboard_Page() -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Dashboard(Frame=Frame_Work_Area_Detail)

def Show_Data_Page() -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Data(Frame=Frame_Work_Area_Detail)

def Show_Information_Page() -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Information(Frame=Frame_Work_Area_Detail)

def Show_Settings_Page() -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Settings(Frame=Frame_Work_Area_Detail)
    
# -------------------------------------------- Functionss -------------------------------------------- #
def Download_Data(Progress_Bar: CTkProgressBar):
    Progress_Bar.start()
    #! Doděalt --> spstit bakcendový process processování
    #! Dodělat --> nějak přebírat z BAckendu to TQDM processy aby bylo vidět jak se stahují a zrpcesovávají věci
    print("Downloadd Button press")
    pass

def Save_Settings():
    #! Doděalt --> uložit všechno do Settings.json
    print("Save_Settings")
    pass

def Download_Project_Activities():
    #! Doděalt --> spstit bakcendový process stažení Projektů a Aktivit, aktualizovat promněný a uložit do Settings.json
    print("Download_Project_Activities")
    pass

def Data_Upload():
    #! Doděalt --> Automaticky spustit Uplod na Sharepoint Backendový process
    print("Data_Upload")
    pass

def Data_Excel():
    #! Doděalt --> otevřít excel na kopírování
    print("Data_Excel")
    pass



#? ----------------------------------------------------- Pages ----------------------------------------------------- #
# -------------------------------------------- Header -------------------------------------------- #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame Preparation
    Frame_Header = Elements.Get_Frame(Frame=Frame, Frame_Size="Header")
    Frame_Header.pack_propagate(False)
    Frame_Header.pack(side="top", fill="x", expand=False)

    Frame_Logo = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Logo_Element")
    Frame_Logo.pack_propagate(False)
    Frame_Logo.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Header_Information = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Information")
    Frame_Header_Information.pack_propagate(False)
    Frame_Header_Information.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    # ------------------------- Logo Area -------------------------#
    Company_Logo = Elements.Get_Button_Picture_Logo(Frame=Frame_Logo)
    Image_var = Elements.Get_Image(light_image=f"Libs\\GUI\\Icons\\Konica_Minolta.png", dark_image=f"Libs\\GUI\\Icons\\Konica_Minolta.png", size= (60, 60))
    Company_Logo.configure(image=Image_var, text="")
    Company_Logo.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    # ------------------------- Logo Area -------------------------#
    # Theme Change - Button
    Button_Theme = Elements.Get_Button_Picture_Theme(Frame=Frame_Header_Information)
    Image_Theme = Elements.Get_Image(light_image=f"Libs\\GUI\\Icons\\Theme_Light.png", dark_image=f"Libs\\GUI\\Icons\\Theme_Dark.png", size= (30, 30))
    Button_Theme.configure(image=Image_Theme, text="")
    Button_Theme.configure(command = Theme_Change)
    Button_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account Mail
    Frame_Account_Mail = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_Mail.configure(text=Account_Email)
    Frame_Account_Mail.pack_propagate(False)
    Frame_Account_Mail.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account ID
    Frame_Account_ID = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_ID.configure(text=Account_ID)
    Frame_Account_ID.pack_propagate(False)
    Frame_Account_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account Name
    Frame_Account_Name = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_Name.configure(text=Account_Name)
    Frame_Account_Name.pack_propagate(False)
    Frame_Account_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Active Area
    #! Dodělat --> nadpist Aktivní PAge

    return Frame_Header

# -------------------------------------------- Side Bar -------------------------------------------- #
def Get_Icon(Frame: CTk|CTkFrame, Icon: str) -> CTkFrame:
    Frame_Icon = Elements.Get_Button_Picture_SideBar(Frame=Frame)
    Image_Settings = Elements.Get_Image(light_image=f"Libs\\GUI\\Icons\\{Icon}_Light.png", dark_image=f"Libs\\GUI\\Icons\\{Icon}_Dark.png", size= (30, 30))
    Frame_Icon.configure(image=Image_Settings, text="")
    Frame_Icon.pack(padx=5, pady=10, expand=True)
    return Frame_Icon

def Get_Side_Bar(Frame: CTk|CTkFrame) -> CTkFrame:
    # Page - Downlaod
    Icon_Frame_Download = Get_Icon(Frame=Frame, Icon="Download")
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page())

    # Page - Dashboard
    Icon_Frame_Dashboard = Get_Icon(Frame=Frame, Icon="Dashboard")
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page())

    # Page - Data
    Icon_Frame_Data = Get_Icon(Frame=Frame, Icon="Table")
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page())

    # Page - Information
    Icon_Frame_Information = Get_Icon(Frame=Frame, Icon="Information")
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page())

    # Page - Settings
    Icon_Frame_Settings = Get_Icon(Frame=Frame, Icon="Settings")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page())
    

# -------------------------------------------- Downlaod Page -------------------------------------------- #
def Page_Download(Frame: CTk|CTkFrame):
    # Default
    Download_Method = IntVar(master=Frame, value=1, name="Download_Method")
    Download_Source = IntVar(master=Frame, value=1, name="Download_Source")

    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(False)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # ------------------------- State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame_Download_State_Area, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.configure(mode="indeterminate")
    Progress_Bar.grid(row=0, column=1, padx=5, pady=0, sticky="e")

    # Download Button
    Button_Download = Elements.Get_Button(Frame=Frame_Download_State_Area, Button_Size="Normal")
    Button_Download.configure(text="Download", command = lambda:Download_Data(Progress_Bar=Progress_Bar))
    Button_Download.grid(row=0, column=0, padx=5, pady=0, sticky="e")

    # ------------------------- Work Area -------------------------#
    # Download Method
    Metdod_Text = Elements.Get_Text_H1(Frame=Frame_Download_Work_Detail_Area)
    Metdod_Text.configure(text="Step 1 - Dates definition")
    Metdod_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Sharepoint_Widget = Widgets.Download_Sharepoint(Frame=Frame_Download_Work_Detail_Area, Download_Method=Download_Method)
    Sharepoint_Widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="n")

    Manual_Widget = Widgets.Download_Manual(Frame=Frame_Download_Work_Detail_Area, Download_Method=Download_Method)
    Manual_Widget.grid(row=1, column=1, padx=20, pady=(5, 20), sticky="n")

    # Download Source
    Source_Text = Elements.Get_Text_H1(Frame=Frame_Download_Work_Detail_Area)
    Source_Text.configure(text="Step 2 - Define data source")
    Source_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

    Exchange_Widget = Widgets.Download_Exchange(Frame=Frame_Download_Work_Detail_Area, Download_Source=Download_Source)
    Exchange_Widget.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="n")

    Outlook_Widget = Widgets.Download_Outlook(Frame=Frame_Download_Work_Detail_Area, Download_Source=Download_Source)
    Outlook_Widget.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="n")

# -------------------------------------------- Dashboadr Page -------------------------------------------- #
def Page_Dashboard(Frame: CTk|CTkFrame):
    pass    

# -------------------------------------------- Data Page -------------------------------------------- #
def Page_Data(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Data_Button_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Data_Button_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(False)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # ------------------------- State Area -------------------------#
    # Download Button
    Button_Upload = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Upload.configure(text="Upload", command = lambda:Data_Upload())
    Button_Upload.grid(row=0, column=0, padx=5, pady=0, sticky="e")

    # Download Button
    Button_Excel = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Excel.configure(text="Excel", command = lambda:Data_Excel())
    Button_Excel.grid(row=0, column=1, padx=5, pady=0, sticky="e")

    # ------------------------- Work Area -------------------------#
    Data_Text = Elements.Get_Text_H1(Frame=Frame_Download_Work_Detail_Area)
    Data_Text.configure(text="Data")
    Data_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Frame_Data = Elements_Groups.Get_Widget_Frame(Frame=Frame, Name="Data", Additional_Text="", Widget_size="Triple_size")
    Frame_Body = Frame_Data.children["!ctkframe2"]
    Frame_Data.pack(side="top", padx=15, pady=15)

    # Data table
    #! Dodělat --> mám Issue na Stuck overFlow https://github.com/Akascape/CTkTable/issues/116
    """Rows = 1
    Values = []
    Data_Table = Elements.Get_Table(Frame=Frame_Download_Work_Detail_Area, Table_size="Triple_size")
    Data_Table.configure(columns=8, rows=Rows, values=Values)
    Data_Table.pack(side="top", expand=True, fill="both", padx=10, pady=10)"""


# -------------------------------------------- Information Page -------------------------------------------- #
def Page_Information(Frame: CTk|CTkFrame):
    pass

# -------------------------------------------- Settings Page -------------------------------------------- #
def Page_Settings(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Settings_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Settings_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(False)
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # ------------------------- State Area -------------------------#
    # Add Button - Downlaod New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Download_Pro_Act.configure(text="Get Proejct/Activity", command = lambda:Download_Project_Activities())
    Button_Download_Pro_Act.grid(row=0, column=0, padx=5, pady=0, sticky="e")

    # Add Button - Save Settings
    Button_Save_Settings = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Save_Settings.configure(text="Save", command = lambda:Save_Settings())
    Button_Save_Settings.grid(row=0, column=1, padx=5, pady=0, sticky="e")

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(False)
    Tab_Gen = TabView.add("General")
    Tab_Gen.pack_propagate(False)
    Tab_Cal = TabView.add("Calendar")
    Tab_Cal.pack_propagate(False)
    Tab_E_G = TabView.add("Events - General")
    Tab_E_G.pack_propagate(False)
    Tab_E_E = TabView.add("Events - Empty/Scheduler")
    Tab_E_E.pack_propagate(False)
    Tab_E_A = TabView.add("Events - AutoFill")
    Tab_E_A.pack_propagate(False)
    TabView.set("General")
    TabView.pack()

    # General Page
    Sharepoint_Widget = Widgets.Settings_General_Sharepoint(Frame=Tab_Gen)
    Sharepoint_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Formats_Widget = Widgets.Settings_General_Formats(Frame=Tab_Gen)
    Formats_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

    # Calendar Page
    Calendar_Working_Widget = Widgets.Settings_Calendar_Working_Hours(Frame=Tab_Cal)
    Calendar_Working_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Calendar_Vacation_Widget = Widgets.Settings_Calendar_Vacation(Frame=Tab_Cal)
    Calendar_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

    Calendar_Start_End_Widget = Widgets.Settings_Calendar_Start_End_Time(Frame=Tab_Cal)
    Calendar_Start_End_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    # Event-General Page
    Event_Lunch_Widget = Widgets.Settings_Events_General_Lunch(Frame=Tab_E_G)
    Event_Lunch_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Event_Vacation_Widget = Widgets.Settings_Events_General_Vacation(Frame=Tab_E_G)
    Event_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

    Event_HomeOffice_Widget = Widgets.Settings_Events_General_HomeOffice(Frame=Tab_E_G)
    Event_HomeOffice_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Event_Skip_Widget = Widgets.Settings_Events_General_Skip(Frame=Tab_E_G)
    Event_Skip_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    Event_Parralel_Widget = Widgets.Settings_Parralel_events(Frame=Tab_E_G)
    Event_Parralel_Widget.grid(row=1, column=1, padx=5, pady=5, sticky="nw")

    # Event-Empty Page
    Event_Empty_General_Widget = Widgets.Settings_Events_Empty_Generaly(Frame=Tab_E_E)
    Event_Empty_General_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    
    Event_Scheduler_Widget = Widgets.Settings_Events_Empt_Schedule(Frame=Tab_E_E)
    Event_Scheduler_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    # Event-AutoFill Page
    Event_AutoFiller_Widget = Widgets.Settings_Events_AutoFill(Frame=Tab_E_A)
    Event_AutoFiller_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")


#! ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
# main window
window = customtkinter.CTk()
window.title("Time Sheet Downloader")

# position window in center
window.eval("tk::PlaceWindow . center")
window.geometry("1800x1000")
"""window.maxsize(width=1800, height=1000)
window.minsize(width=1800, height=1000)
"""
window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
customtkinter.set_appearance_mode("system")  # default
pywinstyles.apply_style(window=window, style="acrylic")

# ---------------------------------- Main Page ----------------------------------#
# Frames
Frame_Background = Elements.Get_Frame(Frame=window, Frame_Size="Background")
Frame_Background.pack(side="top", fill="both", expand=False)

Frame_Header = Get_Header(Frame=Frame_Background)

Frame_Work_Area = Elements.Get_Frame(Frame=Frame_Background, Frame_Size="Work_Area")
Frame_Work_Area.pack(side="top", fill="both", expand=False)

Frame_Side_Bar = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_SideBar")
Frame_Side_Bar.pack_propagate(False)
Frame_Side_Bar.pack(side="left", fill="y", expand=False)

Frame_Work_Area_Detail = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
Frame_Work_Area_Detail.pack_propagate(False)
Frame_Work_Area_Detail.pack(side="left", fill="both", expand=False)

Get_Side_Bar(Frame=Frame_Side_Bar)

Page_Download(Frame=Frame_Work_Area_Detail)

# run
customtkinter.set_appearance_mode("system")  # default
window.mainloop()