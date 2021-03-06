# -*- coding:utf-8 -*-
"""
this module implements the dicthelper
 - search a selected English word in local dictionary and online dictionary
 - display searching result with tk GUI
 - store result into Anki with speical deckname and modlename
"""

import string
import subprocess
import os
import json
import urllib.request
import urllib.error
from xml.etree import ElementTree
from pprint import pprint
from collections import namedtuple

from display import display

# start:local dictionary(ENCN_Collins) file path ###
root_dir, _ = os.path.abspath(__file__).rsplit('/', 1)
local_dict_path_wordforms = os.path.join(root_dir, 'data/wordforms.json')
local_dict_path_tags = os.path.join(root_dir, 'data/tags.json')
local_dict_path_edict = os.path.join(root_dir, 'data/edict')
edict_files = ['part1.json', 'part2.json', 'part3.json', 'part4.json']
# end ###

# command tamplate for getting word on linux
GET_WORD_COMMAND = 'xclip -selection {} -out'

# infomation of dictionary
LOCAL_DICTIONARY = 'ENCN_Collins'
ONLINE_DICTIONARY = 'YouDao'

# online dictinary youdao API
YOUDAO_API_PART1 = 'http://dict.youdao.com/'
YOUDAO_API_PART2 = 'fsearch?client=deskdict&keyfrom=chrome.extension&pos=-1'
YOUDAO_API_PART3 = '&doctype=xml&xmlVersion=3.2&dogVersion=1.0&vendor=unknown'
YOUDAO_API_PART4 = '&appVer=3.1.17.4208&le=eng&q='
YOUDAO_API = (
        YOUDAO_API_PART1 +
        YOUDAO_API_PART2 +
        YOUDAO_API_PART3 +
        YOUDAO_API_PART4
)

Word = namedtuple('Word', ['expression', 'reading', 'glossary'])


def get_word(get_word_method):
    """get word from mouse selected or copied in system clipboard
      - 'primary' means getting word from mouse selected
      - 'clipboard' means getting word from copied in system clipboard
    :return: word which needs to be searched
    :rtype: str
    """
    word = subprocess.Popen(
        GET_WORD_COMMAND.format(get_word_method),
        shell=True,
        stdout=subprocess.PIPE).stdout.read()
    word = word.decode('utf-8')
    return word.strip(string.punctuation)


def search_local_dictionary(word):
    """search in local dictionary(Collins English-Chinese), default
    analysising word root
    :param word: str
    :return: the result of search_local_dictionary
    :rtype: list(cantains all same root words in the local dictionary)
    Usage::
    In [2]: search_local_dictionary('test')
    Out[2]:
    [['test',
    '/te̱st/',
    '',
    ['v.检验；试验；测试<br> When you <b>test</b> something, you try it, for example
    by touching it or using it for a short time, in order to find out what it
    is, what condition it is in, or how well it works. ',
    'n.试验；测试；检验<br> A <b>test</b> is a deliberate action or experiment to find
    out how well something works. ',
    ....]]]
    """
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
    # print(search_words)
    result = []
    for word in search_words:
        for edict_file in edict_files:
            edict_file_path = os.path.join(local_dict_path_edict, edict_file)
            with open(edict_file_path, 'r') as fp:
                edict_part = fp.readlines()
            edict_part = json.loads(edict_part[0])
            index = edict_part['indices'].get(word, None)
            if index:
                res = edict_part['defs'][index[0]]
                if len(res) == 4:
                    del res[2]
                res = Word(res[0], res[1], res[2])
                result.append(res)
                break
    return result


def search_online_dictionary(word):
    """search in online dictionary(YOUDAO_API)
    :param word: str
    :return: the result of search_online_dictionary
    :rtype: list
    Usage::
    In [3]: search_online_dictionary('test')
    Out[3]:
    ['test',
    '/tɛst/',
    ['n. 试验；检验', 'vt. 试验；测试', 'vi. 试验；测试', 'n. (Test)人名；(英)特斯特']]
    """
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
            us_phonetic_symbol = '/' + \
                tree.find('us-phonetic-symbol').text + '/'
            glossary = []
            for node in tree.iter('content'):
                glossary.append(node.text)
        except AttributeError:
            return None
        result = Word(expression, us_phonetic_symbol, glossary)
        return result


def search(word):
    """search word in local and online dictionary
    save local and online result in a dict
    """
    result = {
        'local': search_local_dictionary(word),
        'online': search_online_dictionary(word)
    }
    return result


def dicthelper(get_word_method):
    """entry"""
    word = get_word(get_word_method)
    if word:
        display(search(word), LOCAL_DICTIONARY, ONLINE_DICTIONARY)


def test():
    word = get_selected_word()
    result = search(word)
    print('Input:', word)
    print('result:')
    pprint(result)


if __name__ == '__main__':
    from argparse import ArgumentParser, RawTextHelpFormatter
    parser = ArgumentParser(description='dicthelper', formatter_class=RawTextHelpFormatter)
    parser.add_argument('--source', '-s',action='store', default='primary', type=str,
                        choices=['primary', 'clipboard', 'clip'],
                        help='Specify get word method, from mouse selected or system clipboard\n'
                        'primary --> mouse selected\n'
                        'clipboard or clip --> system clipboard\n' 
                        '[default:primary]')
    args = parser.parse_args()
    dicthelper(get_word_method=args.source)
