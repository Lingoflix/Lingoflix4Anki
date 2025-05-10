

import urllib

from scripts.adapters.AnkiFeatureInjector import AnkiFeatureInjector
from scripts.adapters.VideoSearcher import VideoSearcher
from scripts.domain.Platforms import Platforms

import aqt


def addVideoSearcherToDeck(deck_name:str, platform:str):
    platform = Platforms(platform)

    aqt.utils.showInfo(f"Adding Lingoflix to {deck_name}. Building the video searcher ...")
    vidSearcher = VideoSearcher(platform) # actually not the platform, but the UI element: webview, note model ...
    vidSearcherBuilder = vidSearcher.generate()

    # Get cards
    deck_id = aqt.mw.col.decks.id("Default")
    card_ids = aqt.mw.col.find_cards(f"did:{deck_id}")
    cards = [aqt.mw.col.get_card(cid) for cid in card_ids]

    injector = AnkiFeatureInjector('video_searcher', vidSearcherBuilder, platform)
    injector.apply_feature(cards) 

