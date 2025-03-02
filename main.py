# BUG --> Outlook Client
# BUG --> flickering cause slow program and some times also non updating the not updating the 
# BUG --> Tool Tip for Import Windows is not on Top
# TODO --> Forecast according Calendar only when Start / End date is missing in CAlendar
# TODO --> Show project list and Activity list somewhere
# TODO --> Element_Goutp for labeled area (like in NAV)

# Import Libraries
import os
import time
from  markdown import markdown

from customtkinter import CTk, CTkFrame, CTkButton, set_appearance_mode, deactivate_automatic_dpi_awareness
from tkhtmlview import HTMLLabel
import pywinstyles

import Libs.GUI.Elements as Elements
import Libs.GUI.Elements_Groups as Elements_Groups
import Libs.Defaults_Lists as Defaults_Lists

# ------------------------------------------------------------------------------------------------------------------------------------ Header ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Header(Frame: CTk|CTkFrame) -> CTkFrame:
    User_Name = Settings["0"]["General"]["User"]["Name"]
    User_ID = Settings["0"]["General"]["User"]["Code"]
    User_Email = Settings["0"]["General"]["User"]["Email"]

    # ------------------------- Local Functions -------------------------#
    def Theme_Change():
        Current_Theme = Defaults_Lists.Get_Current_Theme() 
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
        Top_middle_point = Defaults_Lists.Count_coordinate_for_new_window(Clicked_on=Clicked_on, New_Window_width=Version_List_Window_geometry[0])
        Version_List_Window = Elements_Groups.Get_Pop_up_window(Configuration=Configuration ,title="Version List", width=Version_List_Window_geometry[0], height=Version_List_Window_geometry[1], Top_middle_point=Top_middle_point, Fixed=True, Always_on_Top=False)

         # Get Theme --> because of background color
        Current_Theme = Defaults_Lists.Get_Current_Theme() 

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

        with open(Defaults_Lists.Absolute_path(relative_path=f"Libs\\App\\Version_list.md"), "r", encoding="UTF-8") as file:
            html_markdown=markdown(text=file.read())
        file.close()

        Information_html = HTMLLabel(Frame_Information_Scrollable_Area, html=html_markdown, background=HTML_Background_Color, font=("Roboto", 11), fg=HTML_Font_Color,)

        # Build look of Widget
        Frame_Main.pack(side="top", fill="y", expand=False, padx=10, pady=10)
        Frame_Information_Scrollable_Area.pack(side="top", fill="none", expand=False, padx=10, pady=10)
        Information_html.pack(side="top", fill="both", expand=False, padx=10, pady=10)

    # ------------------------- Main Functions -------------------------#
    # Theme Change - Button
    Icon_Theme = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="sun-moon", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Theme.configure(text="")
    Icon_Theme.configure(command = lambda: Theme_Change())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Theme, message="Change theme.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Version list
    Icon_Versions = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Frame, Icon_Name="file-stack", Icon_Size="Header", Button_Size="Picture_Theme")
    Icon_Versions.configure(command = lambda: Show_Version_List(Clicked_on=Icon_Versions))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Versions, message="Show version changes log.", ToolTip_Size="Normal", GUI_Level_ID=0)

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
    Icon_Versions.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Email.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_ID.pack(side="right", fill="none", expand=False, padx=5, pady=5)
    Frame_User_Name.pack(side="right", fill="none", expand=False, padx=5, pady=5)

