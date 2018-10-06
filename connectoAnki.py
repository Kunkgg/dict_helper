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
MODELNAME = "划词原句模板"
# MODELNAME = "Basic"
# tags
TAGS = ["dict-helper"]


def notetemplate(modelname=MODELNAME):
    """make a note template with speical modelname"""
    data_add_note = {
    "action": "addNote",
    "version": ANKICONNECT_VERSION,
    "params": {
        "note": {
            "deckName": DECKNAME,
            "modelName": MODELNAME,
            "fields": {
                # "正面": "front content test",
                # "背面": "Update !back content test"
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

    for field in FIELDS:
        data_add_note["params"]["note"]["fields"][field] = ''
    return data_add_note


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
        field0 = Note['fields'][FIELDS[0]]
        query = FIELDS[0] + ':' + field0
        NoteId = findNote(query)['result']
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

def findNote(query):
    """find note with the query
    :params:query: strtype: "key1:value1 key2:value2 ..."
    :rtype:list
    :return: noteIDs
    """
    data_find_note = {
    "action": "findNotes",
    "version": ANKICONNECT_VERSION,
    "params": {
        "query": query
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

def modelFieldNames(modelname=MODELNAME):
    modelFieldNames = {
    "action": "modelFieldNames",
    "version": 6,
    "params": {
        "modelName": modelname
        }
    }
    return post(modelFieldNames)['result']

FIELDS = modelFieldNames()
data_add_note = notetemplate()
