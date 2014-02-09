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
import platform

from PySide import QtCore, QtGui
from ui.update import Ui_Update
from bb_shared import Shared
import betradar
from betexploerer import BetExploerer




system = platform.system()

class UpdateApp(QtGui.QWidget, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Shared.__init__(self)
        with open(os.path.join('tmp','comm'),'w') as comm:
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
        ## webview settings: don't load images
        settings = self.gui.webView.settings()
        settings.setAttribute(settings.AutoLoadImages,False)
        self.update_state = 0
        self.scrape = 0
        self.bindings()
        self.links_profiles() # website scraping
        #self.links_profiles_fd() #football-data.co.uk
        self.combo_path()

    def closeEvent(self, event):
        with open(os.path.join('tmp','comm'),'w') as comm:
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
       # self.links_profiles_fd()

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
       # self.gui.button_update_fd.clicked.connect(self.update_fd)
        self.gui.button_clear.clicked.connect(self.gui.tree_selected.clear)
        self.page.loadFinished.connect(self._load_finished)
        self.gui.button_delete.clicked.connect(self.delete)
       # self.gui.button_fd_delete.clicked.connect(self.delete_fd)
        self.gui.button_save.clicked.connect(self.save_urls)

    def update(self):
        ''' Download all selected links'''
        self.be_mode = 'results' #betexploere update stage
        self.page.loadFinished.connect(self._load_finished)
        count = self.gui.tree_selected.topLevelItemCount()
        self.gui.button_update.setEnabled(0)
        path = self.gui.combo_path.currentText()
        self.path = os.path.join('leagues', path, '')
        for i in xrange(0, count):
            with open(os.path.join('tmp','comm'),'r') as comm:
            # communicates with update manager
                comm_var = comm.readline()
            if comm_var != '':
                break
            self.page.setZoomFactor(0.7)
            self.update_state = 0
            ############################
            ############################
            child = self.gui.tree_selected.topLevelItem(i)
            self.league = child.text(0)
            self.url = child.text(1)
            ###
            ##Choosing scrape mode
            pattern_br ='betradar'
            pattern_be ='betexplorer'
            if pattern_br in self.url:
                self.update_mode = pattern_br
            else:
                self.update_mode = pattern_be

            # betexploerer
            if self.update_mode == 'betexplorer':
                self.be_mode='results'
                self.url_1 =self.url+'results/'
                self.url_2 =self.url+'fixtures/'
                be_urls = [self.url_1,self.url_2]
                for i in be_urls:
                    self.update_state = 1
                    self.page.load(QtCore.QUrl(i))
                    while self.update_state == 1:
                        QtGui.QApplication.processEvents()
                    print '...........................................'
            #betradar
            if self.update_mode == 'betradar':
                self.update_state = 1
                self.page.load(QtCore.QUrl(self.url))
                while self.update_state == 1:
                    QtGui.QApplication.processEvents()

            self.url = 'about:black'
            self.page.load(QtCore.QUrl(self.url))
            self.gui.textBrowser.append(self.league)
            self.gui.textBrowser.append('--------------')
        self.gui.textBrowser.append('Update finished')
        self.gui.button_update.setEnabled(1)
        self.find_broken_leagues()

    def _load_finished(self):
        ''' When main frame loaded(page fully loaded), start scraping'''
        if self.url != 'about:black' and self.update_state == 1:
            print 'New Scrape'
            html = self.page.toHtml()
            html = html.encode('utf-8') #needed on windows
            with open(os.path.join('tmp','page'),'w') as save_file:
                save_file.write(html)
            if self.update_mode == 'betradar':
                self.scrape = betradar.Scrape(self.path, self.league)
            else:
                if self.be_mode == 'results':
                    self.scrape = BetExploerer(self.path + self.league,self.be_mode)
                    self.be_mode = 'fixtures'
                else:
                    self.scrape = BetExploerer(self.path + self.league,self.be_mode)
                    self.be_mode = 'results'
        self.update_state = 0
            

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
        with open(os.path.join('profiles', 'links', file_name), 'r') as links:
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
        with open(os.path.join('profiles', 'links', str(file_name))\
        , 'w') as file_save:
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
