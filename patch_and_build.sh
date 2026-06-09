#!/bin/bash
python3 -c "
import glob
for f in glob.glob('/home/user/.venv/lib/python*/site-packages/buildozer/__init__.py'):
    txt = open(f).read()
    txt = txt.replace(\"cont = input('Are you sure you want to continue [y/n]? ')\", \"cont = 'y'\")
    open(f, 'w').write(txt)
    print('Patched:', f)
"
buildozer android debug
