
#! Dodělat --> Dodělat nahrávání obrázků a zobrazování (použít k tomu iconpy)

# Import Libraries
import time
from pandas import DataFrame
from datetime import datetime

import webview 
import customtkinter
from customtkinter import CTk, CTkFrame, StringVar, CTkProgressBar, CTkEntry, CTkLabel, CTkCheckBox
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
Configuration = Defaults_Lists.Load_Configuration() 
Account_Email = Settings["General"]["Downloader"]["Outlook"]["Calendar"]
Account_Name = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Name"]
Account_ID = Settings["General"]["Downloader"]["Sharepoint"]["Person"]["Code"]
Format_Date = Settings["General"]["Formats"]["Date"]

GUI_Configuration = Defaults_Lists.Load_Configuration()
Window_Frame_width = GUI_Configuration["Frames"]["Page_Frames"]["Background"]["width"]
Window_Frame_height = GUI_Configuration["Frames"]["Page_Frames"]["Background"]["height"]

Format_Date = Settings["General"]["Formats"]["Date"]

Win_Style_Actual = Configuration["Global_Apperance"]["Window"]["Style"]
Theme_Actual = Configuration["Global_Apperance"]["Window"]["Theme"]

#! ---------------------------------------------------------- Local Functions ---------------------------------------------------------- #
def Trun_Off_Application() -> None:
    window.quit()

def Get_Current_Theme() -> str:
    Current_Theme = customtkinter.get_appearance_mode()
    return Current_Theme

def Theme_Change():
    Current_Theme = Get_Current_Theme() 
    if Current_Theme == "Dark":
        customtkinter.set_appearance_mode("light")
    elif Current_Theme == "Light":
        customtkinter.set_appearance_mode("dark")
    elif Current_Theme == "System":
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("system")

#? ----------------------------------------------------- Buttons ----------------------------------------------------- #
# -------------------------------------------- Page Listing -------------------------------------------- #
def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
    # Find
    for widget in Pre_Working_Frame.winfo_children():
        widget.destroy()
        window.update_idletasks()

def Show_Download_Page(Active_Window: CTkFrame) -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Download(Frame=Frame_Work_Area_Detail)
    Active_Window.grid(row=0, column=0, padx=0, pady=5, sticky="")
    window.update_idletasks()

def Show_Dashboard_Page(Active_Window: CTkFrame) -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Dashboard(Frame=Frame_Work_Area_Detail)
    Active_Window.grid(row=1, column=0, padx=0, pady=5, sticky="")
    window.update_idletasks()

def Show_Data_Page(Active_Window: CTkFrame) -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Data(Frame=Frame_Work_Area_Detail)
    Active_Window.grid(row=2, column=0, padx=0, pady=5, sticky="")
    window.update_idletasks()

def Show_Information_Page(Active_Window: CTkFrame) -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Information(Frame=Frame_Work_Area_Detail)
    Active_Window.grid(row=3, column=0, padx=0, pady=5, sticky="")
    window.update_idletasks()

def Show_Settings_Page(Active_Window: CTkFrame) -> None:
    Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
    time.sleep(0.1)
    Page_Settings(Frame=Frame_Work_Area_Detail)
    Active_Window.grid(row=4, column=0, padx=0, pady=5, sticky="")
    window.update_idletasks()
    

    
# -------------------------------------------- Functionss -------------------------------------------- #
def Download_Data(Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: StringVar, Download_Data_Source: StringVar, Sharepoint_Widget: CTkFrame, Manual_Widget: CTkFrame, Exchange_Widget: CTkFrame):
    Can_Download = True

    # Actuall Values
    Download_Date_Range_Source = Download_Date_Range_Source.get()
    Download_Data_Source = Download_Data_Source.get()
    SP_Password = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkentry"].get()
    SP_Whole_Period = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe5"].children["!ctkframe3"].children["!ctkcheckbox"].get()
    if SP_Whole_Period == 1:
        SP_Whole_Period = True
    else:
        SP_Whole_Period = False
    SP_End_Date_Max_Today_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe6"].children["!ctkframe3"].children["!ctkcheckbox"].get()
    if SP_End_Date_Max_Today_Var == 1:
        SP_End_Date_Max_Today_Var = True
    else:
        SP_End_Date_Max_Today_Var = False
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
        Can_Download = False
        CTkMessagebox(title="Error", message=f"Download Date Range Source: {Download_Date_Range_Source} is not supported. Must be Sharepoint/Manual", icon="cancel", fade_in_duration=1)

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

    if Can_Download == True:
        import Libs.Process as Process
        Process.Download_and_Process(window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, SP_Password=SP_Password, SP_Whole_Period=SP_Whole_Period, SP_End_Date_Max_Today_Var=SP_End_Date_Max_Today_Var, Exchange_Password=Exchange_Password, Input_Start_Date=Input_Start_Date, Input_End_Date=Input_End_Date)
    else:
        CTkMessagebox(title="Error", message="Not possible to download and process data", icon="cancel", fade_in_duration=1)


