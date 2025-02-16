from customtkinter import CTk, CTkFrame, CTkScrollableFrame, CTkToplevel, CTkEntry
from CTkMessagebox import CTkMessagebox

import Libs.GUI.Elements as Elements
import Libs.Defaults_Lists as Defaults_Lists

def Get_Widget_Frame(Configuration:dict, Frame: CTk|CTkFrame, Name: str, Additional_Text: str, Widget_size: str, Widget_Label_Tooltip: str) -> CTkFrame:
    # Build base Frame for Widget
    Frame_Single_Body = Elements.Get_Widget_Frame_Body(Configuration=Configuration, Frame=Frame, Widget_size=Widget_size)

    Frame_Single_Header = Elements.Get_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Name}")

    Header_text_Additional = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header_Additional", Font_Size="Column_Header_Additional")
    Header_text_Additional.configure(text=f"{Additional_Text}")

    Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Set="lucide", Icon_Name="circle-help", Icon_Size="Question")
    Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal")

    Frame_Single_Data_Area = Elements.Get_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_size=Widget_size)

    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=7)
    Header_text.pack(side="left", fill="x")
    Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    Header_text_Additional.pack(side="right", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="y", expand=True, padx=7, pady=7)

    return Frame_Single_Body

def Get_DashBoard_Widget_Frame(Configuration:dict, Frame: CTk|CTkFrame, Label: str, Widget_Line:str, Widget_size: str, Icon_Set: str|None, Icon_Name: str|None, Widget_Label_Tooltip: str, Scrollable: bool) -> CTkFrame:
    # Build base Frame for Widget
    if Scrollable == True:
        Frame_Single_Body = Elements.Get_Dashboard_Widget_Frame_Body_Scrollable(Configuration=Configuration, Frame=Frame, Widget_Line=Widget_Line, Widget_size=Widget_size)
    else:
        Frame_Single_Body = Elements.Get_Dashboard_Widget_Frame_Body(Configuration=Configuration, Frame=Frame, Widget_Line=Widget_Line, Widget_size=Widget_size)

    Frame_Single_Header = Elements.Get_Dashboard_Widget_Frame_Header(Configuration=Configuration, Frame=Frame_Single_Body, Widget_Line=Widget_Line, Widget_size=Widget_size)
    
    Header_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header")
    Header_text.configure(text=f"{Label}")

    if Icon_Name != None:
        Icon_Label_text = Elements.Get_Label_Icon(Configuration=Configuration, Frame=Frame_Single_Header, Label_Size="Column_Header", Font_Size="Column_Header", Icon_Set=Icon_Set, Icon_Name=Icon_Name, Icon_Size="DashBoard_Totals")
        Elements.Get_ToolTip(Configuration=Configuration, widget=Icon_Label_text, message=Widget_Label_Tooltip, ToolTip_Size="Normal")
    else:
        pass

    Frame_Single_Data_Area = Elements.Get_Dashboard_Widget_Frame_Area(Configuration=Configuration, Frame=Frame_Single_Body, Widget_Line=Widget_Line, Widget_size=Widget_size)
    
    # Build look of Widget
    Frame_Single_Body.pack(side="top", fill="none", expand=False, padx=0, pady=0)
    Frame_Single_Header.pack(side="top", fill="x", expand=False, padx=7, pady=(7, 2))
    if Icon_Name != None:
        Icon_Label_text.pack(side="left", fill="none", expand=False, padx=1, pady=0)
    else:
        pass
    Header_text.pack(side="left", fill="x")
    Frame_Single_Data_Area.pack(side="top", fill="both", expand=True, padx=7, pady=(0, 7))

    return Frame_Single_Body

def Get_Widget_Input_row(Settings: dict, Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str, Field_Type: str, Var_Value: int|str|None = None,  Validation: str|None = None) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    if Field_Type == "Input_Normal":
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value, Field_Size="Normal", Validation=Validation)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Password_Normal":
        Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Value)
        Field_Normal.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_Small":
        Field_Small = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value, Field_Size="Small", Validation=Validation)
        Frame_Area.configure(width=300)
        Field_Small.pack(side="left", fill="none")
    elif Field_Type == "Input_RadioButton":
        RadioButton = Elements.Get_RadioButton_Normal(Configuration=Configuration, Frame=Frame_Value, Var_Value=Var_Value)
        RadioButton.pack(side="left", fill="none")
    elif Field_Type == "Input_OptionMenu":
        Input_OptionMenu = Elements.Get_Option_Menu(Configuration=Configuration, Frame=Frame_Value)
        Input_OptionMenu.pack(side="left", fill="x", expand=True)
    elif Field_Type == "Input_CheckBox":
        Input_Check_Box = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
        Input_Check_Box.pack(side="left", fill="x", expand=True)
    else:
        CTkMessagebox(title="Error", message=f"Field type: {Field_Type} not supported.", icon="cancel", fade_in_duration=1)

    return Frame_Area

