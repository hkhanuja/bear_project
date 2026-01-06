from atm.bank import BankAPI
from atm.models import Card

class FakeBank(BankAPI):
    def __init__(self):
        self._card_pins = {"CARD123": "4321"}
        self._accounts = {"CARD123": {"CHK1": 100}}

    def verify_pin(self, card: Card, pin: str) -> bool:
        return self._card_pins.get(card.card_id) == pin

    def get_accounts_for_card(self, card: Card,):
        return self._accounts.get(card.card_id, set())

    def get_balance(self, card: Card, account_id: str) -> int:
        return self._accounts[card.card_id][account_id]

    def deposit(self, card: Card, account_id: str, amount: int) -> None:
        self._accounts[card.card_id][account_id] += amount

    def check_balance(self, card: Card, account_id: str, amount: int) -> bool:
        if self._accounts[card.card_id][account_id] < amount:
            return False
        return True

    def withdraw(self, card: Card, account_id: str, amount: int) -> None:
        self._accounts[card.card_id][account_id] -= amount