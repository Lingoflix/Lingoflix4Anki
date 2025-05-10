
from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from aqt.gui_hooks import card_will_show 
from aqt.utils import showInfo


def select_dropdown(title:str, prompt:str, options:list):
    selection, ok = QInputDialog.getItem(mw, title, prompt, options, 0, False)
    return selection


def select_platform():
    return select_dropdown("Choose platform",
            "On what platform will you search for videos ?",
            ['Desktop', 'Android', 'iOS']
        )


def select_deck():
    decks = list(mw.col.decks.all_names_and_ids())
    deck_names = [d.name for d in decks]
    return select_dropdown("Select Deck", "Choose a deck:", deck_names)

