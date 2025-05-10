

from abc import ABC, abstractmethod
from scripts.domain.Card import Card

class FeatureInjector(ABC):
    def __init__(self, feature_name, feature_script):
        self.feature_name = feature_name
        self.feature_script = feature_script

    @abstractmethod
    def apply_feature(self, cards: list[Card]) -> None:
        # Add a conditional field in the template
        raise NotImplementedError()
    





