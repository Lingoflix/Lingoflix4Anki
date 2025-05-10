
from scripts.adapters.AnkiMediaManager import AnkiMediaManager
import urllib
from typing import Callable
from scripts.domain.Platforms import Platforms

class VideoSearcher:
    # This class is responsible for generating the script to be injected into the webview
    # If iOS, inject URL. Otherwise, inject JS+HTML
    def __init__(self, target_platform):
        self.target_platform = target_platform


    def _html(self) -> Callable:
        # Script to inject in the webview
        def generateHTML() -> str:
            # kanji = card.question()
            # encoded_kanji = urllib.parse.quote(kanji)

            # Load the menu
            media = AnkiMediaManager(addon_name="lingoflix4anki")
            media.import_all()
            script = media.load_file('menu.html')
            # script = script.replace("'%cardFront%'", f'`{card.question()}`')
            # script = script.replace("%kanjiVar%", kanji)
            # script = script.replace("%kanjis%", encoded_kanji)
            # script += media.load_file("VideoSearcher.js")
            return script
        
        return generateHTML
    

    def _URL(self) -> Callable:
        def generateURL(card) -> str:
            # Load the menu
            kanji = card.question()
            url = f"https://www.lingoflix.com/?search={urllib.parse.quote(kanji)}"
            return url
        return generateURL


    def generate(self) -> Callable:
        # Generate the script to inject 
        if self.target_platform == Platforms.IOS:
            return self._URL()
        elif self.target_platform in [Platforms.DESKTOP, Platforms.WEB, Platforms.ANDROID]:
            return self._html()
        else:
            raise ValueError(f"Unknown platform: {self.target_platform}")
