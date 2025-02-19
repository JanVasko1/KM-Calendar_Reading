# Import Libraries
import shutil

from customtkinter import CTk, CTkFrame
from CTkMessagebox import CTkMessagebox
import pywinstyles

import Libs.GUI.Widgets.W_Settings as Settings_Widgets
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["General"]["User"]["User_Type"]
    # ------------------------- Local Functions -------------------------#
    def Download_Project_Activities():
        SP_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        
        if SP_Password == None:
            CTkMessagebox(title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Get_Project_and_Activity(Settings=Settings, SP_Password=SP_Password)
            CTkMessagebox(title="warning", message="Project and Activity downloaded from Sharepoint. Restart app!!", icon="check", option_1="Thanks", fade_in_duration=1)

    def Upload_Project_Activities():
        Exchange_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Exchange Login", text="Write your password", Dialog_Type="Password")
        
        if Exchange_Password == None:
            CTkMessagebox(title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1)
        else:
            import Libs.Download.Exchange as Exchange
            Exchange.Push_Project(Settings=Settings, Exchange_Password=Exchange_Password)
            Exchange.Push_Activity(Settings=Settings, Exchange_Password=Exchange_Password)
            CTkMessagebox(title="Success", message="Project and Activity uploaded to Exchange. Give MS time to upload changes and restart Outlook.", icon="check", option_1="Thanks", fade_in_duration=1)

    def Save_Settings():
        # Copy Settings file into Downloads Folder
        Source_File = Defaults_Lists.Absolute_path(relative_path=f"Libs\\Settings.json")
        Destination_File = Defaults_Lists.Get_Downloads_File_Path(File_Name="TimeSheets_Settings", File_postfix="json")
        shutil.copyfile(src=Source_File, dst=Destination_File)
        CTkMessagebox(title="Success", message="Your settings file has been exported to your downloads folder.", icon="check", option_1="Thanks", fade_in_duration=1)
        
    def Load_Settings():
        def drop_func(file):
            print(file)
            Can_Import = True
            # Check if file is json
            File_Name = file[0]
            File_Name_list = File_Name.split(".")

            if File_Name_list[1] == "json":
                pass
            else:
                Can_Import = False
                CTkMessagebox(title="Error", message=f"Imported file is not .json you have to import only .json.", icon="cancel", fade_in_duration=1)

            # Check if file contain whole structure needed as 
            if Can_Import == True:
                pass
            else:
                pass

            # Take content and place it to file
            if Can_Import == True:
                # TODO --> file is file path file itself
                pass
            else:
                pass

            # Change global Settings 
            if Can_Import == True:
                pass
            else:
                pass
            
            CTkMessagebox(title="Success", message="Your settings file has been imported. You can close Window.", icon="check", option_1="Thanks", fade_in_duration=1)
        
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", width=200, height=200)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop")
        pywinstyles.apply_dnd(widget=Frame_Body, func=drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Set="lucide", Icon_Name="braces", Icon_Size="Header", Button_Size="Picture_Theme")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal")

        Icon_Theme.pack(side="top", padx=50, pady=50)
        
        
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

    # Button - Save Settings
    Button_Save_Settings = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Save_Settings.configure(text="Save Settings", command = lambda:Save_Settings())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Settings, message="Save whole setup into Downloads.", ToolTip_Size="Normal")

    # Button - Load Settings
    Button_Load_Settings = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Load_Settings.configure(text="Load Settings", command = lambda:Load_Settings())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Settings, message="Upload Settings files.", ToolTip_Size="Normal")

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
    Button_Save_Settings.grid(row=0, column=2, padx=5, pady=15, sticky="e")
    Button_Load_Settings.grid(row=0, column=3, padx=5, pady=15, sticky="e")

    TabView.grid(row=0, column=0, padx=5, pady=15, sticky="n")

    Theme_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Color_Palette_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Program_User_Type_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

    Sharepoint_Widget.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    Exchange_Widget.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    Formats_Widget.grid(row=0, column=2, padx=5, pady=5, sticky="nw")

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
