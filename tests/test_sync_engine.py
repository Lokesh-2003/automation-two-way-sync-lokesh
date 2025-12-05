import unittest
from unittest.mock import MagicMock, patch
from sync.engine import SyncEngine

class TestSyncEngine(unittest.TestCase):

    def setUp(self):
        self.trello_patcher = patch('sync.engine.TrelloClient')
        self.sheet_patcher = patch('sync.engine.SheetClient')
        self.MockTrello = self.trello_patcher.start()
        self.MockSheet = self.sheet_patcher.start()
        self.engine = SyncEngine()
        self.engine.trello.get_lists.return_value = {
            "TODO": "list_todo_123",
            "IN_PROGRESS": "list_progress_456",
            "DONE": "list_done_789"
        }

    def tearDown(self):
        self.trello_patcher.stop()
        self.sheet_patcher.stop()

    def test_initial_sync_creates_card(self):
        self.engine.sheet.get_all_leads.return_value = [
            {'ID': '1', 'Name': 'Alice', 'Email': 'alice@test.com', 'Status': 'NEW', 'Trello_Card_ID': ''}
        ]
        self.engine.trello.get_all_cards.return_value = [] 
        self.engine.sync()
        self.engine.trello.create_card.assert_called_with(
            "list_todo_123", 'Alice', 'Email: alice@test.com'
        )
        self.engine.sheet.update_trello_id.assert_called()

    def test_sync_updates_sheet_status(self):
        self.engine.sheet.get_all_leads.return_value = [
            {'ID': '1', 'Name': 'Bob', 'Status': 'NEW', 'Trello_Card_ID': 'card_999'}
        ]
        self.engine.trello.get_all_cards.return_value = [
            {'id': 'card_999', 'idList': 'list_done_789'} 
        ]
        self.engine.sync()
        self.engine.sheet.update_status.assert_called_with(0, 'QUALIFIED')

    def test_idempotency_no_duplicates(self):
        self.engine.sheet.get_all_leads.return_value = [
            {'ID': '1', 'Name': 'Charlie', 'Status': 'NEW', 'Trello_Card_ID': 'card_888'}
        ]
        self.engine.trello.get_all_cards.return_value = [
            {'id': 'card_888', 'idList': 'list_todo_123'} 
        ]
        self.engine.sync()
        self.engine.trello.create_card.assert_not_called()
        self.engine.sheet.update_status.assert_not_called()

if __name__ == '__main__':
    unittest.main()