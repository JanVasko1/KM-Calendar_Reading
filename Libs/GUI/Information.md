# --------------------------------- TimeSheet Downloader ---------------------------------
This program was developed to make TimeSheet administration easier and harmonize it over all fo Konica Minolta employee.


### Outlook Calendar - Pre-Requisite
There must be special Events created for each day and special behavior must be followed

- **Work Start** --> tells program when is particular working day starts
    - must be 0 minutes duration
- **Work End** --> tells program when is particular working day ends
    - must be 0 minutes duration
- **Lunch** --> tells program when is particular lunch is
- **Category** --> is considerate as “Project” from TimeSheets
    - Program is capable to update it from actual TimeSheet excel from Sharepoint
    - If event has category, then program is capable to pick the information and use it (if multiple categories used in Event, then take first only)
<br>
![Category](Libs\\Readme\\Category.png)

- **Templates** --> is considerate to contain “Activity” from Time sheets
    - If event has line: “Activity: Activity”, then program is capable to pick the information and use it
<br>
![Templates](Libs\\Readme\\Templates.png) -> ![Event body](Libs\\Readme\\Activity.png)



# -------------------------------------------- Pages --------------------------------------------
# ----------------------- Downloader -----------------------
### Downloader - Tabs purpose
- **New**: This Tab is used to download new data from Exchange / Outlook Classic Client
- **Past**: This Tab is used to download data from already past months to check my own history (last 5 years as limit)
- **My Team**: This Tab is used to download data from Sharepoint TimeSheet/s for my team members


## ---------- Downloader - New ----------
### Sharepoint
- Used mainly to get dates definition for missing data from Current TimeSheets 
- for this option you have to be in Internal net or connected by VPN
- Dates are defined by 2 Options Fields:
    * **Date From**
        - Last Registered Date: Program scan current TimeSheets and find your las entry add 1 Day 
        - First Report Date: Program will use first day of reporting period
    * **Date To**
        - Today: Today date as last download date from data source
        - Manual: You can manually select date you want (program check if it is after "Date From")
        - Last Report Day: Program will use last day of reporting period
    * **Authentication**
        - you have to put password always into field "Password" to authenticate on Sharepoint
    * **Link**
        - link to the TimeSheet Excel on the KM sharepoint site

### Manual Input
- Manual input you have to select From and To dates
- **Format**: 
    - YYYY-MM-DD

### Download Data Sources
- **Exchange** --> download events directly from Exchange Server for defined User (you mus authenticate by Password)
- **Outlook_classic** --> download events from Outlook (classic) application installed on Windows (you have to open Outlook and let be updated before downloading data)

## ---------- Downloader - Past ----------
### Previous Period Range
- Used for defining periods to check by combination "From Month"/"From Year" --> "To Month"/"To Year"
- here is program limitation to display only 5 years back 

### Sharepoint
- just used to authenticate on Sharepoint for data download

## ---------- Downloader - My Team ----------
### Sharepoint
- just used to authenticate on Sharepoint for data download for my Team members

## ---------- Download process ----------
![Process](Libs\\Readme\\Process.png)

- red --> manual steps
- green --> automatic steps


# ----------------------- Dashboard -----------------------
Is defined to print statistic and all records of selected period to provide better overview of Time spent:

- Total Statistics
- Project Statistics
- Activity Statistics
- WeekDay Statistics
- Week Statistics

## Total Statistics
- **Count**: Shows total counts of Events.
- **Total**: Shows total hours.
- **Average**: Shows Average hours per Event.
- **My Active Days Utilization**: Shows utilization in relation to my calendar and for active days only.
- **Displayed Period surplus**: Shows hours if Im surplus against KM actual day utilization for Input End Date.
- **Reported Period Utilization**: Shows Utilization of Reporting Period.

## Project Statistics
- contain 2 parts
1. Main Project Statistics
    - show table with Projects details
    - Detail button display charts of Projects/Day distribution
2. Projects Totals
    - shows some peeks for each category<br>
![Projects](Libs\\Readme\\Project_Chart_Example.png)

## Activity Statistics
- contain 2 parts
1. Main Activity Statistics
    - show table with Activity details
    - Detail button display charts of Activity/Day distribution
2. Activity Totals
    - shows some peeks for each category<br>
![Activity](Libs\\Readme\\Activity_Chart_Example.png)

