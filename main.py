
#! Dodělat --> List bodů k dodělání
"""
0) vyřešit ty podělaný obrázky
0) Definice promněných a funkce jejich nadčtení a necaht je aktualizovat 
    --> příklad když nchám stáhnout Project a Activity, tak musí být hned k použití
    --> Jeslit je neudělat jako Global --> interní funkce pythonu k použití globálních promněných

Napojení FrontEnd na backend:
    A) Save settins do Settings.json --> dát pozor jestli nebudu muset pro každou věc udělat Textovou promněnou!!!
3) SideBar --> barevnou čárku u aktivního okna --> aby bylo oznat kde jsme jako to má Outlook
4) GRId 
    -->Přidat Frame.configure --> rozdělit prostor jako ve videu!!!!!!!
    --> pro tabulku vyplˇˇnující celý prostor stačí použít sticky="news" --> přiřadí pro celý definovaný prostor
    --> můžu to přidat i dojednotlivých SEttupů a případně přidat rowspan = 2 (pro ty široký Widgety) --> tím bych se teoreticky mol zbavit dalšího seupu
    --> Settup
"""

# Import Libraries
import time
from datetime import datetime

import customtkinter
from tkinter import ttk
from customtkinter import CTk, CTkFrame, StringVar, CTkProgressBar
from CTkToolTip import CTkToolTip
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Widgets as Widgets
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import pywinstyles
import pandas

import Libs.Defaults_Lists as Defaults_Lists

#! ---------------------------------------------------------- Set Defaults ---------------------------------------------------------- #
Settings = Defaults_Lists.Load_Settings()
Account_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]
Account_Name = Settings["General"]["Person"]["Name"]
Account_ID = Settings["General"]["Person"]["Code"]
Format_Date = Settings["General"]["Formats"]["Date"]

GUI_Configuration = Defaults_Lists.Load_Configuration()
Window_Frame_width = GUI_Configuration["Frames"]["Page_Frames"]["Background"]["width"]
Window_Frame_height = GUI_Configuration["Frames"]["Page_Frames"]["Background"]["height"]

Format_Date = Settings["General"]["Formats"]["Date"]

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
def Download_Data(Progress_Bar: CTkProgressBar, Download_Date_Range_Source: StringVar, Download_Data_Source: StringVar, Sharepoint_Widget: CTkFrame, Manual_Widget: CTkFrame, Exchange_Widget: CTkFrame):
    Can_Download = True

    # Actuall Values
    Download_Date_Range_Source = Download_Date_Range_Source.get()
    Download_Data_Source = Download_Data_Source.get()
    SP_Password = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkentry"].get()
    Exchange_Password = Exchange_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()
    Input_Start_Date = Manual_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
    Input_End_Date = Manual_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

    Input_Start_Date = Input_Start_Date.upper()
    Input_End_Date = Input_End_Date.upper()

    # Missing Data handler
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
        pass

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
            pass
    else:
        pass

    if Can_Download == True:
        Progress_Bar.start()    #! Dodělat --> nějak se nespustí (asynchroně?)
        import Libs.Process as Process
        Process.Download_and_Process(Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Password=SP_Password, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
        Progress_Bar.stop()
        CTkMessagebox(title="Success", message="Sucessfully downloaded and processed.", icon="check", option_1="Thanks", fade_in_duration=1)
    else:
        Progress_Bar.stop()


def Save_Settings():
    #! Doděalt --> uložit všechno do Settings.json
    CTkMessagebox(title="Success", message="Changes saved to Settings.", icon="check", option_1="Thanks")

def Download_Project_Activities():
    # Password required
    dialog = Elements.Get_DialogWindow(title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
    SP_Password = dialog.get_input()

    if SP_Password == None:
        pass
    else:
        import Libs.Sharepoint.Sharepoint as Sharepoint
        Sharepoint.Get_Project_and_Activity(SP_Password=SP_Password)
        CTkMessagebox(title="Success", message="Project and Activity downloaded from Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)

        #! Dodělat --> je potřeba aktualizovat promněné Project_Variable a Action_Variable aby byli použitelný v celém systému

def Data_Upload():
    #! Doděalt --> Automaticky spustit Uplod na Sharepoint Backendový process
    CTkMessagebox(title="Success", message="Sucessfully uploaded to Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)


def Data_Excel():
    import subprocess
    #! Doděalt --> musím nastavit cestu dinamicky !!!!
    subprocess.run('start excel "D:\KM-Calendar_Reading\Operational\TimeSheets.csv"', shell=True, capture_output=False, text=False)

#? ----------------------------------------------------- Pages ----------------------------------------------------- #
# -------------------------------------------- Header -------------------------------------------- #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame Preparation
    Frame_Header = Elements.Get_Frame(Frame=Frame, Frame_Size="Header")
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="x", expand=False)

    Frame_Logo = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Logo_Element")
    Frame_Logo.pack_propagate(flag=False)
    Frame_Logo.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    Frame_Header_Information = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Information")
    Frame_Header_Information.pack_propagate(flag=False)
    Frame_Header_Information.pack(side="left", fill="none", expand=False, padx=0, pady=0)

    # ------------------------- Logo Area -------------------------#
    Icon_Frame_Company_Logo = Elements.Get_Icon(Frame=Frame_Logo, Icon="Konica_Minolta", Icon_Size=(60, 60), Picture_size="Picture_Logo")
    Icon_Frame_Company_Logo.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    # ------------------------- Logo Area -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Icon(Frame=Frame_Header_Information, Icon="Theme", Icon_Size=(30, 30), Picture_size="Picture_Theme")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account Mail
    Frame_Account_Mail = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_Mail.configure(text=Account_Email)
    Frame_Account_Mail.pack_propagate(flag=False)
    Frame_Account_Mail.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account ID
    Frame_Account_ID = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_ID.configure(text=Account_ID)
    Frame_Account_ID.pack_propagate(flag=False)
    Frame_Account_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    # Account Name
    Frame_Account_Name = Elements.Get_Text_Column_Header(Frame=Frame_Header_Information)
    Frame_Account_Name.configure(text=Account_Name)
    Frame_Account_Name.pack_propagate(flag=False)
    Frame_Account_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    return Frame_Header

# -------------------------------------------- Side Bar -------------------------------------------- #
def Get_Side_Bar(Frame: CTk|CTkFrame) -> CTkFrame:
    # Page - Downlaod
    Icon_Frame_Download = Elements.Get_Icon(Frame=Frame, Icon="Download", Icon_Size=(30, 30), Picture_size="Picture_SideBar")
    CTkToolTip(widget=Icon_Frame_Download, message="Download page")
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page())
    Icon_Frame_Download.pack(padx=5, pady=10, expand=True)
    

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Icon(Frame=Frame, Icon="Dashboard", Icon_Size=(30, 30), Picture_size="Picture_SideBar")
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page())
    Icon_Frame_Dashboard.pack(padx=5, pady=10, expand=True)
    CTkToolTip(widget=Icon_Frame_Dashboard, message="Dashboard page").show()

    # Page - Data
    Icon_Frame_Data = Elements.Get_Icon(Frame=Frame, Icon="Table", Icon_Size=(30, 30), Picture_size="Picture_SideBar")
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page())
    Icon_Frame_Data.pack(padx=5, pady=10, expand=True)
    CTkToolTip(widget=Icon_Frame_Data, message="Processed Data page")

    # Page - Information
    Icon_Frame_Information = Elements.Get_Icon(Frame=Frame, Icon="Information", Icon_Size=(30, 30), Picture_size="Picture_SideBar")
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page())
    Icon_Frame_Information.pack(padx=5, pady=10, expand=True)
    CTkToolTip(widget=Icon_Frame_Information, message="About page")

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Icon(Frame=Frame, Icon="Settings", Icon_Size=(30, 30), Picture_size="Picture_SideBar")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page())
    Icon_Frame_Settings.pack(padx=5, pady=10, expand=True)
    CTkToolTip(widget=Icon_Frame_Settings, message="Settings page")

