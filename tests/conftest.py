import pytest
from atm import ATMController, ATMState, CashBin, Card
from tests.fakes.fake_bank import FakeBank


@pytest.fixture
def bank():
    return FakeBank()


@pytest.fixture
def atm(bank):
    return ATMController(
        bank=bank,
        cash_bin=CashBin(initial_amount=200),
    )

@pytest.fixture
def card():
    return Card("CARD123")

@pytest.fixture
def authenticated_atm(atm, card):
    atm.insert_card(card)
    assert atm.enter_pin("4321") is True
    assert atm.state == ATMState.AUTHENTICATED
    return atm


@pytest.fixture
def ready_atm(atm, card):
    atm.insert_card(card)
    assert atm.enter_pin("4321") is True
    atm.select_account("CHK1")
    assert atm.state == ATMState.ACCOUNT_SELECTED
    return atm
