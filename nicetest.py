# rich, argparse, parsing website
import os
from pprint import pprint
import json
import subprocess as sp
import argparse


def run(files):
    prog = ['./test.out']
    for file in files:
        test_name = f"data/test_{file[file.rfind('/') + 1:file.rfind('.')]}.json"
        if os.path.exists(test_name):
            with open(test_name) as f:
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


parser = argparse.ArgumentParser()

parser.add_argument('--run', help='run script from path or run default script without arguments', nargs='*')
parser.add_argument('--add', help='add tests to your script')  # TODO:
parser.add_argument('-i', '--input', help='add input to your test (using flag add)',
                    type=str, default='')  # TODO:
parser.add_argument('-a', '--answer', help='add answer to your test (using flag add)',
                    type=str, default='')  # TODO:
parser.add_argument('-c', '--comment', help='add comment to your test (using flag add)',
                    type=str, default='')  # TODO:
# parser.add_argument('--clear', help='clear history',
#                     type=str, default='')

args = parser.parse_args()


run_var = args.run
if run_var == []:
    with open('data/settings.json') as f:
        f = f.read()
        print(*run(json.loads(f)["files"]))
elif run_var:
    print(*run(run_var))
