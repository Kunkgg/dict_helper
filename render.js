// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.

// Configs
const ANKICONNECTURL = 'http://127.0.0.1:8765';
const ANKICONNECT_VERSION = 6;
const DECKNAME = "English growing";
const MODELNAME = "EN_vocabulary";
const TAGS = ["dict-helper"];
const ALLOWDUPLICATE = true;

window.onload = function () {
    const wordList = document.querySelectorAll(".word");
    for (let index = 0; index < wordList.length; index++) {
        const word = wordList[index];
        deal(word);
    }
}

function deal(word) {
    sendAllGlossary(word);
    sendOneGlossary(word);
}

function sendAllGlossary(word) {
    let [expression, reading] = getExprAndReading(word);
    let allGlossary = getAllGlossary(word);
    let linkAll = word.querySelector('.link-all');
    linkAll = linkAll.querySelector('a');
    let note = makeNote(expression, reading, allGlossary);
    linkAll.addEventListener('click', send);

    function send(e) {
        e = e || window.event;
        e.preventDefault();
        invoke(echo, 'addNote', params = note);

        function echo(response) {
            if (response["error"] == null) {
                alert("Success!")
            }
        }
    }
}

function sendOneGlossary(word) {
    let [expression, reading] = getExprAndReading(word);
    let linkOneList = word.querySelectorAll('.link-one');
    for (let index = 0; index < linkOneList.length; index++) {
        let linkOne = linkOneList[index];
        let oneGlossary = getOneGlossary(linkOne);
        let note = makeNote(expression, reading, oneGlossary);
        linkOne = linkOne.querySelector('a');
        linkOne.addEventListener('click', send);

        function send(e) {
            e = e || window.event;
            e.preventDefault();
            invoke(echo, 'addNote', params = note);

            function echo(response) {
                if (response["error"] == null) {
                    alert("Success!")
                }
            }
        }
    }

}

function getExprAndReading(word) {
    let expression = word.querySelector('.expr').textContent;
    let reading = word.querySelector('.reading').textContent;
    return [expression, reading];
}

function getAllGlossary(word) {
    let allGlossary = word.querySelectorAll('.gloss');
    let allText = [];
    for (let index = 0; index < allGlossary.length; index++) {
        allText.push(allGlossary[index].textContent || allGlossary[index].innerText);
    }
    return allText.join('<br>');
}

function getOneGlossary(linkOne) {
    let gloss = linkOne.parentElement.querySelector('.gloss');
    return gloss.textContent || gloss.innerText;
}

function makeNote(expression, reading, glossary) {
    let note = {
        "note": {
            "deckName": DECKNAME,
            "modelName": MODELNAME,
            "fields": {},
            "options": {
                "allowDuplicate": ALLOWDUPLICATE
            },
            "tags": TAGS
        }
    };

    noteFields = {
        "单词": expression,
        "音标": reading,
        "释义": glossary,
        "笔记": "",
        "例句": "",
        "url": "",
        "发音": ""
    };
    note["note"]["fields"] = noteFields;
    // console.log(note);
    return note;
}

// Call AnkiConnect API
function invoke(callback, action, params = {}, version = ANKICONNECT_VERSION) {
    let xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    xhr.open('POST', ANKICONNECTURL);

    xhr.onload = function () {
        callback(xhr.response)
    }
    query = {
        "action": action,
        "version": version,
        "params": params
    }
    console.log(JSON.stringify(query));
    xhr.send(JSON.stringify(query));
}
