class Card:
    def __init__(self, id: str, fields: dict, deck_id: str):
        self.id = id
        self.fields = fields
        self.deck_id = deck_id
        self.features = set()

    def enable_feature(self, feature: str):
        self.features.add(feature)

    def has_feature(self, feature: str) -> bool:
        return feature in self.features
    
    def disable_feature(self, feature: str):
        raise NotImplementedError()

    def remove_feature(self, feature: str):
        raise NotImplementedError()
    
        


class Deck:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name