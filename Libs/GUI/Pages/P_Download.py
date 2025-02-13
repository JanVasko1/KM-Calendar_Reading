# Import Libraries
from datetime import datetime

from customtkinter import CTk, CTkFrame, StringVar, CTkEntry, CTkOptionMenu, CTkProgressBar, CTkLabel
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Widgets.W_Download as W_Download
import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists
import Libs.Process as Process

def Page_Download(Settings: dict, Configuration: dict, window: CTk, Frame: CTk|CTkFrame):
    User_Type = Settings["General"]["User"]["User_Type"]
    Date_format = Settings["General"]["Formats"]["Date"]

    Today = datetime.now()
    Today_str = Today.strftime(Date_format)
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Creation_Date"], Information=Today_str)
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Data_Period"], Information="Current")
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
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
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Creation_Date"], Information=Today_str)
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Data_Period"], Information="Past")
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "DashBoard", "Data_Source"], Information=Download_Date_Range_Source)
        else:
            pass


    def My_Team_Download_Data(My_Team_Sharepoint_Widget: CTkFrame) -> None:
        Can_Download = True

        # Sharepoint
        SP_Password = My_Team_Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"].get()

        # Check filled password
        if SP_Password == "":
            Can_Download = False
            CTkMessagebox(title="Error", message="You forgot to insert Sharepoint password.", icon="cancel", fade_in_duration=1)
        else:
            pass

        # -------------- Download  -------------- #
        if Can_Download == True:
            Process.My_Team_Download_and_Process(Settings=Settings, window=window, Progress_Bar=Progress_Bar, Progress_text=Progress_text, SP_Password=SP_Password)

            # Save into Settings --> to be displayed on Dashboard later 
            Defaults_Lists.Save_Value(Settings=Settings, Configuration=None, Variable=None, File_Name="Settings", JSON_path=["General", "DashBoard", "My_Team", "Creation_Date"], Information=Today_str)
        else:
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

    Sharepoint_Widget = W_Download.Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Date_Range_Source=Download_Date_Range_Source)
    Sharepoint_Usage_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Sharepoint_Date_From_Option_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe4"].children["!ctkframe3"].children["!ctkoptionmenu"]
    Sharepoint_Date_To_Option_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe5"].children["!ctkframe3"].children["!ctkoptionmenu"]
    Sharepoint_Man_Date_To_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe6"].children["!ctkframe3"].children["!ctkentry"]
    Sharepoint_Password_Var = Sharepoint_Widget.children["!ctkframe2"].children["!ctkframe7"].children["!ctkframe3"].children["!ctkentry"]
    
    Manual_Widget = W_Download.Download_Manual(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Date_Range_Source=Download_Date_Range_Source)
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

    Exchange_Widget = W_Download.Download_Exchange(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Data_Source=Download_Data_Source)
    Exchange_Usage_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe"].children["!ctkframe3"].children["!ctkradiobutton"]
    Exchange_Password_Var = Exchange_Widget.children["!ctkframe2"].children["!ctkframe3"].children["!ctkframe3"].children["!ctkentry"]

    Outlook_Widget = W_Download.Download_Outlook(Settings=Settings, Configuration=Configuration, Frame=Tab_New, Download_Data_Source=Download_Data_Source)
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

    Previous_Period_Def_Widget = W_Download.Per_Period_Selection(Settings=Settings, Configuration=Configuration, Frame=Tab_Pre)

    Pre_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Pre, Label_Size="H1", Font_Size="H1")
    Pre_Sharepoint_Text.configure(text="Step 2 - Sharepoint credential")

    Previous_Sharepoint_Widget = W_Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_Pre)

    # Download button
    Pre_Download_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Pre, Label_Size="H1", Font_Size="H1")
    Pre_Download_Text.configure(text="Step 2 - Download and process")

    Pre_Button_Download = Elements.Get_Button(Configuration=Configuration, Frame=Tab_Pre, Button_Size="Normal")
    Pre_Button_Download.configure(text="Download", command = lambda:Pre_Download_Data(Previous_Period_Def_Widget=Previous_Period_Def_Widget, Previous_Sharepoint_Widget=Previous_Sharepoint_Widget))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Pre_Button_Download, message="Initiate Download, then check Dashboard.", ToolTip_Size="Normal")
    
    # ---------- Previous periods ---------- #
    if User_Type == "Manager":
        Team_Sharepoint_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Team, Label_Size="H1", Font_Size="H1")
        Team_Sharepoint_Text.configure(text="Step 1 - Sharepoint credential")

        My_Team_Sharepoint_Widget = W_Download.Pre_Download_Sharepoint(Settings=Settings, Configuration=Configuration, Frame=Tab_Team) # Can most probably by identical as downloads needs to connect same ways as in Pre

        # Download button
        Team_Download_Text = Elements.Get_Label(Configuration=Configuration, Frame=Tab_Team, Label_Size="H1", Font_Size="H1")
        Team_Download_Text.configure(text="Step 2 - Download and process")

        Team_Button_Download = Elements.Get_Button(Configuration=Configuration, Frame=Tab_Team, Button_Size="Normal")
        Team_Button_Download.configure(text="Download", command = lambda:My_Team_Download_Data(My_Team_Sharepoint_Widget=My_Team_Sharepoint_Widget))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Team_Button_Download, message="Initiate Download, then check My Team Dashboard.", ToolTip_Size="Normal")
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
    