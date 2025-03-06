# Import Libraries
import time

from customtkinter import CTk, CTkFrame

import Libs.Defaults_Lists as Defaults_Lists

import Libs.GUI.Elements as Elements

def Get_Side_Bar(Settings: dict, Configuration: dict, window: CTk, Frame_Work_Area_Main: CTkFrame, Side_Bar_Frame: CTkFrame) -> None:
    User_Type = Settings["0"]["General"]["User"]["User_Type"]
    Application = Defaults_Lists.Load_Application()
    Program_Version = Application["Application"]["Version"]
    Initial_Page = Configuration["Global_Appearance"]["Window"]["Init_Page"]["Selected"]

    if User_Type == "User":
        Side_Bar_Icon_top_pady = 290
        Side_Bar_Icon_Bottom_pady = 260
    elif User_Type == "Manager":
        Side_Bar_Icon_top_pady = 250
        Side_Bar_Icon_Bottom_pady = 240

    Icon_Default_pady = 10

    # ------------------------- Local Functions -------------------------#
    def Clear_Frame(Pre_Working_Frame:CTk|CTkFrame) -> None:
        # Find
        for widget in Pre_Working_Frame.winfo_children():
            widget.destroy()
            window.update_idletasks()

    def Show_Download_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Download as P_Download
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        P_Download.Page_Download(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_DashBoard as P_DashBoard
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_DashBoard.Page_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Team_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_My_Team as P_My_Team
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_My_Team.Page_User_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Data_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Data as P_Data
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Data.Page_Data(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Information as P_Information
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Information.Page_Information(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Settings as P_Settings
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Main)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Main)
        window.update_idletasks()

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Logo
    Logo = Elements.Get_Custom_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=40)

    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="download", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    if User_Type == "User":
        Download_Row = 0
    elif User_Type == "Manager":
        Download_Row = 0
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=Download_Row))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Download new data.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="layout-dashboard", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    if User_Type == "User":
        Dashboard_Row = 1
    elif User_Type == "Manager":
        Dashboard_Row = 1
    Icon_Frame_Dashboard.configure(command = lambda: Show_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Dashboard_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Dashboard, message="My dashboard page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Users Dashboard
    if User_Type == "User":
        pass
    elif User_Type == "Manager":
        Team_Row = 2
        Icon_Frame_Users_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="users", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
        Icon_Frame_Users_Dashboard.configure(command = lambda: Show_Team_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Team_Row))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Users_Dashboard, message="My Team page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Data
    Icon_Frame_Data = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-spreadsheet", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    if User_Type == "User":
        Data_Row = 2
    elif User_Type == "Manager":
        Data_Row = 3
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page(Active_Window = Active_Window, Side_Bar_Row=Data_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Data, message="Data to export page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    if User_Type == "User":
        Information_Row = 3
    elif User_Type == "Manager":
        Information_Row = 4
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=Information_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Information, message="Application information page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_Transparent")
    if User_Type == "User":
        Settings_Row = 4
    elif User_Type == "Manager":
        Settings_Row = 5
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=Settings_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_Transparent")
    Icon_Frame_Close.configure(command = lambda: window.quit())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Close, message="Close application.", ToolTip_Size="Normal")

    # Program Version
    Program_Version_text = Elements.Get_Label(Configuration=Configuration, Frame=Side_Bar_Frame, Label_Size="Field_Label", Font_Size="Field_Label")
    Program_Version_text.configure(text=f"{Program_Version}")


    # Build look of Widget
    Logo.grid(row=0, column=0, padx=(0, 0), pady=(10, 0), sticky="n", columnspan=2)
    Active_Window.grid(row=1, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
    if User_Type == "User":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=5, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Program_Version_text.grid(row=6, column=0, padx=(0, 0), pady=(0, 10), sticky="s", columnspan=2)
    elif User_Type == "Manager":
        Icon_Frame_Download.grid(row=0, column=1, padx=(0, 0), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="w")
        Icon_Frame_Dashboard.grid(row=1, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Users_Dashboard.grid(row=2, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Data.grid(row=3, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Information.grid(row=4, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Settings.grid(row=5, column=1, padx=(0, 10), pady=Icon_Default_pady, sticky="w")
        Icon_Frame_Close.grid(row=6, column=1, padx=(0, 10), pady=(Icon_Default_pady, Side_Bar_Icon_Bottom_pady), sticky="w")
        Program_Version_text.grid(row=7, column=0, padx=(0, 0), pady=(0, 10), sticky="s", columnspan=2)

    # Initiate default window
    if Initial_Page == "Downloads":
        Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=Download_Row)
    elif Initial_Page == "Dashboard":
        Show_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Dashboard_Row)
    elif Initial_Page == "My Team":
        Show_Team_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Team_Row)
    elif Initial_Page == "Data":
        Show_Data_Page(Active_Window = Active_Window, Side_Bar_Row=Data_Row)
    elif Initial_Page == "Settings":
        Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=Settings_Row)