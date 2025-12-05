Automation & Integration: Two-Way Sync (Google Sheets ↔ Trello)

This project implements a robust two-way synchronization engine between a Lead Tracker(Google Sheets) and a Work Tracker (Trello).

It ensures that sales leads and development tasks remain consistent across platforms without manual data entry:
Forward Sync (Sheet → Trello): New leads in Google Sheets automatically generate cards in Trello.
Backward Sync (Trello → Sheet): Status changes in Trello ( "TO DO" to "Done") automatically update the status in Google Sheets.

Tech Stack:
Language: Python 
APIs: Trello REST API, Google Sheets API 
Architecture: Polling-based synchronization loop
Testing: unittest with unittest.mock for safe logic verification

Architecture & Flow

The system runs a continuous polling loop (configurable interval) to check for state changes in both systems.



A[Google Sheet] -- Reads Leads --> B(Sync Engine / Python)
C[Trello Board] -- Reads Cards --> B
    
B -- Creates Card if New --> C
B -- Updates Status if Changed --> A
B -- Moves Card if Status Changed --> C

State Mapping Logic:

Google Sheet Status,  Trello List Name
NEW,                   TODO
CONTACTED,             IN_PROGRESS
QUALIFIED,             DONE
LOST,                  DONE

Configuration Environment Variables:
TRELLO_API_KEY=Api-key
TRELLO_TOKEN=trello-token
TRELLO_BOARD_ID=board-id
GOOGLE_SHEET_NAME=Lead Tracker
SYNC_INTERVAL=60

Google Service Account

    Google Cloud JSON key in the root directory and rename it to "service_account.json".
next: Open service_account.json, copy the client_email, and Share your Google Sheet with that email (Editor access).

Google Sheet Headers Ensure your Sheet (Tab 1) has exactly these headers in 
Row 1:
 ID | Name | Email | Status | Trello_Card_ID | Last_Synced


Installation:

python -m venv venv
.venv/Scripts/Activate.ps1

Run: 

python -m unittest tests/test_sync_engine.py  
python main.py
