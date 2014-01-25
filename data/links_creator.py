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
        self.gui.tree_url.setColumnWidth(0,200)
        self.gui.tree_url.setColumnWidth(1,800)
        self.default_url = 'http://stats.betradar.com/s4/?clientid=271&language=en#2_1,22_1'
        self.gui.line_url.setText(self.default_url)
        self.gui.webView.load(QtCore.QUrl(self.default_url))
        self.bindings()
        self.tree_link_saved()


    def bindings(self):
        ''' Widgets connections'''
        self.gui.button_add.clicked.connect(self.add_url)
        self.gui.webView.urlChanged.connect(self.url_change)
        self.gui.button_save.clicked.connect(self.save_urls)
        self.gui.button_next.clicked.connect(self.gui.webView.forward)
        self.gui.button_previous.clicked.connect(self.gui.webView.back)
        self.gui.button_delete.clicked.connect(self.delete)
        self.gui.button_clear.clicked.connect(self.gui.tree_url.clear)
        self.gui.button_remove.clicked.connect(self.remove)
        self.gui.button_load.clicked.connect(self.load_base)
        ## betradar betexplorer buttons
        self.gui.button_betradar.clicked.connect(self.change_to_betradar)
        self.gui.button_betexplorer.clicked.connect(self.change_to_betexplorer)


        self.gui.tree_link_bases.doubleClicked.connect(self.load_base)
        self.gui.button_check.clicked.connect(self.check_link)
        self.gui.line_name.textChanged.connect(self.line_sync)
        self.gui.tree_link_bases.clicked.connect(self.load_name)
    def change_to_betradar(self):
        self.gui.webView.load(QtCore.QUrl(self.default_url))
    def change_to_betexplorer(self):
        url= 'http://www.betexplorer.com/soccer/'
        self.gui.webView.load(QtCore.QUrl(url))
    def load_name(self):
        ''' Sets loaded file name in text line'''
        child = self.gui.tree_link_bases.currentItem()
        file_name = str(child.text(0))
        self.gui.line_save.setText(file_name)
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

    def add_url(self):
        ''' Adds url to list- scrape website'''
        item_url = QtGui.QTreeWidgetItem(self.gui.tree_url)
        item_url.setText(0, self.gui.line_name.text())
        item_url.setText(1, self.gui.line_url.text())


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

    def delete(self):
        ''' Deletes file - websote scraping'''
        path = os.path.join('profiles', 'links', '')
        item = self.gui.tree_link_bases.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.tree_link_saved()

    def remove(self):
        ''' Removes link from tree - scrape website'''
        item = self.gui.tree_url.currentItem()
        index = self.gui.tree_url.indexOfTopLevelItem(item)
        self.gui.tree_url.takeTopLevelItem(index)

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



if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = LinksApp()
    MYAPP.show()
    sys.exit(APP.exec_())
