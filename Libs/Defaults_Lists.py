def Busy_Status_List() -> list[str]:
    Busy_Stuses = ["Free", "Tentative", "Busy", "Out of Office", "Working elsewhere"]
    return Busy_Stuses

def Busy_Status_Priorities_List() -> list[str]:
    # Smaller Index = Higher priority
    Busy_Stuses_Priorities = ["Busy", "Working elsewhere", "Tentative", "Free", "Out of Office"]
    return Busy_Stuses_Priorities
