import requests
from config import settings
from utils.logger import logger

class TrelloClient:
    def __init__(self):
        self.base_url = "https://api.trello.com/1"
        self.auth_params = {
            'key': settings.TRELLO_KEY,
            'token': settings.TRELLO_TOKEN
        }

    def get_lists(self):
        url = f"{self.base_url}/boards/{settings.TRELLO_BOARD_ID}/lists"
        try:
            response = requests.get(url, params=self.auth_params)
            response.raise_for_status()
            return {lst['name'].upper(): lst['id'] for lst in response.json()}
        except Exception as e:
            logger.error(f"Failed to fetch Trello lists: {e}")
            return {}

    def get_all_cards(self):
        url = f"{self.base_url}/boards/{settings.TRELLO_BOARD_ID}/cards"
        try:
            response = requests.get(url, params=self.auth_params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch Trello cards: {e}")
            return []

    def create_card(self, list_id, name, desc):
        url = f"{self.base_url}/cards"
        params = {
            **self.auth_params,
            'idList': list_id,
            'name': name,
            'desc': desc
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            logger.info(f"Created Trello card: {name}")
            return response.json().get('id')
        except Exception as e:
            logger.error(f"Failed to create card: {e}")
            return None

    def update_card_list(self, card_id, list_id):
        url = f"{self.base_url}/cards/{card_id}"
        params = {**self.auth_params, 'idList': list_id}
        try:
            requests.put(url, params=params)
            logger.info(f"Moved Trello card {card_id} to new list.")
        except Exception as e:
            logger.error(f"Failed to move card: {e}")