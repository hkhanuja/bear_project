class CashBin:
    
    #we can use amount here since amount and bills will be same, there are only $1 bills in the world
    def __init__(self, initial_amount: int):
        self._amount = initial_amount
    
    def amount(self) -> int:
        return self._amount

    def amount_available(self, amount: int) -> bool:
        if self._amount >= amount:
            return True
        return False
    
    def can_dispense(self, amount: int) -> bool:
        if not self.amount_available(amount):
            return False
        return True
    
    def dispense(self, amount: int) -> bool:
        self._amount -= amount

    def accept_deposit(self, amount: int) -> None:
        self._amount += amount