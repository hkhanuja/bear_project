import pytest
from atm import ATMState


def test_withdrawal_updates(ready_atm, bank, card):
    new_balance = ready_atm.withdraw(30)
    assert new_balance == 70
    assert bank.get_balance(card, "CHK1") == 70
    assert ready_atm._cash_bin.amount() == 170


def test_withdraw_insufficient_funds_raises(ready_atm, bank, card):
    with pytest.raises(RuntimeError, match=r"Account does not have this much amount"):
        ready_atm.withdraw(150)
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200


def test_withdraw_out_of_cash_raises(ready_atm, bank, card):
    
    with pytest.raises(RuntimeError, match=r"ATM does not have this much amount"):
        ready_atm.withdraw(500)
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200


@pytest.mark.parametrize("amount", [0, -10])
def test_withdraw_rejects_non_positive_amount(ready_atm, bank, amount, card):
    with pytest.raises(RuntimeError, match=r"Amount entered must be positive"):
        ready_atm.withdraw(amount)
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200


def test_withdraw_rejects_non_integer_amount(ready_atm, bank, card):
    with pytest.raises(RuntimeError, match=r"Amount must be an integer"):
        ready_atm.withdraw("10.5")
    assert ready_atm.state == ATMState.IDLE
    assert bank.get_balance(card, "CHK1") == 100
    assert ready_atm._cash_bin.amount() == 200
