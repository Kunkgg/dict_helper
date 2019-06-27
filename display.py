# -*- coding:utf-8 -*-
"""
Write the result of word searching in the special index.html for electron GUI.
"""
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os


# the display file path
dis_file = 'dict_helper-linux-x64/resources/app/index.html'
root_dir, _ = os.path.abspath(__file__).rsplit('/', 1)
DIS_FILE_PATH = os.path.join(root_dir, dis_file)
TEMPLATE_FILENAME = 'base.html'

LOCAL_DICTIONARY = 'ENCN_Collins'
ONLINE_DICTIONARY = 'YouDao'

env = Environment(loader=FileSystemLoader(root_dir))
template = env.get_template(TEMPLATE_FILENAME)


def display(result, local_dictionary, online_dictionary):
    html = template.render(result=result,
                           local_dictionary=local_dictionary,
                           online_dictionary=online_dictionary)
    with open(DIS_FILE_PATH, 'w') as fp:
        fp.writelines(html)
