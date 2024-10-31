# TimeSheet Downlaoder
## Aim
This program was developed to make TimeSheet administration easier and harmonize it over all  

# Settup
## Installation
Process:
    

## Callendar - Pre-Requisit
There must be special Events created for each day
- `Work Start` --> tells program when is particular working day starts
    - must be 0 minutes duration 
    - Event Subject is defined in Settings.json

- `Work End` --> tells program when is particular working day ends
    - must be 0 minutes duration 
    - Event Subject is defined in Settings.json

- `Launch` --> tells program when is particular launch is 
    - Event Subject is defined in Settings.json

- `Category` --> is considerate as “Project” from TimeSheets
    - If event is marke by category, then whole program counts with it base on setup in Setup.json

- `Templates` --> is considerate to contain “Activity” from Timesheets
    - If event has line: “Activity: Activity”, then whole program counts with it base on setup in Settings.json

## Main Setup File Settings.json
- `Calendar`
    - `Working Hours` - specify working hours for each day in week
    - `Vacation Hours` - specify vacation hours for each day in week when all day Vacation is used
- `Personal Information` - contains your KM Code and full name

# Downloader
- This first part of program is used to download events from calendar

## Sharepoint
- Program prompts at the beginning if you want to directly download missing days from Sharepoint (online) and analyze missing days

- Setup data must be correctly maintained to have a correct link to proper TimeSheet Excel on Sharepoint 
    - `Authentication` 
        – first attempt is required to put password (hashed and stored)
        - It is required to reenter it time to time

## Manual Input
- Manual input you have to select form and to dates
- `Format`: 
    YYYY-MM-DD
    Special sign: “t” = Today

## Methods
- `Outlook_classic` --> download data from Outlook (classic) application installed on Windows
- `API_Exchange_server` --> download events directly from Exchange Server for defined User

# Events Handlers

## Overnights
- This handler splits Events if they go over night
- This doest require any setup as it is programmed.
- Videly used for multiday Vacation, travel-time

![Overnight Events](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/OverNight.png?raw=true
 "Overnight Events")

## Fill Empty: General
- This is for filling empty space in the calendar between events
- Works only between “Work - Start” and “Work - End” events (only at the time when I'm at work)
- It select one from the list from Settings.json and use then coverage % to simulate real usage

![Fill Empty General](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Empty_General.png?raw=true
 "Fill Empty General")

## Fill Empty: Scheduled
- This agenda is used for regular record planning like if I have Administration and Emails done after launch at 11:30 – 12:00
- Agenda can have multiple setup (only one used on picture)
- If in the period is another Event then this scheduled is not filled

## Location
- Currently set for all events `Office`

## Launch
- Launch is special event which should be skipped from Timesheet
- Also is used to split  parallel meeting which is planned over the launch (like whole day meetings)
- Search text can be modified in Settings.json

![Launch ](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Launch.png?raw=true
 "Launch")

## Skip Events
- This is the list of evens which should be skiped from registering them into TimeSheets
- Can be extended in Settings.json 
- Text from json is compared with Event subject and if a part of suvject contain text from .json then is recognized and event is not considerate for Time Sheets

## Parralel Events
- This handler helps to process Events which might be in parallelly set in Calendar
- Has 2 modes (only one can be selected in Settings.json):
    - `Keep_Parralel` --> will keep both parallel events for TimeSheet
    - `Divide` --> will divide Parralle Events based on logic:

![Parralel 1](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel1.png?raw=true
 "Parralel 1")

 ![Parralel 2](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel2.png?raw=true
 "Parralel 2")

 ![Parralel 3](https://github.com/JanVasko1/KM-Calendar_Reading/blob/main/images/Parralel3.png?raw=true
 "Parralel 3")

## AutoFiller
- This special function to help automatically fill: `Project`, `Activity`, `Location`
- It can be enhanced in Settings.json 
- If there is empty text --> then is not used
- As `Skip Events` program is based on searching text in the Event Subject to apply mapping

## Vacation
- Handler of Vacation to register correctly 
    - `All Day` --> takes hours from .json and apply them into TimeSheet
    - `Half Day` --> uses only the time defined by Event
- If the text appeared (defined by OKBase) in the event Subject
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
