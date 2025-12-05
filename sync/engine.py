from services.trello_api import TrelloClient
from services.google_sheets import SheetClient
from utils.logger import logger

class SyncEngine:
    def __init__(self):
        self.trello = TrelloClient()
        self.sheet = SheetClient()
        self.status_to_list = {
            "NEW": "TODO",
            "CONTACTED": "IN_PROGRESS",
            "QUALIFIED": "DONE",
            "LOST": "DONE" 
        }
        self.list_id_to_status = {}

    def refresh_mappings(self):
        lists = self.trello.get_lists() 
        self.map_name_to_id = lists
        for name, list_id in lists.items():
            if name == "TODO": self.list_id_to_status[list_id] = "NEW"
            elif name == "IN_PROGRESS": self.list_id_to_status[list_id] = "CONTACTED"
            elif name == "DONE": self.list_id_to_status[list_id] = "QUALIFIED"

    def sync(self):
        logger.info("Starting Sync Cycle...")
        self.refresh_mappings()
        
        leads = self.sheet.get_all_leads()
        trello_cards = {c['id']: c for c in self.trello.get_all_cards()}
        for idx, lead in enumerate(leads):
            if not lead.get('Name') or not lead.get('Status'):
                continue
            self._handle_lead_sync(idx, lead, trello_cards)
        leads_updated = self.sheet.get_all_leads() 
        for idx, lead in enumerate(leads_updated):
            if not lead.get('Name') or not lead.get('Status'):
                continue
            self._handle_task_sync(idx, lead, trello_cards)

    def _handle_lead_sync(self, idx, lead, trello_cards):
        trello_id = lead.get('Trello_Card_ID')
        status = lead.get('Status', 'NEW').upper()
        target_list_id = self.map_name_to_id.get(self.status_to_list.get(status))
        if not target_list_id:
            logger.warning(f"Invalid status in sheet: {status}")
            return
        if not trello_id:
            new_id = self.trello.create_card(target_list_id, lead['Name'], f"Email: {lead['Email']}")
            if new_id:
                self.sheet.update_trello_id(idx, new_id)
        
        elif trello_id in trello_cards:
            card = trello_cards[trello_id]
            if card['idList'] != target_list_id:
                self.trello.update_card_list(trello_id, target_list_id)

    def _handle_task_sync(self, idx, lead, trello_cards):
        trello_id = lead.get('Trello_Card_ID')
        if not trello_id or trello_id not in trello_cards:
            return
        card = trello_cards[trello_id]
        current_list_id = card['idList']
        mapped_status = self.list_id_to_status.get(current_list_id)
        if mapped_status and mapped_status != lead['Status']:
             self.sheet.update_status(idx, mapped_status)