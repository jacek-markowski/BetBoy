#!usr/bin/env python
import os
import shutil

dirs_ = ['.git',
         'data/tmp',
         'data/export',
         'data/tmp',
         'data/leagues',
         'tools']
files_ =['data/icons.zip',
         'data/*.pyc',
         '.gitignore',
         'readme.md']
for i in dirs_:
    try:
        shutil.rmtree(i)
    except:
        print 'erorr:' + i +'\n'
for i in files_:
    try:
        os.remove(i)
    except:
        print 'erorr:' + i +'\n'




