import pytest
from atm import ATMState


def test_deposit_updates(ready_atm, bank, card):
    new_balance = ready_atm.deposit(25)
    assert new_balance == 125
    assert bank.get_balance(card, "CHK1") == 125
    assert ready_atm._cash_bin.amount() == 225


@pytest.mark.parametrize("amount", [0, -10])
def test_deposit_rejects_non_positive_amount(ready_atm, bank, amount, card):
    with pytest.raises(RuntimeError, match=r"Amount entered must be positive"):
        ready_atm.deposit(amount)
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200


def test_deposit_rejects_non_integer_amount(ready_atm, bank, card):
    with pytest.raises(RuntimeError, match=r"Amount must be an integer"):
        ready_atm.deposit("10.5")
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200
