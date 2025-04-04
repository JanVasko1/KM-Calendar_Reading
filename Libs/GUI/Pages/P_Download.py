# Import Libraries
from datetime import datetime
import threading

from customtkinter import CTk, CTkFrame, StringVar, CTkEntry, CTkProgressBar, CTkLabel

import Libs.GUI.Widgets.W_Download as W_Download
import Libs.GUI.Elements as Elements
from Libs.GUI.Widgets.Widgets_Class import WidgetFrame, WidgetTableFrame, WidgetRow_CheckBox, WidgetRow_RadioButton, WidgetRow_Input_Entry, WidgetRow_Double_Input_Entry, WidgetRow_OptionMenu, Widget_Section_Row, WidgetRow_Color_Picker, Widget_Buttons_Row, WidgetRow_Date_Picker
import Libs.Process as Process

import Libs.Data_Functions as Data_Functions

def Page_Download(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["0"]["General"]["User"]["User_Type"]
    Date_format = Settings["0"]["General"]["Formats"]["Date"]

    # Default
    Download_Date_Range_Source = StringVar(master=Frame, value="Sharepoint", name="Download_Date_Range_Source")
    Download_Data_Source = StringVar(master=Frame, value="Exchange", name="Download_Data_Source")


    Today = datetime.now()
    Today_str = Today.strftime(Date_format)
    # ------------------------- Local Functions -------------------------#
    def Download_Data(Progress_Bar: CTkProgressBar, Progress_text: CTkLabel, Download_Date_Range_Source: StringVar, Download_Data_Source: StringVar, Sharepoint_Widget: WidgetFrame, Manual_Widget: WidgetFrame, Exchange_Widget: WidgetFrame):
        Format_Date = Settings["0"]["General"]["Formats"]["Date"]
        Can_Download = True

        # -------------- Actual Values  -------------- #
        Download_Date_Range_Source = Download_Date_Range_Source.get()
        Download_Data_Source = Download_Data_Source.get()

        # Sharepoint
        SP_Date_From_Method = Sharepoint_Widget.Body_Frame.children["!ctkframe3"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        SP_Date_To_Method = Sharepoint_Widget.Body_Frame.children["!ctkframe5"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        SP_Man_Date_To = Sharepoint_Widget.Body_Frame.children["!ctkframe4"].children["!ctkframe3"].children["!ctkentry"].get()
        SP_Password = Sharepoint_Widget.Body_Frame.children["!ctkframe6"].children["!ctkframe3"].children["!ctkentry"].get()

        # Manual
        Input_Start_Date = Manual_Widget.Body_Frame.children["!ctkframe"].children["!ctkframe3"].children["!ctkentry"].get()
        Input_End_Date = Manual_Widget.Body_Frame.children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()
        Input_Start_Date = Input_Start_Date.upper()
        Input_End_Date = Input_End_Date.upper()
        
        # Exchange
        Exchange_Password = Exchange_Widget.Body_Frame.children["!ctkframe2"].children["!ctkframe3"].children["!ctkentry"].get()

        # -------------- Missing Data handler  -------------- #
        # Date Range Source
        if Download_Date_Range_Source == "Sharepoint":
            if SP_Password == "":
                Can_Download = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                Input_Start_Date = None
                Input_End_Date = None

        elif Download_Date_Range_Source == "Manual":
            SP_Password = None
            try:
                datetime.strptime(Input_Start_Date, Format_Date)
                datetime.strptime(Input_End_Date, Format_Date)
            except:
                Can_Download = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Date format is not supported date format, should be {Format_Date}", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            Can_Download = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Download Date Range Source: {Download_Date_Range_Source} is not supported. Must be Sharepoint/Manual", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        # Data source
        if Can_Download == True:
            if Download_Data_Source == "Exchange":
                if Exchange_Password == "":
                    Can_Download = False
                    Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You forgot to insert Exchange password.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
                else:
                    pass
            elif Download_Data_Source == "Outlook_Client":
                Exchange_Password = None
            else:
                Can_Download = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Download Data Source: {Download_Data_Source} is not supported. Must be Exchange/Outlook_Client", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        # -------------- Download  -------------- #
        if Can_Download == True:
            task_thread = threading.Thread(target=Process.Download_and_Process, args=(Settings, Configuration, window, Progress_Bar, Progress_text, Download_Date_Range_Source, Download_Data_Source, SP_Date_From_Method, SP_Date_To_Method, SP_Man_Date_To, SP_Password, Exchange_Password, Input_Start_Date, Input_End_Date))
            task_thread.start()

            # Save into Settings --> to be displayed on Dashboard later 
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Creation_Date"], Information=Today_str)
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Data_Period"], Information="Current")
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
        else:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Not possible to download and process data", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

    def Pre_Download_Data(Previous_Period_Def_Widget: WidgetFrame, Previous_Sharepoint_Widget: WidgetFrame) -> None:
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
        SP_Password = Previous_Sharepoint_Widget.Body_Frame.children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

        # History Period definition and checks
        From_Month = Previous_Period_Def_Widget.Body_Frame.children["!ctkframe"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        From_Year = Previous_Period_Def_Widget.Body_Frame.children["!ctkframe2"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        From_DateTime =datetime(year=From_Year, month=From_Month, day=1)
        To_Month = Previous_Period_Def_Widget.Body_Frame.children["!ctkframe3"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        To_Year = Previous_Period_Def_Widget.Body_Frame.children["!ctkframe4"].children["!ctkframe3"].children["!ctkoptionmenu"].get()
        To_DateTime =datetime(year=To_Year, month=To_Month, day=1)

        # Check filled password
        if Download_Date_Range_Source == "Sharepoint":
            if SP_Password == "":
                Can_Download = False
                Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
            else:
                pass

        if From_DateTime <= To_DateTime:
            Download_Periods = get_year_month_list(start_date=From_DateTime, end_date=To_DateTime)
        else:
            Can_Download = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message=f"Cannot download as From Period is sooner To Period, please check.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)

        # -------------- Download  -------------- #
        if Can_Download == True:
            task_thread = threading.Thread(target=Process.Pre_Periods_Download_and_Process, args=(Settings, Configuration, window, Progress_Bar, Progress_text, SP_Password, Download_Periods))
            task_thread.start()

            # Save into Settings --> to be displayed on Dashboard later 
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Creation_Date"], Information=Today_str)
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Data_Period"], Information="Past")
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
        else:
            pass


    def My_Team_Download_Data(My_Team_Sharepoint_Widget: CTkFrame) -> None:
        Can_Download = True

        # Sharepoint
        SP_Password = My_Team_Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

        # Check filled password
        if SP_Password == "":
            Can_Download = False
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            pass

        # -------------- Download  -------------- #
        if Can_Download == True:
            task_thread = threading.Thread(target=Process.My_Team_Download_and_Process, args=(Settings, Configuration, window, Progress_Bar, Progress_text, SP_Password))
            task_thread.start()

            # Save into Settings --> to be displayed on Dashboard later 
            Data_Functions.Save_Value(Settings=Settings, Configuration=None, window=window, Variable=None, File_Name="Settings", JSON_path=["0", "General", "DashBoard", "My_Team", "Creation_Date"], Information=Today_str)
        else:
            pass


    # ------------------------- Main Functions -------------------------#
    # Divide Working Page into 2 parts
    Frame_Download_State_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame, Frame_Size="Work_Area_Status_Line", GUI_Level_ID=1)

    # ------------------------- State Area -------------------------#
    # Progress Bar
    Progress_Bar = Elements.Get_ProgressBar(Configuration=Configuration, Frame=Frame_Download_State_Area, orientation="Horizontal", Progress_Size="Download_Process", GUI_Level_ID=1)
    Progress_Bar.set(value=0)

    Progress_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Download_State_Area, Label_Size="Field_Label", Font_Size="Field_Label")
    Progress_text.configure(text=f"Download progress", width=200)
    
    # ------------------------- Work Area -------------------------#
    # Tab View
    TabView_New = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    Tab_New = TabView_New.add("New")
    TabView_New.set("New")
    Tab_New_ToolTip_But = TabView_New.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_New_ToolTip_But, message="Used to download new data to be registered, or Current Period checking.", ToolTip_Size="Normal", GUI_Level_ID=1)
    
    # ---------- New Download ---------- #
    Frame_Tab_New_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_New, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Frame_Tab_New_Column_B = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_New, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)

    # Download Method
    Method_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Tab_New_Column_A, Label_Size="H1", Font_Size="H1")
    Method_Text.configure(text="Step 1 - Date Range Source")
    Method_Text.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Download_Sharepoint_Widget = W_Download.Download_Sharepoint(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_New_Column_A, Download_Date_Range_Source=Download_Date_Range_Source, GUI_Level_ID=2)
    Download_Manual_Widget = W_Download.Download_Manual(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_New_Column_A, Download_Date_Range_Source=Download_Date_Range_Source, GUI_Level_ID=2)
    Download_Sharepoint_Widget.Show()
    Download_Manual_Widget.Show()

    # Download Source
    Source_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Tab_New_Column_B, Label_Size="H1", Font_Size="H1")
    Source_Text.configure(text="Step 2 - Download Data Source")
    Source_Text.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Download_Exchange_Widget = W_Download.Download_Exchange(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_New_Column_B, Download_Data_Source=Download_Data_Source, GUI_Level_ID=2)
    Download_Exchange_Widget.Show()

    Button_Download = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Tab_New_Column_B, Button_Size="Normal")
    Button_Download.configure(text="Download", command = lambda:Download_Data(Progress_Bar=Progress_Bar, Progress_text=Progress_text, Download_Date_Range_Source=Download_Date_Range_Source, Download_Data_Source=Download_Data_Source, Sharepoint_Widget=Download_Sharepoint_Widget, Manual_Widget=Download_Manual_Widget, Exchange_Widget=Download_Exchange_Widget))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download, message="Initiate Download and Process data.", ToolTip_Size="Normal", GUI_Level_ID=2)
    
    # ---------- Previous periods ---------- #
    TabView_Past = Elements.Get_Tab_View(Configuration=Configuration, Frame=Frame, Tab_size="Normal", GUI_Level_ID=1)
    Tab_Pre = TabView_Past.add("Past")
    TabView_Past.set("Past")
    if User_Type == "Manager":
        Tab_Team = TabView_Past.add("My Team")
        Tab_Team_ToolTip_But = TabView_Past.children["!ctksegmentedbutton"].children["!ctkbutton2"]
        Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Team_ToolTip_But, message="Used to download data from my team wit current reporting period.", ToolTip_Size="Normal", GUI_Level_ID=1)
    else:
        pass
    Tab_Pre_ToolTip_But = TabView_Past.children["!ctksegmentedbutton"].children["!ctkbutton"]
    Elements.Get_ToolTip(Configuration=Configuration, widget=Tab_Pre_ToolTip_But, message="Used to download already registered date in Time Sheets --> download from Sharepoint previous periods.", ToolTip_Size="Normal", GUI_Level_ID=1)


    Frame_Tab_Pre_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Pre, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
    Previous_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Tab_Pre_Column_A, Label_Size="H1", Font_Size="H1")
    Previous_Text.configure(text="Step 1 - Define previous periods")
    Previous_Text.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Previous_Periods_Widget = W_Download.Per_Period_Selection(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Pre_Column_A, GUI_Level_ID=2)
    Previous_Periods_Widget.Show()

    Pre_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Tab_Pre_Column_A, Label_Size="H1", Font_Size="H1")
    Pre_Sharepoint_Text.configure(text="Step 2 - Sharepoint credential")
    Pre_Sharepoint_Text.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    Pre_Sharepoint_Widget = W_Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Pre_Column_A, GUI_Level_ID=2)
    Pre_Sharepoint_Widget.Show()

    Pre_Button_Download = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Tab_Pre_Column_A, Button_Size="Normal")
    Pre_Button_Download.configure(text="Download", command = lambda:Pre_Download_Data(Previous_Period_Def_Widget=Previous_Periods_Widget, Previous_Sharepoint_Widget=Pre_Sharepoint_Widget))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Pre_Button_Download, message="Initiate Download, then check Dashboard.", ToolTip_Size="Normal", GUI_Level_ID=2)
    
    # ---------- My Team ---------- #
    if User_Type == "Manager":
        Frame_Tab_Team_Column_A = Elements.Get_Frame(Configuration=Configuration, Frame=Tab_Team, Frame_Size="Work_Area_Columns", GUI_Level_ID=1)
        Team_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Tab_Team_Column_A, Label_Size="H1", Font_Size="H1")
        Team_Sharepoint_Text.configure(text="Step 1 - Sharepoint credential")
        Team_Sharepoint_Text.pack(side="top", fill="none", expand=False, padx=5, pady=5)

        Team_Sharepoint_Widget = W_Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Tab_Team_Column_A, GUI_Level_ID=2) # Can most probably by identical as downloads needs to connect same ways as in Pre
        Team_Sharepoint_Widget.Show()

        Team_Button_Download = Elements.Get_Button_Text(Configuration=Configuration, Frame=Frame_Tab_Team_Column_A, Button_Size="Normal")
        Team_Button_Download.configure(text="Download", command = lambda:My_Team_Download_Data(My_Team_Sharepoint_Widget=Team_Sharepoint_Widget))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Team_Button_Download, message="Initiate Download, then check My Team Dashboard.", ToolTip_Size="Normal", GUI_Level_ID=2)
    else:
        pass

    # Build look of Widget
    Frame_Download_State_Area.pack(side="top", fill="x", expand=False, padx=10, pady=10)

    Progress_text.pack(side="left", fill="none", expand=False, padx=5, pady=10)
    Progress_Bar.pack(side="left", fill="none", expand=False, padx=5, pady=10)

    TabView_New.pack(side="left", fill="y", expand=False, padx=10, pady=10)
    Frame_Tab_New_Column_A.pack(side="left", fill="y", expand=False, padx=5, pady=5)
    Frame_Tab_New_Column_B.pack(side="left", fill="y", expand=False, padx=5, pady=5)
    
    Button_Download.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    
    TabView_Past.pack(side="left", fill="y", expand=False, padx=10, pady=10)
    Frame_Tab_Pre_Column_A.pack(side="left", fill="y", expand=False, padx=5, pady=5)
    Pre_Button_Download.pack(side="top", fill="none", expand=False, padx=5, pady=5)

    if User_Type == "Manager":
        Frame_Tab_Team_Column_A.pack(side="left", fill="y", expand=False, padx=5, pady=5)
        Team_Button_Download.pack(side="top", fill="none", expand=False, padx=5, pady=5)
    else:
        pass

    
    