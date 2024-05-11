#!/usr/local/bin/python

# flag at the same directory as the app.py

import ast, os, sys

print("Enter the code to be executed")

def codeiumBanner(c):
    for i in ast.walk(c):
        match type(i):
            case (ast.Import|ast.ImportFrom|ast.FunctionDef|ast.Call|ast.Dict|ast.ClassDef):
                print("Codeium agent detected a banned code ",str(i))
                print("Codeium agent exiting... Bye!!!")
                sys.exit(1)


aboslutePath = os.path.abspath(__file__)
dirname = os.path.dirname(aboslutePath)
os.chdir(dirname)

codeium_code = ""
while True:
    line = input(">")
    if line.startswith("--EOF"):
        break
    codeium_code += line
print("Compiling...")
codeium_compiled = compile(codeium_code, "input.py", 'exec', flags=ast.PyCF_ONLY_AST)
print("Compiled")
codeiumBanner(codeium_compiled)
print("Codeium agent executing the safe code...")
exec(codeium_code)

