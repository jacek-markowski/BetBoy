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
import sys
import re
import os
from csv import reader
import platform
import urllib2

from PySide import QtCore, QtGui
from ui.update import Ui_Update
import time
from bb_shared import Shared



matches = []
system = platform.system()


class Scrape(QtCore.QThread, Shared):
    ''' Scrapes page'''
    def __init__(self, radio, league, parent=None):
        QtCore.QThread.__init__(self)
        Shared.__init__(self)
        self.league = league
        self.path = radio

    def run(self):
        ''' Start thread'''
        self.scrape()

    def scrape(self):
        ''' Scrapes page'''
        global matches
        print 'scrape', str(self.league)
        matches = []
        self.update_state = 1
        with open(os.path.join('tmp','')+'page','r') as f:
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
        with open(os.path.join('tmp','')+'tmp','w') as tmp_file:
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
                matches.append(line)
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
        with (open(os.path.join('tmp','')+'tmp','r')) as to_fix:
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
        with open(os.path.join('tmp','')+'tmp','w') as fixed:
            for i in new_file:
                fixed.write(str(i))
        with open(os.path.join('tmp','')+'tmp','r') as f:
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

class UpdateApp(QtGui.QWidget, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Shared.__init__(self)
        with open(os.path.join('tmp','')+'comm','w') as comm:
            # communicates with export manager
            comm.write('')
        self.gui = Ui_Update()
        self.gui.setupUi(self)
        self.gui.tree_selected.headerItem().setText(0,
                                                   ('League'))
        self.gui.tree_selected.headerItem().setText(1,
                                                    ('url'))
        self.gui.tree_links.headerItem().setText(0,
                                                    ('Links'))
        self.gui.tree_selected.setColumnWidth(0, 200)
        self.gui.tree_selected.setColumnWidth(1, 800)
        self.page = self.gui.webView.page().mainFrame()
        self.update_state = 0
        self.scrape = 0
        self.bindings()
        self.links_profiles() # website scraping
        self.links_profiles_fd() #football-data.co.uk
        self.combo_path()

    def closeEvent(self, event):
        with open(os.path.join('tmp','')+'comm','w') as comm:
            # communicates with export manager
            comm.write('stop')
        self.find_broken_leagues()
        event.accept()

    def delete(self):
        ''' Deletes file'''
        path = os.path.join('profiles', 'links', '')
        item = self.gui.tree_profiles.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.links_profiles()

    def delete_fd(self):
        ''' Deletes file'''
        path = os.path.join('profiles', 'football_data', '')
        item = self.gui.tree_profiles_fd.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.links_profiles_fd()

    def bindings(self):
        ''' Widgets bindings'''
        self.gui.tree_links.clicked.connect(self.set_address)
        self.gui.button_check.clicked.connect(self.check_link)
        self.gui.button_load.clicked.connect(self.links_load)
        self.gui.tree_profiles.doubleClicked.connect(self.links_load)
        self.gui.button_add.clicked.connect(self.links_add)
        self.gui.tree_links.doubleClicked.connect(self.links_add)
        self.gui.button_all.clicked.connect(self.links_add_all)
        self.gui.button_remove.clicked.connect(self.links_remove)
        self.gui.button_update.clicked.connect(self.update)
        self.gui.button_update_fd.clicked.connect(self.update_fd)
        self.gui.button_clear.clicked.connect(self.gui.tree_selected.clear)
        self.page.loadFinished.connect(self._load_finished)
        self.gui.button_delete.clicked.connect(self.delete)
        self.gui.button_fd_delete.clicked.connect(self.delete_fd)
        self.gui.button_save.clicked.connect(self.save_urls)

    def update(self):
        ''' Download all selected links'''
        self.page.loadFinished.connect(self._load_finished)
        count = self.gui.tree_selected.topLevelItemCount()
        self.gui.button_update.setEnabled(0)
        path = self.gui.combo_path.currentText()
        self.path = os.path.join('leagues', path, '')
        for i in xrange(0, count):
            with open(os.path.join('tmp','')+'comm','r') as comm:
            # communicates with export manager
                comm_var = comm.readline()
            if comm_var != '':
                break
            self.page.setZoomFactor(0.7)
            self.update_state = 0
            child = self.gui.tree_selected.topLevelItem(i)
            self.league = child.text(0)
            self.url = child.text(1)
            self.page.load(QtCore.QUrl(self.url))
            while self.update_state == 0:
                QtGui.QApplication.processEvents()
            while self.scrape.isRunning():
                QtGui.QApplication.processEvents()
            self.url = 'about:black'
            self.page.load(QtCore.QUrl(self.url))
            self.gui.textBrowser.append(self.league)
            for i in matches:
                self.gui.textBrowser.append(i)
                QtGui.QApplication.processEvents()
                time.sleep(0.0001)
            self.gui.textBrowser.append('--------------')

        self.gui.button_update.setEnabled(1)
        self.find_broken_leagues()
    def update_fd(self):
        ''' Updates database from football-data.co.uk'''
        item = self.gui.tree_profiles_fd.currentItem()
        profile = item.text(0)
        with open(os.path.join('profiles','football_data','')+profile) as f:
            file_open = reader(f,delimiter=' ')
            for i in file_open:
                url = i[0]
                name = url.split('/')[-1]
                if name != 'fixtures.csv':
                    url_dwonload = urllib2.urlopen(url)
                    with open(os.path.join('tmp','')+'fb', 'wb') as f:
                        meta = url_dwonload.info()
                        file_size = int(meta.getheaders("Content-Length")[0])
                        print "Downloading: %s Bytes: %s" % (name, file_size)
                        file_size_dl = 0
                        block_sz = 8192
                        while True:
                            buffer = url_dwonload.read(block_sz)
                            if not buffer:
                                break
                            file_size_dl += len(buffer)
                            f.write(buffer)
                            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                            status = status + chr(8)*(len(status)+1)
                            print status,
                        self.convert_fd(name)
                        self.gui.textBrowser_fd.append('Downloaded: %s'%name)
                        self.gui.textBrowser_fd.append('-----------------')
                        QtGui.QApplication.processEvents()
                else:
                    url_dwonload = urllib2.urlopen(url)
                    with open(os.path.join('tmp','')+'fixtures', 'wb') as f:
                        meta = url_dwonload.info()
                        file_size = int(meta.getheaders("Content-Length")[0])
                        print "Downloading: %s Bytes: %s" % (name, file_size)
                        file_size_dl = 0
                        block_sz = 8192
                        while True:
                            buffer = url_dwonload.read(block_sz)
                            if not buffer:
                                break
                            file_size_dl += len(buffer)
                            f.write(buffer)
                            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                            status = status + chr(8)*(len(status)+1)
                            print status,
                        self.merge_fixtures(name)
                        self.gui.textBrowser_fd.append('Merged upcoming matches')
                        self.gui.textBrowser_fd.append('-----------------')
                        QtGui.QApplication.processEvents()

    def merge_fixtures(self,name):
        ''' Adding upcoming matches to league files - football_data.co.uk'''
        with open(os.path.join('tmp','')+'fixtures','r') as f:
            csv_file = reader(f)
            dir_bases = os.listdir(os.path.join('leagues','football_data'))
            files = []
            for i in dir_bases:
                files.append(i)
            for i in csv_file:
                if i[0]+'.csv' in files:
                    with open(os.path.join('leagues','football_data','')+i[0]+'.csv','a') as file_old:
                        date = self.fix_date(i[1])
                        home = i[2].replace(' ','')
                        away = i[3].replace(' ','')
                        line = date+','+home+','+away+',NULL'+',NULL'
                        file_old.write(line+self.nl)

    def num_date(self,date):
        date_num = date[0:7]+date[8:]
        date_num = float(date_num)
        return date_num

    def convert_fd(self,name):
        ''' Converts file from football-data.co.uk'''
        with open(os.path.join('tmp','')+'fb','r') as f:
            csv_file = reader(f)
            with open(os.path.join('leagues','football_data','')+name,'w') as out_file:
                for i in csv_file:
                    if i[1] == 'Date':
                        pass
                    if i[1] != 'Date':
                        if len(i[1])>4:
                            date = self.fix_date(i[1])
                            try:
                                fth = i[4]
                                fta = i[5]
                            except:
                                fth = ''
                                fta = ''
                            home = i[2].replace(' ','')
                            away = i[3].replace(' ','')
                            if fth == '' or fta == '':
                                pass
                            else:
                                line = date+','+home+','+away+','+fth+','+fta
                                out_file.write(line+'\n')
    def fix_date(self,date):
        ''' Converts date to betboy format from football-data.co.uk'''
        try:
            day,month,year = date.split('/')
        except:
            pass
        try:
            day,month,year = date.split('.')
        except:
            pass
        if int(year) > 0 and int(year) < 30 and len(year)<4:
            year = 2000 + int(year)
        elif int(year) <= 99  and len(year)<4:
            year = 1900 + int(year)
        new_date = str(year)+'.'+month+'.'+day
        return new_date
    def _load_finished(self):
        ''' When main frame loaded(page fully loaded), start scraping'''
        self.update_state = 1
        self.threads = []
        try:
            x = self.scrape.isRunning()
            print 'Scrape is runing, wait to finish'
        except:
            x = 0
        if x == 1:
            pass
        else:
            if self.url != 'about:black':
                print 'New Scrape'
                html = self.page.toHtml()
                html = html.encode('utf-8') #needed on windows
                with open(os.path.join('tmp','')+'page','w') as save_file:
                    save_file.write(html)
                self.threads.append(self.scrape)
                self.scrape = Scrape(self.path, self.league)
                self.scrape.start()

    def links_remove(self):
        ''' Remove links froma list'''
        item = self.gui.tree_selected.currentItem()
        index = self.gui.tree_selected.indexOfTopLevelItem(item)
        self.gui.tree_selected.takeTopLevelItem(index)

    def links_add(self):
        ''' Add url to list'''
        child = self.gui.tree_links.currentItem()
        name = str(child.text(0))
        item = QtGui.QTreeWidgetItem(self.gui.tree_selected)
        item.setText(0, name)
        item.setText(1, self.links_dict[str(name)])
        self.gui.tree_selected

    def links_add_all(self):
        ''' add alll url to list'''
        count = self.gui.tree_links.topLevelItemCount()
        for i in xrange(0, count):
            child = self.gui.tree_links.topLevelItem(i)
            name = child.text(0)
            item = QtGui.QTreeWidgetItem(self.gui.tree_selected)
            item.setText(0, name)
            item.setText(1, self.links_dict[str(name)])

    def links_load(self):
        ''' Load urls from file'''
        child = self.gui.tree_profiles.currentItem()
        file_name = str(child.text(0))
        with open(os.path.join('profiles', 'links', '')+file_name, 'r') as links:
            self.links_dict = {}
            for i in links:
                key, val = i.split(' ')
                val = self.rm_lines(val)
                self.links_dict[key] = val
            self.links_tree()

    def set_address(self):
        ''' Setes address bar for browser after clicked'''
        item = self.gui.tree_links.currentItem()
        key = item.text(0)
        self.gui.line_address.setText(self.links_dict[str(key)])

    def links_profiles(self):
        ''' Shows saved urls in tree'''
        self.gui.tree_profiles.clear()
        self.gui.tree_profiles.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_profiles.setSortingEnabled(1)
        self.gui.tree_profiles.headerItem().setText(0, ('Saved'))
        dir_bases = os.listdir(os.path.join('profiles','links'))
        for i in dir_bases:
            item = QtGui.QTreeWidgetItem(self.gui.tree_profiles)
            item.setText(0, i)

    def links_profiles_fd(self):
        ''' Shows saved urls in tree - football-data.co.uk '''
        self.gui.tree_profiles_fd.clear()
        self.gui.tree_profiles_fd.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_profiles_fd.setSortingEnabled(1)
        self.gui.tree_profiles_fd.headerItem().setText(0, ('Saved'))
        dir_bases = os.listdir(os.path.join('profiles','football_data'))
        for i in dir_bases:
            item = QtGui.QTreeWidgetItem(self.gui.tree_profiles_fd)
            item.setText(0, i)

    def combo_path(self):
        ''' Combo with path where to download'''
        paths = []
        for path, folder, name in os.walk("leagues/"):
            name = os.path.split(path)
            if name[1] != 'football_data':
                paths.append(name[1])
        paths.pop(0)
        paths.reverse()
        print paths
        self.gui.combo_path.addItems(paths)
        self.gui.combo_path.setCurrentIndex(0)

    def links_tree(self):
        ''' Fills selected links tree witch links'''
        self.gui.tree_links.clear()
        self.gui.tree_links.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_links.setSortingEnabled(1)
        self.gui.tree_links.headerItem().setText(0, ('Links'))
        for i in self.links_dict:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_links)
            item_exp.setText(0, (i))

    def check_link(self):
        ''' Open url in browser'''
        try:
            self.page.loadFinished.disconnect(self._load_finished)
        except:
            pass

        self.url = self.gui.line_address.text()
        x = self.gui.webView.page()
        self.x = x.mainFrame()
        self.x.setZoomFactor(0.7)
        self.x.load(QtCore.QUrl(self.url))

    def save_urls(self):
        ''' Saves url profile'''
        file_name = self.gui.line_save.text()
        with open(os.path.join('profiles', 'links', '')\
        +str(file_name), 'w') as file_save:
            count = self.gui.tree_selected.topLevelItemCount()
            for i in range(0, count):
                item = self.gui.tree_selected.topLevelItem(i)
                name = item.text(0)
                url = item.text(1)
                if i == count-1:
                    line = str(name+' '+url)
                else:
                    line = str(name+' '+url+self.nl)
                file_save.write(line)
        self.links_tree()

    def rm_lines(self, item):
        ''' Removes new lines from string'''
        rem = item.replace('\n', '')
        rem = rem.replace('\r', '')
        rem = rem.replace(' ', '')
        return rem

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = UpdateApp()
    MYAPP.show()
    sys.exit(APP.exec_())
