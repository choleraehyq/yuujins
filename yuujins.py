#!/usr/bin/env python3

import sys
import readline

import scope
import repl

version: str = "YuujinS 0.0.1"

if sys.version_info.minor < 6:
    print("YuujinS required python 3.6 or higher version.")
    sys.exit(1)

def load_std_lib() -> str:
    ret: str
    with open('./stdlib.ss', 'r') as f:
        ret = f.read()
    return ret

def eval_file(name: str, env: scope.Scope) -> None:
    with open(name) as f:
        while True:
            line: str = f.readline()
            if not line:
                break
            print(repl.REPL(line, env))

def main() -> None:
    lib: str = load_std_lib()
    env: scope.Scope = scope.root_scope()
    repl.REPL(lib, env)

    if len(sys.argv) == 2:
        if sys.argv[1] == '--version':
            print(version)
            return
        else:
            eval_file(sys.argv[1])
    elif len(sys.argv) > 2:
        print('Too many arguments')
        sys.exit(2)

    readline.parse_and_bind('set editing-mode vi')
    
    while True:
        line: str = input(">> ")
        r: str = repl.REPL(line, env)
        if len(r) > 0:
            print(r)