def Get_Widget_Button_row(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Buttons_count: int, Button_Size: str) -> CTkFrame:
    # Build one line for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Value
    Frame_Buttons = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Buttons.pack_propagate(flag=False)
    Frame_Buttons.pack(side="right", fill="x", expand=True, padx=0, pady=0)

    for Button in range(Buttons_count): 
        Button_Normal = Elements.Get_Button(Configuration=Configuration, Frame=Frame_Buttons, Button_Size=Button_Size)
        Button_Normal.pack(side="right", fill="none", expand=False, padx=(10,0))

    return Frame_Area

def Get_Double_Field_Input(Settings: dict, Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str,  Validation: str|None = None) -> CTkFrame:
    # Build one line for two input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value1
    Frame_Value1 = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value1.pack_propagate(flag=False)
    Frame_Value1.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small1 = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value1, Field_Size="Small", Validation=Validation)
    Field_Small1.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space2 = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space2.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    Space_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Space2, Label_Size="Field_Label", Font_Size="Field_Label")
    Space_text.configure(text=f"-")
    Space_text.pack(side="left", fill="none")

    # Frame Value2
    Frame_Value2 = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value2.pack_propagate(flag=False)
    Frame_Value2.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Field_Small2 = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Value2, Field_Size="Small", Validation=Validation)
    Field_Small2.pack(side="left", fill="none")

    return Frame_Area

def Get_Double_Label(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str,  Validation: str|None = None) -> CTkFrame:
    # Build one line for two input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=10, pady=(0,5))

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="left", fill="x", expand=False, padx=0, pady=7)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}:")
    Label_text.pack(side="right", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="left", fill="none", expand=True, padx=0, pady=0)

    # Frame Value1
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="left", fill="x", expand=True, padx=0, pady=0)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Value, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.pack(side="right", fill="none")

    return Frame_Area

