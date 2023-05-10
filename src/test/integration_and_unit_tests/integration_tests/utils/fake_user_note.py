from mimesis import Text

from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate

text = Text('en')

def generate_random_user_note_to_create(user_id: int) -> UserNoteCreate:
    note_title = text.title()
    note_text = text.sentence()
    user_note = UserNoteCreate(user_id=user_id, title=note_title, text=note_text)
    return user_note
