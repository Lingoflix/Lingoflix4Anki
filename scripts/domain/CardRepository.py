

from abc import ABC, abstractmethod
from typing import List
from .card import Deck, Card

class CardRepository(ABC):
    @abstractmethod
    def get_cards_by_deck(self, deck: Deck) -> List[Card]:
        ...