def Get_Vertical_Field_Input(Configuration:dict, Frame: CTk|CTkFrame, Field_Frame_Type: str, Label: str,  Validation: str|None = None) -> CTkFrame:
    # Build one column for one input field
    Frame_Area = Elements.Get_Widget_Field_Frame_Area(Configuration=Configuration, Frame=Frame, Field_Frame_Type=Field_Frame_Type)
    Frame_Area.pack_propagate(flag=False)
    Frame_Area.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Label
    Frame_Label = Elements.Get_Widget_Field_Frame_Label(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Label.pack_propagate(flag=False)
    Frame_Label.pack(side="top", fill="y", expand=False, padx=0, pady=0)

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Label, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{Label}")
    Label_text.pack(side="top", fill="none")

    # Frame Space between Label and Value
    Frame_Space = Elements.Get_Widget_Field_Frame_Space(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Space.pack(side="top", fill="none", expand=True, padx=0, pady=0)

    # Frame Value
    Frame_Value = Elements.Get_Widget_Field_Frame_Value(Configuration=Configuration, Frame=Frame_Area, Field_Frame_Type=Field_Frame_Type)
    Frame_Value.pack_propagate(flag=False)
    Frame_Value.pack(side="top", fill="y", expand=True, padx=0, pady=0)

    Input_checkbox = Elements.Get_CheckBox(Configuration=Configuration, Frame=Frame_Value)
    Input_checkbox.pack(side="top", fill="none")

    return Frame_Area

def Get_Table_Frame(Configuration:dict, Frame: CTk|CTkFrame, Table_Size: str, Table_Values: list|None, Table_Columns: int, Table_Rows: int) -> CTkScrollableFrame:
    # Build only one frame which contain whole Table
    Frame_Scrollable_Area = Elements.Get_Widget_Scrollable_Frame(Configuration=Configuration, Frame=Frame, Frame_Size=Table_Size)
    Frame_Scrollable_Area.pack(side="top", fill="y", expand=True, padx=10, pady=(0,5))

    # Table
    Skip_List_Table = Elements.Get_Table(Configuration=Configuration, Frame=Frame_Scrollable_Area, Table_size=Table_Size, columns=Table_Columns, rows=Table_Rows)
    if Table_Values == None:
        pass
    else:
        Skip_List_Table.configure(values=Table_Values)
    Skip_List_Table.pack(side="top", fill="y", expand=True, padx=10, pady=10)

    return Frame_Scrollable_Area

def Get_Pop_up_window(Configuration:dict, title: str, width: int, height: int) -> CTkToplevel:
    def drag_win():
        x = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window._offsetx
        y = Pop_Up_Window.winfo_pointery() - Pop_Up_Window._offsety
        Pop_Up_Window.geometry(f"+{x}+{y}")

    def click_win():
        Pop_Up_Window._offsetx = Pop_Up_Window.winfo_pointerx() - Pop_Up_Window.winfo_rootx()
        Pop_Up_Window._offsety = Pop_Up_Window.winfo_pointery() - Pop_Up_Window.winfo_rooty()

    # TopUp Window
    Pop_Up_Window = CTkToplevel()
    Pop_Up_Window.configure(fg_color="#000001")
    Pop_Up_Window.title(title)
    Pop_Up_Window.geometry(f"{width}x{height}")
    Pop_Up_Window.bind(sequence="<Escape>", func=lambda event: Pop_Up_Window.destroy())
    Pop_Up_Window.bind(sequence="<Button-1>", func=lambda event:click_win())
    Pop_Up_Window.bind(sequence="<B1-Motion>", func=lambda event:drag_win())
    Pop_Up_Window.overrideredirect(boolean=True)
    Pop_Up_Window.iconbitmap(bitmap=Defaults_Lists.Absolute_path(relative_path=f"Libs\\GUI\\Icons\\TimeSheet.ico"))
    Pop_Up_Window.resizable(width=False, height=False)

    # Rounded corners 
    Pop_Up_Window.config(background="#000001")
    Pop_Up_Window.attributes("-transparentcolor", "#000001")

    return Pop_Up_Window

def Get_My_Dialog_Window(Settings: dict, Configuration:dict, title: str, tooltip: str, width: int, height: int, text: str, Password: bool) -> CTkFrame:
    # TODO --> must be finished to be used instead of Elements.Get_DialogWindow
    def Confirm_Choice(Field_Normal: CTkEntry):
        return Field_Normal.get()

    def Reject_Choice():
        return ""

    Dialog_Window = Get_Pop_up_window(Configuration=Configuration, title=title, width=width, height=height)

    # Frame - General
    Frame_Main = Get_Widget_Frame(Configuration=Configuration, Frame=Dialog_Window, Name=title, Additional_Text="", Widget_size="Single_size", Widget_Label_Tooltip=tooltip)
    Frame_Body = Frame_Main.children["!ctkframe2"]

    Label_text = Elements.Get_Label(Configuration=Configuration, Frame=Frame_Body, Label_Size="Field_Label", Font_Size="Field_Label")
    Label_text.configure(text=f"{text}:")
    Label_text.pack(side="top", fill="none", expand=True, padx=10, pady=5)

    if Password == False:
        Field_Normal = Elements.Get_Entry_Field(Settings=Settings, Configuration=Configuration, Frame=Frame_Body, Field_Size="Normal")
        Field_Normal.pack(side="top", fill="none", expand=True, padx=10, pady=5)
    elif Password == True:
        Field_Normal = Elements.Get_Password_Normal(Configuration=Configuration, Frame=Frame_Body)
        Field_Normal.pack(side="top", fill="none", expand=True, padx=10, pady=5)

    # Buttons
    Button_Frame = Get_Widget_Button_row(Frame=Frame_Body, Configuration=Configuration, Field_Frame_Type="Single_Column" , Buttons_count=2, Button_Size="Normal") 
    Button_Confirm_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton"]
    Button_Confirm_Var.configure(text="Confirm", command = lambda:Confirm_Choice(Field_Normal=Field_Normal))
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Confirm_Var, message="Confirm.", ToolTip_Size="Normal")

    Button_Reject_Var = Button_Frame.children["!ctkframe"].children["!ctkbutton2"]
    Button_Reject_Var.configure(text="Reject", command = lambda:Reject_Choice())
    Elements.Get_ToolTip(Configuration=Configuration, widget=Button_Reject_Var, message="Reject.", ToolTip_Size="Normal")
