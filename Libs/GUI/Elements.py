from customtkinter import CTkButton, CTk, CTkFrame, CTkEntry, CTkLabel, CTkFont, CTkImage, CTkRadioButton, CTkTabview, CTkTextbox, CTkOptionMenu, CTkCheckBox, CTkProgressBar, CTkInputDialog, CTkToplevel
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox

import json
from PIL import Image

File = open(file=f"Libs\\GUI\\Configuration.json", mode="r", encoding="UTF-8", errors="ignore")
Configuration = json.load(fp=File)
File.close()

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

def Get_Text_Main(Frame: CTk|CTkFrame) -> CTkLabel:
    Configuration_Text_Main = Configuration["Texts"]["Main"]
    Text_Main = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size="Main"),
        height = Configuration_Text_Main["height"],
        fg_color = Configuration_Text_Main["fg_color"],
        text_color = tuple(Configuration_Text_Main["text_color"]),
        anchor = Configuration_Text_Main["anchor"],
        padx = Configuration_Text_Main["padx"],
        pady = Configuration_Text_Main["pady"])
    return Text_Main

def Get_Text_H1(Frame: CTk|CTkFrame) -> CTkLabel:
    Configuration_Text_H1 = Configuration["Texts"]["H1"]
    Text_H1 = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size="H1"),
        height = Configuration_Text_H1["height"],
        fg_color = Configuration_Text_H1["fg_color"],
        text_color = tuple(Configuration_Text_H1["text_color"]),
        anchor = Configuration_Text_H1["anchor"],
        padx = Configuration_Text_H1["padx"],
        pady = Configuration_Text_H1["pady"])
    return Text_H1

def Get_Text_Column_Header(Frame: CTk|CTkFrame) -> CTkLabel:
    Configuration_Text_Column_Header = Configuration["Texts"]["Column_Header"]
    Text_Column_Header = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size="Column_Header"),
        height = Configuration_Text_Column_Header["height"],
        fg_color = Configuration_Text_Column_Header["fg_color"],
        text_color = tuple(Configuration_Text_Column_Header["text_color"]),
        anchor = Configuration_Text_Column_Header["anchor"],
        padx = Configuration_Text_Column_Header["padx"],
        pady = Configuration_Text_Column_Header["pady"])
    return Text_Column_Header

def Get_Text_Column_Header_additional(Frame: CTk|CTkFrame) -> CTkLabel:
    Configuration_Text_Column_Header_Additional = Configuration["Texts"]["Column_Header_Additional"]
    Text_Column_Header = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size="Column_Header_Additional"),
        height = Configuration_Text_Column_Header_Additional["height"],
        fg_color = Configuration_Text_Column_Header_Additional["fg_color"],
        text_color = tuple(Configuration_Text_Column_Header_Additional["text_color"]),
        anchor = Configuration_Text_Column_Header_Additional["anchor"],
        padx = Configuration_Text_Column_Header_Additional["padx"],
        pady = Configuration_Text_Column_Header_Additional["pady"])
    return Text_Column_Header

def Get_Text_Field(Frame: CTk|CTkFrame) -> CTkLabel:
    Configuration_Text_Field_Label = Configuration["Texts"]["Field_Label"]
    Text_Field_Label = CTkLabel(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        height = Configuration_Text_Field_Label["height"],
        fg_color = Configuration_Text_Field_Label["fg_color"],
        text_color = tuple(Configuration_Text_Field_Label["text_color"]),
        anchor = Configuration_Text_Field_Label["anchor"],
        padx = Configuration_Text_Field_Label["padx"],
        pady = Configuration_Text_Field_Label["pady"])
    return Text_Field_Label

# ---------------------------------------------- Buttons ----------------------------------------------# 
def Get_Button(Frame: CTk|CTkFrame, Button_Size: str) -> CTkButton:
    Configuration_Button_Normal = Configuration["Buttons"][f"{Button_Size}"]
    Button_Normal = CTkButton(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Button_Normal["width"],
        height = Configuration_Button_Normal["height"],
        corner_radius = Configuration_Button_Normal["corner_radius"],
        border_width = Configuration_Button_Normal["border_width"],
        border_color = tuple(Configuration_Button_Normal["border_color"]),
        bg_color = Configuration_Button_Normal["bg_color"],
        fg_color = tuple(Configuration_Button_Normal["fg_color"]),
        hover = Configuration_Button_Normal["hover"],
        hover_color = tuple(Configuration_Button_Normal["hover_color"]),
        anchor = Configuration_Button_Normal["anchor"])
    return Button_Normal

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
    RadioButton_Normal = CTkRadioButton(
        master = Frame,
        width = Configuration_RadioButton_Normal["width"],
        height = Configuration_RadioButton_Normal["height"],
        radiobutton_width = Configuration_RadioButton_Normal["radiobutton_width"],
        radiobutton_height = Configuration_RadioButton_Normal["radiobutton_height"],
        corner_radius = Configuration_RadioButton_Normal["corner_radius"],
        border_width_unchecked = Configuration_RadioButton_Normal["border_width_unchecked"],
        border_width_checked = Configuration_RadioButton_Normal["border_width_checked"],
        fg_color = tuple(Configuration_RadioButton_Normal["fg_color"]),
        border_color = tuple(Configuration_RadioButton_Normal["border_color"]),
        hover_color = tuple(Configuration_RadioButton_Normal["hover_color"]),
        hover = Configuration_RadioButton_Normal["hover"])
    return RadioButton_Normal

