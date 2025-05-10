

import urllib

from .AddFeatureToCards import AddFeatureToCards
from scripts.adapters.AnkiFeatureInjector import AnkiFeatureInjector
from scripts.adapters.AnkiMediaManager import AnkiMediaManager
from scripts.adapters.VideoSearcher import VideoSearcher

import aqt


media = AnkiMediaManager(addon_name="lingoflix4anki")


def addVideoSearcherToDeck(deck_name:str, platform:str):
    vidSearcher = VideoSearcher(platform) # actually not the platform, but the UI element: webview, note model ...
    vidSearcherBuilder = vidSearcher.generate()

    cards = aqt.mw.col.decks.id(deck_name)
    injector = AnkiFeatureInjector('video_searcher', vidSearcherBuilder, platform)
    injector.apply_feature(cards) 
    # if it's for desktop, we added a callback.
    # But if it's for mobile, we added a script that 

