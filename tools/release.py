#!usr/bin/env python
import os
import shutil

shutil.rmtree('data/tmp')
shutil.rmtree('data/export')
shutil.rmtree('data/tmp')
shutil.rmtree('data/leagues')
os.remove('data/icons.zip')
os.remove('data/*.pyc')



