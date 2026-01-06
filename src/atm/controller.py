from enum import Enum, auto
from .bank import BankAPI
from .hardware import CashBin
from .models import Card


class ATMState(Enum):
    """ATM state machine phases."""
    IDLE = auto()
    CARD_INSERTED = auto()
    AUTHENTICATED = auto()
    ACCOUNT_SELECTED = auto()


class ATMController:
    """Coordinate actions and acts as the main controller for the ATM."""

    def __init__(self, bank: BankAPI, cash_bin: CashBin) -> None:
        self._bank = bank
        self._cash_bin = cash_bin

        self._state: ATMState = ATMState.IDLE
        self._card = None
        self._selected_account = None

    @property
    def state(self) -> ATMState:
        """Current state of the ATM."""
        return self._state

    def _require_state(self, *allowed: ATMState) -> None:
        """Guard against invalid state transitions and eject if invalid."""
        if self._state not in allowed:
            current_state = self._state
            self.eject_card()
            raise RuntimeError(f"Operation not allowed in state {current_state.name}. ")

    def _validate_amount(self, amount: int) -> None:
        """Validate cash amounts before any cash operation."""
        if not isinstance(amount, int):
            self.eject_card()
            raise RuntimeError("Amount must be an integer.")
        if amount <= 0:
            self.eject_card()
            raise RuntimeError("Amount entered must be positive")

    def insert_card(self, card: Card) -> None:
        """Insert a card and move into CARD_INSERTED state."""
        self._require_state(ATMState.IDLE)
        self._card = card
        self._selected_account = None
        self._state = ATMState.CARD_INSERTED

    def eject_card(self) -> None:
        """Eject the card and reset the session state."""
        self._card = None
        self._selected_account = None
        self._state = ATMState.IDLE

    def enter_pin(self, pin: str) -> bool:
        """Verify PIN and authenticate the session."""
        self._require_state(ATMState.CARD_INSERTED)
        assert self._card is not None

        if self._bank.verify_pin(self._card, pin):
            self._state = ATMState.AUTHENTICATED
            return True

        self.eject_card()
        raise RuntimeError("Entered PIN is incorrect, card ejected.")

    def select_account(self, account_id: str) -> None:
        """Select an account for transactions after authentication."""
        self._require_state(ATMState.AUTHENTICATED)

        accounts = self._bank.get_accounts_for_card(self._card)
        if account_id not in accounts:
            self.eject_card()
            raise RuntimeError("Account does not belong to this card, card ejected.")
        self._selected_account = account_id
        self._state = ATMState.ACCOUNT_SELECTED

    def list_accounts(self) -> set[str]:
        """List accounts available for the authenticated card."""
        self._require_state(ATMState.AUTHENTICATED)
        return self._bank.get_accounts_for_card(self._card)

    def get_account_balance(self) -> int:
        """Return the balance for the selected account."""
        self._require_state(ATMState.ACCOUNT_SELECTED)
        return self._bank.get_balance(self._card, self._selected_account)

    def deposit(self, amount: int) -> int:
        """Deposit cash into the selected account and return new balance."""
        self._require_state(ATMState.ACCOUNT_SELECTED)
        self._validate_amount(amount)

        self._cash_bin.accept_deposit(amount)
        self._bank.deposit(self._card, self._selected_account, amount)
        return self._bank.get_balance(self._card, self._selected_account)

    def withdraw(self, amount: int) -> int:
        """Withdraw cash from the selected account and return new balance."""
        self._require_state(ATMState.ACCOUNT_SELECTED)
        self._validate_amount(amount)

        if not self._cash_bin.can_dispense(amount):
            self.eject_card()
            raise RuntimeError("ATM does not have this much amount, card ejected.")

        if not self._bank.check_balance(self._card, self._selected_account, amount):
            account_balance = self._bank.get_balance(self._card, self._selected_account)
            self.eject_card()
            raise RuntimeError(
                f"Account does not have this much amount, you have {account_balance} amount, card ejected."
            )

        self._bank.withdraw(self._card, self._selected_account, amount)
        self._cash_bin.dispense(amount)

        return self._bank.get_balance(self._card, self._selected_account)