def Save_Settings():
    #! Dodělat --> uložit všechno do Settings.json
    CTkMessagebox(title="Success", message="Changes saved to Settings.", icon="check", option_1="Thanks")

def Dialog_Window_Request(title: str, text: str, Dialog_Type: str) -> str|None:
    # Password required
    dialog = Elements.Get_DialogWindow(title=title, text=text, Dialog_Type=Dialog_Type)
    SP_Password = dialog.get_input()
    return SP_Password

def Download_Project_Activities():
    SP_Password = Dialog_Window_Request(title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
    
    if SP_Password == None:
        CTkMessagebox(title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1)
    else:
        import Libs.Sharepoint.Sharepoint as Sharepoint
        Sharepoint.Get_Project_and_Activity(SP_Password=SP_Password)
        #! Dodělat --> je potřeba aktualizovat promněné Project_Variable a Action_Variable aby byli použitelný v celém systému
        CTkMessagebox(title="Success", message="Project and Activity downloaded from Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)

def Data_Upload(Events: DataFrame):
    SP_Password = Dialog_Window_Request(title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
    if SP_Password == None:
        CTkMessagebox(title="Error", message="Cannot upload, because of missing Password", icon="cancel", fade_in_duration=1)
    else:
        import Libs.Sharepoint.Sharepoint as Sharepoint
        Sharepoint.Upload(Events=Events, SP_Password=SP_Password)
        CTkMessagebox(title="Success", message="Sucessfully uploaded to Sharepoint.", icon="check", option_1="Thanks", fade_in_duration=1)

def Data_Excel():
    import subprocess
    subprocess.run('start excel "Operational\\Events.csv"', shell=True, capture_output=False, text=False)

def Change_Download_Date_Range_Source(Download_Date_Range_Source: StringVar, Manual_Date_From_Var: CTkEntry, Manual_Date_To_Var: CTkEntry, Sharepoint_Password_Var: CTkEntry, Sharepoint_Whole_Period_Var: CTkCheckBox, Sharepoint_Active_Per_Days_Var: CTkCheckBox) -> None:
    if Download_Date_Range_Source.get() == "Manual":
        Manual_Date_From_Var.focus()
        Manual_Date_From_Var.configure(state="normal")
        Manual_Date_To_Var.configure(state="normal")

        Sharepoint_Password_Var.delete(first_index=0, last_index=1000)
        Sharepoint_Password_Var.configure(state="disabled")
        Sharepoint_Whole_Period_Var.configure(state="disabled")
        Sharepoint_Active_Per_Days_Var.configure(state="disabled")
    elif Download_Date_Range_Source.get() == "Sharepoint":
        Sharepoint_Password_Var.focus()
        Sharepoint_Password_Var.configure(state="normal")
        Sharepoint_Whole_Period_Var.configure(state="normal")
        Sharepoint_Active_Per_Days_Var.configure(state="normal")

        Manual_Date_From_Var.delete(first_index=0, last_index=1000)
        Manual_Date_From_Var.configure(placeholder_text="Date From")
        Manual_Date_From_Var.configure(state="disabled")
        Manual_Date_To_Var.delete(first_index=0, last_index=1000)
        Manual_Date_To_Var.configure(placeholder_text="Date To")
        Manual_Date_To_Var.configure(state="disabled")
    else:
        pass

def Change_Download_Data_Source(Download_Data_Source: StringVar, Exchange_Password_Var: CTkEntry):
    if Download_Data_Source.get() == "Exchange":
        Exchange_Password_Var.focus()
        Exchange_Password_Var.configure(state="normal")
    elif Download_Data_Source.get() == "Outlook_Client":
        Exchange_Password_Var.delete(first_index=0, last_index=1000)
        Exchange_Password_Var.configure(state="disabled")
    else:
        pass

#? ----------------------------------------------------- Pages ----------------------------------------------------- #
# -------------------------------------------- Header -------------------------------------------- #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    # Frame Preparation
    Frame_Header = Elements.Get_Frame(Frame=Frame, Frame_Size="Header")
    Frame_Header.pack_propagate(flag=False)

    Frame_Logo = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Logo_Element")
    Frame_Logo.pack_propagate(flag=False)

    Frame_Header_Information = Elements.Get_Frame(Frame=Frame_Header, Frame_Size="Header_Information")
    Frame_Header_Information.pack_propagate(flag=False)

    # ------------------------- Logo Area -------------------------#
    #Icon_Frame_Company_Logo = Elements.Get_Button_Icon(Frame=Frame_Logo, Icon="Konica_Minolta", Icon_Size=(60, 60), Button_Size="Picture_Logo")

    # ------------------------- Logo Area -------------------------#  
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Frame=Frame_Header_Information, Icon_Set="lucide", Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Theme.configure(command = lambda: Theme_Change())

    # Account Mail
    Frame_Account_Mail = Elements.Get_Label(Frame=Frame_Header_Information, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_Account_Mail.configure(text=Account_Email)
    Frame_Account_Mail.pack_propagate(flag=False)

    # Account ID
    Frame_Account_ID = Elements.Get_Label(Frame=Frame_Header_Information, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_Account_ID.configure(text=Account_ID)
    Frame_Account_ID.pack_propagate(flag=False)

    # Account Name
    Frame_Account_Name = Elements.Get_Label(Frame=Frame_Header_Information, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_Account_Name.configure(text=Account_Name)
    Frame_Account_Name.pack_propagate(flag=False)

    #? Build look of Widget
    Frame_Header.pack(side="top", fill="x", expand=False)
    Frame_Logo.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    Frame_Header_Information.pack(side="left", fill="none", expand=False, padx=0, pady=0)
    #Icon_Frame_Company_Logo.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_Account_Mail.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_Account_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_Account_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    return Frame_Header



# -------------------------------------------- Side Bar -------------------------------------------- #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame) -> CTkFrame:
    Active_Window = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="tally-1", Icon_Size="Side_Bar", Button_Size="Picture_Active_SideBar")   #! Dodělat --> předělat na Pouhou ikonu / Label
    
    # Page - Downlaod
    Icon_Frame_Download = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="download", Icon_Size="Side_Bar", Button_Size="Picture_SideBar")
    CTkToolTip(widget=Icon_Frame_Download, message="Download page")
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window))    

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="layout-dashboard", Icon_Size="Side_Bar", Button_Size="Picture_SideBar")
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page(Active_Window = Active_Window))
    CTkToolTip(widget=Icon_Frame_Dashboard, message="Dashboard page").show()

    # Page - Data
    Icon_Frame_Data = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="file-spreadsheet", Icon_Size="Side_Bar", Button_Size="Picture_SideBar")
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page(Active_Window = Active_Window))
    CTkToolTip(widget=Icon_Frame_Data, message="Processed Data page")

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="info", Icon_Size="Side_Bar", Button_Size="Picture_SideBar")
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window))
    CTkToolTip(widget=Icon_Frame_Information, message="About page")

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="settings", Icon_Size="Side_Bar", Button_Size="Picture_SideBar")
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window))
    CTkToolTip(widget=Icon_Frame_Settings, message="Settings page")

    # Close Aplication
    Close_Application = Elements.Get_Button_Icon(Frame=Side_Bar_Frame, Icon_Set="lucide", Icon_Name="power", Icon_Size="Side_Bar", Button_Size="Picture_Theme")
    Close_Application.configure(command = lambda: Trun_Off_Application())
    CTkToolTip(widget=Icon_Frame_Settings, message="Close program")

    #? Build look of Widget
    Active_Window.grid(row=1, column=0, padx=0, pady=5, sticky="e")
    Icon_Frame_Download.grid(row=0, column=1, padx=0, pady=5, sticky="")
    Icon_Frame_Dashboard.grid(row=1, column=1, padx=0, pady=5, sticky="")
    Icon_Frame_Data.grid(row=2, column=1, padx=0, pady=5, sticky="")
    Icon_Frame_Information.grid(row=3, column=1, padx=0, pady=5, sticky="")
    Icon_Frame_Settings.grid(row=4, column=1, padx=0, pady=5, sticky="")
    Close_Application.grid(row=5, column=1, padx=0, pady=5, sticky="")

    window.update_idletasks()


