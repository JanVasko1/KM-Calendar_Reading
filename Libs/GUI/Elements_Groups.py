from customtkinter import CTk, CTkFrame
import Libs.GUI.Elements as Elements

def Get_Widget_Frame(Frame: CTk|CTkFrame, Name: str, Additional_Text: str, Widget_size: str) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Frame=Frame, Widget_size=Widget_size)
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Frame=Frame_Single_Body, Widget_size=Widget_size)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    
    Header_text = Elements.Get_Text_Column_Header(Frame=Frame_Single_Header)
    Header_text.configure(text=f"{Name}")
    Header_text.pack(side="left", fill="x")

    Header_text_Additional = Elements.Get_Text_Column_Header_additional(Frame=Frame_Single_Header)
    Header_text_Additional.configure(text=f"{Additional_Text}")
    Header_text_Additional.pack(side="right", fill="x")

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Frame=Frame_Single_Body, Widget_size=Widget_size)
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_Single_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=0)

    Label_text = Elements.Get_Text_Field(Frame=Frame_Label)
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Field_Normal(Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="none")
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="none")
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Field_Small(Frame=Frame_Value)
        Frame_Area.configure(width=300)
        Field_Small.pack(side="left", fill="none")
    elif Field_Type == "Input_RadioButton":
        RadioButton = Elements.Get_RadioButton_Normal(Frame=Frame_Value)
        RadioButton.pack(side="left", fill="none")
    elif Field_Type == "Input_OptionMenu":
        Input_OptionMenu = Elements.Get_Option_Menu(Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="none")
    else:
        pass
        #! Dodělat --> Nějak zapsat chybu

    return Frame_Area

def Get_Double_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str) -> CTkFrame:
    # Build one line for two input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=0)

    Label_text = Elements.Get_Text_Field(Frame=Frame_Label)
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value1
    Frame_Value1 = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value1.pack_propagate(False)
    Frame_Value1.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small1 = Elements.Get_Field_Small(Frame=Frame_Value1)
    Field_Small1.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space2 = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space2.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    Space_text = Elements.Get_Text_Field(Frame=Frame_Space2)
    Space_text.configure(text=f"-")
    Space_text.pack(side="left", fill="none")

    # Frame Value2
    Frame_Value2 = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value2.pack_propagate(False)
    Frame_Value2.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small2 = Elements.Get_Field_Small(Frame=Frame_Value2)
    Field_Small2.pack(side="left", fill="none")

    return Frame_Area

def Get_Vertical_Field_Imput(Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str) -> CTkFrame:
    # Build one column for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(False)
    Frame_Label.pack(side="top", fill="y", expand=False, padx=0, pady=0)

    Label_text = Elements.Get_Text_Field(Frame=Frame_Label)
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="top", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(False)
    Frame_Value.pack(side="top", fill="y", expand=True, padx=0, pady=0)

    Input_checkbox = Elements.Get_CheckBox(Frame=Frame_Value)
    Input_checkbox.pack(side="top", fill="none")

    return Frame_Area