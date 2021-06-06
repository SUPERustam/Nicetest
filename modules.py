# rich, argparse, parsing website
import os
from pprint import pprint
import json
import subprocess as sp

# TODO:
def run(file: str, test: str):
    prog = ['./test.out']
    test_name = f"data/test_{file[file.rfind('/') + 1:file.rfind('.')]}.json"
    if os.path.exists(test):
        with open(test) as f:
            f = f.read()
    else:
        with open('data/template_test.json') as f:
            f = f.read()
    tests = json.loads(f)

    compiling = sp.run(['g++', file, '-o', 'test.out'], stdout=sp.PIPE)
    for test in tests:
        inpt = test['input'].encode('utf-8')
        oupt = sp.run(prog, stdout=sp.PIPE, input=inpt).stdout.decode('utf-8')

        if not os.path.exists(test_name):
            test["output"], test["result"] = [], []
        test['output'].append(oupt)
        rslt = "OK" if oupt == test['answer'] else "WA"
        test['result'].append(rslt)

    tests = json.dumps(tests)
    with open(test_name, 'w', encoding='utf8') as f:
        f.write(tests)
    yield f'Done {file}\n'
