from PyQt5.QtWidgets import QAction
from aqt import mw
from scripts.application.AddVideoSearcherToCards import AddVideoSearcherToCards
from scripts.adapters.AnkiCardRepository import AnkiCardRepository
from scripts.adapters.AnkiFeatureInjector import AnkiFeatureInjector
from scripts.domain.Card import Deck

from typing import Callable

def addAction(title:str, callback:Callable):
    action = QAction(title, mw)
    action.triggered.connect(callback)
    mw.form.menuTools.addAction(action)

