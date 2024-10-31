# TimeSheet Downlaoder
This program was developed to make TimeSheet administration easier and harmonize it over all fo Konica Minolta employee.

# Setup
## Installation
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/)
2. Run `Installation_libs.ps1` code (reflect correct path to your python installation)
3. Update `TimeSheets.bat` to reflect correct path to your python installation

## Process
![Process](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Process.png?raw=true
 "Overal process")

- red --> manual steps
- green --> automatic steps

## Callendar - Pre-Requisit
There must be special Events created for each day
- `Work Start` --> tells program when is particular working day starts
    - must be 0 minutes duration 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Start_End_Events / Start`)

- `Work End` --> tells program when is particular working day ends
    - must be 0 minutes duration 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Start_End_Events / End`)

- `Lunch` --> tells program when is particular lunch is 
    - Event Subject is defined in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events/ Special_Events / Lunch / Search_Text`)

- `Category` --> is considerate as “Project” from TimeSheets
    - Must be manually updated when needed from TimeSheet from Shareponit
    - If event is marke by category, then whole program counts with it base on setup in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Project / Method`)

> [!TIP]
> ![Category ](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Category.png?raw=true
 "Category")

- `Templates` --> is considerate to contain “Activity” from Timesheets
    - If event has line: “Activity: Activity”, then whole program counts with it base on setup in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Activity / Method`)

> [!TIP]
> ![Tempaltes ](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Templates.png?raw=true
 "Tempaltes")

> [!TIP]
> ![Event body](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Activity.png?raw=true
 "Event body")


## Main Setup File `Settings.json`
- `Calendar`
    - `Working Hours` - specify working hours for each day in week
        [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`General / Calendar / ... / Work_Hours`)
    - `Vacation Hours` - specify vacation hours for each day in week when all day Vacation is used
        [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`General / Calendar / ... / Vacation`)
- `Personal Information` - contains your KM Code and full name (Code is used as Personnel number in TimeSheets)

# Downloader
- This first part of program is used to download events from calendar

## Sharepoint
- Program prompts at the beginning if you want to directly download missing days from Sharepoint (online) and analyze missing days

- Setup data must be correctly maintained to have a correct link to proper TimeSheet Excel on Sharepoint 
    - `Authentication`
        - first attempt is required to put password (hashed and stored)
        - It is required to reenter it time to time

    - `Link` 
        - link to the TimeSheet Excel on the KM sharepoint site

## Manual Input
- Manual input you have to select form and to dates
- `Format`: 
    YYYY-MM-DD
    Special sign: “t” = Today

## Methods
- `Outlook_classic` --> download data from Outlook (classic) application installed on Windows
- `API_Exchange_server` --> download events directly from Exchange Server for defined User

> [!CAUTION]
> API_Exchange_server --> Under Developemnt

# Events Handlers

## Overnights
- This handler splits Events if they go over midnight
- This doesn´t require any setup as it is programmed.
- Videly used for multiday Vacation, travel-time ...

> [!TIP]
> ![Overnight Events](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/OverNight.png?raw=true
 "Overnight Events")

## Fill Empty: General
- This is for filling empty space in the calendar between events
- Works only between “Work - Start” and “Work - End” events (only at the time when I'm at work)
- It select one from the list from [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Empty / General / ...`) and use then coverage [%] to simulate real usage

> [!TIP]
> ![Fill Empty General](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Empty_General.png?raw=true
 "Fill Empty General")

## Fill Empty: Scheduled
- This agenda is used for regular record planning like if I have Administration and Emails done after lunch at 11:30 – 12:00
- Agenda can have multiple setup (only one used on picture)
- If in the period is another Event then this scheduled is not filled

## Location
- Currently set for all events `Office`

## Lunch
- lunch is special event which should be skipped from Timesheet
- Also is used to split  parallel meeting which is planned over the lunch (like whole day meetings)
- Search text can be modified in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Special_Events / Lunch / ...`) 

> [!TIP]
> ![Lunch Event](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Lunch.png?raw=true
 "!unch")

## Skip Events
- This is the list of evens which should be skiped from registering them into TimeSheets
- Can be extended in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Skip / ...`) 

- Text from `Settings.json` is compared with Event subject and if a part of subject contain text from (`Event_Handler / Events / Skip / ...`) then is recognized and event is not considerate for Time Sheets

## Parralel Events
- This handler helps to process Events which might be in parallelly set in Calendar
- has 2 modes only one can be selected in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Parralel_Events / Divide_Method`):
    - `Keep_Parralel` --> will keep both parallel events for TimeSheet
    - `Divide` --> will divide Parralle Events based on logic:

> [!TIP]
> ![Parralel 1](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel1.png?raw=true
 "Divide")

> [!TIP]
> ![Parralel 2](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel2.png?raw=true
 "Divide and use shorter")

> [!TIP]
> ![Parralel 3](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel3.png?raw=true
 "Divide")

> [!TIP]
> ![Parralel Keep](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel_keep.png?raw=true
 "Parralel Keep")

- has 2 methods for Events start at the same time:
    - `Use_Shorter` --> will consider the shortest event as first pick
    - `Use_Longer` --> will consider the shortest event as first pick

> [!CAUTION]
> Use_Longer --> Under development (now is defaulty used Use_Shorter)

## AutoFiller
- This special function to help automatically fill: `Project`, `Activity`, `Location`
- It can be enhanced in [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Auto_Filler / Details / ...`)
- If there is empty text --> then is not used
- As `Skip Events` program is based on searching text in the Event Subject to apply mapping

## Vacation
- Handler of Vacation to register correctly 
    - `All Day` --> takes hours from [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
  and apply them into TimeSheet
    - `Half Day` --> uses only the time defined by Event
- If the text appeared (defined by OKBase) in the event Subject [`Settings.json`](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/Libs/Settings.json):
 (`Event_Handler / Events / Special_Events / Vacation / ...`) 

- All Events within the Vacation period and Working hours are deleted

## Home Office
- Currently is not maintaining anything as HomeOffice is not used as special Location of TimeSheets

## Summary
- Is defined to print statistic of selected period to provide better overview of Time spent:
    - Total Statistics
    - Project Statistics
    - Activity Statistics
    - WeekDay Statistics
    - Week Statistics
- Also print all lines before export to .csv
- Open .csv in the format read to “Copy + Paste” to TimeSheet on Sharepoint

# Uploader
> [!CAUTION]
> Under Developemnt as whole functionality

# Export csv
The processed result is automatically exported to the defined path and automatically opened by Windows