# -------------------------------------------- Downlaod Page -------------------------------------------- #
def Page_Download(Frame: CTk|CTkFrame):
    # Default
    Download_Date_Range_Source = StringVar(master=Frame, value="Sharepoint", name="Download_Date_Range_Source")
    Download_Data_Source = StringVar(master=Frame, value="Exchange", name="Download_Data_Source")

    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # ------------------------- Work Area -------------------------#
    # Download Method
    Metdod_Text = Elements.Get_Text_H1(Frame=Frame_Download_Work_Detail_Area)
    Metdod_Text.configure(text="Step 1 - Dates definition")
    Metdod_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    Sharepoint_Widget = Widgets.Download_Sharepoint(Frame=Frame_Download_Work_Detail_Area, Download_Date_Range_Source=Download_Date_Range_Source)
    Sharepoint_Widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="n")

    Manual_Widget = Widgets.Download_Manual(Frame=Frame_Download_Work_Detail_Area, Download_Date_Range_Source=Download_Date_Range_Source)
    Manual_Widget.grid(row=1, column=1, padx=20, pady=(5, 20), sticky="n")

    # Download Source
    Source_Text = Elements.Get_Text_H1(Frame=Frame_Download_Work_Detail_Area)
    Source_Text.configure(text="Step 2 - Define data source")
    Source_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

    Exchange_Widget = Widgets.Download_Exchange(Frame=Frame_Download_Work_Detail_Area, Download_Data_Source=Download_Data_Source)
    Exchange_Widget.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="n")

    Outlook_Widget = Widgets.Download_Outlook(Frame=Frame_Download_Work_Detail_Area, Download_Data_Source=Download_Data_Source)
    Outlook_Widget.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="n")

    # ------------------------- State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame_Download_State_Area, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.configure(mode="indeterminate")
    Progress_Bar.grid(row=0, column=1, padx=5, pady=0, sticky="e")

    # Download Button
    Button_Download = Elements.Get_Button(Frame=Frame_Download_State_Area, Button_Size="Normal")
    Button_Download.configure(text="Download", command = lambda:Download_Data(Progress_Bar=Progress_Bar, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, Sharepoint_Widget=Sharepoint_Widget, Manual_Widget=Manual_Widget, Exchange_Widget=Exchange_Widget))
    Button_Download.grid(row=0, column=0, padx=5, pady=0, sticky="e")
    CTkToolTip(widget=Button_Download, message="Initiate Download and Process")

