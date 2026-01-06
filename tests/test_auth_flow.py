import pytest
from atm import ATMState


@pytest.fixture
def authenticated_atm(atm, card):
    atm.insert_card(card)
    assert atm.enter_pin("4321") is True
    assert atm.state == ATMState.AUTHENTICATED
    return atm


def test_auth_flow_success(atm, card):
    atm.insert_card(card)
    assert atm.state == ATMState.CARD_INSERTED

    assert atm.enter_pin("4321") is True
    assert atm.state == ATMState.AUTHENTICATED

    assert list(atm.list_accounts().keys()) == ["CHK1"]

    atm.select_account("CHK1")
    assert atm.state == ATMState.ACCOUNT_SELECTED


def test_insert_card_rejects_when_already_inserted(atm, card):
    atm.insert_card(card)
    with pytest.raises(RuntimeError, match=r"Operation not allowed in state CARD_INSERTED"):
        atm.insert_card(card)
    assert atm.state == ATMState.IDLE


def test_enter_pin_requires_card(atm):
    with pytest.raises(RuntimeError, match=r"Operation not allowed in state IDLE"):
        atm.enter_pin("4321")
    assert atm.state == ATMState.IDLE


def test_enter_pin_failure_ejects_card(atm, card):
    atm.insert_card(card)
    with pytest.raises(RuntimeError, match=r"Entered PIN is incorrect"):
        atm.enter_pin("0000")
    assert atm.state == ATMState.IDLE


def test_authentication_required_before_listing_accounts(atm, card):
    atm.insert_card(card)
    with pytest.raises(RuntimeError, match=r"Operation not allowed in state CARD_INSERTED"):
        atm.list_accounts()
    assert atm.state == ATMState.IDLE


def test_list_accounts_keeps_state_authenticated(authenticated_atm):
    assert list(authenticated_atm.list_accounts().keys()) == ["CHK1"]
    assert authenticated_atm.state == ATMState.AUTHENTICATED


def test_select_account_invalid_ejects_card(authenticated_atm):
    with pytest.raises(RuntimeError, match=r"Account does not belong to this card"):
        authenticated_atm.select_account("SAV1")
    assert authenticated_atm.state == ATMState.IDLE

def test_withdrawing_before_selecting_account(atm, card):
    atm.insert_card(card)
    atm.enter_pin("4321")
    with pytest.raises(RuntimeError, match=r"Operation not allowed in state AUTHENTICATED"):
        atm.withdraw(50)
    assert atm.state == ATMState.IDLE

def test_depositing_before_selecting_account(atm, card):
    atm.insert_card(card)
    atm.enter_pin("4321")
    with pytest.raises(RuntimeError, match=r"Operation not allowed in state AUTHENTICATED"):
        atm.deposit(50)
    assert atm.state == ATMState.IDLE