# dict_helper

## Features
 - dict_helper is a simple dictionary helper script
 - search a selected English word in local dictionary and online dictionary
 - display searching result with tk GUI
 - store result into Anki with speical deckname and modlename 

## Requirements
 - python 3.x
 - Anki client 2.1.x with addon [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
 - tk 8.6 `sudo apt install python3-tk`
 - xclip on Linux `sudo apt install xclip`

## Usage
 - `git clone https://github.com/Kunkgg/dict_helper.git`
 - Set a keyboard shortcut in system keyboard shortcuts setting
    - command: `python3 /path/to/dict_helper.py`
 - replace your deckname and modlename in `connectoAnki.py` file
 -  To make sure AnkiConnect working, you have to luanch anki client first
 -  After above items are ready. Select one word anywhere by mouse, then push the keyboard shortcut.

## Reference
 - [AnkiConnect](https://foosoft.net/projects/anki-connect/)
 - [dae/ankidocs](https://github.com/dae/ankidocs)
 - [dae/anki](https://github.com/dae/anki)
