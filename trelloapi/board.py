from typing import Dict, List, Type

from .base_class import BaseClass
from .card_list import CardList
from .utils import trello_requests


class Board(BaseClass):
    """Board class definition. It holds and interacts with the Lists."""

    def __init__(self, trello: Type[BaseClass], board_id: str) -> None:
        super().__init__(trello.apikey, trello.token)
        self.__board_id = board_id
        board = self.fetch_data()
        self.name = board["name"]
        self.closed = board["closed"]
        self.__list_ids = []
        self.fetch_list_ids()

    @property
    def board_id(self) -> str:
        return self.__board_id

    @property
    def list_ids(self) -> List[str]:
        return self.__list_ids

    def fetch_data(self) -> Dict[str, str]:
        """Loads board information."""
        url = f"https://api.trello.com/1/boards/{self.board_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            board = {
                "name": response["data"]["name"],
                "closed": response["data"]["closed"],
            }
        else:
            board = {"name": None, "closed": None}
        return board

    def has_list(self, list_id: str) -> bool:
        """Check if the List exists on the Board."""
        has_it = False
        url = f"https://api.trello.com/1/lists/{list_id}"
        response = trello_requests.get_request(self, url)
        if trello_requests.was_successful(response):
            if response["data"]["idBoard"] == self.board_id:
                has_it = True
        return has_it

    def add_list_id(self, list_id: str) -> List[str]:
        """Add a new List ID to the Board."""
        if self.has_list(list_id):
            if len(self.list_ids) == 0:
                self.list_ids.append(list_id)
            else:
                if list_id not in self.list_ids:
                    self.list_ids.append(list_id)
        return self.list_ids

    def fetch_list_ids(self) -> Dict[str, str]:
        """Requests all List IDs the current Board has from Trello API."""
        url = f"https://api.trello.com/1/boards/{self.board_id}/lists"
        response = trello_requests.get_request(self, url)
        if response["status"] == 200:
            for trello_list in response["data"]:
                self.add_list_id(trello_list["id"])
        else:
            self.__list_ids = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.list_ids,
        }

    def card_list(self, list_id: str) -> Type[CardList]:
        """Get by ID a new instance of a CardList the Board has."""
        return CardList(self, list_id) if self.has_list(list_id) else None

    def __str__(self) -> str:
        """Print Board by ID, and Name."""
        return f"{self.board_id} - {self.name}"
