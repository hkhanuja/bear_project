from abc import ABC, abstractmethod
from .models import Card
from typing import Set

class BankAPI(ABC):

    @abstractmethod
    def verify_pin(self, card: Card, pin: str) -> bool:
        pass
    
    @abstractmethod
    def get_accounts_for_card(self, card: Card) -> Set[str]:
        pass

    @abstractmethod
    def get_balance(self, card: Card, account_id: str) -> int:
        pass

    @abstractmethod
    def deposit(self, card: Card, account_id: str, amount: int) -> None:
        pass

    @abstractmethod
    def check_balance(self, card: Card, account_id: str, amount: int) -> bool:
        pass

    @abstractmethod
    def withdraw(self, card: Card, account_id: str, amount: int) -> None:
        pass

