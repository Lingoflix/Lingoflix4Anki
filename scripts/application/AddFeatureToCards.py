from scripts.adapters.FeatureInjector.AnkiFeatureInjector import AnkiFeatureInjector

class AddFeatureToCards:
    def __init__(self, repo, injector):
        self.repo = repo
        self.injector = injector

    # def run(self, deck, feature: str):
    #     cards = self.repo.get_cards_by_deck(deck)
    #     for card in cards:
    #         if not card.has_feature(feature):
    #             card.enable_feature(feature)
    #             self.injector.apply_feature(card, feature)

    def run(self):
        pass

