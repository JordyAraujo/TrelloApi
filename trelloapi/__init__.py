"""Library initializer."""
from .board import Board
from .utils import trello_requests


class Trello:
    """Trello class definition. It holds and interacts with the Boards."""

    def __init__(self, apikey, token):
        """Class constructor. Boards are set when the request is successful."""
        self.apikey = apikey
        self.token = token
        self.auto_load()
        self.board_ids = []
        self.fetch_board_ids()

    def auto_load(self):
        """Load all user data."""
        url = "https://api.trello.com/1/members/me"
        response = trello_requests.get_request(self, url)
        if response["status"] == 200:
            self.user = {
                "id": response["data"]["id"],
                "fullName": response["data"]["fullName"],
                "url": response["data"]["url"],
                "username": response["data"]["username"],
            }
        else:
            self.user = {
                "id": None,
                "fullName": None,
                "url": None,
                "username": None,
            }
        return self.user

    def has_board(self, board_id):
        """Check if the Board exists for user."""
        url = f"https://api.trello.com/1/boards/{board_id}"
        response = trello_requests.get_request(self, url)
        return response["status"] == 200

    def add_board_id(self, board_id):
        """Add a new Board ID to the list."""
        if self.has_board(board_id):
            if len(self.board_ids) == 0:
                self.board_ids.append(board_id)
            else:
                if board_id not in self.board_ids:
                    self.board_ids.append(board_id)
        return self.board_ids

    def fetch_board_ids(self):
        """Requests all Board IDs the current user has from Trello API."""
        url = "https://api.trello.com/1/members/me/boards"
        response = trello_requests.get_request(self, url)
        if response["status"] == 200:
            for board in response["data"]:
                self.add_board_id(board["id"])
        else:
            self.board_ids = []
        return {
            "status": response["status"],
            "url": url,
            "data": self.board_ids,
        }

    def board_by_id(self, board_id):
        """Get a new instance of a board by ID."""
        return Board(self, board_id) if self.has_board(board_id) else None

    def __str__(self):
        """Print current User by name."""
        return f'{self.user["username"]} - {self.user["fullName"]}'
