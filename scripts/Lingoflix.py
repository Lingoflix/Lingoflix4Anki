
# Domainer layer

class CardContext:
    def __init__(self, note_id: int, ):
        self.note_id = note_id
        self.note = self.load_note()
        self.target_word = self.extract_target_word()

    def load_note(self):
        # Use mw.col.get_note(self.note_id)
        ...

    def extract_target_word(self):
        # Based on a specific field like note["Word"]
        ...

    def getTemplate(self, video_url: str, timestamp: float):
        pass



    def injectScript(self, script: str, timestamp: float):
        # Store this in a custom field or a JSON field
        ...


