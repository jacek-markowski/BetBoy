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
import platform
import os

from PySide import QtCore, QtGui
from ui.match_selector import Ui_Selector
from ng_engine import Database

system = platform.system()
if system == 'Windows':
    new_line = '\r\n'
elif system == 'Linux':
    new_line = '\n'
elif system == 'Darwin':
    new_line = '\r'
else:
    new_line = '\r\n'



class SelectorApp(QtGui.QWidget,Database):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Database.__init__(self)
        self.gui = Ui_Selector()
        self.gui.setupUi(self)
        self.gui.tree_selected.headerItem().setText(0, ('Selected'))
        self.filters_tree()
        self.leagues_tree()
        self.bindings()
        self.filters_load()

    def delete_file(self, file_delete, path):
        ''' Deletes file'''
        reply = QtGui.QMessageBox.question(self, 'Delete?',
            "Are you sure to delete %s?"%file_delete, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if file_delete != 'default':
                os.remove(path+file_delete)

    def bindings(self):
        ''' Bindings for widgets'''
        self.gui.button_filters_save.clicked.connect(self.filters_save)
        self.gui.button_filters_load.clicked.connect(self.filters_load)
        self.gui.button_select.clicked.connect(self.match_select)
        self.gui.button_filters_delete.clicked.connect(self.filters_delete)
    def filters_delete(self):
        ''' Deletes match filter'''
        path = os.path.join('profiles','selector','')
        item = self.gui.tree_filters_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.filters_tree()

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

    def filters_save(self):
        ''' Save match filter'''
        # series
        combo_h_wins = self.gui.combo_h_wins.currentText()
        combo_h_winshome = self.gui.combo_h_winshome.currentText()
        combo_h_draws = self.gui.combo_h_draws.currentText()
        combo_h_drawshome = self.gui.combo_h_drawshome.currentText()
        combo_h_loses = self.gui.combo_h_loses.currentText()
        combo_h_loseshome = self.gui.combo_h_loseshome.currentText()
        combo_h_nowins = self.gui.combo_h_nowins.currentText()
        combo_h_nowinshome = self.gui.combo_h_nowinshome.currentText()
        combo_h_nodraws = self.gui.combo_h_nodraws.currentText()
        combo_h_nodrawshome = self.gui.combo_h_nodrawshome.currentText()
        combo_h_noloses = self.gui.combo_h_noloses.currentText()
        combo_h_noloseshome = self.gui.combo_h_noloseshome.currentText()
        combo_a_wins = self.gui.combo_a_wins.currentText()
        combo_a_winsaway = self.gui.combo_a_winsaway.currentText()
        combo_a_draws = self.gui.combo_a_draws.currentText()
        combo_a_drawsaway = self.gui.combo_a_drawsaway.currentText()
        combo_a_loses = self.gui.combo_a_loses.currentText()
        combo_a_losesaway = self.gui.combo_a_losesaway.currentText()
        combo_a_nowins = self.gui.combo_a_nowins.currentText()
        combo_a_nowinsaway = self.gui.combo_a_nowinsaway.currentText()
        combo_a_nodraws = self.gui.combo_a_nodraws.currentText()
        combo_a_nodrawsaway = self.gui.combo_a_nodrawsaway.currentText()
        combo_a_noloses = self.gui.combo_a_noloses.currentText()
        combo_a_nolosesaway = self.gui.combo_a_nolosesaway.currentText()
        spin_h_wins = self.gui.spin_h_wins.value()
        spin_h_winshome = self.gui.spin_h_winshome.value()
        spin_h_draws = self.gui.spin_h_draws.value()
        spin_h_drawshome = self.gui.spin_h_drawshome.value()
        spin_h_loses = self.gui.spin_h_loses.value()
        spin_h_loseshome = self.gui.spin_h_loseshome.value()
        spin_h_nowins = self.gui.spin_h_nowins.value()
        spin_h_nowinshome = self.gui.spin_h_nowinshome.value()
        spin_h_nodraws = self.gui.spin_h_nodraws.value()
        spin_h_nodrawshome = self.gui.spin_h_nodrawshome.value()
        spin_h_noloses = self.gui.spin_h_noloses.value()
        spin_h_noloseshome = self.gui.spin_h_noloseshome.value()
        spin_a_wins = self.gui.spin_a_wins.value()
        spin_a_winsaway = self.gui.spin_a_winsaway.value()
        spin_a_draws = self.gui.spin_a_draws.value()
        spin_a_drawsaway = self.gui.spin_a_drawsaway.value()
        spin_a_loses = self.gui.spin_a_loses.value()
        spin_a_losesaway = self.gui.spin_a_losesaway.value()
        spin_a_nowins = self.gui.spin_a_nowins.value()
        spin_a_nowinsaway = self.gui.spin_a_nowinsaway.value()
        spin_a_nodraws = self.gui.spin_a_nodraws.value()
        spin_a_nodrawsaway = self.gui.spin_a_nodrawsaway.value()
        spin_a_noloses = self.gui.spin_a_noloses.value()
        spin_a_nolosesaway = self.gui.spin_a_nolosesaway.value()
        # odds
        spin_odd_1 = self.gui.spin_odd_1.value()
        spin_odd_x = self.gui.spin_odd_x.value()
        spin_odd_2 = self.gui.spin_odd_2.value()
        spin_odd_1x = self.gui.spin_odd_1x.value()
        spin_odd_x2 = self.gui.spin_odd_x2.value()

        val =[
        combo_h_wins,
        combo_h_winshome,
        combo_h_draws,
        combo_h_drawshome,
        combo_h_loses,
        combo_h_loseshome,
        combo_h_nowins,
        combo_h_nowinshome,
        combo_h_nodraws,
        combo_h_nodrawshome,
        combo_h_noloses,
        combo_h_noloseshome,
        combo_a_wins,
        combo_a_winsaway,
        combo_a_draws,
        combo_a_drawsaway,
        combo_a_loses,
        combo_a_losesaway,
        combo_a_nowins,
        combo_a_nowinsaway,
        combo_a_nodraws,
        combo_a_nodrawsaway,
        combo_a_noloses,
        combo_a_nolosesaway,
        spin_h_wins,
        spin_h_winshome,
        spin_h_draws,
        spin_h_drawshome,
        spin_h_loses,
        spin_h_loseshome,
        spin_h_nowins,
        spin_h_nowinshome,
        spin_h_nodraws,
        spin_h_nodrawshome,
        spin_h_noloses,
        spin_h_noloseshome,
        spin_a_wins,
        spin_a_winsaway,
        spin_a_draws,
        spin_a_drawsaway,
        spin_a_loses,
        spin_a_losesaway,
        spin_a_nowins,
        spin_a_nowinsaway,
        spin_a_nodraws,
        spin_a_nodrawsaway,
        spin_a_noloses,
        spin_a_nolosesaway,
        spin_odd_1,
        spin_odd_x,
        spin_odd_2,
        spin_odd_1x,
        spin_odd_x2
        ]
        file_name = self.gui.line_filters.text()
        save = open(os.path.join('profiles','selector','')+file_name,'w')
        for i in val:
            save.write(str(i)+new_line)
        save.close()
        self.filters_tree()

    def filters_load(self,file_name=None):
        ''' Load match filter'''
        val =[
        self.gui.combo_h_wins,
        self.gui.combo_h_winshome,
        self.gui.combo_h_draws,
        self.gui.combo_h_drawshome,
        self.gui.combo_h_loses,
        self.gui.combo_h_loseshome,
        self.gui.combo_h_nowins,
        self.gui.combo_h_nowinshome,
        self.gui.combo_h_nodraws,
        self.gui.combo_h_nodrawshome,
        self.gui.combo_h_noloses,
        self.gui.combo_h_noloseshome,
        self.gui.combo_a_wins,
        self.gui.combo_a_winsaway,
        self.gui.combo_a_draws,
        self.gui.combo_a_drawsaway,
        self.gui.combo_a_loses,
        self.gui.combo_a_losesaway,
        self.gui.combo_a_nowins,
        self.gui.combo_a_nowinsaway,
        self.gui.combo_a_nodraws,
        self.gui.combo_a_nodrawsaway,
        self.gui.combo_a_noloses,
        self.gui.combo_a_nolosesaway, #23
        self.gui.spin_h_wins,
        self.gui.spin_h_winshome,
        self.gui.spin_h_draws,
        self.gui.spin_h_drawshome,
        self.gui.spin_h_loses,
        self.gui.spin_h_loseshome,
        self.gui.spin_h_nowins,
        self.gui.spin_h_nowinshome,
        self.gui.spin_h_nodraws,
        self.gui.spin_h_nodrawshome,
        self.gui.spin_h_noloses,
        self.gui.spin_h_noloseshome,
        self.gui.spin_a_wins,
        self.gui.spin_a_winsaway,
        self.gui.spin_a_draws,
        self.gui.spin_a_drawsaway,
        self.gui.spin_a_loses,
        self.gui.spin_a_losesaway,
        self.gui.spin_a_nowins,
        self.gui.spin_a_nowinsaway,
        self.gui.spin_a_nodraws,
        self.gui.spin_a_nodrawsaway,
        self.gui.spin_a_noloses,
        self.gui.spin_a_nolosesaway,
        self.gui.spin_odd_1,
        self.gui.spin_odd_x,
        self.gui.spin_odd_2,
        self.gui.spin_odd_1x,
        self.gui.spin_odd_x2
        ]

        if file_name == None:
            item = self.gui.tree_filters_profile.currentItem()
            file_name = item.text(0)
        load = open(os.path.join('profiles','selector','')+file_name,'r')
        load = list(load)

        self.combo_h_wins = load[0]
        self.combo_h_winshome = load[1]
        self.combo_h_draws = load[2]
        self.combo_h_drawshome = load[3]
        self.combo_h_loses = load[4]
        self.combo_h_loseshome = load[5]
        self.combo_h_nowins = load[6]
        self.combo_h_nowinshome = load[7]
        self.combo_h_nodraws = load[8]
        self.combo_h_nodrawshome = load[9]
        self.combo_h_noloses = load[10]
        self.combo_h_noloseshome = load[11]
        self.combo_a_wins = load[12]
        self.combo_a_winsaway = load[13]
        self.combo_a_draws = load[14]
        self.combo_a_drawsaway = load[15]
        self.combo_a_loses = load[16]
        self.combo_a_losesaway = load[17]
        self.combo_a_nowins = load[18]
        self.combo_a_nowinsaway = load[19]
        self.combo_a_nodraws = load[20]
        self.combo_a_nodrawsaway = load[21]
        self.combo_a_noloses = load[22]
        self.combo_a_nolosesaway = load[23]
        self.spin_h_wins = load[24]
        self.spin_h_winshome = load[25]
        self.spin_h_draws = load[26]
        self.spin_h_drawshome = load[27]
        self.spin_h_loses = load[28]
        self.spin_h_loseshome = load[29]
        self.spin_h_nowins = load[30]
        self.spin_h_nowinshome = load[32]
        self.spin_h_nodraws = load[32]
        self.spin_h_nodrawshome = load[33]
        self.spin_h_noloses = load[34]
        self.spin_h_noloseshome = load[35]
        self.spin_a_wins = load[36]
        self.spin_a_winsaway = load[37]
        self.spin_a_draws = load[38]
        self.spin_a_drawsaway = load[39]
        self.spin_a_loses = load[40]
        self.spin_a_losesaway = load[41]
        self.spin_a_nowins = load[42]
        self.spin_a_nowinsaway = load[43]
        self.spin_a_nodraws = load[44]
        self.spin_a_nodrawsaway = load[45]
        self.spin_a_noloses = load[46]
        self.spin_a_nolosesaway = load[47]
        self.spin_odds_1 = load[48]
        self.spin_odds_x = load[49]
        self.spin_odds_2 = load[50]
        self.spin_odds_1x = load[51]
        self.spin_odds_x2 = load[52]
        for i in range(0,len(val)):
            if i <= 23:  #combobox
                item =self.rm_lines(load[i])
                index = val[i].findText(item)
                val[i].setCurrentIndex(index)
            if i > 23:
                item =self.rm_lines(load[i])
                item =float(item)
                val[i].setValue(item)

    def odds_rescale(self,val):
        ''' Rescaling odds from [-1,1]'''
        old_range = 2
        new_range = 19
        odd = (((val + 1) * new_range) / old_range) + 1
        odd = round(odd,2)
        if odd<1:
            odd = 1
        return odd

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
        try:
            min_date = self.relations_base.execute('''SELECT min(date_num)
                                        From Results WHERE
                                        gHomeEnd == "NULL"''')
            min_date = min_date.fetchone()
            min_date = min_date[0]
            matches = self.relations_base.execute('''SELECT home,away
                            From Results WHERE
                            gHomeEnd == "NULL" and date_num=%f'''%min_date)

            matches = matches.fetchall()

            self.item_sim = QtGui.QTreeWidgetItem(self.gui.tree_selected)
            line = league+' filter: '+file_name
            self.item_sim.setText(0,(line))
            self.gui.tree_selected.setCurrentItem(self.item_sim)

            for i in matches:
                home,away = i
                self.simulation_filters(home,away)
                self.filter_status = ''
                self.batch_filters()
                if self.filter_status == 'yes':
                    line = home+' - '+away+\
                    '  1: '+str(round(self.odd_1,2))+\
                    '  x: '+str(round(self.odd_x,2))+\
                    '  2: '+str(round(self.odd_2,2))+\
                    '  1x: '+str(round(self.odd_1x,2))+\
                    '  x2: '+str(round(self.odd_x2,2))
                    QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))

            item = self.gui.tree_selected.currentItem()
            child = item.childCount()
            if child == 0:
                index = self.gui.tree_selected.indexOfTopLevelItem(item)
                self.gui.tree_selected.takeTopLevelItem(index)
        except:
            pass

    def batch_filters(self):
        ''' Match filters check'''
        self.filter_status = 'yes' # when 'yes' then adds match to filtered
        ############
        ## Series
        ############
        T12 = [
        (str(self.t1_wins)+self.combo_h_wins+self.spin_h_wins,'T1-wins'),
        (str(self.t1_winshome)+self.combo_h_winshome+self.spin_h_winshome,
         'T1-winshome'),
        (str(self.t1_draws)+self.combo_h_draws+self.spin_h_draws,
         'T1-draws'),
        (str(self.t1_drawshome)+self.combo_h_drawshome+self.spin_h_drawshome,
         'T1-drawshome'),
        (str(self.t1_loses)+self.combo_h_loses+self.spin_h_loses,
         'T1-loses'),
        (str(self.t1_loseshome)+self.combo_h_loseshome+self.spin_h_loseshome,
         'T1-loseshome'),
        (str(self.t1_nowins)+self.combo_h_nowins+self.spin_h_nowins,
         'T1-nowins'),
        (str(self.t1_nowinshome)+self.combo_h_nowinshome+self.spin_h_nowinshome,
         'T1-nowinshome'),
        (str(self.t1_nodraws)+self.combo_h_nodraws+self.spin_h_nodraws,
         'T1-nodraws'),
        (str(self.t1_nodrawshome)+self.combo_h_nodrawshome+self.spin_h_nodrawshome,
         'T1-nodrawshome'),
        (str(self.t1_noloses)+self.combo_h_noloses+self.spin_h_noloses,
         'T1-noloses'),
        (str(self.t1_noloseshome)+self.combo_h_noloseshome+self.spin_h_noloseshome,
         'T1-nolosesHome'),
        (str(self.t2_wins)+self.combo_a_wins+self.spin_a_wins,'T2-wins'),
        (str(self.t2_winsaway)+self.combo_a_winsaway+self.spin_a_winsaway,
         'T2-winsaway'),
        (str(self.t2_draws)+self.combo_a_draws+self.spin_a_draws,
         'T2-draws'),
        (str(self.t2_drawsaway)+self.combo_a_drawsaway+self.spin_a_drawsaway,
         'T2-drawsaway'),
        (str(self.t2_loses)+self.combo_a_loses+self.spin_a_loses,
         'T2-loses'),
        (str(self.t2_losesaway)+self.combo_a_losesaway+self.spin_a_losesaway,
         'T2-losesaway'),
        (str(self.t2_nowins)+self.combo_a_nowins+self.spin_a_nowins,
         'T2-nowins'),
        (str(self.t2_nowinsaway)+self.combo_a_nowinsaway+self.spin_a_nowinsaway,
         'T2-nowinsaway'),
        (str(self.t2_nodraws)+self.combo_a_nodraws+self.spin_a_nodraws,
         'T2-nodraws'),
        (str(self.t2_nodrawsaway)+self.combo_a_nodrawsaway+self.spin_a_nodrawsaway,
         'T2-nodrawsaway'),
        (str(self.t2_noloses)+self.combo_a_noloses+self.spin_a_noloses,
         'T2-noloses'),
        (str(self.t2_nolosesaway)+self.combo_a_nolosesaway+self.spin_a_nolosesaway,
         'T2-nolosesaway')]
        # HomeAway-series
        for i in T12:
            if self.filter_status == 'yes':
                line=i[0]
                'When getting file from linux on windows'
                line = self.rm_lines(line)

                if eval(line):
                    pass
                else:
                    self.filter_status = 'no'

        ######
        # Odds
        ######
        odds = [
        (self.odd_1,self.spin_odds_1),
        (self.odd_x,self.spin_odds_x),
        (self.odd_2,self.spin_odds_2),
        (self.odd_1x,self.spin_odds_1x),
        (self.odd_x2,self.spin_odds_x2)]
        for i in odds:
            if self.filter_status == 'yes':
                if float(i[0])>=float(i[1]):
                    pass
                else:
                    self.filter_status = 'no'



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

    def rm_lines(self, item):
        ''' Removes new lines from string'''
        rem = item.replace('\n', '')
        rem = rem.replace('\r', '')
        rem = rem.replace(' ', '')
        return rem
if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = SelectorApp()
    MYAPP.show()
    sys.exit(APP.exec_())