def Get_Option_Menu(Frame: CTk|CTkFrame) -> CTkOptionMenu:
    Configuration_Option_Menu = Configuration["Fields"]["OptionMenu"]["Normal"]
    Option_Menu = CTkOptionMenu(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Option_Menu["width"],
        height = Configuration_Option_Menu["height"],
        corner_radius = Configuration_Option_Menu["corner_radius"],
        bg_color = Configuration_Option_Menu["bg_color"],
        fg_color = tuple(Configuration_Option_Menu["fg_color"]),
        button_color = tuple(Configuration_Option_Menu["button_color"]),
        button_hover_color = tuple(Configuration_Option_Menu["button_hover_color"]),
        text_color = tuple(Configuration_Option_Menu["text_color"]),
        text_color_disabled = tuple(Configuration_Option_Menu["text_color_disabled"]),
        dropdown_fg_color = tuple(Configuration_Option_Menu["dropdown_fg_color"]),
        dropdown_hover_color = tuple(Configuration_Option_Menu["dropdown_hover_color"]),
        dropdown_text_color = tuple(Configuration_Option_Menu["dropdown_text_color"]),
        hover = Configuration_Option_Menu["hover"],
        dynamic_resizing = Configuration_Option_Menu["dynamic_resizing"],
        anchor = Configuration_Option_Menu["anchor"])
    return Option_Menu

def Get_CheckBox(Frame: CTk|CTkFrame) -> CTkCheckBox:
    Configuration_Check_Box = Configuration["Fields"]["CheckBox"]["Normal"]
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
        fg_color = tuple(Configuration_Check_Box["fg_color"]),
        hover_color = tuple(Configuration_Check_Box["hover_color"]),
        checkmark_color = tuple(Configuration_Check_Box["checkmark_color"]),
        text_color = tuple(Configuration_Check_Box["text_color"]),
        hover = Configuration_Check_Box["hover"])
    return Check_Box


# ---------------------------------------------- Frames ----------------------------------------------# 
def Get_Frame(Frame: CTk|CTkFrame, Frame_Size: str) -> CTkFrame:
    Configuration_Bacground = Configuration["Frames"]["Page_Frames"][f"{Frame_Size}"]
    # fg_color - Preparation
    fg_color_json = Configuration_Bacground["fg_color"]
    if type(fg_color_json) is list:
        fg_color = tuple(Configuration_Bacground["fg_color"])
    else:
        fg_color = Configuration_Bacground["fg_color"]

    Frame_Big = CTkFrame(
        master = Frame,
        width = Configuration_Bacground["width"],
        height = Configuration_Bacground["height"],
        corner_radius = Configuration_Bacground["corner_radius"],
        border_width = Configuration_Bacground["border_width"],
        border_color = Configuration_Bacground["border_color"],
        bg_color = Configuration_Bacground["bg_color"],
        fg_color = fg_color)
    return Frame_Big

# ------------------------------------------------------------------------------------------------------------ Widgets  ------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------ Widget Frames ------------------------------------------#
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
    TabView_Normal = CTkTabview(
        master = Frame,
        width = Configuration_TabView_Normal["width"],
        height = Configuration_TabView_Normal["height"],
        corner_radius = Configuration_TabView_Normal["corner_radius"],
        border_width = Configuration_TabView_Normal["border_width"],
        border_color = tuple(Configuration_TabView_Normal["border_color"]),
        bg_color = Configuration_TabView_Normal["bg_color"],
        segmented_button_fg_color = tuple(Configuration_TabView_Normal["segmented_button_fg_color"]),
        segmented_button_selected_color = tuple(Configuration_TabView_Normal["segmented_button_selected_color"]),
        segmented_button_selected_hover_color = tuple(Configuration_TabView_Normal["segmented_button_selected_hover_color"]),
        segmented_button_unselected_color = tuple(Configuration_TabView_Normal["segmented_button_unselected_color"]),
        segmented_button_unselected_hover_color = tuple(Configuration_TabView_Normal["segmented_button_unselected_hover_color"]),
        text_color = tuple(Configuration_TabView_Normal["text_color"]),
        text_color_disabled = tuple(Configuration_TabView_Normal["text_color_disabled"]),
        anchor = Configuration_TabView_Normal["anchor"])
    return TabView_Normal

