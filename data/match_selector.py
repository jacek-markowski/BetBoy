#!/usr/bin/env python
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
from ui.match_selector import Ui_Selector
from bb_engine import Database
from bb_shared import Shared

class SelectorApp(QtGui.QWidget, Database, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Database.__init__(self)
        Shared.__init__(self)
        self.odds_level = 100
        self.app = 'selector'
        self.gui = Ui_Selector()
        self.gui.setupUi(self)
        self.gui.tree_selected.headerItem().setText(0, ('Selected'))
        self.filters_tree()
        self.leagues_tree()
        self.bindings()
        self.filters_load()

    def closeEvent(self, event):
        self.stop_action = 1
        event.accept()

    def bindings(self):
        ''' Bindings for widgets'''
        self.gui.button_filters_save.clicked.connect(self.filters_save)
        self.gui.button_filters_load.clicked.connect(self.filters_load)
        self.gui.tree_filters_profile.clicked.connect(self.filters_name)
        self.gui.button_select.clicked.connect(self.match_select)
        self.gui.button_filters_delete.clicked.connect(self.filters_delete)

    def filters_delete(self):
        ''' Deletes match filter'''
        path = os.path.join('profiles','selector','')
        item = self.gui.tree_filters_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.filters_tree()

    def filters_name(self):
        item = self.gui.tree_filters_profile.currentItem()
        file_name = str(item.text(0))
        self.gui.line_filters.setText(file_name)
    def leagues_tree(self):
        ''' Creates leageues tree'''
        self.gui.tree_leagues.headerItem().setText(0, ('Leagues'))
        self.gui.tree_leagues.sortItems(0, QtCore.Qt.SortOrder(0))

        paths = []
        for i in os.walk("leagues/"):
            paths.append(i[0])
        paths.pop(0)
        paths.reverse()
        for i in paths:
            name = os.path.split(i)
            name = name[1]
            item = QtGui.QTreeWidgetItem(self.gui.tree_leagues)
            item.setText(0, (name))
            files = os.listdir(i)
            for f in files:
                QtGui.QTreeWidgetItem(item).setText(0, f)
        self.gui.tree_leagues.setSortingEnabled(0)
        item.setExpanded(1)
        self.gui.tree_leagues.setCurrentItem(item.child(0))
        self.gui.tree_leagues.setSortingEnabled(1)

    def match_select(self):
        ''' Select matches from league or all leagues from directory'''
        self.gui.button_select.setEnabled(0)
        child = self.gui.tree_leagues.currentItem()
        league = child.text(0)
        try:
            parent = child.parent()
            parent = parent.text(0)
        except:
            parent = 0

        if parent:
            path = os.path.join('leagues',parent,'')
            self.batch_bets(path,league)
        else:
            self.gui.progress_bar.setValue(0)
            dir_leagues = os.listdir(os.path.join('leagues',league))
            dir_leagues.sort()
            number_of_leagues = len(dir_leagues)
            index = 1.0
            for i in dir_leagues:
                path = os.path.join('leagues',league,'')
                #if self.stop_action == 0:
                self.batch_bets(path,i)
                QtGui.QApplication.processEvents()
                index += 1.0
                prog_val = index/number_of_leagues*100
                self.gui.progress_bar.setValue(prog_val)
        self.item_sim = QtGui.QTreeWidgetItem(self.gui.tree_selected)
        line = '_________________Done.________________'
        self.item_sim.setText(0,(line))
        self.gui.button_select.setEnabled(1)

    def batch_bets(self,path,league):
        ''' Gives bets'''
        # filter
        item = self.gui.tree_filters.currentItem()
        file_name = item.text(0)
        self.filters_load(file_name)
        ####
        self.load_csv(path,league)
        min_date = self.relations_base.execute('''SELECT min(date_num)
                                    From Results WHERE
                                    gHomeEnd == "NULL"''')
        min_date = min_date.fetchone()
        min_date = min_date[0]
        if min_date:
            matches = self.relations_base.execute('''SELECT date_txt,home,away
                            From Results WHERE
                            gHomeEnd == "NULL" and date_num=%f'''%min_date)
            matches = matches.fetchall()
        else:
            matches = []


        if len(matches)>0:
            self.item_sim = QtGui.QTreeWidgetItem(self.gui.tree_selected)
            line = league+' filter: '+file_name
            self.item_sim.setText(0,(line))
            self.gui.tree_selected.setCurrentItem(self.item_sim)
            for i in matches:
                date,home,away = i
                self.simulation_filters(home,away)
                self.filter_status = ''
                self.simulation_match_filters()
                if self.filter_status == 'yes':
                    line = date+' '+home+' - '+away+\
                    '  1: '+str(round(self.odd_1,2))+\
                    '  x: '+str(round(self.odd_x,2))+\
                    '  2: '+str(round(self.odd_2,2))+\
                    '  1x: '+str(round(self.odd_1x,2))+\
                    '  x2: '+str(round(self.odd_x2,2))
                    QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))


    def filters_tree(self):
        ''' Tree with saved match filters'''
        self.gui.tree_filters_profile.clear()
        self.gui.tree_filters_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters_profile.setSortingEnabled(1)
        self.gui.tree_filters_profile.headerItem().setText(0, ('Match filters'))
        dir_exports = os.listdir(os.path.join('profiles','selector'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters_profile)
            item_exp.setText(0, (i))
        self.gui.tree_filters_profile.setCurrentItem(item_exp)

        self.gui.tree_filters.clear()
        self.gui.tree_filters.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters.setSortingEnabled(1)
        self.gui.tree_filters.headerItem().setText(0, ('Match filters'))
        dir_exports = os.listdir(os.path.join('profiles','selector'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters)
            item_exp.setText(0, (i))
        self.gui.tree_filters.setCurrentItem(item_exp)

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = SelectorApp()
    MYAPP.show()
    sys.exit(APP.exec_())

