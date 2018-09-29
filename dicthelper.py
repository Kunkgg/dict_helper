# -*- coding:utf-8 -*-




import string
import subprocess
import os
import json

local_dict_path_wordforms = './data/wordforms.json'
local_dict_path_tags = './data/tags.json'
local_dict_path_edict = './data/edict'
edict_files = ['part1.json', 'part2.json', 'part3.json', 'part4.json']
get_word_command = 'xclip -selection primary -o'
http://dict.youdao.com/fsearch?client=deskdict&keyfrom=chrome.extension&pos=-1&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown&appVer=3.1.17.4208&le=eng&q=good
youdao_API = 'http://openapi.youdao.com/api'

http://openapi.youdao.com/api?q=good&from=EN&to=zh_CHS&appKey=R27I3ZwEH6w4PMGEfnHDJVKW2Qmr2m4L&salt=2&sign=1995882C5064805BC30A39829B779D7B

def get_selected_word():
    word = subprocess.Popen(
                get_word_command, 
                shell=True, 
                stdout=subprocess.PIPE).stdout.read()
    word = word.decode('utf-8')
    return word.strip(string.punctuation)

def search_local_dictionary(word):
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


    pass

def search(word):

    local_search_res = search_local_dictionary(word)
    youdao_search_res = search_online_dictionary(word)
    result = {
        'local_dict':local_search_res, 
        'youdao':youdao_search_res
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
    result = search_local_dictionary(word)
    print('Input:', word)
    print('result:', result)


if __name__ == '__main__':
    test()