## Week Days
- display detail statistic for each day of week
- Utilization button display charts of cumulated utilization over KM cumulated time

## Weeks
- display detail statistic for each week
- Utilization button display charts of cumulated utilization over KM cumulated time<br>
![Utilization](Libs\\Readme\\Utilization_Chart_Example.png)

## Charts
- display detail charts between Projects / Activity / Utilization<br>

**[!CAUTION]**
Under Development as whole functionality


# ----------------------- My Team -----------------------
- build for Management to display same statistic as on Dashboard, but only for current period for every member of my team
- Totals<br>
**[!CAUTION]**
Under Development as whole functionality



# ----------------------- Data -----------------------
- display downloaded data formatted as on TimeSheets on Sharepoint
### Button: Upload
- Function which uploads automatically my data (which are here displayed) into TimeSheets on Sharepoint<br>
**[!CAUTION]**
Under Development as whole functionality

### Button: Excel
- will open excel with data --> prepared for "COPY + PASTE" to online TimeSheets


# ----------------------- Information -----------------------
- program information page


# ----------------------- Settings -----------------------
Program settings page
## Settings - Tabs purpose
- **General**
    - General program settings like appearance and my account
- **Data Source**
    - Technical page about data sources and formats
- **Calendar**
    - All related things to my Working Hours / Vacation calendar and Start / End Events
- **Events - General**
    - Event handler for skipping / joining Events and solving Parallel Events
- **Events - Special**
    - Events which needs special treatment line Lunch, Vacation, SickDays ...
- **Events - Empty**
    - Settings of program behavior for missing Events in Calendar
- **Events - Empty Scheduler**
    - Simple Scheduler
- **Events - Rules**
    - Rule base handler for more automation
- **My Team**
    - My team definition page

