# Import Libraries
import os
import json
from glob import glob

import pywinstyles
from customtkinter import CTk, CTkFrame, CTkButton, IntVar, set_appearance_mode
from Libs.GUI.CTk.ctk_scrollable_dropdown import CTkScrollableDropdown as CTkScrollableDropdown 
from tkhtmlview import HTMLLabel
from markdown import markdown

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.CustomTkinter_Functions as CustomTkinter_Functions
import Libs.Defaults_Lists as Defaults_Lists
import Libs.File_Manipulation as File_Manipulation

import Libs.Data_Functions as Data_Functions
from Libs.Download.Exchange import Exchange_OAuth_Test

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Settings: dict, Configuration: dict, window: CTk|None, Frame: CTkFrame) -> CTkFrame:
    User_Name = Settings["0"]["General"]["User"]["Name"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    User_Email = Settings["0"]["General"]["User"]["Email"]

    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 
        if Current_Theme == "Dark":
            set_appearance_mode(mode_string="light")
        elif Current_Theme == "Light":
            set_appearance_mode(mode_string="dark")
        elif Current_Theme == "System":
            set_appearance_mode(mode_string="dark")
        else:
            set_appearance_mode(mode_string="system")

    def Show_Version_List(Clicked_on: CTkButton) -> None:
        Work_Area_Detail_Font = Configuration["Labels"]["Main"]["text_color"]
        Work_Area_Detail_Background = list(Configuration["Global_Appearance"]["GUI_Level_ID"]["2"]["fg_color"])

        # TopUp Window
        Version_List_Window_geometry = (2000, 800)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Version List", max_width=Version_List_Window_geometry[0], max_height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=False)

         # Get Theme --> because of background color
        Current_Theme = CustomTkinter_Functions.Get_Current_Theme() 

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

        # Frame - General
        Frame_Main = Elements_Groups.Get_Widget_Frame(Configuration=Configuration, Frame=Version_List_Window, Name="Version List", Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip="Show software changes.", GUI_Level_ID=1)
        Frame_Main.configure(bg_color = "#000001")
        Frame_Body = Frame_Main.children["!ctkframe2"]

        Frame_Information_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame_Body, Frame_Size="Double_size", GUI_Level_ID=2)

        with open(Data_Functions.Absolute_path(relative_path=f"Libs\\App\\Version_list.md"), "r", encoding="UTF-8") as file:
            html_markdown=markdown(text=file.read())
        file.close()

        Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=html_markdown, background=HTML_Background_Color, font=("Roboto", 11), fg=HTML_Font_Color,)

        # Build look of Widget
        Frame_Main.pack(side="top", fill="y", expand=False, padx=10, pady=10)
        Frame_Information_Scrollable_Area.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        Information_html.pack(side="top", fill="both", expand=False, padx=10, pady=10)

    def Download_Project_Activities():
        SP_Password = CustomTkinter_Functions.Dialog_Window_Request(Configuration=Configuration, title="Sharepoint Login", text="Write your password", Dialog_Type="Password")
        
        if SP_Password == None:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            import Libs.Sharepoint.Sharepoint as Sharepoint
            Sharepoint.Get_Project_and_Activity(Settings=Settings, Configuration=Configuration, window=window, SP_Password=SP_Password)
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Project and Activity downloaded from Sharepoint.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Upload_Project_Activities():
        Exchange_Password = CustomTkinter_Functions.Dialog_Window_Request(Configuration=Configuration, title="Exchange Login", text="Write your password", Dialog_Type="Password")
        
        if Exchange_Password == None:
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Error", message="Cannot download, because of missing Password", icon="cancel", fade_in_duration=1, GUI_Level_ID=1)
        else:
            import Libs.Download.Exchange as Exchange
            Exchange.Push_Project(Settings=Settings, Configuration=Configuration, window=window, Exchange_Password=Exchange_Password)
            Exchange.Push_Activity(Settings=Settings, Configuration=Configuration, window=window, Exchange_Password=Exchange_Password)
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Project and Activity uploaded to Exchange. Give MS time to upload changes and restart Outlook.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Save_Settings():
        # Export Settings into Downloads Folder - backup
        Export_dict = {
            "Type": "Settings",
            "Data": Settings["0"]}
        Save_Path = File_Manipulation.Get_Downloads_File_Path(File_Name="TimeSheets_Settings", File_postfix="json")
        with open(file=Save_Path, mode="w") as file: 
            json.dump(Export_dict, file)
        Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Your settings file has been exported to your downloads folder.", icon="check", fade_in_duration=1, GUI_Level_ID=1)

    def Load_Settings(Button_Load_Settings: CTkButton):
        def drop_func(file):
            Data_Functions.Import_Data(Settings=Settings, Configuration=Configuration, window=window, import_file_path=file, Import_Type="Settings", JSON_path=["0"], Method="Overwrite")
            Import_window.destroy()
            Elements.Get_MessageBox(Configuration=Configuration, window=window, title="Success", message="Your settings file has been imported. You can close Window and restart app.", icon="check", fade_in_duration=1, GUI_Level_ID=1)
        
        Import_window_geometry = (200, 200)
        Top_middle_point = CustomTkinter_Functions.Count_coordinate_for_new_window(Clicked_on=Button_Load_Settings, New_Window_width=Import_window_geometry[0])
        Import_window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration, title="Drop file", max_width=Import_window_geometry[0], max_height=Import_window_geometry[1], Top_middle_point=Top_middle_point, Fixed=False, Always_on_Top=True)

        Frame_Body = Elements.Get_Frame(Configuration=Configuration, Frame=Import_window, Frame_Size="Import_Drop", GUI_Level_ID=2)
        Frame_Body.configure(bg_color = "#000001")
        pywinstyles.apply_dnd(widget=Frame_Body, func=drop_func)
        Frame_Body.pack(side="top", padx=15, pady=15)

        Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame_Body, Icon_Name="circle-fading-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
        Icon_Theme.configure(text="")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Drop file here.", ToolTip_Size="Normal", GUI_Level_ID=2)

        Icon_Theme.pack(side="top", padx=50, pady=50)
        

    # ------------------------- Main Functions -------------------------#
    # Authorization OAuth2 Flag
    try:
        Auth_Result = Exchange_OAuth_Test()
    except:
        Auth_Result = False
    Auth_Result_Variable = IntVar(master=Frame, value=Auth_Result, name="Auth_Result_Variable")
    Authorization_Frame = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Frame, Var_Value=True) 
    Authorization_Frame.configure(width=2, height=2, radiobutton_width=10, radiobutton_height=10, border_width_unchecked=2, border_width_checked=2, fg_color="#517A31", text="", state="disabled", variable=Auth_Result_Variable)
    Elements.Get_ToolTip(Configuration=Configuration, widget=Authorization_Frame, message="Authorization status.", ToolTip_Size="Normal", GUI_Level_ID=0)
    
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Version list
    Icon_Versions = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="file-stack", Icon_Size="Header", Button_Size="Picture_Transparent")
    Icon_Versions.configure(command = lambda: Show_Version_List(Clicked_on=Icon_Versions))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Versions, message="Show version changes log.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Account Mail
    Frame_User_Email = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Email.configure(text=User_Email)

    # Account ID
    Frame_User_ID = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_ID.configure(text=User_ID)
    Frame_User_ID.pack_propagate(flag=False)

    # Account Name
    Frame_User_Name = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Name.configure(text=User_Name)

    # Account Mail
    Frame_User_Email = Elements.Get_Label(Configuration=Configuration, Frame=Frame, Label_Size="Column_Header", Font_Size="Column_Header")
    Frame_User_Email.configure(text=User_Email)

    # Button - Download New Project and Activities
    Button_Download_Pro_Act = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="list-plus", Icon_Size="Header", Button_Size="Picture_Transparent")
    Button_Download_Pro_Act.configure(text="")
    Button_Download_Pro_Act.configure(command = lambda: Download_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Download_Pro_Act, message="Actualize the list of Projects and Activities inside the app from actual Sharepoint.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Upload New Project and Activities
    Button_Upload_Pro_Act = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="server", Icon_Size="Header", Button_Size="Picture_Transparent")
    Button_Upload_Pro_Act.configure(text="")
    Button_Upload_Pro_Act.configure(command = lambda: Upload_Project_Activities())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Upload_Pro_Act, message="Upload the list of Projects and Activities into Exchange.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Save Settings
    Button_Save_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="cloud-upload", Icon_Size="Header", Button_Size="Picture_Transparent")
    Button_Save_Settings.configure(text="")
    Button_Save_Settings.configure(command = lambda: Save_Settings())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Save_Settings, message="Save whole setup into Downloads.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Button - Load Settings
    Button_Load_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="cloud-download", Icon_Size="Header", Button_Size="Picture_Transparent")
    Button_Load_Settings.configure(text="")
    Button_Load_Settings.configure(command = lambda: Load_Settings(Button_Load_Settings=Button_Load_Settings))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Load_Settings, message="Load Settings files.", ToolTip_Size="Normal", GUI_Level_ID=0)


    # Build look of Widget
    Authorization_Frame.pack(side="right", fill="none", expand=False, padx=(0, 5), pady=(0, 40))
    Icon_Theme.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Email.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

    Button_Download_Pro_Act.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Button_Upload_Pro_Act.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Button_Save_Settings.pack(side="left", fill="none", expand=False, padx=5, pady=5)
    Button_Load_Settings.pack(side="left", fill="none", expand=False, padx=5, pady=5)