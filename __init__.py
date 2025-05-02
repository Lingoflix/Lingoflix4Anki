import urllib.parse, os,shutil,json
from os.path import join as pathJoin
import requests

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from aqt.gui_hooks import card_will_show 
from aqt.utils import showInfo

from .Logging import logger

from . import VideoHandler

logpath = pathJoin(os.path.dirname(__file__), 'lingoflix.log')


# def log(text):
#     with open(logpath, 'a') as f:
#         f.write('-'*50 + '\n' + text)


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


def is_kanji(char):
    if not isinstance(char, str) :
        raise Exception("Expected string, got", type(char))  
    else :
        return '\u4e00' <= char <= '\u9fff'


def getFirstKanjiSequence(front:str) -> str :
    # if 1+ kanji characters, search (leave an option to change the word)
    maxlen = len(front)
    i = -1
    kanji = ''
    init = True
    while i < maxlen :
        if is_kanji(front[i]) :
            kanji += front[i]
            i+=1
            if init:
                init = False
        else :
            if init :
                i+=1
                continue
            else :
                break
    return kanji


def showMenu(html, card, kind) -> str:
    logger.debug("hook called: " + kind)

    shutil.copytree(
        pathJoin(os.path.dirname(__file__), 'lingoflix4anki'), 
        pathJoin(mw.pm.profileFolder(), "collection.media", 'lingoflix4anki'),
        dirs_exist_ok=True
    )
   
    if kind == "reviewAnswer":
        # Parse the Kanji on card question
        kanji = getFirstKanjiSequence(card.question() )
        encoded_kanji = urllib.parse.quote(kanji)

        # Load the menu
        menu = loadMediaFile('menu.html')
        menu = menu.replace("'%cardFront%'", f'`{card.question()}`')
        menu = menu.replace("%kanjiVar%", kanji)
        menu = menu.replace("%kanjis%", encoded_kanji)
        # menu = menu.replace("//%JS_IMPORTS%", loadMediaFile('flicks.js'))

        html += menu
    return html

            
if os.path.exists(logpath):
    os.remove(logpath)

action = QAction("🎥 Add context video for Kanji", mw)
mw.form.menuTools.addAction(action)
card_will_show.append(showMenu)
VideoHandler.start_server()


