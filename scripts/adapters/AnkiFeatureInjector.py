

from scripts.domain.FeatureInjector import FeatureInjector
from scripts.domain.Card import Card
from scripts.adapters.AnkiCard import AnkiCard
from scripts.domain.Platforms import Platforms

import aqt
from aqt import mw
from aqt.utils import showInfo
from aqt.gui_hooks import card_will_show
from scripts.adapters.AnkiMediaManager import AnkiMediaManager
import urllib
from typing import Callable


class AnkiFeatureInjector(FeatureInjector):
    # Defines the injection strategy

    def __init__(self, feature_name: str, feature_script: Callable, target_platform:str):
        super().__init__(feature_name, feature_script)
        self.target_platform = target_platform
        self.feature_script = feature_script


    def _inject_in_webview(self, html, card, kind):
    # logger.debug("hook called: " + kind)
        if kind == "reviewAnswer":
            html += self.feature_script
        return html
    

    def _inject_in_template(self, cards: list[AnkiCard]):

        aqt.utils.showInfo(f"Adding {self.feature_name} to {len(cards)} card(s)...")

        # 1. Enable feature ---------------
        # Ensure cards' note models support the feature
        # Check if each model has the conditional field
        models = set(card.note().model()["name"] for card in cards)
        for model in models:
            if self.feature_name not in model["flds"]:
                new_field = mw.col.models.newField(self.feature_name)
                mw.col.models.addField(model, new_field)
        else : 
                pass

        # 2. Inject feature ---------------
        # Inject HTML into template(s)
        for template in model["tmpls"]:
            side = "afmt" # "qfmt" - only include videos in answer for now

            # Add the conditional field
            cond_field = f"{{{{#{self.feature_name}}}}}"
            if cond_field not in template[side]:
                injection = f"\n{{{{#{self.feature_name}}}}}{self.feature_script}{{{{/{self.feature_name}}}}}"
                template[side] += injection
                print(f"Injected into {template['name']} [{side}]")

            # Add a hidden div so that the JS can easily get the front's value
            template[side] += '\n<div id="question-value" style="display:none">{{Front}}</div>'

        aqt.utils.showInfo("Done.")


    def apply_feature(self, cards):
        if self.target_platform == Platforms.DESKTOP:
                card_will_show.append(self._inject_in_webview)
        
        else : # mobile
                    
            if self.target_platform == Platforms.ANDROID: 
                # inject script in template copy
                self._inject_in_template(cards)
                # Need to replace the variables with the actual values

            elif self.target_platform == Platforms.IOS:
                injection = '' # or lambda

