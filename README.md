# ATM Simulator

Simple ATM controller with a base class for Bank for future integration and unit tests using fake bank and cash bin implementations.

## Requirements

- Conda (Miniconda or Anaconda)
- Python 3.10

## Setup

```bash
conda env create -f environment.yml
conda activate bear_project
```

## Run tests

```bash
pytest -q
```

## Run Python

```bash
python -m pip install -e .
python
```

```python
from atm import ATMController, CashBin, Card
```

## Example usage

```python
from atm import ATMController, CashBin, Card
from tests.fakes.fake_bank import FakeBank

bank = FakeBank()
atm = ATMController(bank=bank, cash_bin=CashBin(initial_amount=200))

atm.insert_card(Card("CARD123"))
atm.enter_pin("4321")
accounts = atm.list_accounts()
atm.select_account("CHK1")
balance = atm.get_account_balance()
```

## Project layout

- `src/atm/controller.py`: main ATM flow and state machine
- `src/atm/bank.py`: bank interface and main class
- `src/atm/hardware.py`: cash bin hardware abstraction
- `src/atm/models.py`: currently only has Card dataclass
- `tests/`: pytest suite and fakes

## CI

GitHub Actions runs the pytest suite on pull requests via
`.github/workflows/tests.yml`.