# -------------------------------------------- Downlaod Page -------------------------------------------- #
def Page_Download(Frame: CTk|CTkFrame):
    # Default
    Download_Date_Range_Source = StringVar(master=Frame, value="Sharepoint", name="Download_Date_Range_Source")
    Download_Data_Source = StringVar(master=Frame, value="Exchange", name="Download_Data_Source")

    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Download_State_Area.pack_propagate(flag=False)

    Frame_Download_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Download_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- Work Area -------------------------#
    # Download Method
    Metdod_Text = Elements.Get_Label(Frame=Frame_Download_Work_Detail_Area, Label_Size="H1", Font_Size="H1")
    
    Metdod_Text.configure(text="Step 1 - Dates definition")

    Sharepoint_Widget = Widgets.Download_Sharepoint(Frame=Frame_Download_Work_Detail_Area, Download_Date_Range_Source=Download_Date_Range_Source)
    Sharepoint_Usage_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Sharepoint_Password_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_Whole_Period_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe5"].children["!ctkframe3"].children["!ctkcheckbox"]
    Sharepoint_Active_Per_Days_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe6"].children["!ctkframe3"].children["!ctkcheckbox"]

    Manual_Widget = Widgets.Download_Manual(Frame=Frame_Download_Work_Detail_Area, Download_Date_Range_Source=Download_Date_Range_Source)
    Manual_Usage_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Manual_Date_From_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"]
    Manual_Date_To_Var = Manual_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"]
    Manual_Date_From_Var.configure(state="disabled")
    Manual_Date_To_Var.configure(state="disabled")

    # Disabling fields --> Download_Date_Range_Source
    Sharepoint_Usage_Var.configure(command = lambda:Change_Download_Date_Range_Source(Download_Date_Range_Source=Download_Date_Range_Source, Manual_Date_From_Var=Manual_Date_From_Var, Manual_Date_To_Var=Manual_Date_To_Var, Sharepoint_Password_Var=Sharepoint_Password_Var, Sharepoint_Whole_Period_Var=Sharepoint_Whole_Period_Var, Sharepoint_Active_Per_Days_Var=Sharepoint_Active_Per_Days_Var))
    Manual_Usage_Var.configure(command = lambda:Change_Download_Date_Range_Source(Download_Date_Range_Source=Download_Date_Range_Source, Manual_Date_From_Var=Manual_Date_From_Var, Manual_Date_To_Var=Manual_Date_To_Var, Sharepoint_Password_Var=Sharepoint_Password_Var, Sharepoint_Whole_Period_Var=Sharepoint_Whole_Period_Var, Sharepoint_Active_Per_Days_Var=Sharepoint_Active_Per_Days_Var))

    # Download Source
    Source_Text = Elements.Get_Label(Frame=Frame_Download_Work_Detail_Area, Label_Size="H1", Font_Size="H1")
    Source_Text.configure(text="Step 2 - Define data source")

    Exchange_Widget = Widgets.Download_Exchange(Frame=Frame_Download_Work_Detail_Area, Download_Data_Source=Download_Data_Source)
    Exchange_Usage_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Exchange_Password_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"]

    Outlook_Widget = Widgets.Download_Outlook(Frame=Frame_Download_Work_Detail_Area, Download_Data_Source=Download_Data_Source)
    Outlook_Usage_Var = Outlook_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]

    # Disabling fields --> Download_Data_Source
    Exchange_Usage_Var.configure(command = lambda:Change_Download_Data_Source(Download_Data_Source=Download_Data_Source, Exchange_Password_Var=Exchange_Password_Var))
    Outlook_Usage_Var.configure(command = lambda:Change_Download_Data_Source(Download_Data_Source=Download_Data_Source, Exchange_Password_Var=Exchange_Password_Var))

    # ------------------------- State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Frame=Frame_Download_State_Area, orientation="Horizontal", Progress_Size="Download_Process")
    Progress_Bar.set(value=0)

    Progress_text = Elements.Get_Label(Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Progress_text.configure(text=f"", width=200)

    Button_Download = Elements.Get_Button(Frame=Frame_Download_State_Area, Button_Size="Normal")
    Button_Download.configure(text="Download", command = lambda:Download_Data(Progress_Bar=Progress_Bar, Progress_text=Progress_text, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, Sharepoint_Widget=Sharepoint_Widget, Manual_Widget=Manual_Widget, Exchange_Widget=Exchange_Widget))
    CTkToolTip(widget=Button_Download, message="Initiate Download and Process")
    
    #? Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Download_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)
    
    Metdod_Text.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Sharepoint_Widget.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="n")
    Manual_Widget.grid(row=1, column=1, padx=20, pady=(5, 20), sticky="n")
    Source_Text.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    Exchange_Widget.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="n")
    Outlook_Widget.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="n")

    Button_Download.pack(side="left", fill="none", expand=False, padx=5, pady=0)
    Progress_text.pack(side="left", fill="none", expand=False, padx=5, pady=0)
    Progress_Bar.pack(side="left", fill="none", expand=False, padx=10, pady=0)

    

