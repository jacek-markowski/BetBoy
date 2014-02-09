# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski, jacek87markowski@gmail.com

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

from PySide import QtCore,QtGui
import re
import os
from csv import reader
from bb_shared import Shared

class Scrape(Shared):
    ''' Scrapes page'''
    def __init__(self, radio, league, parent=None):
        Shared.__init__(self)
        self.league = league
        self.path = radio
        self.run()
    def run(self):
        ''' Start'''
        self.scrape()

    def scrape(self):
        ''' Scrapes page'''
        #global matches
        print 'scrape', str(self.league)
        matches = []
        self.update_state = 1
        with open(os.path.join('tmp','page'),'r') as f:
            html_page = f.read()
        re_patternA = '<td class="datetime">\s*(?P<date>.{8}).*?</td>.*? \
        <span class="home.*?">\s*(?P<team_home>.*?)\s*</span>.*? \
        <span class="away.*?">\s*(?P<team_away>.*?)\s*</span>.*? \
        <td class="p1 ">\s*(?P<result_half>.*?)\s*</td>.*? \
        <td class="nt ftx ">\s*(?P<result_final>.*?)\s*</td>'
        re_patternB = '<td class="datetime">\s*(?P<date>.{8}).*?</td>.*? \
        <span class="home.*?">\s*(?P<team_home>.*?)\s*</span>.*? \
        <span class="away.*?">\s*(?P<team_away>.*?)\s*</span>.*? \
        <td class="nt ftx ">\s*(?P<result_final>.*?)\s*</td>'
        check = re.compile('<td class="p1 ">', re.DOTALL)
        page_check = check.search(html_page)
        with open(os.path.join('tmp','tmp'),'w') as tmp_file:
            if page_check:
                # 'Halftime and finaltime scores'
                pattern_compiled = re.compile(re_patternA, re.DOTALL)
                page_final = pattern_compiled.search(html_page)
            else:
                # 'Only finaltime scores'
                pattern_compiled = re.compile(re_patternB, re.DOTALL)
                page_final = pattern_compiled.search(html_page)
            while page_final:
                result_html = page_final.group('date', 'team_home',
                                               'team_away', 'result_final')
                final = re.search('(?P<home>.*)-(?P<away>.*)', result_html[3])
                try:
                    final_goals = final.group('home','away')
                except:
                    final_goals = ('NULL','NULL')
                line = str(result_html[0:3])+' '+str(final_goals)
                #matches.append(line)
                QtGui.QApplication.processEvents()
                date = result_html[0].strip()
                day, month, year = date.split('/')
                day = float(day)/10000
                month = float(month)/100
                year = float(year)
                if year > 30:
                    year = 1900 + year
                else:
                    year = 2000 + year

                date = year + month + day
                date = str(date)
                date = date[0:7]+'.'+date[7:]
                if len(date)<10:
                    date = date+'0'
                tmp_file.write(date+',')
                tmp_file.write(result_html[1].strip()+',')
                tmp_file.write(result_html[2].strip()+',')
                tmp_file.write(final_goals[0].strip()+',')
                tmp_file.write(final_goals[1].strip()+self.nl)
                html_page = re.sub(pattern_compiled, ' ', html_page, 1)
                page_final = pattern_compiled.search(html_page)
        #Fix file when downloading other sport disciplines with overtime tag
        new_file = []
        with (open(os.path.join('tmp','tmp'),'r')) as to_fix:
            n = reader(to_fix)
            for i in n:
                # re pattern
                re_fix = """(?P<value>.*?)<.*"""
                re_fix_compl = re.compile(re_fix)
                fixed_value = re.search(re_fix_compl, i[4])
                if fixed_value:
                    new_value = fixed_value.group('value')
                    i[4] = new_value
                fixed_value = re.search(re_fix_compl, i[3])
                if fixed_value:
                    new_value = fixed_value.group('value')
                    i[3] = new_value
                line = i[0]+','+i[1]+','+i[2]+','+i[3]+','+i[4]+'\n'
                new_file.append(line)
        with open(os.path.join('tmp','tmp'),'w') as fixed:
            for i in new_file:
                fixed.write(str(i))
        with open(os.path.join('tmp','tmp'),'r') as f:
            tmp_file = reader(f)
            tmp_file = list(tmp_file)
            tmp_file.reverse()
        # removes null matches in of middle file
        status = 'OK'
        match_list = []
        for i in xrange(0, len(tmp_file)):
            if tmp_file[i][3] == 'NULL' and status == 'OK':
                match_list.append(tmp_file[i])
            elif tmp_file[i][3] != 'NULL' and status == 'OK':
                status = 'BAD'
                match_list.append(tmp_file[i])
            elif tmp_file[i][3] != 'NULL' and status == 'BAD':
                match_list.append(tmp_file[i])
        with open(self.path+str(self.league),'w') as fix_file:
            match_list.reverse()
            for i in xrange(0, len(match_list)):
                line = str(match_list[i])
                line = line.replace('[','')
                line = line.replace(']','')
                line = line.replace("'",'')
                line = line.replace(' ','')
                fix_file.write(line+self.nl)
