from aqt import mw
from aqt import QAction
from typing import Callable

def addAction(title:str, callback:Callable):
    action = QAction(title, mw)
    action.triggered.connect(callback)
    mw.form.menuTools.addAction(action)