# -------------------------------------------- Dashboadr Page -------------------------------------------- #
def Page_Dashboard(Frame: CTk|CTkFrame):
    def DashBoard_Project():
        Theme = Get_Current_Theme()
        if Theme == "System":
            Theme = "Dark"
        else:
            pass
        webview.create_window(title="Project Detail", width=1645, height=428, url=f"Operational\\DashBoard_Project_{Theme}.html", frameless=True, easy_drag=True, resizable=True) 
        webview.start()

    def DashBoard_Activity():
        Theme = Get_Current_Theme()
        if Theme == "System":
            Theme = "Dark"
        else:
            pass
        webview.create_window(title="Activity Detail", width=1645, height=428, url=f"Operational\\DashBoard_Activity_{Theme}.html", frameless=True, easy_drag=True, resizable=True) 
        webview.start()

    def DashBoard_Utilization():
        Theme = Get_Current_Theme()
        if Theme == "System":
            Theme = "Dark"
        else:
            pass
        webview.create_window(title="Utilization Detail", width=1645, height=428, url=f"Operational\\DashBoard_Utilization_{Theme}.html", frameless=True, easy_drag=True, resizable=True) 
        webview.start()

    # Divide Working Page into 2 parts
    Frame_Dashboard_Header_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")
    Frame_Dashboard_Header_Area.pack_propagate(flag=False)

    Frame_Dashboard_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Dashboard_Work_Detail_Area.grid_propagate(flag=False)

    Frame_DashBoard_Scrolable_Area = Elements.Get_Widget_Scrolable_Frame(Frame=Frame_Dashboard_Work_Detail_Area, Frame_Size="Triple_size")

    # ------------------------- Buttons Area -------------------------#
    Project_Detail_button = customtkinter.CTkButton(master=Frame_Dashboard_Header_Area, text="Project Detail", command=DashBoard_Project)

    Activity_Detail_button = customtkinter.CTkButton(master=Frame_Dashboard_Header_Area, text="Activity Detail", command=DashBoard_Activity)

    Utilization_Detail_button = customtkinter.CTkButton(master=Frame_Dashboard_Header_Area, text="Utilization Detail", command=DashBoard_Utilization)

    # ------------------------- Dashboard work Area -------------------------#
    Totals_Summary_Df = pandas.read_csv(f"Operational\\Events_Totals.csv", sep=";")
    Projec_DF = pandas.read_csv(f"Operational\\Events_Project.csv", sep=";")
    Activity_Df = pandas.read_csv(f"Operational\\Events_Activity.csv", sep=";")
    WeekDays_Df = pandas.read_csv(f"Operational\\Events_WeekDays.csv", sep=";")
    Weeks_DF = pandas.read_csv(f"Operational\\Events_Weeks.csv", sep=";")
    Events_DF = pandas.read_csv(f"Operational\\Events.csv", sep=";")

    # Total Line
    Total_Duration_hours = float(Totals_Summary_Df.iloc[0]["Total_Duration_hours"])
    Mean_Duration_hours = float(Totals_Summary_Df.iloc[0]["Mean_Duration_hours"])
    Event_counts = int(Totals_Summary_Df.iloc[0]["Event_counts"])
    Reporting_Period_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["Reporting_Period_Utilization"], ndigits=2))
    My_Calendar_Utilization = float(round(number=Totals_Summary_Df.iloc[0]["My_Calendar_Utilization"], ndigits=2))
    Utilization_Surplus_hours = float(Totals_Summary_Df.iloc[0]["Utilization_Surplus_hours"])

    Frame_Dashboard_Total_Line = Elements.Get_Dashboards_Frame(Frame=Frame_DashBoard_Scrolable_Area, Frame_Size="Totals_Line")
    Frame_Dashboard_Total_Line.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Counter = Widgets.DashBoard_Totals_Counter_Widget(Frame=Frame_Dashboard_Total_Line, Label="Count", Widget_Line="Totals_Line", Widget_size="Normal", Data=Event_counts)
    Frame_DashBoard_Totals_Counter.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Total = Widgets.DashBoard_Totals_Total_Widget(Frame=Frame_Dashboard_Total_Line, Label="Total", Widget_Line="Totals_Line", Widget_size="Normal", Data=Total_Duration_hours)
    Frame_DashBoard_Totals_Total.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Average = Widgets.DashBoard_Totals_Average_Widget(Frame=Frame_Dashboard_Total_Line, Label="Average", Widget_Line="Totals_Line", Widget_size="Normal", Data=Mean_Duration_hours)
    Frame_DashBoard_Totals_Average.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Report_Per_Util = Widgets.DashBoard_Totals_Report_Period_Util_Widget(Frame=Frame_Dashboard_Total_Line, Label="Reported Period Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=Reporting_Period_Utilization)
    Frame_DashBoard_Totals_Report_Per_Util.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Active_Day_Util = Widgets.DashBoard_Totals_Active_Day_Util_Widget(Frame=Frame_Dashboard_Total_Line, Label="My Active Days Utilization", Widget_Line="Totals_Line", Widget_size="Normal", Data=My_Calendar_Utilization)
    Frame_DashBoard_Totals_Active_Day_Util.pack_propagate(flag=False)
    Frame_DashBoard_Totals_Util_by_today_surplus = Widgets.DashBoard_Totals_Utilization_Surplus_Widget(Frame=Frame_Dashboard_Total_Line, Label="Util. surplus by Input End Date", Widget_Line="Totals_Line", Widget_size="Normal", Data=Utilization_Surplus_hours)
    Frame_DashBoard_Totals_Util_by_today_surplus.pack_propagate(flag=False)

    # Project Activity Line
    Frame_Dashboard_Project_Activity_Line = Elements.Get_Dashboards_Frame(Frame=Frame_DashBoard_Scrolable_Area, Frame_Size="Project_Activity_Line")
    Frame_Dashboard_Project_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section")
    Frame_Dashboard_Project_Detail_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Detail_Section")
    Frame_DashBoard_Project_Frame = Widgets.DashBoard_Project_Widget(Frame=Frame_Dashboard_Project_Detail_Section, Label="Projects", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Projec_DF=Projec_DF)
    Frame_Dashboard_Project_Side_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Project_Section, Frame_Size="Project_Activity_Side_Section")
    Frame_DashBoard_Project_Detail1_Frame = Widgets.DashBoard_Project_Detail1_Widget(Frame=Frame_Dashboard_Project_Side_Section, Label="Most Occcurence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Projec_DF=Projec_DF)
    Frame_DashBoard_Project_Detail1_Frame.pack_propagate(flag=False)
    Frame_DashBoard_Project_Detail2_Frame = Widgets.DashBoard_Project_Detail2_Widget(Frame=Frame_Dashboard_Project_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Projec_DF=Projec_DF)
    Frame_DashBoard_Project_Detail2_Frame.pack_propagate(flag=False)
    Frame_DashBoard_Project_Detail3_Frame = Widgets.DashBoard_Project_Detail3_Widget(Frame=Frame_Dashboard_Project_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Projec_DF=Projec_DF)
    Frame_DashBoard_Project_Detail3_Frame.pack_propagate(flag=False)

    Frame_Dashboard_Activity_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Project_Activity_Line, Frame_Size="Project_Activity_Section")
    Frame_Dashboard_Activity_Detail_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Detail_Section")
    Frame_DashBoard_Activity_Frame = Widgets.DashBoard_Activity_Widget(Frame=Frame_Dashboard_Activity_Detail_Section, Label="Activity", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity", Activity_Df=Activity_Df)
    Frame_Dashboard_Activity_Side_Section = Elements.Get_Dashboards_Frame(Frame=Frame_Dashboard_Activity_Section, Frame_Size="Project_Activity_Side_Section")
    Frame_DashBoard_Activity_Detail1_Frame = Widgets.DashBoard_Activity_Detail1_Widget(Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Occcurence", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
    Frame_DashBoard_Activity_Detail1_Frame.pack_propagate(flag=False)
    Frame_DashBoard_Activity_Detail2_Frame = Widgets.DashBoard_Activity_Detail2_Widget(Frame=Frame_Dashboard_Activity_Side_Section, Label="Most Hours", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
    Frame_DashBoard_Activity_Detail2_Frame.pack_propagate(flag=False)
    Frame_DashBoard_Activity_Detail3_Frame = Widgets.DashBoard_Activity_Detail3_Widget(Frame=Frame_Dashboard_Activity_Side_Section, Label="Highest Average", Widget_Line="Project_Activity_Line", Widget_size="Project_Activity_Details", Activity_Df=Activity_Df)
    Frame_DashBoard_Activity_Detail3_Frame.pack_propagate(flag=False)

    # WeekDay and Weeks Line
    Frame_Dashboard_WeekDay_Weeks_Line = Elements.Get_Dashboards_Frame(Frame=Frame_DashBoard_Scrolable_Area, Frame_Size="WeekDay_Weeks_Line")
    Frame_DashBoard_WeekDays_Frame = Widgets.DashBoard_WeekDays_Widget(Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="WeekDays", Widget_Line="WeekDay_Weeks", Widget_size="Normal", WeekDays_Df=WeekDays_Df)
    Frame_DashBoard_Weeks_Frame = Widgets.DashBoard_Weeks_Widget(Frame=Frame_Dashboard_WeekDay_Weeks_Line, Label="Weeks", Widget_Line="WeekDay_Weeks", Widget_size="Normal", Weeks_DF=Weeks_DF)

    # Day Chart Line
    Frame_Dashboard_Day_Chart_Line = Elements.Get_Dashboards_Frame(Frame=Frame_DashBoard_Scrolable_Area, Frame_Size="Day_Chart_Line")
    Frame_DashBoard_Day_Chart_Frame = Widgets.DashBoard_DaysChart_Widget(Frame=Frame_Dashboard_Day_Chart_Line, Label="Day Project/Activity distribution", Widget_Line="WeekChart", Widget_size="Normal", Events_DF=Events_DF)
    Frame_DashBoard_Day_Chart_Frame.pack_propagate(flag=False)
    Frame_DashBoard_Cumulated_Chart_Frame = Widgets.DashBoard_Cumulated_Time_Widget(Frame=Frame_Dashboard_Day_Chart_Line, Label="My reported time vs KM planned util.", Widget_Line="WeekChart", Widget_size="Normal", Events_DF=Events_DF)
    Frame_DashBoard_Cumulated_Chart_Frame.pack_propagate(flag=False)

    #? Build look of Widget
    Frame_Dashboard_Header_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Dashboard_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_DashBoard_Scrolable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)

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
    Frame_DashBoard_Day_Chart_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)
    Frame_DashBoard_Cumulated_Chart_Frame.pack(side="top", fill="none", expand=True, padx=5, pady=5)

    Project_Detail_button.pack(side="left", pady=10, expand=True)
    Activity_Detail_button.pack(side="left", pady=10, expand=True)
    Utilization_Detail_button.pack(side="left", pady=10, expand=True)



# -------------------------------------------- Data Page -------------------------------------------- #
def Page_Data(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Data_Button_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Data_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Data_Work_Detail_Area.grid_propagate(flag=False)

    Events = pandas.read_csv(f"Operational\\Events.csv", sep=";")

    # ------------------------- Buttons Area -------------------------#
    # Download Button
    Button_Upload = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Upload.configure(text="Upload", command = lambda:Data_Upload(Events=Events))
    CTkToolTip(widget=Button_Upload, message="Upload processed data directly to Sharepoint TimeSheets")

    # Download Button
    Button_Excel = Elements.Get_Button(Frame=Frame_Data_Button_Area, Button_Size="Normal")
    Button_Excel.configure(text="Excel", command = lambda:Data_Excel())
    CTkToolTip(widget=Button_Excel, message="Show generated Excel file")

    # ------------------------- Work Area -------------------------#
    # Data table
    Events_List = [["Personnel number", "Date", "Network Description", "Activity", "Activity description", "Start Time", "End Time", "Location"]]
    for row in Events.iterrows():
        Events_List.append(row[1].to_list())

    Frame_Events_Table = Elements_Groups.Get_Table_Frame(Frame=Frame_Data_Work_Detail_Area, Table_Size="Triple_size", Table_Values=Events_List, Table_Columns=8, Table_Rows=len(Events_List))
    Frame_Events_Table_Var = Frame_Events_Table.children["!ctktable"]
    Frame_Events_Table_Var.configure(wraplength=180)

    #? Build look of Widget
    Frame_Data_Button_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Data_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    Button_Upload.grid(row=0, column=0, padx=5, pady=0, sticky="e")
    Button_Excel.grid(row=0, column=1, padx=5, pady=0, sticky="e")

    Frame_Events_Table.pack(side="top", fill="both", expand=True, padx=10, pady=10)



# -------------------------------------------- Information Page -------------------------------------------- #
def Page_Information(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Info_Header_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Information_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Information_Work_Detail_Area.grid_propagate(flag=False)
    
    # ------------------------- Info Header Area -------------------------#

    # ------------------------- Info Text Area -------------------------#
    # Description
    #! Dodělat --> text ohledně projektu a linka na víc info na Githubu (nejlepší by bylo, kdyby to přímo přečetlo Readme.md)!!!
    Frame_Information_Scrolable_Area = Elements.Get_Widget_Scrolable_Frame(Frame=Frame_Information_Work_Detail_Area, Frame_Size="Triple_size")

    #? Build look of Widget
    Frame_Info_Header_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Information_Work_Detail_Area.pack(side="top", fill="both", expand=True, padx=0, pady=0)
    Frame_Information_Scrolable_Area.pack(side="top", fill="both", expand=True, padx=10, pady=10)



# -------------------------------------------- Settings Page -------------------------------------------- #
def Page_Settings(Frame: CTk|CTkFrame):
    # Divide Working Page into 2 parts
    Frame_Settings_State_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Status_Line")

    Frame_Settings_Work_Detail_Area = Elements.Get_Frame(Frame=Frame, Frame_Size="Work_Area_Detail")
    Frame_Settings_Work_Detail_Area.grid_propagate(flag=False)

    # ------------------------- State Area -------------------------#
    # Add Button - Downlaod New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Download_Pro_Act.configure(text="Get Project/Activity", command = lambda:Download_Project_Activities())
    CTkToolTip(widget=Button_Download_Pro_Act, message="Actualize the list of Projects and Activities")

    # Add Button - Save Settings
    Button_Save_Settings = Elements.Get_Button(Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Save_Settings.configure(text="Save", command = lambda:Save_Settings())
    CTkToolTip(widget=Button_Save_Settings, message="Save settings to Settings.json")

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Frame=Frame_Settings_Work_Detail_Area, Tab_size="Normal")
    TabView.pack_propagate(flag=False)
    Tab_Ape = TabView.add("Apperance")
    Tab_Ape.pack_propagate(flag=False)
    Tab_Gen = TabView.add("Data Source")
    Tab_Gen.pack_propagate(flag=False)
    Tab_Cal = TabView.add("Calendar")
    Tab_Cal.pack_propagate(flag=False)
    Tab_E_G = TabView.add("Events - General")
    Tab_E_G.pack_propagate(flag=False)
    Tab_E_E = TabView.add("Events - Empty/Scheduler")
    Tab_E_E.pack_propagate(flag=False)
    Tab_E_A = TabView.add("Events - AutoFill")
    Tab_E_A.pack_propagate(flag=False)
    TabView.set("Apperance")

    # Apperance
    Theme_Widget = Widgets.Settings_Aperance_Theme(Frame=Tab_Ape, window=window)
    Color_Pallete_Widget = Widgets.Settings_Aperance_Color_Pallete(Frame=Tab_Ape)

    # General Page
    Sharepoint_Widget = Widgets.Settings_General_Sharepoint(Frame=Tab_Gen)
    Exchange_Widget = Widgets.Settings_General_Exchange(Frame=Tab_Gen)
    Formats_Widget = Widgets.Settings_General_Formats(Frame=Tab_Gen)

    # Calendar Page
    Calendar_Working_Widget = Widgets.Settings_Calendar_Working_Hours(Frame=Tab_Cal)
    Calendar_Vacation_Widget = Widgets.Settings_Calendar_Vacation(Frame=Tab_Cal)
    Calendar_Start_End_Widget = Widgets.Settings_Calendar_Start_End_Time(Frame=Tab_Cal)

    # Event-General Page
    Event_Lunch_Widget = Widgets.Settings_Events_General_Lunch(Frame=Tab_E_G)
    Event_Vacation_Widget = Widgets.Settings_Events_General_Vacation(Frame=Tab_E_G)
    Event_HomeOffice_Widget = Widgets.Settings_Events_General_HomeOffice(Frame=Tab_E_G)
    Event_Skip_Widget = Widgets.Settings_Events_General_Skip(Frame=Tab_E_G)
    Event_Parralel_Widget = Widgets.Settings_Parralel_events(Frame=Tab_E_G)
    Event_Join_Widget = Widgets.Settings_Join_events(Frame=Tab_E_G)

    # Event-Empty Page
    Event_Empty_General_Widget = Widgets.Settings_Events_Empty_Generaly(Frame=Tab_E_E)
    Event_Scheduler_Widget = Widgets.Settings_Events_Empt_Schedule(Frame=Tab_E_E)

    # Event-AutoFill Page
    Event_AutoFiller_Widget = Widgets.Settings_Events_AutoFill(Frame=Tab_E_A)

    #? Build look of Widget
    Frame_Settings_State_Area.pack(side="top", fill="x", expand=False, padx=0, pady=0)
    Frame_Settings_Work_Detail_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    Button_Download_Pro_Act.grid(row=0, column=0, padx=5, pady=0, sticky="e")
    Button_Save_Settings.grid(row=0, column=1, padx=5, pady=0, sticky="e")
    TabView.grid(row=0, column=0, padx=5, pady=0, sticky="n")

    Theme_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Color_Pallete_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

    Sharepoint_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Exchange_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Formats_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Calendar_Working_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Calendar_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Calendar_Start_End_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Event_Lunch_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Vacation_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Event_HomeOffice_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
    Event_Skip_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    Event_Parralel_Widget.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    Event_Join_Widget.grid(row=1, column=2, padx=5, pady=5, sticky="nw")

    Event_Empty_General_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Event_Scheduler_Widget.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

    Event_AutoFiller_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")



#! ---------------------------------------------------------- Main Program ---------------------------------------------------------- #
# main window
window = customtkinter.CTk()
window.title("Time Sheet Downloader")

display_widht = window.winfo_screenwidth()
display_height = window.winfo_screenheight()
left_position = int(display_widht // 2 - Window_Frame_width // 2)
top_position = int(display_height // 2 - Window_Frame_height // 2)
window.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

window.iconbitmap(bitmap=f"Libs\\GUI\\Icons\\TimeSheet.ico")
customtkinter.set_appearance_mode(mode_string=Theme_Actual)
window.overrideredirect(boolean=True)
pywinstyles.apply_style(window=window, style=Win_Style_Actual)

# ---------------------------------- Main Page ----------------------------------#
# Frames
Frame_Background = Elements.Get_Frame(Frame=window, Frame_Size="Background")
Frame_Background.pack(side="top", fill="both", expand=False)

Frame_Header = Get_Header(Frame=Frame_Background)

Frame_Work_Area = Elements.Get_Frame(Frame=Frame_Background, Frame_Size="Work_Area")
Frame_Work_Area.pack(side="top", fill="both", expand=False)

Frame_Side_Bar = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_SideBar")
Frame_Side_Bar.grid_propagate(flag=False)
Frame_Side_Bar.pack(side="left", fill="y", expand=True)

Frame_Work_Area_Detail = Elements.Get_Frame(Frame=Frame_Work_Area, Frame_Size="Work_Area_Main")
Frame_Work_Area_Detail.pack_propagate(flag=False)
Frame_Work_Area_Detail.pack(side="left", fill="both", expand=False)

Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar)

Page_Dashboard(Frame=Frame_Work_Area_Detail)

# run
window.mainloop()