# ------------------------------------------------------------------------------------------------------------------------------------ Side Bar ------------------------------------------------------------------------------------------------------------------------------------ #
def Get_Side_Bar(Side_Bar_Frame: CTk|CTkFrame) -> CTkFrame:
    User_Type = Settings["0"]["General"]["User"]["User_Type"]
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
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=(Side_Bar_Icon_top_pady, Icon_Default_pady), sticky="e")
        time.sleep(0.1)
        P_Download.Page_Download(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_DashBoard as P_DashBoard
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_DashBoard.Page_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Team_Dashboard_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_My_Team as P_My_Team
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_My_Team.Page_User_Dashboard(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Data_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Data as P_Data
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Data.Page_Data(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Information_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Information as P_Information
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Information.Page_Information(Settings=Settings, Configuration=Configuration, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    def Show_Settings_Page(Active_Window: CTkFrame, Side_Bar_Row: int) -> None:
        import Libs.GUI.Pages.P_Settings as P_Settings
        Clear_Frame(Pre_Working_Frame=Frame_Work_Area_Detail)
        Active_Window.grid(row=Side_Bar_Row, column=0, padx=(10, 2), pady=Icon_Default_pady, sticky="e")
        time.sleep(0.1)
        P_Settings.Page_Settings(Settings=Settings, Configuration=Configuration, window=window, Frame=Frame_Work_Area_Detail)
        window.update_idletasks()

    # ------------------------- Main Functions -------------------------#
    Active_Window = Elements.Get_Frame(Configuration=Configuration, Frame=Side_Bar_Frame, Frame_Size="SideBar_active")

    # Logo
    Logo = Elements.Get_Custom_Image(Configuration=Configuration, Frame=Side_Bar_Frame, Image_Name="Company", postfix="png", width=70, heigh=40)

    # Page - Download
    Icon_Frame_Download = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="download", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Download_Row = 0
    elif User_Type == "Manager":
        Download_Row = 0
    Icon_Frame_Download.configure(command = lambda: Show_Download_Page(Active_Window = Active_Window, Side_Bar_Row=Download_Row))    
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Download, message="Download new data.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Dashboard
    Icon_Frame_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="layout-dashboard", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
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
        Icon_Frame_Users_Dashboard = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="users", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
        Icon_Frame_Users_Dashboard.configure(command = lambda: Show_Team_Dashboard_Page(Active_Window = Active_Window, Side_Bar_Row=Team_Row))
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Users_Dashboard, message="My Team page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Data
    Icon_Frame_Data = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="file-spreadsheet", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Data_Row = 2
    elif User_Type == "Manager":
        Data_Row = 3
    Icon_Frame_Data.configure(command = lambda: Show_Data_Page(Active_Window = Active_Window, Side_Bar_Row=Data_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Data, message="Data to export page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Information
    Icon_Frame_Information = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="info", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Information_Row = 3
    elif User_Type == "Manager":
        Information_Row = 4
    Icon_Frame_Information.configure(command = lambda: Show_Information_Page(Active_Window = Active_Window, Side_Bar_Row=Information_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Information, message="Application information page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Page - Settings
    Icon_Frame_Settings = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="settings", Icon_Size="Side_Bar_regular", Button_Size="Picture_SideBar")
    if User_Type == "User":
        Settings_Row = 4
    elif User_Type == "Manager":
        Settings_Row = 5
    Icon_Frame_Settings.configure(command = lambda: Show_Settings_Page(Active_Window = Active_Window, Side_Bar_Row=Settings_Row))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Frame_Settings, message="Settings page.", ToolTip_Size="Normal", GUI_Level_ID=0)

    # Close Application
    Icon_Frame_Close = Elements.Get_Button_Icon(Configuration=Configuration, Frame=Side_Bar_Frame, Icon_Name="power", Icon_Size="Side_Bar_close", Button_Size="Picture_SideBar")
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


# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheets")
        super().iconbitmap(bitmap=Defaults_Lists.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\TimeSheet.ico"))

        display_width = self.winfo_screenwidth()
        display_height = self.winfo_screenheight()
        Window_Frame_width = 1800
        Window_Frame_height = 900
        left_position = int(display_width // 2 - Window_Frame_width // 2)
        top_position = int(display_height // 2 - Window_Frame_height // 2)
        self.geometry(f"{Window_Frame_width}x{Window_Frame_height}+{left_position}+{top_position}")

        # Rounded corners 
        self.config(background="#000001")
        self.attributes("-transparentcolor", "#000001")

        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>",self.click_win)
        super().bind("<B1-Motion>", self.drag_win)

    def drag_win(self, event):
        # Move only when on Side Bar
        if (self._offsetx < SideBar_Width):
            x = super().winfo_pointerx() - self._offsetx
            y = super().winfo_pointery() - self._offsety
            super().geometry(f"+{x}+{y}")
        else:
            pass

    def click_win(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

if __name__ == "__main__":
    deactivate_automatic_dpi_awareness()
    Application = Defaults_Lists.Load_Application()
    Settings = Defaults_Lists.Load_Settings()
    Configuration = Defaults_Lists.Load_Configuration() 

    Win_Style_Actual = Configuration["Global_Appearance"]["Window"]["Style"]
    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

    # Create folders if do not exists
    try:
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\DashBoard\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\Downloads\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\My_Team\\"))
        os.mkdir(Defaults_Lists.Absolute_path(relative_path=f"Operational\\History\\"))
    except:
        pass

    window = Win()
    
    # Base Windows style setup --> always keep normal before change
    set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")
    pywinstyles.apply_style(window=window, style=Win_Style_Actual)

    # ---------------------------------- Content ----------------------------------#
    # Background
    Frame_Background = Elements.Get_Frame(Configuration=Configuration, Frame=window, Frame_Size="Background", GUI_Level_ID=0)
    Frame_Background.pack(side="top", fill="none", expand=False)

    # SideBar
    Frame_Side_Bar = Elements.Get_SideBar_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="SideBar")
    Frame_Side_Bar.pack(side="left", fill="y", expand=False)

    # Work Area
    Frame_Work_Area = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Background, Frame_Size="Work_Area", GUI_Level_ID=0)
    Frame_Work_Area.pack(side="top", fill="both", expand=False)

    Frame_Header = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Header", GUI_Level_ID=0)
    Frame_Header.pack_propagate(flag=False)
    Frame_Header.pack(side="top", fill="both", expand=False)

    Frame_Work_Area_Detail = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Work_Area_Detail.pack_propagate(flag=False)
    Frame_Work_Area_Detail.pack(side="left", fill="none", expand=False)

    Get_Header(Frame=Frame_Header)
    Get_Side_Bar(Side_Bar_Frame=Frame_Side_Bar)

    # run
    window.mainloop()