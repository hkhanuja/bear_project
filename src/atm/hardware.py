class CashBin:
    """Represent the ATM's cash on hand and its ability to dispense and accept cash."""

    def __init__(self, initial_amount: int):
        """Initialize the cash bin with the given amount. We don't have to worry about denominations since there are only $1 bills in this world"""
        self._amount = initial_amount

    def amount(self) -> int:
        """Return the current cash available in the bin."""
        return self._amount

    def amount_available(self, amount: int) -> bool:
        """Return True when the bin has at least the requested amount."""
        if self._amount >= amount:
            return True
        return False

    def can_dispense(self, amount: int) -> bool:
        """Return True when the bin can dispense the requested amount."""
        if not self.amount_available(amount):
            return False
        return True

    def dispense(self, amount: int) -> None:
        """Remove cash from the bin."""
        self._amount -= amount

    def accept_deposit(self, amount: int) -> None:
        """Add cash to the bin."""
        self._amount += amount
