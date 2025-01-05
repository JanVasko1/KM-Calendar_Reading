from customtkinter import CTk, CTkFrame, CTkScrollableFrame
from CTkMessagebox import CTkMessagebox
import pywinstyles

import Libs.GUI.Elements as Elements

def Get_Widget_Frame(Frame: CTk|CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Frame=Frame, Widget_size=Widget_size)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    Icon_Label_text = Elements.Get_Label_Icon(Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Set="lucide", Icon_Name="circle-help", Icon_Size="Question")
    Elements.Get_ToolTip(widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal")

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Frame=Frame_Single_Body, Widget_size=Widget_size)

    #? Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_DashBoard_Widget_Frame(Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Icon_Set: str|None, Icon_Name: str|None, Widget_Label_Tooltip: str, Scrollable: bool) -> CTkFrame:
    # Build base Frame for Widget
    if Scrollable == True:
        Frame_Single_Body = Elements.Get_Dashboard_Widget_Frame_Body_Scrollable(Frame=Frame, Widget_Line=Widget_Line, Widget_size=Widget_size)
    else:
        Frame_Single_Body = Elements.Get_Dashboard_Widget_Frame_Body(Frame=Frame, Widget_Line=Widget_Line, Widget_size=Widget_size)

    Frame_Single_Header = Elements.Get_Dashboard_Widget_Frame_Header(Frame=Frame_Single_Body, Widget_Line=Widget_Line, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Label}")

    if Icon_Name != None:
        Icon_Label_text = Elements.Get_Label_Icon(Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size="DashBoard_Totals")
        Elements.Get_ToolTip(widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal")
    else:
        pass

    Frame_Single_Data_Area = Elements.Get_Dashboard_Widget_Frame_Area(Frame=Frame_Single_Body, Widget_Line=Widget_Line, Widget_size=Widget_size)
    
    #? Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=(7, 2))
    if Icon_Name != None:
        Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    else:
        pass
    Header_text.pack(side="left", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="both", expand=True, padx=7, pady=(0, 7))

    return Frame_Single_Body

def Get_Single_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Entry_Field(Frame=Frame_Value, Field_Size="Normal")
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Entry_Field(Frame=Frame_Value, Field_Size="Normal")
        Frame_Area.configure(width=300)
        Field_Small.pack(side="left", fill="none")
    elif Field_Type == "Input_RadioButton":
        RadioButton = Elements.Get_RadioButton_Normal(Frame=Frame_Value)
        RadioButton.pack(side="left", fill="none")
    elif Field_Type == "Input_OptionMenu":
        Input_OptionMenu = Elements.Get_Option_Menu(Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_CheckBox":
        Input_OptionMenu = Elements.Get_CheckBox(Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="x", expand=True)
    else:
        CTkMessagebox(title="Error", message=f"Field type: {Field_Type} not uspported.", icon="cancel", fade_in_duration=1)

    return Frame_Area

def Get_Double_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str) -> CTkFrame:
    # Build one line for two input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value1
    Frame_Value1 = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value1.pack_propagate(flag=False)
    Frame_Value1.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small1 = Elements.Get_Entry_Field(Frame=Frame_Value1, Field_Size="Small")
    Field_Small1.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space2 = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space2.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    Space_text = Elements.Get_Label(Frame=Frame_Space2, Label_Size="Field_Label", Font_Size="Field_Label")
    Space_text.configure(text=f"-")
    Space_text.pack(side="left", fill="none")

    # Frame Value2
    Frame_Value2 = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value2.pack_propagate(flag=False)
    Frame_Value2.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small2 = Elements.Get_Entry_Field(Frame=Frame_Value2, Field_Size="Small")
    Field_Small2.pack(side="left", fill="none")

    return Frame_Area

def Get_Vertical_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str) -> CTkFrame:
    # Build one column for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="top", fill="y", expand=False, padx=0, pady=0)

    Label_text = Elements.Get_Label(Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="top", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="top", fill="y", expand=True, padx=0, pady=0)

    Input_checkbox = Elements.Get_CheckBox(Frame=Frame_Value)
    Input_checkbox.pack(side="top", fill="none")

    return Frame_Area

def Get_Table_Frame(Frame: CTk|CTkFrame, Table_Size: str, Table_Values: list, Table_Columns: int, Table_Rows: int) -> CTkScrollableFrame:
    # Buld only one frame wich contain whole Table
    Frame_Scrolable_Area = Elements.Get_Widget_Scrolable_Frame(Frame=Frame, Frame_Size=Table_Size)
    Frame_Scrolable_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Table
    Skip_List_Table = Elements.Get_Table(Frame=Frame_Scrolable_Area, Table_size=Table_Size, columns=Table_Columns, rows=Table_Rows)
    Skip_List_Table.configure(values=Table_Values)
    Skip_List_Table.pack(side="top", fill="none", expand=True, padx=10, pady=10)

    return Frame_Scrolable_Area
