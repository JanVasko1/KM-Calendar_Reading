# Import Libraries
import json

from customtkinter import CTk, CTkFrame, CTkButton
import pywinstyles

import Libs.GUI.Widgets.W_Settings as W_Settings
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Page_Settings(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["0"]["General"]["User"]["User_Type"]
    # ------------------------- Local Functions -------------------------#
    def Download_Project_Activities():
        SP_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        
        if SP_Password == None:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Get_Project_and_Activity(Settings=Settings, Configuration=Configuration, SP_Password=SP_Password)
            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Project and Activity downloaded from Sharepoint.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Upload_Project_Activities():
        Exchange_Password = Defaults_Lists.Dialog_Window_Request(Configuration=Configuration, title="Exchange Login", text="Write your password", Dialog_Type="Password")
        
        if Exchange_Password == None:
            Elements.Get_MessageBox(Configuration=Configuration, title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            import Libs.Download.Exchange as Exchange
            Exchange.Push_Project(Settings=Settings, Configuration=Configuration, Exchange_Password=Exchange_Password)
            Exchange.Push_Activity(Settings=Settings, Configuration=Configuration, Exchange_Password=Exchange_Password)
            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Project and Activity uploaded to Exchange. Give MS time to upload changes and restart Outlook.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Save_Settings():
        # Export Settings into Downloads Folder - backup
        Export_dict = {
            "Type": "Settings",
            "Data": Settings["0"]}
        Save_Path = Defaults_Lists.Get_Downloads_File_Path(File_Name="TimeSheets_Settings", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Your settings file has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Settings(Button_Load_Settings: CTkButton):
        def drop_func(file):
            Defaults_Lists.Import_Data(Settings=Settings, Configuration=Configuration, import_file_path=file, Import_Type="Settings", JSON_path=["0"], Method="Overwrite")
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, title="Success", message="Your settings file has been imported. You can close Window and restart app.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = Defaults_Lists.Count_coordinate_for_new_window(Clicked_on=Button_Load_Settings, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", width=Import_window_geometry[0], height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=2)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Theme")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=2)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        
        
    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Settings_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line", GUI_Level_ID=1)

    # ------------------------- State Area -------------------------#
    # Button - Download New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Download_Pro_Act.configure(text="Get Project/Activity", command = lambda:Download_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download_Pro_Act, message="Actualize the list of Projects and Activities inside the app from actual Sharepoint.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # Button - Download New Project and Activities
    Button_Upload_Pro_Act = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Upload_Pro_Act.configure(text="Upload Project/Activity", command = lambda:Upload_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Upload_Pro_Act, message="Upload the list of Projects and Activities into Exchange.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # Button - Save Settings
    Button_Save_Settings = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Save_Settings.configure(text="Save Settings", command = lambda:Save_Settings())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Settings, message="Save whole setup into Downloads.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # Button - Load Settings
    Button_Load_Settings = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Settings_State_Area, Button_Size="Normal")
    Button_Load_Settings.configure(text="Load Settings", command = lambda:Load_Settings(Button_Load_Settings=Button_Load_Settings))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Settings, message="Upload Settings files.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    Tab_Gen = TabView.add("General")
    Tab_Dat = TabView.add("Data Source")
    Tab_Cal = TabView.add("Calendar")
    Tab_E_G = TabView.add("Events - General")
    Tab_E_Spec = TabView.add("Events - Special")
    Tab_E_E = TabView.add("Events - Empty")
    Tab_E_A = TabView.add("Events - Rules")
    if User_Type == "Manager":
        Tab_Team = TabView.add("My Team")

        Tab_Team_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton8"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="MY Team base setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    else:
        pass
    TabView.set("General")

    Tab_Gen_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Tab_Dat_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton2"]
    Tab_Cal_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton3"]
    Tab_E_G_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton4"]
    Tab_E_Spec_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton5"]
    Tab_E_E_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton6"]
    Tab_E_A_ToolTip_But = TabView.children["!ctksegmentedbutton"].children["!ctkbutton7"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Gen_ToolTip_But, message="Application General Setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Dat_ToolTip_But, message="Setup related to Downloading date.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Cal_ToolTip_But, message="Base calendar From/To + Day Starting and Ending Event setup.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_G_ToolTip_But, message="Multiple general setup related to Events.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_Spec_ToolTip_But, message="Special Events which needs special treatment.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_E_ToolTip_But, message="Filling Empty time Tool and Split too long Empty place.", ToolTip_Size="Normal", GUI_Level_ID=1)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_E_A_ToolTip_But, message="Rule base Event Handling tools setup.", ToolTip_Size="Normal", GUI_Level_ID=1)

    # ---------- General ---------- #
    Frame_Tab_Gen_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Gen_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Gen, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Theme_Widget = W_Settings.Settings_General_Theme(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Gen_Column_A, window=window, GUI_Level_ID=2)
    Color_Palette_Widget = W_Settings.Settings_General_Color(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Gen_Column_B, GUI_Level_ID=2)
    Program_User_Type_Widget = W_Settings.Settings_User_Widget(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Gen_Column_C, GUI_Level_ID=2)

    # ---------- General Page ---------- #
    Frame_Tab_Dat_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Dat, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Dat_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Dat, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Dat_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Dat, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Sharepoint_Widget = W_Settings.Settings_General_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Dat_Column_A, GUI_Level_ID=2)
    Exchange_Widget = W_Settings.Settings_General_Exchange(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Dat_Column_B, GUI_Level_ID=2)
    Formats_Widget = W_Settings.Settings_General_Formats(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Dat_Column_C, GUI_Level_ID=2)

    # ---------- Calendar Page ---------- #
    Frame_Tab_Cal_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_Cal_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Cal, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Calendar_Working_Widget = W_Settings.Settings_Calendar_Working_Hours(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Cal_Column_A, GUI_Level_ID=2)
    Calendar_Vacation_Widget = W_Settings.Settings_Calendar_Vacation(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Cal_Column_B, GUI_Level_ID=2)
    Calendar_Start_End_Widget = W_Settings.Settings_Calendar_Start_End_Time(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Cal_Column_C, GUI_Level_ID=2)

    # ---------- Event-General Page ---------- #
    Frame_Tab_E_G_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_G_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_G_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_G, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_Skip_Widget = W_Settings.Settings_Events_General_Skip(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_G_Column_A, GUI_Level_ID=2)
    Event_Join_Widget = W_Settings.Settings_Join_events(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_G_Column_B, GUI_Level_ID=2)
    Event_Split_Widget = W_Settings.Settings_Events_Split(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_G_Column_B, GUI_Level_ID=2)
    Event_Parallel_Widget = W_Settings.Settings_Parallel_events(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_G_Column_C, GUI_Level_ID=2)

    # ---------- Event-Special Page ---------- #
    Frame_Tab_E_Spec_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_Spec_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_E_Spec_Column_C = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_Spec, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_Lunch_Widget = W_Settings.Settings_Events_General_Lunch(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_Spec_Column_A, GUI_Level_ID=2)
    Event_Vacation_Widget = W_Settings.Settings_Events_General_Vacation(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_Spec_Column_A, GUI_Level_ID=2)
    Event_SickDay_Widget = W_Settings.Settings_Events_General_SickDay(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_Spec_Column_B, GUI_Level_ID=2)
    Event_HomeOffice_Widget = W_Settings.Settings_Events_General_HomeOffice(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_Spec_Column_B, GUI_Level_ID=2)
    Event_Private_Widget = W_Settings.Settings_Events_General_Private(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_Spec_Column_C, GUI_Level_ID=2)

    # ---------- Event-Empty Page ---------- #
    Frame_Tab_E_E_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_E, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_Empty_General_Widget = W_Settings.Settings_Events_Empty_Generally(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_E_Column_A, GUI_Level_ID=2)
    Event_Scheduler_Widget = W_Settings.Settings_Events_Empty_Schedule(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_E_Column_A, GUI_Level_ID=2)

    # ---------- Event-AutoFill Page ---------- #
    Frame_Tab_E_A_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_E_A, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    Event_AutoFiller_Widget = W_Settings.Settings_Events_AutoFill(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_A_Column_A, GUI_Level_ID=2)
    Event_Activity_Correction_Widget = W_Settings.Settings_Events_Activity_Correction(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_E_A_Column_A, GUI_Level_ID=2)

    if User_Type == "Manager":
        # ---------- Managed Team ---------- #
        Frame_Tab_Team_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Team, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

        Managed_Team_Widget = W_Settings.Settings_My_Team(Settings=Settings, Configuration=Configuration, Frame=Frame_Tab_Team_Column_A, GUI_Level_ID=2)
    else:
        pass
    
    # Build look of Widget
    Frame_Settings_State_Area.pack(side="top", fill="x", expand=False, padx=10, pady=10)

    Button_Download_Pro_Act.grid(row=0, column=0, padx=5, pady=15, sticky="e")
    Button_Upload_Pro_Act.grid(row=0, column=1, padx=5, pady=15, sticky="e")
    Button_Save_Settings.grid(row=0, column=2, padx=5, pady=15, sticky="e")
    Button_Load_Settings.grid(row=0, column=3, padx=5, pady=15, sticky="e")

    TabView.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    Frame_Tab_Gen_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Gen_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Gen_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Theme_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Color_Palette_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Program_User_Type_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_Dat_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Dat_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Dat_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Sharepoint_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Exchange_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Formats_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_Cal_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Cal_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_Cal_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Calendar_Working_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Calendar_Vacation_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Calendar_Start_End_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_E_G_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_G_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_G_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Event_Skip_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Join_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Split_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Parallel_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Frame_Tab_E_Spec_Column_A.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_Spec_Column_B.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Frame_Tab_E_Spec_Column_C.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    Event_Lunch_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Vacation_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_SickDay_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_HomeOffice_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    Event_Private_Widget.pack(side="top", fill="none", expand=False, padx=5, pady=5)

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
