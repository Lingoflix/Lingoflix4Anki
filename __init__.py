import urllib.parse, os,shutil,json
from os.path import join as pathJoin
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from aqt.gui_hooks import card_will_show 
from aqt.utils import showInfo


logpath = pathJoin(os.path.dirname(__file__), 'lingoflix.log')

def log_message(self, format, *args):
    # Disable default logging or redirect it somewhere harmless
    return

BaseHTTPRequestHandler.log_message = log_message # disable logging bc interfering with anki

class VideoHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        print(f"GET request received for path: {self.path}")
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"GET Not Allowed")

    def do_POST(self):
        if self.path == "/add_video":
            try :
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)

                cardID = data.get("cardID", "")
                video_url = data.get("videoUrl", "")

                card = mw.col.get_card(cardID)
                note = card.note()

                # Append to existing field
                note["Back"] += f'<br><iframe width="300" src="{video_url}" frameborder="0"></iframe>'
                note.flush()  # Save changes

                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b"Video added")
            except Exception as e :
                self.send_response(500)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b"{}".format(str(e)))


        if self.path == "/getVideoSuggestions":
                log("APIsuggest was called")
                
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode("utf-8"))

                try :
                    # # Wrap the word in double quotes and URL-encode it
                    # quoted_word = urllib.parse.quote(f'"{word}"')
                    word = data.get("word", "")
                    quoted_word =f'"{word}"'

                    # Insert it into the URL
                    url = f"https://filmot.com/search/{quoted_word}/1?lang=ja&searchManualSubs=1&country=98&sortField=likecount&sortOrder=desc&gridView=1&"

                    response = requests.get(url)
                    response.raise_for_status()  # Will raise exception on bad response
                    html = response.text
                    # log(f'\n{"-"*50} \n Received html: \n" + {html}')

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                    log(f"Sent a HTML response: {len(html)} bytes")

                except Exception as e :
                    self.send_response(500)
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(str.encode(str(e)))
                except requests.exceptions.HTTPError as e :
                    self.send_response(500)
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(str.encode(str(e)))
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(str.encode(self.path+ " not found"))




def log(text):
    with open(logpath, 'a') as f:
        f.write('-'*50 + '\n' + text)


def _loadFile(componentFpath:str) -> str:
    if not os.path.exists(componentFpath):
        return "Error: could not find file "+componentFpath
    with open(componentFpath, 'r') as f :
        return f.read()


def loadMediaFile(fPath) -> str:
    mediaDir = pathJoin(mw.pm.profileFolder(), "collection.media")
    savePath = pathJoin(mediaDir, fPath)
    myaddonDir = os.path.dirname(__file__)

    shutil.copy(pathJoin(myaddonDir, fPath), savePath)   
    # if not os.path.isfile(savePath):
    #     shutil.copy(pathJoin(myaddonDir, fPath), savePath)   
    log("Copied "+ pathJoin(myaddonDir, fPath) + "to "+ savePath)

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
    log("hook called: " + kind)

    shutil.copy(
        pathJoin(os.path.dirname(__file__), 'flicks.js'), 
        pathJoin(mw.pm.profileFolder(), "collection.media")
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

            
# Start server on a different thread at addon load
def start_server():
    import threading
    server = HTTPServer(('localhost', 8766), VideoHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()


if os.path.exists(logpath):
    os.remove(logpath)

action = QAction("🎥 Add context video for Kanji", mw)
mw.form.menuTools.addAction(action)
card_will_show.append(showMenu)
start_server()

