# dict_helper

## Features
 - dict_helper is a simple dictionary helper script
 - search a selected English word in local dictionary and online dictionary
 - display searching result with Electron GUI
 - store result into Anki with speical deckname and modlename 

## Requirements
 - Anki client 2.1.x with addon [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
 - xclip on Linux `sudo apt install xclip`
 - python3.6 or above
 - jinja2
 - Electron
 - Electron-packager

## Usage
 - Clone repo `git clone https://github.com/Kunkgg/dict_helper.git`
 - Install python environment according with Pipfile `cd dict_helper && pipenv install`
 - Replace your DECKNAME in `render.js` file
 - Import the model file `EN_vocabulary.apkg` to your Anki
 - Install Electron and Electron-packager with npm `npm install electron electron-packager --save-dev`
 - Build the electron GUI `./node_modules/electron-packager/bin/electron-packager.js .`
 - Edit `dis_file` path in `display.py`, the default value is: `dict_helper-linux-x64/resources/app/index.html`, it's used for linux-x64.
Other system is different, you have to configure it manually
 - Edit the start script `dicthelper_selected.sh` and `dicthelper_clip.sh`, according comments
  - `dicthelper_selected.sh` is for word was selected by mouse on screen
  - `dicthelper_clip.sh` is for word was copied in system clipboard
 - Set keyboard shortcuts in system keyboard shortcuts setting for each run script
    - command: `absolute/path/to/dicthelper_selected.sh`
    - command: `absolute/path/to/dicthelper_clip.sh`
 -  To make sure AnkiConnect working, you have to launch Anki client first
 -  After above items are ready. Select one word anywhere by mouse, then push the keyboard shortcut

## Reference
 - [AnkiConnect](https://foosoft.net/projects/anki-connect/)
 - [dae/ankidocs](https://github.com/dae/ankidocs)
 - [dae/anki](https://github.com/dae/anki)
 - [老黄-划词原句模板](https://www.laohuang.net/20160817/anki-dict-helper-chrome-extension/)
