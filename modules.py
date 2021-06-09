# rich, parsing website
import os
from pprint import pprint
import json
import subprocess as sp


def clear_func(clear_var: list, settings: dict) -> None:
    if not clear_var:
        if input("Are you really want clear all tests and results? [Y/n] ")[0] == 'Y':
            from shutil import rmtree
            rmtree('Nicetest/data')
            os.mkdir('Nicetest/data')
            with open('Nicetest/data/settings.json', 'w') as f:
                f.write(json.dumps({}))
            print('Done')
        return
    if input(f"Are you really want clear tests and results from {', '.join(clear_var)}? [Y/n] ") != 'Y':
        return
    if not settings:
        with open('Nicetest/data/settings.json') as f:
            f = f.read()
        settings = json.loads(f)
    for file in clear_var:
        if file in settings:
            os.remove(settings[file])
            del settings[file]
            print(f"Removed tests & results from {file}")
        else:
            print(f'Not found tests & results from {file}')

    file = json.dumps(settings)
    with open('Nicetest/data/settings.json', 'w', encoding='utf-8') as f:
        f.write(file)


def test_func(test_var: list, file='', dct=None) -> dict:
    prog = ['./test.out']
    if file:
        compiling = sp.run(['g++', file, '-o', 'test.out'], stdout=sp.PIPE)
        for i, test in enumerate(dct["tests"]):
            oupt = sp.run(prog, stdout=sp.PIPE, input=test['input'].encode('utf-8')).stdout.decode("utf-8")
            rslt = "OK" if oupt == test['answer'] else "WA"
            dct["results"][i]["output"].append(oupt)
            dct["results"][i]["result"].append(rslt)
        print(f"Done {file}")
        return dct
    with open('Nicetest/data/settings.json') as f:
        f = f.read()
    settings = json.loads(f)
    for file in test_var:
        try:
            with open(settings[file]) as f:
                f = f.read()
        except KeyError:  # todo: error, not found file in settings.json
            return
        dct = json.loads(f)
        compiling = sp.run(['g++', file, '-o', 'test.out'], stdout=sp.PIPE)
        for i, test in enumerate(dct["tests"]):
            oupt = sp.run(prog, stdout=sp.PIPE, input=test['input'].encode('utf-8')).stdout.decode("utf-8")
            rslt = "OK" if oupt == test['answer'] else "WA"
            dct["results"][i]["output"].append(oupt)
            dct["results"][i]["result"].append(rslt)

        dct = json.dumps(dct, ensure_ascii=False)
        with open(settings[file], 'w', encoding='utf8') as f:
            f.write(dct)
        print(f"Done {file}")


def add_func(add_var: list, dct: dict, count: list) -> dict:
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
    return dct
