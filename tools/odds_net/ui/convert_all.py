#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os

class ConvertAll():
    def __init__(self):
        x = os.listdir(os.getcwd())
        for i in x:
            if i[-2:] == 'ui':
               os.system('pyside-uic %s -o %spy'%(i,i[:-2]))
if __name__ == '__main__':
    conv = ConvertAll()

