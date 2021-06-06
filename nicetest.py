# rich, argparse, parsing website
import os
from pprint import pprint
import json
import subprocess as sp
import argparse

from modules import run

parser = argparse.ArgumentParser()

parser.add_argument('-r', '--run', help='run script from path or run default script without arguments', nargs='?')
parser.add_argument('-c', '--connect', help='connect tests to your scripts', nargs='+')
parser.add_argument('-a', '--add',
                    help='''add test: "input0" "answer0" "comment0" "input1" "answer1" "comment1" etc.''',
                    nargs='+')  # TODO:

args = parser.parse_args()
run_var = args.run
connect_var = args.connect
add_var = args.add

if connect_var:
    if not add_var:  # todo: error you should input values
        pass
    elif len(add_var) % 3 != 0:  # todo: error you should write "input", "answer", "comment" to every test
        pass

    with open('data/settings.json') as f:
        f = f.read()
    settings = json.loads(f)
    for item in connect_var:
        count = 0  # count of tests

        if item not in settings:
            settings[item] = f"data/test_{item[item.rfind('/') + 1:item.rfind('.')]}.json"
            dct = {
                "tests": [],
                "results": []
            }
        else:
            with open(settings[item]) as f:
                f = f.read()
            dct = json.loads(f)
            count = len(dct["results"][0]['result'])

        if add_var:
            count *= ['']
            for i in range(0, len(add_var), 3):
                dct2 = {
                    "input": add_var[i],
                    "answer": add_var[i + 1],
                    "comment": add_var[i + 2]
                }
                dct["tests"].append(dct2)
                dct["results"].append({
                    "output": count,
                    "result": count
                })

        dct = json.dumps(dct)
        with open(settings[item], 'w', encoding='utf8') as f:
            f.write(dct)

    settings = json.dumps(settings)
    with open('data/settings.json', 'w', encoding='utf8') as f:
        f.write(settings)

if run_var:
    with open('data/settings.json') as f:
        f = f.read()
    settings = json.loads(f)
    settings2 = settings.copy()

    if run_var == '':
        ky = next(iter(settings))
        print(*run(ky, settings[ky]))
    else:
        settings.setdefault(run_var, '')
        if settings2 != settings:
            file = json.dumps(settings)
            with open('data/settings.json', 'w', encoding='utf8') as f:
                f.write(file)
        print(*run(run_var, settings[run_var]))
