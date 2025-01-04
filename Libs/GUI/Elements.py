# Import Libraries
from PIL import Image

from customtkinter import CTkButton, CTk, CTkFrame, CTkScrollableFrame, CTkEntry, CTkLabel, CTkFont, CTkImage, CTkRadioButton, CTkTabview, CTkOptionMenu, CTkCheckBox, CTkProgressBar, CTkInputDialog
from CTkTable import CTkTable
from CTkColorPicker import CTkColorPicker
from CTkToolTip import CTkToolTip

from iconipy import IconFactory 

import Libs.Defaults_Lists as Defaults_Lists

Configuration = Defaults_Lists.Load_Configuration() 
Accent_Color_Style = Configuration["Global_Apperance"]["Window"]["Accent_Color_Mode"]
Accent_Color_Style_Manual = Configuration["Global_Apperance"]["Window"]["Accent_Color_Manual"]

# ---------------------------------------------- Font ----------------------------------------------# 
def Get_Font(Font_Size: str) -> CTkFont:
    Configuration_Font_Text_Main = Configuration["Font"][f"{Font_Size}"]
    Font_Text_Main = CTkFont(
        family = Configuration_Font_Text_Main["family"],
        size = Configuration_Font_Text_Main["size"],
        weight = Configuration_Font_Text_Main["weight"],
        slant = Configuration_Font_Text_Main["slant"],
        underline = Configuration_Font_Text_Main["underline"],
        overstrike = Configuration_Font_Text_Main["overstrike"])
    return Font_Text_Main

# ---------------------------------------------- Text ----------------------------------------------# 
def Get_Label(Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str) -> CTkLabel:
    Configuration_Text_Main = Configuration["Texts"][f"{Label_Size}"]
    Text_Main = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size=Font_Size),
        height = Configuration_Text_Main["height"],
        fg_color = Configuration_Text_Main["fg_color"],
        text_color = tuple(Configuration_Text_Main["text_color"]),
        anchor = Configuration_Text_Main["anchor"],
        padx = Configuration_Text_Main["padx"],
        pady = Configuration_Text_Main["pady"])
    return Text_Main

