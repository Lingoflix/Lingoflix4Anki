import sys, os
sys.path.append(os.path.dirname(__file__))

from scripts.ui.AnkiMenu import addAction
from scripts.ui.dialog import select_platform, select_deck
from scripts.application.AddVideoSearcherToCards import addVideoSearcherToDeck
from scripts.adapters import VideoHandler

def videoSearcherMenu() -> str:

    platform = select_platform()
    deck = select_deck()
    addVideoSearcherToDeck(deck, platform)

    VideoHandler.start_server()

    

addAction("🎥 Add Lingoflix to flashcards", videoSearcherMenu)
# addAction("🎥(for Ankimobile) Synchronize with Lingoflix")

