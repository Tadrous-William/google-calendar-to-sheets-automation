# Google Calendar to Google Sheets Automation

A Python script that reads every event from a Google Calendar (one year back and one year ahead) and writes them into a Google Sheet as a clean table. Useful for reports, shared schedules and keeping a record of meetings.

## What you get in the sheet

| Subject | Start Date | Start Time | End Date | End Time | Description | Location |
|---|---|---|---|---|---|---|

One row per event, up to 2,500 events.

## How it works

1. Logs in with a Google **service account** (no browser sign-in needed).
2. Reads events from the Google Calendar API.
3. Splits each start and end into date and time, and handles all-day events.
4. Writes the table into the first tab of your Google Sheet with `gspread`.

## Setup

1. In Google Cloud, enable the **Google Calendar API** and **Google Sheets API**, create a service account and download its key as `service_account.json` next to the script. (Never upload this file.)
2. Share your calendar and your Google Sheet with the service account's email.
3. In `dates.py`, set `SHEET_ID` and `CALENDAR_ID`.
4. Install and run:
   ```bash
   pip install google-api-python-client google-auth gspread
   python dates.py
   ```

`Google Calendar.pdf` shows the process with screenshots.

## Tech

Python · Google Calendar API · Google Sheets API · gspread · service account auth
