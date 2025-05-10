import urllib.parse, os,shutil,json
from os.path import join as pathJoin
import requests

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from aqt.gui_hooks import card_will_show 
from aqt.utils import showInfo

from .scripts.adapters.Logging import logger

from .scripts.adapters import VideoHandler

from .scripts import domain


# aqt extension -----------
# Chooses the platform: "On what platform will you search for videos ? 
    # Note: videos will appear in any deck, regardless of the platform you used to add them": Android, iOs
# chooses the Deck
# everytime a card is displayed in the given deck, 
    # a hook is called and a script is injected in the webview.