def Get_Label_Icon(Frame: CTk|CTkFrame, Label_Size: str, Font_Size: str, Icon_Set: str, Icon_Name: str, Icon_Size: str,) -> CTkLabel:
    Frame_Label = Get_Label(Frame=Frame, Label_Size=Label_Size, Font_Size=Font_Size)
    CTK_Image = Get_CTk_Image(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Label.configure(image=CTK_Image, text="", anchor="e")
    return Frame_Label

# ---------------------------------------------- Buttons ----------------------------------------------# 
def Get_Button(Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Button_Normal = CTkButton(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        border_color = tuple(Configuration_Button_Normal["border_color"]),
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = tuple([Accent_Color, Accent_Color]),
        hover = Configuration_Button_Normal["hover"],
        hover_color = tuple([Accent_Color, Accent_Color]),
        anchor = Configuration_Button_Normal["anchor"],
        text_color=tuple(Configuration_Button_Normal["text_color"]))
    return Button_Normal

def Get_Button_Icon(Frame: CTk|CTkFrame, Icon_Set: str, Icon_Name: str, Icon_Size: str, Button_Size: str) -> CTkFrame:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Frame_Button = CTkButton(
        master = Frame,
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = Configuration_Button_Normal["fg_color"],
        hover = Configuration_Button_Normal["hover"],
        hover_color = tuple([Accent_Color, Accent_Color]),
        anchor = Configuration_Button_Normal["anchor"],
        text = "")
    CTK_Image = Get_CTk_Image(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size)
    Frame_Button.configure(image=CTK_Image, text="")
    return Frame_Button

def Get_Button_Chart(Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Frame_Button = CTkButton(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = Configuration_Button_Normal["fg_color"],
        hover = Configuration_Button_Normal["hover"],
        hover_color = tuple([Accent_Color, Accent_Color]),
        anchor = Configuration_Button_Normal["anchor"],
        text_color=tuple(Configuration_Button_Normal["text_color"]))
    return Frame_Button

# ---------------------------------------------- Fields ----------------------------------------------# 
def Get_Entry_Field(Frame: CTk|CTkFrame, Field_Size: str) -> CTkEntry:
    Configuration_Field = Configuration["Fields"]["Entry"][f"{Field_Size}"]
    Field = CTkEntry(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Field["width"],
        height = Configuration_Field["height"],
        corner_radius = Configuration_Field["corner_radius"],
        border_width = Configuration_Field["border_width"],
        border_color = Configuration_Field["border_color"],
        bg_color = Configuration_Field["bg_color"],
        fg_color = tuple(Configuration_Field["fg_color"]),
        text_color = tuple(Configuration_Field["text_color"]),
        placeholder_text_color = tuple(Configuration_Field["placeholder_text_color"]))
    return Field

def Get_Password_Normal(Frame: CTk|CTkFrame) -> CTkEntry:
    Configuration_Password_Normal = Configuration["Fields"]["Entry"]["Normal"]
    Password_Normal = CTkEntry(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Password_Normal["width"],
        height = Configuration_Password_Normal["height"],
        corner_radius = Configuration_Password_Normal["corner_radius"],
        border_width = Configuration_Password_Normal["border_width"],
        border_color = Configuration_Password_Normal["border_color"],
        bg_color = Configuration_Password_Normal["bg_color"],
        fg_color = tuple(Configuration_Password_Normal["fg_color"]),
        text_color = tuple(Configuration_Password_Normal["text_color"]),
        placeholder_text_color = tuple(Configuration_Password_Normal["placeholder_text_color"]),
        show="*")
    return Password_Normal

def Get_RadioButton_Normal(Frame: CTk|CTkFrame) -> CTkRadioButton:
    Configuration_RadioButton_Normal = Configuration["Fields"]["RadioButton"]["Normal"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    RadioButton_Normal = CTkRadioButton(
        master = Frame,
        width = Configuration_RadioButton_Normal["width"],
        height = Configuration_RadioButton_Normal["height"],
        radiobutton_width = Configuration_RadioButton_Normal["radiobutton_width"],
        radiobutton_height = Configuration_RadioButton_Normal["radiobutton_height"],
        corner_radius = Configuration_RadioButton_Normal["corner_radius"],
        border_width_unchecked = Configuration_RadioButton_Normal["border_width_unchecked"],
        border_width_checked = Configuration_RadioButton_Normal["border_width_checked"],
        fg_color = tuple([Accent_Color, Accent_Color]),
        border_color = tuple(Configuration_RadioButton_Normal["border_color"]),
        hover_color = tuple([Accent_Color, Accent_Color]),
        hover = Configuration_RadioButton_Normal["hover"])
    return RadioButton_Normal

def Get_Option_Menu(Frame: CTk|CTkFrame) -> CTkOptionMenu:
    Configuration_Option_Menu = Configuration["Fields"]["OptionMenu"]["Normal"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Option_Menu = CTkOptionMenu(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Option_Menu["width"],
        height = Configuration_Option_Menu["height"],
        corner_radius = Configuration_Option_Menu["corner_radius"],
        bg_color = Configuration_Option_Menu["bg_color"],
        fg_color = tuple(Configuration_Option_Menu["fg_color"]),
        button_color = tuple([Accent_Color, Accent_Color]),
        button_hover_color = tuple([Accent_Color, Accent_Color]),
        text_color = tuple(Configuration_Option_Menu["text_color"]),
        text_color_disabled = tuple(Configuration_Option_Menu["text_color_disabled"]),
        dropdown_fg_color = tuple(Configuration_Option_Menu["dropdown_fg_color"]),
        dropdown_hover_color = tuple([Accent_Color, Accent_Color]),
        dropdown_text_color = tuple(Configuration_Option_Menu["dropdown_text_color"]),
        hover = Configuration_Option_Menu["hover"],
        dynamic_resizing = Configuration_Option_Menu["dynamic_resizing"],
        anchor = Configuration_Option_Menu["anchor"])
    return Option_Menu

def Get_CheckBox(Frame: CTk|CTkFrame) -> CTkCheckBox:
    Configuration_Check_Box = Configuration["Fields"]["CheckBox"]["Normal"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Check_Box = CTkCheckBox(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Check_Box["width"],
        height = Configuration_Check_Box["height"],
        checkbox_width = Configuration_Check_Box["checkbox_width"],
        checkbox_height = Configuration_Check_Box["checkbox_height"],
        corner_radius = Configuration_Check_Box["corner_radius"],
        border_width = Configuration_Check_Box["border_width"],
        border_color = tuple(Configuration_Check_Box["border_color"]),
        bg_color = Configuration_Check_Box["bg_color"],
        fg_color = tuple([Accent_Color, Accent_Color]),
        hover_color = tuple([Accent_Color, Accent_Color]),
        checkmark_color = tuple(Configuration_Check_Box["checkmark_color"]),
        text_color = tuple(Configuration_Check_Box["text_color"]),
        hover = Configuration_Check_Box["hover"])
    return Check_Box


# ---------------------------------------------- Frames ----------------------------------------------# 
# NonScrolable
def Get_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_NonScrollable = Configuration["Frames"]["Page_Frames"][f"{Frame_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    # fg_color - Preparation
    fg_color_json = Configuration_NonScrollable["fg_color"]
    if type(fg_color_json) is list:
        fg_color = tuple(Configuration_NonScrollable["fg_color"])
    else:
        if fg_color_json == "Accent_Color":
            fg_color = Accent_Color
        else:
            fg_color = Configuration_NonScrollable["fg_color"]

    Frame_NonScrolable = CTkFrame(
        master = Frame,
        width = Configuration_NonScrollable["width"],
        height = Configuration_NonScrollable["height"],
        corner_radius = Configuration_NonScrollable["corner_radius"],
        border_width = Configuration_NonScrollable["border_width"],
        border_color = Configuration_NonScrollable["border_color"],
        bg_color = Configuration_NonScrollable["bg_color"],
        fg_color = fg_color)
    return Frame_NonScrolable

def Get_Dashboards_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_Dashboard = Configuration["Frames"]["Dashboard"]["Backbround_Frames"][f"{Frame_Size}"]
    # fg_color - Preparation
    fg_color_json = Configuration_Dashboard["fg_color"]
    if type(fg_color_json) is list:
        fg_color = tuple(Configuration_Dashboard["fg_color"])
    else:
        fg_color = Configuration_Dashboard["fg_color"]

    Frame_NonScrolable = CTkFrame(
        master = Frame,
        width = Configuration_Dashboard["width"],
        height = Configuration_Dashboard["height"],
        corner_radius = Configuration_Dashboard["corner_radius"],
        border_width = Configuration_Dashboard["border_width"],
        border_color = Configuration_Dashboard["border_color"],
        bg_color = Configuration_Dashboard["bg_color"],
        fg_color = fg_color)
    return Frame_NonScrolable

# ------------------------------------------------------------------------------------------------------------ Widgets  ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------ Dashboards Widgets Frames ------------------------------------------#
def Get_Dashboard_Widget_Frame_Body(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Body = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body"]
    Frame_Body = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body["width"],
        height = Configuration_Frame_Dash_Body["height"],
        corner_radius = Configuration_Frame_Dash_Body["corner_radius"],
        border_width = Configuration_Frame_Dash_Body["border_width"],
        border_color = tuple(Configuration_Frame_Dash_Body["border_color"]),
        bg_color = Configuration_Frame_Dash_Body["bg_color"],
        fg_color = tuple(Configuration_Frame_Dash_Body["fg_color"]))
    return Frame_Body

def Get_Dashboard_Widget_Frame_Body_Scrollable(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkScrollableFrame:
    Configuration_Frame_Dash_Body_Scroll = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Body_Scrollable"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Frame_Body_Scroll = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Body_Scroll["width"],
        height = Configuration_Frame_Dash_Body_Scroll["height"],
        corner_radius = Configuration_Frame_Dash_Body_Scroll["corner_radius"],
        border_width = Configuration_Frame_Dash_Body_Scroll["border_width"],
        border_color = tuple(Configuration_Frame_Dash_Body_Scroll["border_color"]),
        bg_color = Configuration_Frame_Dash_Body_Scroll["bg_color"],
        fg_color = tuple(Configuration_Frame_Dash_Body_Scroll["fg_color"]),
        scrollbar_fg_color = Configuration_Frame_Dash_Body_Scroll["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Frame_Dash_Body_Scroll["scrollbar_button_color"]),
        scrollbar_button_hover_color = tuple([Accent_Color, Accent_Color]))
    return Frame_Body_Scroll

def Get_Dashboard_Widget_Frame_Header(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Header = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Header"]
    Frame_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Header["width"],
        height = Configuration_Frame_Dash_Header["height"],
        corner_radius = Configuration_Frame_Dash_Header["corner_radius"],
        border_width = Configuration_Frame_Dash_Header["border_width"],
        bg_color = Configuration_Frame_Dash_Header["bg_color"],
        fg_color = Configuration_Frame_Dash_Header["fg_color"])
    return Frame_Header

def Get_Dashboard_Widget_Frame_Area(Frame: CTk|CTkFrame, Widget_Line: str, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Dash_Data = Configuration["Frames"]["Dashboard"]["Widgets"][f"{Widget_Line}"][f"{Widget_size}"]["Data_Area"]
    Frame_Area = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Dash_Data["width"],
        height = Configuration_Frame_Dash_Data["height"],
        corner_radius = Configuration_Frame_Dash_Data["corner_radius"],
        border_width = Configuration_Frame_Dash_Data["border_width"],
        bg_color = Configuration_Frame_Dash_Data["bg_color"],
        fg_color = Configuration_Frame_Dash_Data["fg_color"])
    return Frame_Area

# ------------------------------------------ Widget Frames ------------------------------------------#
# Scrolable --> Frames For tables
def Get_Widget_Scrolable_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkScrollableFrame:
    Configuration_Scrollable = Configuration["Frames"]["Widgets"]["Widget_Frames"]["Scrollable_Frames"][f"{Frame_Size}"]
    Frame_Scrollable = CTkScrollableFrame(
        master = Frame,
        width = Configuration_Scrollable["width"],
        corner_radius = Configuration_Scrollable["corner_radius"],
        border_width = Configuration_Scrollable["border_width"],
        border_color = tuple(Configuration_Scrollable["border_color"]),
        bg_color = Configuration_Scrollable["bg_color"],
        fg_color = Configuration_Scrollable["bg_color"],
        scrollbar_fg_color = Configuration_Scrollable["scrollbar_fg_color"],
        scrollbar_button_color = tuple(Configuration_Scrollable["scrollbar_button_color"]),
        scrollbar_button_hover_color = tuple(Configuration_Scrollable["scrollbar_button_hover_color"]))
    return Frame_Scrollable

def Get_Widget_Frame_Body(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Body"]
    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column["width"],
        corner_radius = Configuration_Frame_Single_Column["corner_radius"],
        border_width = Configuration_Frame_Single_Column["border_width"],
        border_color = tuple(Configuration_Frame_Single_Column["border_color"]),
        bg_color = Configuration_Frame_Single_Column["bg_color"],
        fg_color = tuple(Configuration_Frame_Single_Column["fg_color"]))
    return Frame_Single_Column

def Get_Widget_Frame_Header(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Header = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Header"]
    Frame_Single_Column_Header = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Header["width"],
        height = Configuration_Frame_Single_Column_Header["height"],
        corner_radius = Configuration_Frame_Single_Column_Header["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Header["border_width"],
        bg_color = Configuration_Frame_Single_Column_Header["bg_color"],
        fg_color = Configuration_Frame_Single_Column_Header["fg_color"])
    return Frame_Single_Column_Header

def Get_Widget_Frame_Area(Frame: CTk|CTkFrame, Widget_size: str) -> CTkFrame:
    Configuration_Frame_Single_Column_Data_Area = Configuration["Frames"]["Widgets"]["Widget_Frames"][f"{Widget_size}"]["Data_Area"]
    Frame_Single_Column = CTkFrame(
        master = Frame,
        width = Configuration_Frame_Single_Column_Data_Area["width"],
        corner_radius = Configuration_Frame_Single_Column_Data_Area["corner_radius"],
        border_width = Configuration_Frame_Single_Column_Data_Area["border_width"],
        bg_color = Configuration_Frame_Single_Column_Data_Area["bg_color"],
        fg_color = Configuration_Frame_Single_Column_Data_Area["fg_color"])
    return Frame_Single_Column

# ------------------------------------------ Widget Field Frames ------------------------------------------#
def Get_Widget_Field_Frame_Area(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Area = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Area"]
    Frame_Field_Single_Area = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Area["width"],
        height = Configuration_Field_Single_Area["height"],
        corner_radius = Configuration_Field_Single_Area["corner_radius"],
        border_width = Configuration_Field_Single_Area["border_width"],
        bg_color = Configuration_Field_Single_Area["bg_color"],
        fg_color = Configuration_Field_Single_Area["fg_color"])
    return Frame_Field_Single_Area

def Get_Widget_Field_Frame_Label(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Label = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Label"]
    Frame_Field_Single_Label = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Label["width"],
        height = Configuration_Field_Single_Label["height"],
        corner_radius = Configuration_Field_Single_Label["corner_radius"],
        border_width = Configuration_Field_Single_Label["border_width"],
        bg_color = Configuration_Field_Single_Label["bg_color"],
        fg_color = Configuration_Field_Single_Label["fg_color"])
    return Frame_Field_Single_Label

def Get_Widget_Field_Frame_Space(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Space = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Space"]
    Frame_Field_Single_Space = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Space["width"],
        height = Configuration_Field_Single_Space["height"],
        corner_radius = Configuration_Field_Single_Space["corner_radius"],
        border_width = Configuration_Field_Single_Space["border_width"],
        bg_color = Configuration_Field_Single_Space["bg_color"],
        fg_color = Configuration_Field_Single_Space["fg_color"])
    return Frame_Field_Single_Space

def Get_Widget_Field_Frame_Value(Frame: CTk|CTkFrame, Field_Frame_Type: str) -> CTkFrame:
    Configuration_Field_Single_Value = Configuration["Frames"]["Widgets"]["Field_Frames"][f"{Field_Frame_Type}"]["Value"]
    Frame_Field_Single_Value = CTkFrame(
        master = Frame,
        width = Configuration_Field_Single_Value["width"],
        height = Configuration_Field_Single_Value["height"],
        corner_radius = Configuration_Field_Single_Value["corner_radius"],
        border_width = Configuration_Field_Single_Value["border_width"],
        bg_color = Configuration_Field_Single_Value["bg_color"],
        fg_color = Configuration_Field_Single_Value["fg_color"])
    return Frame_Field_Single_Value

# ------------------------------------------ Tab View ------------------------------------------ 
def Get_Tab_View(Frame: CTk|CTkFrame, Tab_size: str) -> CTkTabview:
    Configuration_TabView_Normal = Configuration["TabView"][f"{Tab_size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    TabView_Normal = CTkTabview(
        master = Frame,
        width = Configuration_TabView_Normal["width"],
        height = Configuration_TabView_Normal["height"],
        corner_radius = Configuration_TabView_Normal["corner_radius"],
        border_width = Configuration_TabView_Normal["border_width"],
        border_color = tuple(Configuration_TabView_Normal["border_color"]),
        bg_color = Configuration_TabView_Normal["bg_color"],
        segmented_button_fg_color = tuple(Configuration_TabView_Normal["segmented_button_fg_color"]),
        segmented_button_selected_color = tuple([Accent_Color, Accent_Color]),
        segmented_button_selected_hover_color = tuple([Accent_Color, Accent_Color]),
        segmented_button_unselected_color = tuple(Configuration_TabView_Normal["segmented_button_unselected_color"]),
        segmented_button_unselected_hover_color = tuple([Accent_Color, Accent_Color]),
        text_color = tuple(Configuration_TabView_Normal["text_color"]),
        text_color_disabled = tuple(Configuration_TabView_Normal["text_color_disabled"]),
        anchor = Configuration_TabView_Normal["anchor"])
    return TabView_Normal

# ---------------------------------------------- Tables ----------------------------------------------# 
def Get_Table(Frame: CTk|CTkFrame, Table_size: str, rows: int, columns: int) -> CTkTable:
    Configuration_Table_Single = Configuration["Tables"][f"{Table_size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Table_Single = CTkTable(
        master = Frame,
        row = rows,
        column = columns,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Table_Single["width"],
        colors = Configuration_Table_Single["colors"],
        border_width = Configuration_Table_Single["border_width"],
        border_color = tuple(Configuration_Table_Single["border_color"]),
        color_phase = Configuration_Table_Single["color_phase"],
        orientation = Configuration_Table_Single["orientation"],
        header_color = Accent_Color,
        corner_radius = Configuration_Table_Single["corner_radius"],
        hover_color = tuple([Accent_Color, Accent_Color]),
        wraplength = Configuration_Table_Single["wraplength"],
        justify = Configuration_Table_Single["justify"],
        anchor = Configuration_Table_Single["anchor"])
    return Table_Single

# ---------------------------------------------- Icons ----------------------------------------------# 
def Create_Icon(Icon_Set: str, Icon_Name: str, Icon_Size: str, Theme_index: int) -> Image:
    # Theme_Index: 0 --> light, 1 --> dark
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    if Icon_Size == "Side_Bar_active":
        Used_Icon_Color = Accent_Color
    else:
        Used_Icon_Color = Configuration_Icon["font_color"][Theme_index]
    
    Icon_Fact = IconFactory(
        icon_set = Icon_Set,
        icon_size = Configuration_Icon["icon_size"],
        font_size = Configuration_Icon["font_size"],
        font_color = Used_Icon_Color,
        outline_width = Configuration_Icon["outline_width"],
        outline_color = Configuration_Icon["outline_color"][Theme_index],
        background_color = Configuration_Icon["background_color"][Theme_index],
        background_radius = Configuration_Icon["background_radius"])
    Icon_PIL = Icon_Fact.asPil(Icon_Name)
    return Icon_PIL

def Get_CTk_Image(Icon_Set: str, Icon_Name: str, Icon_Size: str) -> CTkImage:
    Configuration_Icon = Configuration["Icons"][f"{Icon_Size}"]
    Icon_Size_px = Configuration_Icon["icon_size"]
    Picture = CTkImage(
        light_image = Create_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=0),
        dark_image =Create_Icon(Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size=Icon_Size, Theme_index=1),
        size = (Icon_Size_px, Icon_Size_px))
    return Picture

# ---------------------------------------------- Progress Bar ----------------------------------------------# 
def Get_ProgressBar(Frame: CTk|CTkFrame, orientation: str, Progress_Size: str) -> CTkProgressBar:
    Configuration_ProgressBar = Configuration["ProgressBar"][f"{orientation}"][f"{Progress_Size}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Progress_Bar = CTkProgressBar(
        master = Frame,
        width = Configuration_ProgressBar["width"],
        height = Configuration_ProgressBar["height"],
        border_width = Configuration_ProgressBar["border_width"],
        border_color = tuple(Configuration_ProgressBar["border_color"]),
        corner_radius = Configuration_ProgressBar["corner_radius"],
        bg_color = Configuration_ProgressBar["bg_color"],
        fg_color = tuple(Configuration_ProgressBar["fg_color"]),
        progress_color = tuple([Accent_Color, Accent_Color]),
        orientation = Configuration_ProgressBar["orientation"],
        determinate_speed = Configuration_ProgressBar["determinate_speed"],
        indeterminate_speed = Configuration_ProgressBar["indeterminate_speed"],
        mode = Configuration_ProgressBar["mode"])
    return Progress_Bar


# ---------------------------------------------- InputDialog ----------------------------------------------# 
def Get_DialogWindow(text: str, title: str, Dialog_Type: str) -> CTkInputDialog:
    Configuration_Dialog = Configuration["InputDialog"][f"{Dialog_Type}"]
    Accent_Color = Defaults_Lists.Get_Accent_Collor(Accent_Color_Style=Accent_Color_Style, Accent_Color_Style_Manual=Accent_Color_Style_Manual)
    Dialog = CTkInputDialog(
        text=text,
        title=title,
        font = Get_Font(Font_Size="Field_Label"),
        fg_color = tuple(Configuration_Dialog["fg_color"]),
        text_color = tuple(Configuration_Dialog["text_color"]),
        button_fg_color = tuple(Configuration_Dialog["button_fg_color"]),
        button_hover_color = tuple([Accent_Color, Accent_Color]),
        button_text_color = tuple(Configuration_Dialog["button_text_color"]),
        entry_fg_color = tuple(Configuration_Dialog["entry_fg_color"]),
        entry_border_color = tuple(Configuration_Dialog["entry_border_color"]),
        entry_text_color = tuple(Configuration_Dialog["entry_text_color"]),
        password = Configuration_Dialog["password"])
    return Dialog

# ---------------------------------------------- ColorPicker ----------------------------------------------# 
def Get_Color_Picker(Frame: CTk|CTkFrame, Accent_Color_Manual_Frame_Var: CTkEntry) -> CTkColorPicker:
    def Change_Entry_Information(color: str) -> None:
        Accent_Color_Manual_Frame_Var.delete(first_index=0, last_index=8)
        Accent_Color_Manual_Frame_Var.insert(index=0, string=color)

    Configuration_ColorPicker = Configuration["ColorPicker"]
    Color_Picker = CTkColorPicker(
        master = Frame,
        width = Configuration_ColorPicker["width"],
        initial_color = Configuration_ColorPicker["initial_color"],
        fg_color = Configuration_ColorPicker["fg_color"],
        slider_border = Configuration_ColorPicker["slider_border"],
        corner_radius = Configuration_ColorPicker["corner_radius"],
        command = lambda color: Change_Entry_Information(color=color),
        orientation = Configuration_ColorPicker["orientation"])
    return Color_Picker

# ---------------------------------------------- CTkToolTip ----------------------------------------------# 
def Get_ToolTip(widget: any, message: str, ToolTip_Size) -> CTkToolTip:
    Configuration_ToolTip = Configuration["Tooltips"][f"{ToolTip_Size}"]
    ToolTip = CTkToolTip(
        widget = widget,
        message = message,
        delay = Configuration_ToolTip["delay"],
        follow = Configuration_ToolTip["follow"],
        x_offset = Configuration_ToolTip["x_offset"],
        y_offset = Configuration_ToolTip["y_offset"],
        bg_color = Configuration_ToolTip["bg_color"],
        corner_radius = Configuration_ToolTip["corner_radius"],
        border_width = Configuration_ToolTip["border_width"],
        border_color = Configuration_ToolTip["border_color"],
        alpha = Configuration_ToolTip["alpha"],
        padding = tuple(Configuration_ToolTip["padding"]))
    return ToolTip