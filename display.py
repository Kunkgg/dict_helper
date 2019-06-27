# -*- coding:utf-8 -*-

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_PATH = '.'
TEMPLATE_FILENAME = 'base.html'
DIS_FILE = '/home/gk07/mytools/dict_helper/index.html'

LOCAL_DICTIONARY = 'ENCN_Collins'
ONLINE_DICTIONARY = 'YouDao'

env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
template = env.get_template(TEMPLATE_FILENAME)


def display(result, local_dictionary, online_dictionary):
    html = template.render(result=result,
                           local_dictionary=local_dictionary,
                           online_dictionary=online_dictionary)
    with open(DIS_FILE, 'w') as fp:
        fp.writelines(html)
