import sys, os

from scripts.ui.AnkiMenu import addAction
from scripts.application.AddVideoSearcherToCards import addVideoSearcherToDeck

sys.path.append(os.path.dirname(__file__))

from scripts.ui.dialog import select_platform, select_deck

from aqt.gui_hooks import card_will_show


def videoSearcherMenu() -> str:

    platform = select_platform()
    deck = select_deck()
    feature = addVideoSearcherToDeck(deck, platform)
    feature.run(platform)
    

addAction("🎥 Add Lingoflix to flashcards", videoSearcherMenu)
addAction("🎥(for Ankimobile) Synchronize with Lingoflix")