"""Bank API abstraction for the ATM controller."""

from abc import ABC, abstractmethod
from typing import Set

from .models import Card

class BankAPI(ABC):
    """Interface for bank operations used by the ATM."""

    @abstractmethod
    def verify_pin(self, card: Card, pin: str) -> bool:
        """Return True when the PIN is valid for the card."""
        pass
    
    @abstractmethod
    def get_accounts_for_card(self, card: Card) -> Set[str]:
        """Return account IDs linked to the card."""
        pass

    @abstractmethod
    def get_balance(self, card: Card, account_id: str) -> int:
        """Return the current balance for an account."""
        pass

    @abstractmethod
    def deposit(self, card: Card, account_id: str, amount: int) -> None:
        """Deposit cash into an account."""
        pass

    @abstractmethod
    def check_balance(self, card: Card, account_id: str, amount: int) -> bool:
        """Return True when the account can cover the withdrawal."""
        pass

    @abstractmethod
    def withdraw(self, card: Card, account_id: str, amount: int) -> None:
        """Withdraw cash from an account."""
        pass
