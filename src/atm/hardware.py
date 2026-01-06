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
    
    def dispense(self, amount: int) -> None:
        if amount<=0:
          raise ValueError("Amount entered must be positive")

        if not self.amount_available(amount):
          raise ValueError("Amount not available in ATM")  

        self._amount -= amount
    
    def deposit(self, amount: int) -> None:
        if amount<=0:
          raise ValueError("Amount entered must be positive")
        self._amount += amount