# ---------------------------------------------- Tables ----------------------------------------------# 
def Get_Table(Frame: CTk|CTkFrame, Table_size: str) -> CTkTable:
    Configuration_Table_Single = Configuration["Tables"][f"{Table_size}"]
    Table_Single = CTkTable(
        master = Frame,
        font = Get_Font(Font_Size="Field_Label"),
        width = Configuration_Table_Single["width"],
        height = Configuration_Table_Single["height"],
        colors = Configuration_Table_Single["colors"],
        border_width = Configuration_Table_Single["border_width"],
        border_color = tuple(Configuration_Table_Single["border_color"]),
        color_phase = Configuration_Table_Single["color_phase"],
        orientation = Configuration_Table_Single["orientation"],
        header_color = Configuration_Table_Single["header_color"],
        corner_radius = Configuration_Table_Single["corner_radius"],
        hover_color = tuple(Configuration_Table_Single["hover_color"]),
        wraplength = Configuration_Table_Single["wraplength"],
        justify = Configuration_Table_Single["justify"],
        anchor = Configuration_Table_Single["anchor"])
    return Table_Single

# ---------------------------------------------- Images ----------------------------------------------# 
def Get_Icon(Frame: CTk|CTkFrame, Icon: str, Icon_Size: tuple, Picture_size: str) -> CTkFrame:
    Frame_Icon = Get_Icon_Button(Frame=Frame, Picture_size=Picture_size)
    Image_Settings = Get_Image(light_image=f"Libs\\GUI\\Icons\\{Icon}_Light.png", dark_image=f"Libs\\GUI\\Icons\\{Icon}_Dark.png", size=Icon_Size)
    Frame_Icon.configure(image=Image_Settings, text="")
    return Frame_Icon

def Get_Image(light_image: str, dark_image: str, size: tuple) -> CTkImage:
    Picture = CTkImage(
        light_image = Image.open(f"{light_image}"),
        dark_image = Image.open(f"{dark_image}"),
        size = size)
    return Picture

def Get_Icon_Button(Frame: CTk|CTkFrame, Picture_size: str) -> CTkButton:
    Configuration_Button_Picture_SideBar = Configuration["Buttons"][f"{Picture_size}"]
    Button_Picture_SideBar = CTkButton(
        master = Frame,
        width = Configuration_Button_Picture_SideBar["width"],
        height = Configuration_Button_Picture_SideBar["height"],
        corner_radius = Configuration_Button_Picture_SideBar["corner_radius"],
        border_width = Configuration_Button_Picture_SideBar["border_width"],
        bg_color = Configuration_Button_Picture_SideBar["bg_color"],
        fg_color = Configuration_Button_Picture_SideBar["fg_color"],
        hover = Configuration_Button_Picture_SideBar["hover"],
        hover_color = tuple(Configuration_Button_Picture_SideBar["hover_color"]),
        anchor = Configuration_Button_Picture_SideBar["anchor"])
    return Button_Picture_SideBar

# ---------------------------------------------- Progress Bar ----------------------------------------------# 
def Get_ProgressBar(Frame: CTk|CTkFrame, orientation: str, Progress_Size: str) -> CTkProgressBar:
    Configuration_ProgressBar = Configuration["ProgressBar"][f"{orientation}"][f"{Progress_Size}"]
    Progress_Bar = CTkProgressBar(
        master = Frame,
        width = Configuration_ProgressBar["width"],
        height = Configuration_ProgressBar["height"],
        border_width = Configuration_ProgressBar["border_width"],
        border_color = tuple(Configuration_ProgressBar["border_color"]),
        corner_radius = Configuration_ProgressBar["corner_radius"],
        bg_color = Configuration_ProgressBar["bg_color"],
        fg_color = tuple(Configuration_ProgressBar["fg_color"]),
        progress_color = tuple(Configuration_ProgressBar["progress_color"]),
        orientation = Configuration_ProgressBar["orientation"],
        determinate_speed = Configuration_ProgressBar["determinate_speed"],
        indeterminate_speed = Configuration_ProgressBar["indeterminate_speed"])
    return Progress_Bar


# ---------------------------------------------- InputDialog ----------------------------------------------# 
def Get_DialogWindow(text: str, title: str, Dialog_Type: str) -> CTkInputDialog:
    Configuration_Dialog = Configuration["InputDialog"][f"{Dialog_Type}"]
    Dialog = CTkInputDialog(
        text=text,
        title=title,
        font = Get_Font(Font_Size="Field_Label"),
        fg_color = tuple(Configuration_Dialog["fg_color"]),
        text_color = tuple(Configuration_Dialog["text_color"]),
        button_fg_color = tuple(Configuration_Dialog["button_fg_color"]),
        button_hover_color = tuple(Configuration_Dialog["button_hover_color"]),
        button_text_color = tuple(Configuration_Dialog["button_text_color"]),
        entry_fg_color = tuple(Configuration_Dialog["entry_fg_color"]),
        entry_border_color = tuple(Configuration_Dialog["entry_border_color"]),
        entry_text_color = tuple(Configuration_Dialog["entry_text_color"]),
        password = Configuration_Dialog["password"])
    return Dialog