## ---------- Settings - General ----------
### General Appearance
- Widget build to define
- **Them**: Dark/ Light (system starts on Windows Theme)
- **Windows Style**: Experimental feature to provide more unique styles [Link](https://github.com/Akascape/py-window-styles)


### Colors
- **Accent Color Mode**
    - **Windows**: Use windows accent color
    - **Manual**: you can define your own accent color either by manual put of hex color into field "Accent Color Manual" or by selecting it by "Accent Color Picker"
    - **App default**: Program will define default accent color from code it self


- **Hover Color Mode**
    - **Accent Lighter**: Accent Color be lightened by 20%
    - **Manual**: you can define your own accent color either by manual put of hex color into field "Accent Color Manual" or by selecting it by "Accent Color Picker"
    - **App default**: Program will define default accent color from code it self


### User
- **User ID**: Your Konica ID
- **User Name**: Your Name
- **User Email**: Your Email
- **User Type**
    - User: Common user of program 
    - Manager: User type handling own team (Admin password protected)


## ---------- Settings - Data Sources ----------
### Sharepoint
- Technical fields related to Sharepoint communication (not possible to change)
- **Team**: You have to select team to which you belong


### Exchange
- Technical fields related to Exchange server communication (not possible to change)
- **User ID**: You can pick the color of category created in Exchange


### Formats
- display all date and time formats used all over system
- not possible to change

## ---------- Settings - Calendar ----------
### Calendar - MY own calendar
- Setup of my general working hours I usually have. Used for Utilization forecast. Lunch brake automatically subtracted.
- **Lunch Brake duration**: Your usual lunch brake you are used to have (default 30minutes)
- **Total Time**: Your total week time - for check if you have enough hours
### Button: Upload
- Calculate according to defined data


### Calendar - KM Working/Vacation/SickDay Hours
- These hours be used in case of whole day vacation/SickDay and for KM Utilization charts and information
### Button: Upload
- Calculate according to defined data

### Workday - Start / End Events
- Events Subject which defines Start and End time of each day in Calendar.
- **Work Start** --> tells program when is particular working day starts
    - must be 0 minutes duration
- **Work End** --> tells program when is particular working day ends
    - must be 0 minutes duration


## ---------- Settings - Events - General ----------
### Skip Events
- This is the list of evens which should be skipped from registering them into TimeSheets
- Text is compared with Event subject and if a part of subject contain text then is recognized and event is not considerate for Time Sheets
- Export / import function available
    - **Export** --> Create .json file to Download folder
    - **Import** --> Drag&Drop file to marked area


### Joining Events
- This part is to cumulate multiple meeting into one in the case that condition are met:
    1. Date
    2. Project
    3. Activity
    4. Activity Description<br>
![Join Event](Libs\\Readme\\Join_Event.png)


### Parallel Events
- This handler helps to process Events which might be in parallel set in Calendar
- **Same Start Time** --> tells program what to do if 2 Events has same start time
    - **Use Shorter**: program will prioritize the shorter Event over longer one 
    - **Use Longer**: program will prioritize the longer Event over shorter one

**Divide:**<br>
![Parallel 1](Libs\\Readme\\Parallel1.png)

**Divide and Use Shorter:**<br>
![Parallel 2](Libs\\Readme\\Parallel2.png)

**When not used:**<br>
![Parallel Keep](Libs\\Readme\\Parallel_keep.png)

- has 2 methods for Events start at the same time:
    - **Use Shorter** --> will consider the shortest event as first pick
    - **Use Longer** --> will consider the longest event as first pick



## ---------- Settings - Events - Special ----------
### Lunch
- lunch is special event which should be skipped from Time sheet
- Also is used to split  parallel meeting which is planned over the lunch (like whole day meetings)
- Search text can be modified<br>

![Lunch Event](Libs\\Readme\\Lunch.png)


### Vacation
- Handler of Vacation to register correctly, If the text appeared (defined by OKBase) in the event Subject. All Events within the Vacation period and Working hours are deleted


### SickDay
- Handler of SickDay to register correctly, If the text appeared (defined by OKBase) in the event Subject. All Events within the SickDay period and Working hours are deleted

### HomeOffice
- Handled of Home Office --> currently is not doing anything as in Time Sheets there is no Location for HomeOffice


### Private
- Private is special event which should be skipped from Time sheet, User for registering time within WorkingHours, but as nonworking event 
- this Special Event has same behavior as Lunch
 

## ---------- Settings - Events - Empty ----------
### Empty Space coverage Events
- This is for filling empty space in the calendar between events where it react on **coverage** placed by each record (sum must be equal to 100%)
- Works only between “Work - Start” and “Work - End” events (only at the time when I'm at work)
- It select one from the list and use then coverage [%] to simulate real usage<br>

![Fill Empty General](Libs\\Readme\\Empty_General.png)

- Export / import function available
    - **Export** --> Create .json file to Download folder
    - **Import** --> Drag&Drop file to marked area

### Empty Spiting
This handler splits Empty space between 2 Events into multiple parts
- **Duration**: Time in minutes which is as referential: if higher then program will perform splitting<br>
- **Minimal Time**: Program will creates splits with minimal time of this parameter<br>
- **Methods**:<br>
    - **Equal Split** --> Program will divide duration by 2 (if odd number then second Event has +1 minute)<br>
    - **Random Split** --> Program will split Event duration by random number selected between "Minimal Time" and "Event Duration - Minimal Time" to secure that both splits has at lease 15 minutes<br>

![Overnight Events](Libs\\Readme\\Too_Long_Empty_Space.png)


## ---------- Settings - Events - Empty Scheduler ----------
### Events Scheduler
- This agenda is used for regular record planning like if I have Administration and Emails done after lunch at 11:30 – 12:00 of the week day
- Agenda can have multiple rows
- If in the period is another Event then this scheduled is not filled / cut
- Export / import function available
    - **Export** --> Create .json file to Download folder
    - **Import** --> Drag&Drop file to marked area

## ---------- Settings - Events - Rules ----------
### AutoFill Rules
- This special function to help automatically fill: **Project**, **Activity**, **Location**
- Program apply rule when find a **Search Text** in the Event Subject
- If there is empty text int one of the field --> then is not applied
- Export / import function available
    - **Export** --> Create .json file to Download folder
    - **Import** --> Drag&Drop file to marked area

### Activity corrections
- Change Activity in the processing of Events, when non-proper activity for Project is selected in calendar.
- Export / import function available
    - **Export** --> Create .json file to Download folder
    - **Import** --> Drag&Drop file to marked area

## ---------- Settings - Not Settable ----------
### Overnights
- This handler splits Events if they go over midnight
- This doesn't require any setup as it is programmed.
- Widely used for multi day Vacation, travel-time ...<br>

![Overnight Events](Libs\\Readme\\OverNight.png)


# --------------------------------- Development ---------------------------------
