from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import gspread

# --- Google Calendar + Sheets Setup ---
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets"
]

# Use a generic placeholder filename (do not upload your real JSON!)
SERVICE_ACCOUNT_FILE = "service_account.json"

# Authenticate
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build Calendar service
calendar_service = build("calendar", "v3", credentials=creds)

# Build Sheets client
gc = gspread.authorize(creds)

# Replace with your own Google Sheet ID
SHEET_ID = "YOUR_SHEET_ID"
sheet = gc.open_by_key(SHEET_ID).sheet1

# Replace with your own Calendar ID (usually your Gmail address or shared calendar ID)
CALENDAR_ID = "YOUR_CALENDAR_ID"

# --- Fetch events from Google Calendar (past + future) ---
time_min = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=365)).isoformat()
time_max = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365)).isoformat()

events_result = calendar_service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=time_min,
    timeMax=time_max,
    maxResults=2500,
    singleEvents=True,
    orderBy="startTime"
).execute()

events = events_result.get("items", [])

# --- Prepare data ---
data = [["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description", "Location"]]

for event in events:
    subject = event.get("summary", "No Title")
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    desc = event.get("description", "")
    location = event.get("location", "")

    # Convert datetime into readable format
    if "T" in start:
        start_date, start_time = start.split("T")
        start_time = start_time.replace("Z", "")
    else:
        start_date, start_time = start, ""

    if "T" in end:
        end_date, end_time = end.split("T")
        end_time = end_time.replace("Z", "")
    else:
        end_date, end_time = end, ""

    data.append([subject, start_date, start_time, end_date, end_time, desc, location])

# --- Write data into Google Sheets ---
if len(data) > 1:
    sheet.update(range_name="A1", values=data)   # keyword form works in gspread 5 and 6
    print(f"{len(data)-1} events fetched from Google Calendar and written to Google Sheets!")
else:
    print("No events found in the given time range.")
