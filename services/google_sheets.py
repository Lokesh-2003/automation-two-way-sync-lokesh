import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import settings
from utils.logger import logger

class SheetClient:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLE_CREDENTIALS, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(settings.SHEET_NAME).sheet1

    def get_all_leads(self):
        return self.sheet.get_all_records()

    def update_trello_id(self, row_idx, trello_id):
        try:
            self.sheet.update_cell(row_idx + 2, 5, trello_id) 
        except Exception as e:
            logger.error(f"Error updating Sheet cell: {e}")

    def update_status(self, row_idx, status):
        try:
            self.sheet.update_cell(row_idx + 2, 4, status) 
            logger.info(f"Updated Sheet Row {row_idx+2} status to {status}")
        except Exception as e:
            logger.error(f"Error updating Sheet status: {e}")