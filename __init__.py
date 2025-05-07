import urllib.parse, os,shutil,json
from os.path import join as pathJoin
import requests

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from aqt.gui_hooks import card_will_show 
from aqt.utils import showInfo

from .scripts.Logging import logger

from .scripts import VideoHandler

logpath = pathJoin(os.path.dirname(__file__), 'lingoflix.log')


# def log(text):
#     with open(logpath, 'a') as f:
#         f.write('-'*50 + '\n' + text)


def select_platform():
    platforms  = ['Desktop', 'Android', 'iOS']
    platform, ok = QInputDialog.getItem(mw, "On what platform will you search for videos ?", "Choose a deck:", platforms, 0, False)
    return platform

def select_deck():
    decks = list(mw.col.decks.all_names_and_ids())
    deck_names = [d.name for d in decks]
    deck_name, ok = QInputDialog.getItem(mw, "Select Deck", "Choose a deck:", deck_names, 0, False)
    return deck_name


def importMediaFiles(addon='lingoflix4anki'):
        shutil.copytree(
            pathJoin(os.path.dirname(__file__), addon), 
            pathJoin(mw.pm.profileFolder(), "collection.media", addon),
            dirs_exist_ok=True
        )



def _loadFile(componentFpath:str) -> str:
    if not os.path.exists(componentFpath):
        return "Error: could not find file "+componentFpath
    with open(componentFpath, 'r') as f :
        return f.read()


def loadMediaFile(fPath) -> str:
    mediaDir = pathJoin(mw.pm.profileFolder(), "collection.media")
    savePath = pathJoin(mediaDir, 'lingoflix4anki', fPath)
    myaddonDir = os.path.dirname(__file__)

    shutil.copy(pathJoin(myaddonDir, 'lingoflix4anki', fPath), savePath)   
    # if not os.path.isfile(savePath):
    #     shutil.copy(pathJoin(myaddonDir, fPath), savePath)   
    logger.debug("Copied "+ pathJoin(myaddonDir, fPath) + "to "+ savePath)

    jssrc = _loadFile(savePath)
    return jssrc


def injectInWebview(html, card, kind):
    logger.debug("hook called: " + kind)

    if kind == "reviewAnswer":
        # Parse the Kanji on card question
        kanji = card.question()
        encoded_kanji = urllib.parse.quote(kanji)

        # Load the menu
        menu = loadMediaFile('menu.html')
        menu = menu.replace("'%cardFront%'", f'`{card.question()}`')
        menu = menu.replace("%kanjiVar%", kanji)
        menu = menu.replace("%kanjis%", encoded_kanji)
        # menu = menu.replace("//%JS_IMPORTS%", loadMediaFile('flicks.js'))

        html += menu
    return html

def injectScript(element, script):
    element += script
    return element


def getTemplateCopy(template):
    # if the template does not have a copy :
    #   Create a template copy
    #   new_template.back += lingoflixScript
    # else : 
    #   Select the new template

    # (Check that the template is not already a copy)
    return template


def injectInTemplateCopy(deck, injection):
    # Make a copy of the cards' template and inject the lingoflix script in it
    templates = []
    # For card in deck.cards :
    #   new_template = getTemplateCopy(card)
    #   new_template = injectScript(new_template)
    #   change card template
    
    # Android
        # HTML/js script
    # iOS
        # user prefs: language
    pass

def showLingoflix() -> str:

    platform = select_platform()

    if platform == 'Desktop' :
        card_will_show.append(injectInWebview)
    
    else : # mobile
                
        if platform == 'Android' :
            # inject script in template copy
            injection = '<html><src>' # or lambda

        elif platform == 'iOS':
            injection = '' # or lambda

        deck = select_deck()
        injectInTemplateCopy(deck, injection)
    


            
if os.path.exists(logpath):
    os.remove(logpath)


# User clicks on "Add Lingoflix to a deck"
vidAdder = QAction("🎥 Add Lingoflix to flashcards", mw)
synchronizer = QAction("🎥(for Ankimobile) Synchronize with Lingoflix", mw)
mw.form.menuTools.addAction(vidAdder)
mw.form.menuTools.addAction(synchronizer)

VideoHandler.start_server()


# aqt extension -----------
# Chooses the platform: "On what platform will you search for videos ? 
    # Note: videos will appear in any deck, regardless of the platform you used to add them": Android, iOs
# chooses the Deck
# everytime a card is displayed in the given deck, 
    # a hook is called and a script is injected in the webview.