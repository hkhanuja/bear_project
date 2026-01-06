from abc import ABC, abstractmethod
from typing import Set

class BankAPI(ABC):

    @abstractmethod
    def verify_pin(self, card_id: str, pin: str) -> bool:
        pass
    
    @abstractmethod
    def get_accounts_for_card(self, card_id: str) -> Set[str]:
        pass

    @abstractmethod
    def get_balance(self, account_id: str) -> int:
        pass

    @abstractmethod
    def deposit(self, account_id: str, amount: int) -> None:
        pass

    @abstractmethod
    def check_balance(self, account_id: str, amount: int) -> bool:
        pass

    @abstractmethod
    def withdraw(self, account_id: str, amount: int) -> None:
        pass

