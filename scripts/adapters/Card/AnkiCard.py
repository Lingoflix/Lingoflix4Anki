from scripts.domain.Card import Card
from aqt import mw

class AnkiCard(Card):
    def __init__(self, cid, fields, deck_id):
        super().__init__(cid, fields, deck_id)
        card = mw.col.getCard(cid)
        self.ankicard = card
        self.note = card.note()
        self.model = self.note().model()

    def get_templates(self) :
        # A card can have several note models
        return self.model["tmpls"]
    
    def get_fields(self):


        # Add the field if it's not present
        existing_fields = [f["name"] for f in model["flds"]]
        if field_name not in existing_fields:
            new_field = col.models.newField(field_name)
            col.models.addField(model, new_field)
            print(f"Added field: {field_name}")
        else:
            print(f"Field '{field_name}' already exists")