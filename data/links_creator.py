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
import os

from PySide import QtCore, QtGui
from ui.links import Ui_Links
from bb_shared import Shared

class LinksApp(QtGui.QWidget, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Shared.__init__(self)
        self.gui = Ui_Links()
        self.gui.setupUi(self)

        self.gui.tree_url.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_url.setSortingEnabled(1)
        self.gui.tree_url.headerItem().setText(0, ('League'))
        self.gui.tree_url.headerItem().setText(1, ('url'))
        self.gui.tree_url_fd.headerItem().setText(0, ('url'))
        self.gui.tree_url.setColumnWidth(0,200)
        self.gui.tree_url.setColumnWidth(1,800)
        self.gui.tree_url_fd.setColumnWidth(0,200)
        self.gui.tree_url_fd.setColumnWidth(1,800)
        self.default_url = 'http://stats.betradar.com/s4/?clientid=271&language=en#2_1,22_1'
        self.default_url_fd = 'http://www.football-data.co.uk/englandm.php'
        self.gui.line_url.setText(self.default_url)
        self.gui.line_address_fd.setText(self.default_url_fd)
        self.gui.webView.load(QtCore.QUrl(self.default_url))
        self.gui.webView_fd.load(QtCore.QUrl(self.default_url_fd))
        self.bindings()
        self.tree_link_saved()
        self.tree_link_saved_fd()

    def bindings(self):
        ''' Widgets connections'''
        self.gui.button_add.clicked.connect(self.add_url)
        self.gui.button_add_fd.clicked.connect(self.add_url_fd)
        self.gui.webView.urlChanged.connect(self.url_change)
        self.gui.webView_fd.urlChanged.connect(self.url_change_fd)
        self.gui.button_save.clicked.connect(self.save_urls)
        self.gui.button_save_fd.clicked.connect(self.save_urls_fd)
        self.gui.button_next.clicked.connect(self.gui.webView.forward)
        self.gui.button_previous.clicked.connect(self.gui.webView.back)
        self.gui.button_next_fd.clicked.connect(self.gui.webView_fd.forward)
        self.gui.button_prev_fd.clicked.connect(self.gui.webView_fd.back)
        self.gui.button_delete.clicked.connect(self.delete)
        self.gui.button_delete_fd.clicked.connect(self.delete_fd)
        self.gui.button_clear.clicked.connect(self.gui.tree_url.clear)
        self.gui.button_clear_fd.clicked.connect(self.gui.tree_url_fd.clear)
        self.gui.button_remove.clicked.connect(self.remove)
        self.gui.button_remove_fd.clicked.connect(self.remove_fd)
        self.gui.button_load.clicked.connect(self.load_base)
        self.gui.button_load_fd.clicked.connect(self.load_base_fd)
        self.gui.tree_link_bases.doubleClicked.connect(self.load_base)
        self.gui.button_check.clicked.connect(self.check_link)
        self.gui.line_name.textChanged.connect(self.line_sync)
    def line_sync(self):
        ''' Line (league name) to line (save) synchronization'''
        self.gui.line_save.setText(self.gui.line_name.text())
    def check_link(self):
        ''' Open url in browser'''
        item = self.gui.tree_url.currentItem()
        url = item.text(1)
        x = self.gui.webView.page()
        self.x = x.mainFrame()
        self.x.load(QtCore.QUrl(url))

    def url_change(self):
        ''' Changes url in addres bar - website scraping'''
        url = self.gui.webView.url()
        url = url.toString()
        self.gui.line_url.setText(url)

    def url_change_fd(self):
        ''' Changes url in addres bar - football data'''
        url = self.gui.webView_fd.url()
        url = url.toString()
        self.gui.line_address_fd.setText(url)

    def add_url(self):
        ''' Adds url to list- scrape website'''
        item_url = QtGui.QTreeWidgetItem(self.gui.tree_url)
        item_url.setText(0, self.gui.line_name.text())
        item_url.setText(1, self.gui.line_url.text())

    def add_url_fd(self):
        ''' Adds url to list - football-data.co.uk'''
        item_url = QtGui.QTreeWidgetItem(self.gui.tree_url_fd)
        item_url.setText(0, self.gui.line_url_fd.text())

    def save_urls(self):
        ''' Saves url profile - website scraping'''
        file_name = self.gui.line_save.text()
        with open(os.path.join('profiles', 'links', '')\
                    +str(file_name), 'w') as file_save:
            count = self.gui.tree_url.topLevelItemCount()
            for i in range(0, count):
                item = self.gui.tree_url.topLevelItem(i)
                name = item.text(0)
                url = item.text(1)
                if i == count-1:
                    line = str(name+' '+url)
                else:
                    line = str(name+' '+url+self.nl)
                file_save.write(line)
        self.tree_link_saved()

    def save_urls_fd(self):
        ''' Saves url profile - football data'''
        file_name = self.gui.line_save_fd.text()
        with open(os.path.join('profiles', 'football_data', '')\
                +str(file_name), 'w') as file_save:
            count = self.gui.tree_url_fd.topLevelItemCount()
            for i in range(0, count):
                item = self.gui.tree_url_fd.topLevelItem(i)
                url = item.text(0)
                if i == count-1:
                    line = str(url)
                else:
                    line = str(url+self.nl)
                file_save.write(line)
        self.tree_link_saved_fd()

    def tree_link_saved(self):
        ''' Shows list of saved profiles in tree'''
        self.gui.tree_link_bases.clear()
        self.gui.tree_link_bases.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_link_bases.setSortingEnabled(1)
        self.gui.tree_link_bases.headerItem().setText(0, ('Saved'))
        dir_bases = os.listdir(os.path.join('profiles','links'))
        for i in dir_bases:
            item = QtGui.QTreeWidgetItem(self.gui.tree_link_bases)
            item.setText(0, i)

    def tree_link_saved_fd(self):
        ''' Shows list of saved profiles in tree'''
        self.gui.tree_link_bases_fd.clear()
        self.gui.tree_link_bases_fd.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_link_bases_fd.setSortingEnabled(1)
        self.gui.tree_link_bases_fd.headerItem().setText(0, ('Saved'))
        dir_bases = os.listdir(os.path.join('profiles','football_data'))
        for i in dir_bases:
            item = QtGui.QTreeWidgetItem(self.gui.tree_link_bases_fd)
            item.setText(0, i)

    def delete(self):
        ''' Deletes file - websote scraping'''
        path = os.path.join('profiles', 'links', '')
        item = self.gui.tree_link_bases.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.tree_link_saved()

    def delete_fd(self):
        ''' Deletes file - football date'''
        path = os.path.join('profiles', 'football_data', '')
        item = self.gui.tree_link_bases_fd.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.tree_link_saved_fd()

    def remove(self):
        ''' Removes link from tree - scrape website'''
        item = self.gui.tree_url.currentItem()
        index = self.gui.tree_url.indexOfTopLevelItem(item)
        self.gui.tree_url.takeTopLevelItem(index)

    def remove_fd(self):
        ''' Removes link from tree - football-data.co.uk'''
        item = self.gui.tree_url_fd.currentItem()
        index = self.gui.tree_url_fd.indexOfTopLevelItem(item)
        self.gui.tree_url_fd.takeTopLevelItem(index)

    def load_base(self):
        ''' Load url profile to tree - website scraping'''
        child = self.gui.tree_link_bases.currentItem()
        file_name = str(child.text(0))
        with open(os.path.join('profiles', 'links', '')+file_name, 'r') as file_load:
            self.gui.tree_url.clear()
            for i in file_load:
                name, url = i.split(' ')
                url = self.rm_lines(url)
                item_url = QtGui.QTreeWidgetItem(self.gui.tree_url)
                item_url.setText(0, name)
                item_url.setText(1, url)

    def load_base_fd(self):
        ''' Load url profile to tree - football data'''
        child = self.gui.tree_link_bases_fd.currentItem()
        file_name = str(child.text(0))
        with open(os.path.join('profiles', 'football_data', '')+file_name, 'r') as file_load:
            self.gui.tree_url_fd.clear()
            for i in file_load:
                url = i
                url = self.rm_lines(url)
                item_url = QtGui.QTreeWidgetItem(self.gui.tree_url_fd)
                item_url.setText(0, url)

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = LinksApp()
    MYAPP.show()
    sys.exit(APP.exec_())
