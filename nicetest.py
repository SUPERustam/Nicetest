# rich, parsing website
import os
from pprint import pprint
import json
import argparse

from modules import test_func, add_func, clear_func

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help="test your files: cppfile0.cpp cppfile1.cpp...", nargs='*',
                    metavar='')
parser.add_argument('-c', '--connect', help='connect tests to your scripts: cppfile0.cpp cppfile1.cpp...', nargs='+',
                    metavar='')
parser.add_argument('-a', '--add',
                    help='''add tests: "input0" "answer0" "comment0" "input1" "answer1" "comment1"...''',
                    nargs='+', metavar='')
parser.add_argument('--clear',
                    help="""clear all tests and results from files (without arguments: from all files):
                     "cppfile0.cpp" "cppfile1.cpp"...""",
                    metavar='', nargs='*')

args = parser.parse_args()
test_var = args.test
connect_var = args.connect
add_var = args.add
clear_var = args.clear
settings = {}

# output: settings
if connect_var:
    if not add_var:  # todo: error you should input values
        pass
    elif len(add_var) % 3 != 0:  # todo: error you should write "input", "answer", "comment" to every test
        pass
    with open('Nicetest/data/settings.json') as f:
        f = f.read()
    settings = json.loads(f)
    for item in connect_var:
        count = 0  # count of tests

        if item not in settings:
            settings[item] = f"Nicetest/data/test_{item[item.rfind('/') + 1:item.rfind('.')]}.json"
            dct = {
                "tests": [],
                "results": []
            }
        else:
            with open(settings[item]) as f:
                f = f.read()
            dct = json.loads(f)
            count = len(dct["results"][0]['result'])

        # settings[item]: dct == file: dict from test.json
        if add_var:
            dct = add_func(add_var, dct, count * [''])
        if test_var == []:
            dct = test_func([], item, dct)

        dct = json.dumps(dct, ensure_ascii=False)
        with open(settings[item], 'w', encoding='utf8') as f:
            f.write(dct)

    file = json.dumps(settings)
    with open('Nicetest/data/settings.json', 'w', encoding='utf8') as f:
        f.write(file)

elif test_var:
    test_func(test_var)

if clear_var == [] or clear_var:
    clear_func(clear_var, settings)
