import urllib.request
import json

ANKICONNECT_URL = 'http://127.0.0.1:8765'
DECKNAME = "English growing"
# DECKNAME = "Default"
MODELNAME = "基础(左对齐)"
# MODELNAME = "Basic"

TAGS = ["dict-helper"]

data_add_note = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": DECKNAME,
            "modelName": MODELNAME,
            "fields": {
                "正面": "front content test",
                "背面": "back content test"
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

def addNote(data_add_note):
    req = urllib.request.Request(url=ANKICONNECT_URL, method='POST')
    req.data = json.dumps(data_add_note).encode()
    try:
        with urllib.request.urlopen(req) as res:
            html = json.loads(res.read())
            # print(html)
    except urllib.error.HTTPError:
        return 
    
