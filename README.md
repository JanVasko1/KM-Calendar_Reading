# TimeSheet Downloader
This program was developed to make TimeSheet administration easier and harmonize it over all fo Konica Minolta employee.

# Setup
### Installation
1. Install [Python 3.11.2](https://www.python.org/downloads/release/python-3112/) - recomended or higher
    - install it as "Run as Administrator"
    - on pop-up page mark "Add Python 3.11.2 to PATH" and unmark "Instal launcher for all users" (if possible)
2. Run **Installation_libs.ps1** code (reflect correct path to your python installation)
3. Update **TimeSheets.bat** to reflect correct path to your python installation

## Process
![Process](Libs\\Readme\\Process.png)<br>
- red --> manual steps<br>
- green --> automatic steps

### Outlook Calendar - Pre-Requisit
There must be special Events created for each day and special behavior must be followed<br>
1. **Work Start** --> tells program when is particular working day starts<br>
    - must be 0 minutes duration <br>
2. **Work End** --> tells program when is particular working day ends<br>
    - must be 0 minutes duration <br>
3. **Lunch** --> tells program when is particular lunch is <br>
4. **Category** --> is considerate as “Project” from TimeSheets<br>
    - Must be manually updated when needed from TimeSheet from Shareponit<br>
    - If event is marke by category, then whole program counts with it base on setup

![Category](Libs\\Readme\\Category.png)<br>

- **Templates** --> is considerate to contain “Activity” from Timesheets
    - If event has line: “Activity: Activity”, then whole program counts with it base on setup 

![Tempaltes](Libs\\Readme\\Templates.png)<br>


![Event body](Libs\\Readme\\Activity.png)<br>


### Main Setup File **Settings.json**
- **Calendar**
    - **Working Hours** - specify working hours for each day in week
    - **Vacation Hours** - specify vacation hours for each day in week when all day Vacation is used
- **Personal Information** - contains your KM Code and full name (Code is used as Personnel number in TimeSheets)

# Downloader
This first part of program is used to download events from calendar

### Sharepoint
- Program prompts at the beginning if you want to directly download missing days from Sharepoint (online) and analyze missing days (when working from home, you have to be on KM VPN) 
- Program is also capable to download whole reporting period nevertheless if there is some records of my ID

- Setup data must be correctly maintained to have a correct link to proper TimeSheet Excel on Sharepoint 
    - **Authentication**
        - first attempt is required to put password (hashed and stored)
        - It is required to reenter it time to time

    - **Link** 
        - link to the TimeSheet Excel on the KM sharepoint site

### Manual Input
- Manual input you have to select form and to dates
- **Format**: 
    - YYYY-MM-DD
    - Special sign: “t” = Today

### Methods
- **Outlook_classic** --> download events from Outlook (classic) application installed on Windows, there is draback, must be only one account in Outlook client
- **Exchange** --> download events directly from Exchange Server for defined User

# Events Handlers
Here are steps which process the downloaded date into the shape suitable for TimeSheets

### Overnights
- This handler splits Events if they go over midnight
- This doesn´t require any setup as it is programmed.
- Videly used for multiday Vacation, travel-time ...


![Overnight Events](Libs\\Readme\\OverNight.png)<br>

### Too Long Empty space split
- This handler splits Empty space between 2 Events into multiple parts

- **Do nothing** --> Program will keep Empty Duration as it is 
- **Equal Split** --> Program will divide duration by 2 (if odd number then second Event has +1 minute)
- **Random Split** --> Program will split Event duration by random nubmer selected between "Minimal Time" and "Event Duration - Minimal Time" to secure taht both splits has at lease 15 minutes. Also Events are rounded by same argument.

![Overnight Events](Libs\\Readme\\Too_Long_Empty_Space.png)<br>


### Fill Empty: General
- This is for filling empty space in the calendar between events where it react on **coverage** palced by each record (sum must be equal to 100%)
- Works only between “Work - Start” and “Work - End” events (only at the time when I'm at work)
- It select one from the list and use then coverage [%] to simulate real usage


![Fill Empty General](Libs\\Readme\\Empty_General.png)<br>


![Empty General setup](Libs\\Readme\\Empty_General_setup.png)<br>

### Fill Empty: Scheduled
- This agenda is used for regular record planning like if I have Administration and Emails done after lunch at 11:30 – 12:00 of the week day
- Agenda can have multiple setup (only one used on picture)
- If in the period is another Event then this scheduled is not filled


![Empty Schedules setup](Libs\\Readme\\Empty_Schedules_setup.png)<br>

### Location
- Currently set for all events **Office**

### Lunch
- lunch is special event which should be skipped from Timesheet
- Also is used to split  parallel meeting which is planned over the lunch (like whole day meetings)
- Search text can be modified


![Lunch Event](Libs\\Readme\\Lunch.png)<br>

### Skip Events
- This is the list of evens which should be skiped from registering them into TimeSheets
- Text is compared with Event subject and if a part of subject contain text then is recognized and event is not considerate for Time Sheets

### Parallel Events
- This handler helps to process Events which might be in parallelly set in Calendar
- has 2 modes only one can be selected
    - **Divide** --> will divide Parralle Events based on logic (eveerytime takes as separator the begining of Event)
    - **Keep Parallel** --> will keep both parallel events for TimeSheet
    
**Divide:**<br>
![Parallel 1](Libs\\Readme\\Parallel1.png)<br>


**Divide and Use Shorter:**<br>
![Parallel 2](Libs\\Readme\\Parallel2.png)<br>


**Keep Parallel:**<br>
![Parallel Keep](Libs\\Readme\\Parallel_keep.png)<br>

- has 2 methods for Events start at the same time:
    - **Use Shorter** --> will consider the shortest event as first pick
    - **Use Longer** --> will consider the longest event as first pick

**[!CAUTION]**<br>
Use_Longer --> Under development (now is defaulty used Use Shorter)

### AutoFiller
- This special function to help automatically fill: **Project**, **Activity**, **Location**
- If there is empty text --> then is not used
- As **Skip Events** program is based on searching text in the Event Subject to apply mapping

### Vacation
- Handler of Vacation to register correctly 
    - **All Day** --> takes hours and apply them into TimeSheet
    - **Half Day** --> uses only the time defined by Event
- If the text appeared (defined by OKBase) in the event Subject

- All Events within the Vacation period and Working hours are deleted

### Home Office
- Currently is not maintaining anything as HomeOffice is not used as special Location of TimeSheets

### Join Events
- This part is to cumulate multiple meeting into one in the case that condition are met:
    1. Date
    2. Project
    3. Activity
    4. Activity Description


![Join Event](Libs\\Readme\\Join_Event.png)<br>

# Summary
Is defined to print statistic and all records of selected period to provide better overview of Time spent:
    - Total Statistics
    - Project Statistics
    - Activity Statistics
    - WeekDay Statistics
    - Week Statistics

# Uploader
**[!CAUTION]**<br>
Under Developemnt as whole functionality

# Export csv
The processed result is automatically exported to the defined path and automatically opened by Windows in the format ready to “Copy + Paste” to TimeSheet on Sharepoint

# FrontEnd
**[!CAUTION]**<br>
Under Developemnt as whole functionality, Will have to udpate whole Readmme.md --> because of change on global scale


# Footer
The Settings.json is real file of Jan Vasko usage