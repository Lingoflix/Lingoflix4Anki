

from domain.card_repository import CardRepository
from domain.card import Card

class AnkiCardRepository(CardRepository):
    def get_cards_by_deck(self, deck):
        # Replace this with actual mw.col logic
        return [Card("id1", {"Front": "こんにちは"}, deck.id)]
    

