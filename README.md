# TimeSheet Downlaoder
# Aim
This program was developed to make TimeSheet administration easier and harmonize it over all  

# Settup
## Callendar - Pre-Requisit
There must be special Events created for each day
- `Work Start` --> tells program when is particular working day starts
    - must be 0minutes duration 
    - Event Subject is defined in Settings.json

- `Work End` --> tells program when is particular working day ends
    - must be 0minutes duration 
    - Event Subject is defined in Settings.json

- `Launch` --> tells program when is particular launch is 
    - Event Subject is defined in Settings.json

- `Category` --> is considerate as “Project” from TimeSheets
    - If event is marke by category, then whole program counts with it base on setup in Setup.json

- `Templates` --> is considerate to contain “Activity” from Timesheets
    - If event has line: “Activity: Activity”, then whole program counts with it base on setup in .json


## Main Setup File
- `Calendar`
    - `Working Hours` - specify working hours for each day in week
    - `Vacation Hours` - specify vacation hours for each day in week when all day Vacation is used
- `Personal Information` - contains your KM Code and full name

# Downloader
## Downloader - Sharepoint
- Program prompts at the beginning if you want to directly download missing days from Sharepoint (online) and analyze missing days

- Setup data must be correctly maintained to have a correct link to proper TimeSheet Excel on Sharepoint 
    - `Authentication` 
        – first attempt is required to put password (hashed and stored)
        - It is required to reenter it time to time

## Downloader - Manual Input
- Manual input you have to select form and to dates
- `Format`: 
    YYYY-MM-DD
    Special sign: “t” = Today
