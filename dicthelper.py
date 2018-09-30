# -*- coding:utf-8 -*-



import pprint
import string
import subprocess
import os
import json
import urllib.request
import urllib.error
from xml.etree import ElementTree


local_dict_path_wordforms = './data/wordforms.json'
local_dict_path_tags = './data/tags.json'
local_dict_path_edict = './data/edict'
edict_files = ['part1.json', 'part2.json', 'part3.json', 'part4.json']
GET_WORD_COMMAND = 'xclip -selection primary -o'
YOUDAO_API = 'http://dict.youdao.com/fsearch?client=deskdict&keyfrom=chrome.extension&pos=-1&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown&appVer=3.1.17.4208&le=eng&q='

def get_selected_word():
    """get seleced word from screen"""
    word = subprocess.Popen(
                GET_WORD_COMMAND, 
                shell=True, 
                stdout=subprocess.PIPE).stdout.read()
    word = word.decode('utf-8')
    return word.strip(string.punctuation)

def search_local_dictionary(word):
    """search in local dictionary"""
    search_words = [word]
    word_lowercase = word.lower()
    if word_lowercase not in search_words:
        search_words.append(word_lowercase)

    with open(local_dict_path_wordforms, 'r') as fp:
        wordforms = fp.readlines()
    wordforms = json.loads(''.join(wordforms))
    wordforms_res = (
                wordforms.get(word, None) or 
                wordforms.get(word.lower(), None)
                )
    if wordforms_res:
        search_words.extend(wordforms_res)
    print(search_words)
    result = []
    for word in search_words:
        for edict_file in edict_files:
            edict_file_path = os.path.join(local_dict_path_edict, edict_file)
            with open(edict_file_path, 'r') as fp:
                edict_part = fp.readlines()
            edict_part = json.loads(edict_part[0])
            index = edict_part['indices'].get(word, None)
            if index:
                result.append(edict_part['defs'][index[0]])
                break
    return result
            

def search_online_dictionary(word):
    """search in online dictionary"""
    url = YOUDAO_API + word
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as res:
            html = res.read().decode('utf-8')
    except urllib.error.HTTPError:
        html = ''
        return None
    if html:
        tree = ElementTree.fromstring(html)
        try:
            expression = tree.find('return-phrase').text
            us_phonetic_symbol = '/' + tree.find('us-phonetic-symbol').text + '/'
            glossary = []
            for node in tree.iter('content'):
                glossary.append(node.text)
        except AttributeError:
            return None
        result = [expression, us_phonetic_symbol, glossary]
        return result

def search(word):
    """search word in local and online dictionary"""
    result = {
        'local':search_local_dictionary(word), 
        'online':search_online_dictionary(word)
    }
    return result

def display(result):
    pass

def helper():
    word = get_selected_word()
    if word:
        result = search(word)
        display(result)


def test():
    word = get_selected_word()
    result = search(word)
    print('Input:', word)
    print('result:', result)


if __name__ == '__main__':
    test()




