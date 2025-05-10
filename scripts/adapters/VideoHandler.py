
# MOVE THIS FILE/VIDEOHANDLER TO LINGOFLIX

from os.path import join as pathJoin
import os,json,requests

from http.server import BaseHTTPRequestHandler, HTTPServer
from aqt import mw

from .Logging import logger

request_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://filmot.com/",
}

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
                logger.debug("APIsuggest was called")
                
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode("utf-8"))

                try :
                    # # Wrap the word in double quotes and URL-encode it
                    # quoted_word = urllib.parse.quote(f'"{word}"')
                    word = data.get("word", "")
                    quoted_word =f'"{word}"'
                    logger.debug(f"searching for {word}")


                    # Insert it into the URL
                    url = f"https://filmot.com/search/{quoted_word}/1?lang=ja&searchManualSubs=1&country=98&sortField=likecount&sortOrder=desc&gridView=1&"

                    response = requests.get(url, headers=request_headers)
                    response.raise_for_status()  # Will raise exception on bad response
                    html = response.text
                    logger.debug(f"\n{'-'*50}\nReceived HTML of size:\n{len(html)}")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(html.encode("utf-8"))
                    # log(f"Sent a HTML response: {len(html)} bytes")

                except Exception as e :
                    logger.error(f"Error: {str.encode(str(e))}")

                    self.send_response(500)
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(str.encode(str(e)))
                except requests.exceptions.HTTPError as e :
                    logger.error(f"HTTP Error: {str.encode(str(e))}")
                    self.send_response(500)
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(str.encode(str(e)))
        
        else:
            logger.error(f"[404] '{self.path}' not found")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(str.encode(self.path+ " not found"))


# Start server on a different thread at addon load
def start_server():
    import threading
    server = HTTPServer(('localhost', 8766), VideoHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()





