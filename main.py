# BUG --> Outlook Client
# TODO --> Forecast according Calendar only when Start / End date is missing in CAlendar
# TODO --> Show project list and Activity list somewhere

# Import Libraries
import os

from customtkinter import CTk, set_appearance_mode, deactivate_automatic_dpi_awareness
import pywinstyles

import Libs.GUI.Elements as Elements

import Libs.Defaults_Lists as Defaults_Lists
import Libs.Data_Functions as Data_Functions

# -------------------------------------------------------------------------------------------------------------------------------------------------- Main Program -------------------------------------------------------------------------------------------------------------------------------------------------- #
class Win(CTk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().title("Time Sheets")
        super().iconbitmap(bitmap=Data_Functions.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\TimeSheet.ico"))

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

    Theme_Actual = Configuration["Global_Appearance"]["Window"]["Theme"]
    SideBar_Width = Configuration["Frames"]["Page_Frames"]["SideBar"]["width"]

    # Create folders if do not exists
    try:
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\"))
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\DashBoard\\"))
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\Downloads\\"))
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\My_Team\\"))
        os.mkdir(Data_Functions.Absolute_path(relative_path=f"Operational\\History\\"))
    except:
        pass
    try:
        # Crate authentication file if not exists
        File_Exists = os.path.isfile(path=Data_Functions.Absolute_path(relative_path=f"Libs\\Download\\Authorization.pkl"))
        if File_Exists == True:
            pass
        else:
            Defaults_Lists.Create_Azure_Auth()
    except:
        pass

    window = Win()
    
    # Base Windows style setup --> always keep normal before change
    set_appearance_mode(mode_string=Theme_Actual)
    pywinstyles.apply_style(window=window, style="normal")

    # ---------------------------------- Content ----------------------------------#
    import Libs.GUI.Pages.P_Header as P_Header
    import Libs.GUI.Pages.P_Side_Bar as P_Side_Bar
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

    Frame_Work_Area_Main = Elements.Get_Frame(Configuration=Configuration, Frame=Frame_Work_Area, Frame_Size="Work_Area_Main", GUI_Level_ID=0)
    Frame_Work_Area_Main.pack_propagate(flag=False)
    Frame_Work_Area_Main.pack(side="left", fill="none", expand=False)

    P_Header.Get_Header(Settings=Settings, Configuration=Configuration, Frame=Frame_Header)
    P_Side_Bar.Get_Side_Bar(Settings=Settings, Configuration=Configuration, window=window, Frame_Work_Area_Main=Frame_Work_Area_Main, Side_Bar_Frame=Frame_Side_Bar)

    # run
    window.mainloop()