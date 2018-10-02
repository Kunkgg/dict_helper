"""
this module implements store in Anki
Use AnkiConnect respostry, DOCs:https://foosoft.net/projects/anki-connect/
"""
import urllib.request
import json

ANKICONNECT_URL = 'http://127.0.0.1:8765'
ANKICONNECT_VERSION = 6
# deck name
DECKNAME = "English growing"
# DECKNAME = "Default"
# model name
MODELNAME = "基础(左对齐)"
# MODELNAME = "Basic"
# tags
TAGS = ["dict-helper"]

data_add_note = {
    "action": "addNote",
    "version": ANKICONNECT_VERSION,
    "params": {
        "note": {
            "deckName": DECKNAME,
            "modelName": MODELNAME,
            "fields": {
                "正面": "front content test",
                "背面": "Update !back content test"
                # "Front": "front content test",
                # "Back": "back content test"
            },
            "tags": TAGS
            # "audio": {
            #     "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
            #     "filename": "yomichan_ねこ_猫.mp3",
            #     "skipHash": "7e2c2f954ef6051373ba916f000168dc",
            #     "fields": [
            #         "Front"
            #     ]
            # }
        }
    }
}

data_updateNoteFields = {
        "action": "updateNoteFields",
        "version": ANKICONNECT_VERSION,
            }


def post(data):
    req = urllib.request.Request(url=ANKICONNECT_URL, method='POST')
    req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req) as res:
            html = json.loads(res.read())
            # print(html)
            return html
    except urllib.error.HTTPError:
        return
        
def addNote(data_add_note):
    html = post(data_add_note)
    if html['error'] == 'cannot create note because it is a duplicate':
        Note = data_add_note['params']['note']
        Note_front = Note['fields']['正面']
        search_keyword = Note_front.split('/', 1)[0]
        NoteId = findNote(search_keyword)['result']
        if len(NoteId) == 1:
            NoteId = NoteId[0]
            update_Note = {
                "id": NoteId,
                "fields": Note['fields']
            }
            data_updateNoteFields['params'] = {'note': update_Note}
            # print(data_updateNoteFields)
            html = post(data_updateNoteFields)
            # print(html)
    return html

def findNote(frontfeild):
    data_find_note = {
    "action": "findNotes",
    "version": ANKICONNECT_VERSION,
    "params": {
        "query": frontfeild
        }
    }
    return post(data_find_note)


def notesInfo(notesId):
    data_notesInfo = {
        "action": "notesInfo",
        "version": ANKICONNECT_VERSION,
        "params": {
            "notes": notesId
        }
    }
    return post(data_notesInfo)