# -------------------------------------------- Dashboadr Page -------------------------------------------- #
def Page_Dashboard(Frame: CTk|CTkFrame):
    pass    

# -------------------------------------------- Data Page -------------------------------------------- #
def Page_Data(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Data_Button_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Data_Button_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    # ------------------------- State Area -------------------------#
    # Download Button
    Button_Upload = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Upload.configure(text="Upload", command = lambda:Data_Upload())
    Button_Upload.grid(row=0, column=0, padx=5, pady=0, sticky="e")
    CTkToolTip(widget=Button_Upload, message="Upload processed data directly to Sharepoint TimeSheets")

    # Download Button
    Button_Excel = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Excel.configure(text="Excel", command = lambda:Data_Excel())
    Button_Excel.grid(row=0, column=1, padx=5, pady=0, sticky="e")
    CTkToolTip(widget=Button_Excel, message="Show generated Excel file")

    # ------------------------- Work Area -------------------------#
    # Data table
    Events = pandas.read_csv(f"Operational\\TimeSheets.csv", sep=";")
    Events_List = [["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]]
    for row in Events.iterrows():
        Events_List.append(row[1].to_list())

    Frame_Events_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Download_Work_Detail_Area, Table_Size="Triple_size", Table_Values=Events_List, Table_Columns=8, Table_Rows=len(Events_List))
    Frame_Events_Table_Var = Frame_Events_Table.children["!ctktable"]
    Frame_Events_Table_Var.configure(wraplength=180)
    Frame_Events_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# -------------------------------------------- Information Page -------------------------------------------- #
def Page_Information(Frame: CTk|CTkFrame):
    pass

# -------------------------------------------- Settings Page -------------------------------------------- #
def Page_Settings(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Settings_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Settings_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)

    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(flag=False)
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # ------------------------- State Area -------------------------#
    # Add Button - Downlaod New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Download_Pro_Act.configure(text="Get Project/Activity", command = lambda:Download_Project_Activities())
    Button_Download_Pro_Act.grid(row=0, column=0, padx=5, pady=0, sticky="e")
    CTkToolTip(widget=Button_Download_Pro_Act, message="Actualize the list of Projects and Activities")

    # Add Button - Save Settings
    Button_Save_Settings = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Save_Settings.configure(text="Save", command = lambda:Save_Settings())
    Button_Save_Settings.grid(row=0, column=1, padx=5, pady=0, sticky="e")
    CTkToolTip(widget=Button_Save_Settings, message="Save settings to Settings.json")

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    #TabView.pack_propagate(flag=False)
    Tab_Gen = TabView.add("General")
    Tab_Gen.pack_propagate(flag=False)
    Tab_Cal = TabView.add("Calendar")
    Tab_Cal.pack_propagate(flag=False)
    Tab_E_G = TabView.add("Events - General")
    Tab_E_G.pack_propagate(flag=False)
    Tab_E_E = TabView.add("Events - Empty/Scheduler")
    Tab_E_E.pack_propagate(flag=False)
    Tab_E_A = TabView.add("Events - AutoFill")
    Tab_E_A.pack_propagate(flag=False)
    TabView.set("General")
    TabView.grid(row=0, column=0, padx=5, pady=0, sticky="n")

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
window.bind(sequence="<Escape>", func=lambda evet: window.quit())
window.overrideredirect(boolean=True)

display_widht = window.winfo_screenwidth()
display_height = window.winfo_screenheight()

left_position = int(display_widht // 2 - Window_Frame_width // 2)
top_position = int(display_height // 2 - Window_Frame_height // 2)

window.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
pywinstyles.apply_style(window=window, style="aero")     #! Dodělat v knihovně je poznámka, že se má background color natřít na černo aby to fungovalo

# ---------------------------------- Main Page ----------------------------------#
# Frames
Frame_Background = Elements.Get_Frame(Frame=window, Frame_Size="Background")
Frame_Background.pack(side="top", fill="both", expand=False)

Frame_Header = Get_Header(Frame=Frame_Background)

Frame_Work_Area = Elements.Get_Frame(Frame=Frame_Background, Frame_Size="Work_Area")
Frame_Work_Area.pack(side="top", fill="both", expand=False)

Frame_Side_Bar = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_SideBar")
Frame_Side_Bar.pack_propagate(flag=False)
Frame_Side_Bar.pack(side="left", fill="y", expand=True)

Frame_Work_Area_Detail = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
Frame_Work_Area_Detail.pack_propagate(flag=False)
Frame_Work_Area_Detail.pack(side="left", fill="both", expand=False)

Get_Side_Bar(Frame=Frame_Side_Bar)

Page_Download(Frame=Frame_Work_Area_Detail)

# run
window.mainloop()