from dataclass import dataclass

@dataclass(frozen=True)
class Card:
    card_id: str
