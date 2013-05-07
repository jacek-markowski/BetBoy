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
from csv import reader
import platform

from PySide import QtCore, QtGui
from ui.simulator import Ui_Simulator
from ng_engine import Database
import locale

system = platform.system()
if system == 'Windows':
    new_line = '\r\n'
elif system == 'Linux':
    new_line = '\n'
elif system == 'Darwin':
    new_line = '\r'
else:
    new_line = '\r\n'

class SimulatorApp(QtGui.QWidget, Database):
    '''Creates gui and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Database.__init__(self, parent)
        self.gui = Ui_Simulator()
        self.gui.setupUi(self)
        labels = ['Path',
                        'League',
                        'Net',
                        'Match filter',
                        'Net ranges',
                        'Bet filters',
                        'R_min',
                        'R_max']
        for i in range(0, len(labels)):
            self.gui.tree_batch.headerItem().setText(i,
                                                   (labels[i]))
        labels = ['Path',
                        'League',
                        'Net',
                        'Filter',
                        'Ranges',
                        'Bet_selector',
                        'Net frequency',
                        'R_min',
                        'R_max',
                        '1',
                        '1%',
                        '1x',
                        '1x%',
                        'x',
                        'x%',
                        'x2',
                        'x2%',
                        '2',
                        '2%',
                        '1 Profit',
                        'x Profit',
                        '2 Profit',
                        '1x Profit',
                        'x2 Profit']
        for i in range(0, len(labels)):
            self.gui.tree_hits.headerItem().setText(i,
                                                  (labels[i]))
        labels = ['Selected bets']
        for i in range(0, 1):
            self.gui.tree_bets_selected.headerItem().setText(i,
                                                   (labels[i]))

        self.bindings()
        self.leagues_tree()
        self.nets_tree()
        self.ranges_tree()
        self.bets_tree()
        self.batch_profiles_tree()
        self.filters_tree()
        self.filter_combos_spins()
        # load filters at startup
        self.bets_load()
        self.ranges_load()
        self.filters_load()

    def delete_file(self, file_delete, path):
        ''' Dialog for deleting file'''
        reply = QtGui.QMessageBox.question(self, 'Delete?',
            "Are you sure to delete %s?"%file_delete, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if file_delete != 'default':
                os.remove(path+file_delete)

    def bindings(self):
        ''' Widgets bindings'''
        self.gui.spin_1_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_1x_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_x_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_x2_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_2_max.valueChanged.connect(self.spins_manage)
        self.gui.spin_1_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_1x_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_x_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_x2_min.valueChanged.connect(self.spins_manage)
        self.gui.spin_2_min.valueChanged.connect(self.spins_manage)
        self.gui.button_ranges_save.clicked.connect(self.ranges_save)
        self.gui.button_ranges_load.clicked.connect(self.ranges_load)
        self.gui.tree_ranges_profile.doubleClicked.connect(self.ranges_load)
        self.gui.button_ranges_delete.clicked.connect(self.ranges_delete)
        self.gui.button_add.clicked.connect(self.batch_add)
        self.gui.button_batch_remove.clicked.connect(self.batch_remove)
        self.gui.button_batch_clear.clicked.connect(self.batch_clear)
        self.gui.button_batch_save.clicked.connect(self.batch_save)
        self.gui.button_batch_load.clicked.connect(self.batch_load)
        self.gui.tree_profiles.doubleClicked.connect(self.batch_load)
        self.gui.button_batch_delete.clicked.connect(self.batch_delete)
        self.gui.button_bets_load.clicked.connect(self.bets_load)
        self.gui.tree_bets_profile.clicked.connect(self.bets_load)
        self.gui.button_bets_save.clicked.connect(self.bets_save)
        self.gui.button_bets_delete.clicked.connect(self.bets_delete)
        self.gui.button_filters_save.clicked.connect(self.filters_save)
        self.gui.button_filters_load.clicked.connect(self.filters_load)
        self.gui.tree_filters_profile.doubleClicked.connect(self.filters_load)
        self.gui.button_filters_delete.clicked.connect(self.filters_delete)
        self.gui.button_batch_run.clicked.connect(self.batch_run)
        self.gui.button_preview_show.clicked.connect(self.batch_preview_run)
        self.gui.button_preview_remove.clicked.connect(self.batch_preview_remove)
        self.gui.button_preview_save.clicked.connect(self.batch_preview_save)
        self.gui.button_bets_final_save.clicked.connect(self.bets_final_save)
        self.gui.combo_points.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_points_ha.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_form.currentIndexChanged.connect(self.filter_combos_spins)
        self.gui.combo_form_ha.currentIndexChanged.connect(self.filter_combos_spins)

        self.gui.spin_points.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_points_ha.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_form.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_form_ha.valueChanged.connect(self.filter_combos_spins)
        self.gui.spin_rounds_min.valueChanged.connect(self.combos_rounds)
        self.gui.spin_rounds_max.valueChanged.connect(self.combos_rounds)

    def combos_rounds(self):
        ''' Prevents spins to have conflicting values'''
        val = [
        self.gui.spin_rounds_min,
        self.gui.spin_rounds_max,
        ]

        for i in range(1, len(val)):
            if val[i].value() <= val[i-1].value():
                number = val[i].value()
                val[i-1].setValue(number-1)
    def filter_combos_spins(self):
        ''' Changes values of combos and spins for away team'''
        combos = [
        (self.gui.combo_points,self.gui.combo_points_2),
        (self.gui.combo_points_ha,self.gui.combo_points_ha_2),
        (self.gui.combo_form,self.gui.combo_form_2),
        (self.gui.combo_form_ha,self.gui.combo_form_ha_2)]
        spins = [
        (self.gui.spin_points,self.gui.spin_points_2),
        (self.gui.spin_points_ha,self.gui.spin_points_ha_2),
        (self.gui.spin_form,self.gui.spin_form_2),
        (self.gui.spin_form_ha,self.gui.spin_form_ha_2)]

        for i in combos:
            if i[0].currentText() == '>=':
                i[1].setItemText(0,'<=')
            elif  i[0].currentText() == '<=':
                i[1].setItemText(0,'>=')

        for i in spins:
            val1 = i[0].value()
            val2 = 100 - i[0].value()
            i[0].setValue(val1)
            i[1].setValue(val2)


    def spins_manage(self):
        ''' Prevents spins to have conflicting values'''
        val = [
        self.gui.spin_1_min,
        self.gui.spin_1_max,
        self.gui.spin_1x_min,
        self.gui.spin_1x_max,
        self.gui.spin_x_min,
        self.gui.spin_x_max,
        self.gui.spin_x2_min,
        self.gui.spin_x2_max,
        self.gui.spin_2_min,
        self.gui.spin_2_max
        ]

        for i in range(1, len(val)):
            if val[i].value() <= val[i-1].value():
                number = val[i-1].value()
                val[i].setValue(number)

    def leagues_tree(self):
        ''' Fills tree with available csv files'''
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

    def nets_tree(self):
        ''' Fills tree with available csv files'''
        self.gui.tree_nets.clear()
        self.gui.tree_nets.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_nets.setSortingEnabled(1)
        self.gui.tree_nets.headerItem().setText(0, ('Nets'))
        dir_exports = os.listdir(os.path.join('net'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_nets)
            item_exp.setText(0, (i))
        self.gui.tree_nets.setCurrentItem(item_exp)
        self.gui.tree_nets.setSortingEnabled(1)

    def batch_profiles_tree(self):
        self.gui.tree_profiles.clear()
        self.gui.tree_profiles.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_profiles.setSortingEnabled(1)
        self.gui.tree_profiles.headerItem().setText(0, ('Batches'))
        dir_exports = os.listdir(os.path.join('profiles','simulation'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_profiles)
            item_exp.setText(0, (i))

    def ranges_tree(self):
        ''' Fills tree with available files'''
        self.gui.tree_ranges.clear()
        self.gui.tree_ranges.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_ranges.setSortingEnabled(1)
        self.gui.tree_ranges.headerItem().setText(0, ('Net ranges'))
        dir_exports = os.listdir(os.path.join('profiles','ranges'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_ranges)
            item_exp.setText(0, (i))
        self.gui.tree_ranges.setCurrentItem(item_exp)
        self.gui.tree_ranges.setSortingEnabled(1)
        self.gui.tree_ranges_profile.clear()
        self.gui.tree_ranges_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_ranges_profile.setSortingEnabled(1)
        self.gui.tree_ranges_profile.headerItem().setText(0, ('Net ranges'))
        dir_exports = os.listdir(os.path.join('profiles','ranges'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_ranges_profile)
            item_exp.setText(0, (i))
        self.gui.tree_ranges_profile.setCurrentItem(item_exp)

    def ranges_save(self):
        ''' Saves ranges profiles'''
        self.min_1=self.gui.spin_1_min.value()
        self.min_1x=self.gui.spin_1x_min.value()
        self.min_x=self.gui.spin_x_min.value()
        self.min_x2=self.gui.spin_x2_min.value()
        self.min_2=self.gui.spin_2_min.value()
        self.max_1=self.gui.spin_1_max.value()
        self.max_1x=self.gui.spin_1x_max.value()
        self.max_x=self.gui.spin_x_max.value()
        self.max_x2=self.gui.spin_x2_max.value()
        self.max_2=self.gui.spin_2_max.value()
        val = [
        self.min_1,
        self.max_1,
        self.min_1x,
        self.max_1x,
        self.min_x,
        self.max_x,
        self.min_x2,
        self.max_x2,
        self.min_2,
        self.max_2
        ]
        file_name = self.gui.line_ranges.text()
        save = open(os.path.join('profiles','ranges','')+file_name,'w')
        for i in val:
            save.write(str(i)+new_line)
        save.close()
        self.ranges_tree()

    def ranges_delete(self):
        ''' Delete ranges profile'''
        path = os.path.join('profiles','ranges','')
        item = self.gui.tree_ranges_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.ranges_tree()

    def ranges_load(self):
        ''' Load ranges profiles'''
        val = [
        self.gui.spin_1_min,
        self.gui.spin_1_max,
        self.gui.spin_1x_min,
        self.gui.spin_1x_max,
        self.gui.spin_x_min,
        self.gui.spin_x_max,
        self.gui.spin_x2_min,
        self.gui.spin_x2_max,
        self.gui.spin_2_min,
        self.gui.spin_2_max
        ]
        item = self.gui.tree_ranges_profile.currentItem()
        file_name = item.text(0)
        load = open(os.path.join('profiles','ranges','')+file_name,'r')
        load = list(load)
        for i in range(0,len(val)):
            item =self.rm_lines(load[i])
            val[i].setValue(float(item))

    def batch_remove(self):
        ''' Delete batch profile'''
        item = self.gui.tree_batch.currentItem()
        index = self.gui.tree_batch.indexOfTopLevelItem(item)
        self.gui.tree_batch.takeTopLevelItem(index)

    def batch_clear(self):
        ''' Clears batch tree'''
        self.gui.tree_batch.clear()

    def batch_add(self):
        ''' Add item to batch tree'''
        item = self.gui.tree_nets.currentItem()
        net = item.text(0)
        item = self.gui.tree_leagues.currentItem()
        league = item.text(0)
        path =item.parent()
        path = path.text(0)
        item = self.gui.tree_filters.currentItem()
        filters = item.text(0)
        item = self.gui.tree_ranges.currentItem()
        ranges = item.text(0)
        item = self.gui.tree_bets.currentItem()
        bets = item.text(0)
        r_min = self.gui.spin_rounds_min.value()
        r_max = self.gui.spin_rounds_max.value()
        if path != None:
            val = [path,
                    league,
                    net,
                    filters,
                    ranges,
                    bets,
                    r_min,
                    r_max]

            item = QtGui.QTreeWidgetItem(self.gui.tree_batch)
            for i in range(0,len(val)):
                item.setText(i,(str(val[i])))

    def batch_save(self):
        ''' Save items in bath tree'''
        file_name = self.gui.line_batch.text()
        file_save = open(os.path.join('profiles','simulation','')+\
                                                    str(file_name), 'w')
        count = self.gui.tree_batch.topLevelItemCount()
        for i in range(0,count):
            item = self.gui.tree_batch.topLevelItem(i)
            path = item.text(0)
            league = item.text(1)
            net = item.text(2)
            filters = item.text(3)
            ranges = item.text(4)
            bets = item.text(5)
            r_min = item.text(6)
            r_max = item.text(7)
            val = [path,
                    league,
                    net,
                    filters,
                    ranges,
                    bets,
                    r_min,
                    r_max]
            line = ''
            for i in val:
                line+=i+','
            line = line +new_line
            file_save.write(line)
        file_save.close()
        self.batch_profiles_tree()

    def batch_delete(self):
        ''' Deletes batch profile'''
        path = os.path.join('profiles','simulation','')
        item = self.gui.tree_profiles.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.batch_profiles_tree()

    def batch_load(self):
        ''' Loads batch profile'''
        self.gui.tree_batch.clear()
        item = self.gui.tree_profiles.currentItem()
        file_name = item.text(0)
        load = reader(open(os.path.join('profiles','simulation','')+\
                                                            file_name,'r'))
        for i in load:
            item = QtGui.QTreeWidgetItem(self.gui.tree_batch)
            for n in range(0,8):
                item.setText(n,(i[n]))

    def bets_tree(self):
        ''' Filss tree in both tabs with saved bets filters'''
        self.gui.tree_bets.clear()
        self.gui.tree_bets.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_bets.setSortingEnabled(1)
        self.gui.tree_bets.headerItem().setText(0, ('Bet filters'))
        dir_exports = os.listdir(os.path.join('profiles','bets'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_bets)
            item_exp.setText(0, (i))
        self.gui.tree_bets.setCurrentItem(item_exp)
        self.gui.tree_bets.setSortingEnabled(1)
        self.gui.tree_bets_profile.clear()
        self.gui.tree_bets_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_bets_profile.setSortingEnabled(1)
        self.gui.tree_bets_profile.headerItem().setText(0, ('Bet filters'))
        dir_exports = os.listdir(os.path.join('profiles','bets'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_bets_profile)
            item_exp.setText(0, (i))
        self.gui.tree_bets_profile.setCurrentItem(item_exp)

    def bets_load(self):
        ''' Load bets profiles'''
        val = [
        self.gui.spin_acc_1,
        self.gui.spin_acc_x,
        self.gui.spin_acc_2,
        self.gui.spin_acc_1x,
        self.gui.spin_acc_x2,
        self.gui.spin_freq,
        self.gui.spin_bet_odd_1,
        self.gui.spin_bet_odd_x,
        self.gui.spin_bet_odd_2,
        self.gui.spin_bet_odd_1x,
        self.gui.spin_bet_odd_x2
        ]
        item = self.gui.tree_bets_profile.currentItem()
        file_name = item.text(0)
        load = open(os.path.join('profiles','bets','')+file_name,'r')
        load = list(load)
        for i in range(0,len(val)):
            item =self.rm_lines(load[i])
            val[i].setValue(float(item))


    def bets_delete(self):
        ''' Deletes bets profile'''
        path = os.path.join('profiles','bets','')
        item = self.gui.tree_bets_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.bets_tree()

    def bets_final_save(self):
        ''' Save selected bets'''
        file_name = QtGui.QFileDialog.getSaveFileName(self)
        file_save = open(file_name[0],'w')
        count = self.gui.tree_bets_selected.topLevelItemCount()
        for i in range(0,count):
            item = self.gui.tree_bets_selected.topLevelItem(i)
            simulation = item.text(0)
            line = simulation+new_line
            file_save.write(line)
            child_num = item.childCount()
            for i in range(0,child_num):
                name = item.child(i)
                name = name.text(0)
                line = name+new_line
                file_save.write('.........'+line)
        file_save.close()

    def bets_save(self):
        ''' Saves bets profiles'''
        acc_1=self.gui.spin_acc_1.value()
        acc_x=self.gui.spin_acc_x.value()
        acc_2=self.gui.spin_acc_2.value()
        acc_1x=self.gui.spin_acc_1x.value()
        acc_x2=self.gui.spin_acc_x2.value()
        freq=self.gui.spin_freq.value()
        odd_1=self.gui.spin_bet_odd_1.value()
        odd_x=self.gui.spin_bet_odd_x.value()
        odd_2=self.gui.spin_bet_odd_2.value()
        odd_1x=self.gui.spin_bet_odd_1x.value()
        odd_x2=self.gui.spin_bet_odd_x2.value()

        val = [
        acc_1,
        acc_x,
        acc_2,
        acc_1x,
        acc_x2,
        freq,
        odd_1,
        odd_x,
        odd_2,
        odd_1x,
        odd_x2
        ]
        file_name = self.gui.line_bets_save.text()
        save = open(os.path.join('profiles','bets','')+file_name,'w')
        for i in val:
            save.write(str(i)+new_line)
        save.close()
        self.bets_tree()

    def batch_preview_remove(self):
        ''' Remove item from filtered accuracy stats'''
        item = self.gui.tree_hits.currentItem()
        index = self.gui.tree_hits.indexOfTopLevelItem(item)
        self.gui.tree_hits.takeTopLevelItem(index)

    def batch_preview_save(self):
        ''' Saves batch profile'''
        file_name = self.gui.line_preview_save.text()
        file_save = open(os.path.join('profiles','simulation','')+\
                                                    str(file_name), 'w')
        count = self.gui.tree_hits.topLevelItemCount()
        for i in range(0,count):
            item = self.gui.tree_hits.topLevelItem(i)
            path = item.text(0)
            league = item.text(1)
            net = item.text(2)
            filters = item.text(3)
            ranges = item.text(4)
            bets = item.text(5)

            val = [path,
                    league,
                    net,
                    filters,
                    ranges,
                    bets]
            line = ''
            for i in val:
                line+=i+','
            line = line +new_line
            file_save.write(line)
        file_save.close()
        self.batch_profiles_tree()

    def batch_preview_run(self):
        ''' Run selected simulation without clearing tree and bets'''
        item = self.gui.tree_hits.currentItem()
        sim = item
        self.sim_stats = {
        'Path':'-',
        'League':'-',
        'Net':'-',
        'Filter':'-',
        'Ranges':'-',
        'Bet_selector':'-',
        'R_min':'-',
        'R_max':'-',
        'matches':0.0,
        'bets':0.0,
        '1':0.0,
        '1 hit':0.0,
        '1x':0.0,
        '1x hit':0.0,
        'x':0.0,
        'x hit':0.0,
        'x2':0.0,
        'x2 hit':0.0,
        '2':0.0,
        '2 hit':0.0,
        '1LSP':0.0,
        'xLSP':0.0,
        '2LSP':0.0,
        '1xLSP':0.0,
        'x2LSP':0.0,}
        self.sim_stats['Path']= str(sim.text(0))
        self.sim_stats['League']= str(sim.text(1))
        self.sim_stats['Net']= str(sim.text(2))
        self.sim_stats['Filter']= str(sim.text(3))
        self.sim_stats['Ranges']= str(sim.text(4))
        self.sim_stats['Bet_selector']= str(sim.text(5))
        self.sim_stats['R_min']= str(sim.text(7))
        self.sim_stats['R_max']= str(sim.text(8))

        self.gui.table_preview.clear()
        labels = ['Date','Home','Away','Result','Bet','Odd','Net']
        self.gui.table_preview.setColumnCount(len(labels))
        self.gui.table_preview.setHorizontalHeaderLabels(labels)
        self.gui.table_preview.setRowCount(0)
        self.gui.table_filtered.setColumnCount(len(labels))
        self.gui.table_filtered.setHorizontalHeaderLabels(labels)
        self.gui.table_filtered.setRowCount(0)
        self.gui.tabWidget.setCurrentIndex(1)
        # ranges
        ranges = open(os.path.join('profiles','ranges','')+\
                                        self.sim_stats['Ranges'],'r')
        load = list(ranges)
        ranges.close()
        val = []
        for i in range(0,len(load)):
            item = self.rm_lines(load[i])
            item = float(item)
            val.append(item)
        self.min_1 = val[0]
        self.max_1 = val[1]
        self.min_1x = val[2]
        self.max_1x = val[3]
        self.min_x = val[4]
        self.max_x = val[5]
        self.min_x2 = val[6]
        self.max_x2 = val[7]
        self.min_2 = val[8]
        self.max_2 = val[9]
        # filters
        filters = open(os.path.join('profiles','filters','')+\
                                        self.sim_stats['Filter'],'r')
        load = list(filters)
        val = []
        for i in range(0,len(load)):
            item = self.rm_lines(load[i])
            val.append(item)

        self.check_points = val[0]
        self.check_points_ha = val[1]
        self.check_form = val[2]
        self.check_form_ha = val[3]
        self.combo_points = val[4]
        self.combo_points_ha = val[5]
        self.combo_form = val[6]
        self.combo_form_ha = val[7]
        self.combo_h_wins = val[8]
        self.combo_h_winshome = val[9]
        self.combo_h_draws = val[10]
        self.combo_h_drawshome = val[11]
        self.combo_h_loses = val[12]
        self.combo_h_loseshome = val[13]
        self.combo_h_nowins = val[14]
        self.combo_h_nowinshome = val[15]
        self.combo_h_nodraws = val[16]
        self.combo_h_nodrawshome = val[17]
        self.combo_h_noloses = val[18]
        self.combo_h_noloseshome = val[19]
        self.combo_a_wins = val[20]
        self.combo_a_winsaway = val[21]
        self.combo_a_draws = val[22]
        self.combo_a_drawsaway = val[23]
        self.combo_a_loses = val[24]
        self.combo_a_losesaway = val[25]
        self.combo_a_nowins = val[26]
        self.combo_a_nowinsaway = val[27]
        self.combo_a_nodraws = val[28]
        self.combo_a_nodrawsaway = val[29]
        self.combo_a_noloses = val[30]
        self.combo_a_nolosesaway = val[31]
        self.spin_points = val[32]
        self.spin_points_ha = val[33]
        self.spin_form = val[34]
        self.spin_form_ha = val[35]
        self.spin_h_wins = val[36]
        self.spin_h_winshome = val[37]
        self.spin_h_draws = val[38]
        self.spin_h_drawshome = val[39]
        self.spin_h_loses = val[40]
        self.spin_h_loseshome = val[41]
        self.spin_h_nowins = val[42]
        self.spin_h_nowinshome = val[43]
        self.spin_h_nodraws = val[44]
        self.spin_h_nodrawshome = val[45]
        self.spin_h_noloses = val[46]
        self.spin_h_noloseshome = val[47]
        self.spin_a_wins = val[48]
        self.spin_a_winsaway = val[49]
        self.spin_a_draws = val[50]
        self.spin_a_drawsaway = val[51]
        self.spin_a_loses = val[52]
        self.spin_a_losesaway = val[53]
        self.spin_a_nowins = val[54]
        self.spin_a_nowinsaway = val[55]
        self.spin_a_nodraws = val[56]
        self.spin_a_nodrawsaway = val[57]
        self.spin_a_noloses = val[58]
        self.spin_a_nolosesaway = val[59]
        self.spin_odds_1 = val[60]
        self.spin_odds_x = val[61]
        self.spin_odds_2 = val[62]
        self.spin_odds_1x = val[63]
        self.spin_odds_x2 = val[64]

        locale.setlocale(locale.LC_ALL, "C")
        self.load_csv(os.path.join('leagues',
                    self.sim_stats['Path'].lower(),''),
                    self.sim_stats['League'],
                    r_min = int(self.sim_stats['R_min']),
                    r_max = int(self.sim_stats['R_max']),
                    mode=2,
                    net=self.sim_stats['Net'])

    def batch_run(self):
        ''' Runs all selected simulations'''
        self.gui.tree_hits.clear()
        self.gui.tree_bets_selected.clear()
        count = self.gui.tree_batch.topLevelItemCount()
        self.gui.tabWidget.setCurrentIndex(1)
        self.start = 0

        for i in range(0,count):
            self.start = 1
            sim = self.gui.tree_batch.topLevelItem(i)
            self.sim_stats = {
            'Path':'-',
            'League':'-',
            'Net':'-',
            'Filter':'-',
            'Ranges':'-',
            'Bet_selector':'-',
            'R_min':'-',
            'R_max':'-',
            'matches':0.0,
            'bets':0.0,
            '1':0.0,
            '1 hit':0.0,
            '1x':0.0,
            '1x hit':0.0,
            'x':0.0,
            'x hit':0.0,
            'x2':0.0,
            'x2 hit':0.0,
            '2':0.0,
            '2 hit':0.0,
            '1LSP':0.0,
            'xLSP':0.0,
            '2LSP':0.0,
            '1xLSP':0.0,
            'x2LSP':0.0}
            self.sim_stats['Path']= str(sim.text(0))
            self.sim_stats['League']= str(sim.text(1))
            self.sim_stats['Net']= str(sim.text(2))
            self.sim_stats['Filter']= str(sim.text(3))
            self.sim_stats['Ranges']= str(sim.text(4))
            self.sim_stats['Bet_selector']= str(sim.text(5))
            self.sim_stats['R_min']= str(sim.text(6))
            self.sim_stats['R_max']= str(sim.text(7))
            rounds_min = int(sim.text(6))
            rounds_max = int(sim.text(7))
            self.gui.table_preview.clear()
            labels = ['Date','Home','Away','Result','Bet','Odd','Net']
            self.gui.table_preview.setColumnCount(len(labels[:-2]))
            self.gui.table_preview.setHorizontalHeaderLabels(labels)
            self.gui.table_preview.setRowCount(0)
            self.gui.table_filtered.setColumnCount(len(labels))
            self.gui.table_filtered.setHorizontalHeaderLabels(labels)
            self.gui.table_filtered.setRowCount(0)
             # size of columns
            self.gui.table_filtered.setColumnWidth(0, 90)
            self.gui.table_filtered.setColumnWidth(1, 90)
            self.gui.table_filtered.setColumnWidth(2, 90)
            self.gui.table_filtered.setColumnWidth(3, 60)
            self.gui.table_filtered.setColumnWidth(4, 60)
            self.gui.table_filtered.setColumnWidth(5, 60)
            self.gui.table_filtered.setColumnWidth(6, 100)

            self.gui.table_preview.setColumnWidth(0, 100)
            self.gui.table_preview.setColumnWidth(1, 100)
            self.gui.table_preview.setColumnWidth(2, 100)
            self.gui.table_preview.setColumnWidth(3, 50)
            self.gui.table_preview.setColumnWidth(4, 80)
            # ranges
            ranges = open(os.path.join('profiles','ranges','')+\
                                            self.sim_stats['Ranges'],'r')
            load = list(ranges)
            ranges.close()
            val = []
            for i in range(0,len(load)):
                item = self.rm_lines(load[i])
                item = float(item)
                val.append(item)
            self.min_1 = val[0]
            self.max_1 = val[1]
            self.min_1x = val[2]
            self.max_1x = val[3]
            self.min_x = val[4]
            self.max_x = val[5]
            self.min_x2 = val[6]
            self.max_x2 = val[7]
            self.min_2 = val[8]
            self.max_2 = val[9]
            # filters
            filters = open(os.path.join('profiles','filters','')+\
                                            self.sim_stats['Filter'],'r')
            load = list(filters)
            val = []
            for i in range(0,len(load)):
                item = self.rm_lines(load[i])
                val.append(item)

            self.check_points = val[0]
            self.check_points_ha = val[1]
            self.check_form = val[2]
            self.check_form_ha = val[3]
            self.combo_points = val[4]
            self.combo_points_ha = val[5]
            self.combo_form = val[6]
            self.combo_form_ha = val[7]
            self.combo_h_wins = val[8]
            self.combo_h_winshome = val[9]
            self.combo_h_draws = val[10]
            self.combo_h_drawshome = val[11]
            self.combo_h_loses = val[12]
            self.combo_h_loseshome = val[13]
            self.combo_h_nowins = val[14]
            self.combo_h_nowinshome = val[15]
            self.combo_h_nodraws = val[16]
            self.combo_h_nodrawshome = val[17]
            self.combo_h_noloses = val[18]
            self.combo_h_noloseshome = val[19]
            self.combo_a_wins = val[20]
            self.combo_a_winsaway = val[21]
            self.combo_a_draws = val[22]
            self.combo_a_drawsaway = val[23]
            self.combo_a_loses = val[24]
            self.combo_a_losesaway = val[25]
            self.combo_a_nowins = val[26]
            self.combo_a_nowinsaway = val[27]
            self.combo_a_nodraws = val[28]
            self.combo_a_nodrawsaway = val[29]
            self.combo_a_noloses = val[30]
            self.combo_a_nolosesaway = val[31]
            self.spin_points = val[32]
            self.spin_points_ha = val[33]
            self.spin_form = val[34]
            self.spin_form_ha = val[35]
            self.spin_h_wins = val[36]
            self.spin_h_winshome = val[37]
            self.spin_h_draws = val[38]
            self.spin_h_drawshome = val[39]
            self.spin_h_loses = val[40]
            self.spin_h_loseshome = val[41]
            self.spin_h_nowins = val[42]
            self.spin_h_nowinshome = val[43]
            self.spin_h_nodraws = val[44]
            self.spin_h_nodrawshome = val[45]
            self.spin_h_noloses = val[46]
            self.spin_h_noloseshome = val[47]
            self.spin_a_wins = val[48]
            self.spin_a_winsaway = val[49]
            self.spin_a_draws = val[50]
            self.spin_a_drawsaway = val[51]
            self.spin_a_loses = val[52]
            self.spin_a_losesaway = val[53]
            self.spin_a_nowins = val[54]
            self.spin_a_nowinsaway = val[55]
            self.spin_a_nodraws = val[56]
            self.spin_a_nodrawsaway = val[57]
            self.spin_a_noloses = val[58]
            self.spin_a_nolosesaway = val[59]
            self.spin_odds_1 = val[60]
            self.spin_odds_x = val[61]
            self.spin_odds_2 = val[62]
            self.spin_odds_1x = val[63]
            self.spin_odds_x2 = val[64]

            locale.setlocale(locale.LC_ALL, "C")
            self.load_csv(os.path.join('leagues',
                        self.sim_stats['Path'],''),
                        self.sim_stats['League'],
                        r_min=rounds_min,
                        r_max=rounds_max,
                        mode=2,
                        net=self.sim_stats['Net'])
            self.batch_stats()
        if self.start == 1:
            self.gui.tabWidget.setCurrentIndex(2)  #change tab

    def batch_stats(self):
        ''' Adds simulation stats to tree preview'''
        item = QtGui.QTreeWidgetItem(self.gui.tree_hits)
        item.setText(0,(self.sim_stats['Path']))
        item.setText(1,(self.sim_stats['League']))
        item.setText(2,(self.sim_stats['Net']))
        item.setText(3,(self.sim_stats['Filter']))
        item.setText(4,(self.sim_stats['Ranges']))
        item.setText(5,(self.sim_stats['Bet_selector']))
        item.setText(7,(self.sim_stats['R_min']))
        item.setText(8,(self.sim_stats['R_max']))
        ### net frequency
        matches = self.gui.table_filtered.rowCount()
        try:
            self.c_freq = self.sim_stats['bets']/matches*100
        except:
            self.c_freq = 0
        item.setText(6,(str(self.c_freq)))
        ### bets
        val = ['1','1x','x','x2','2']
        index = 9
        for i in range(0,len(val)):
            a = int(self.sim_stats[val[i]])
            b = int(self.sim_stats[val[i]+' hit'])
            count = str(b)+'/'+str(a)
            try:
                percent = self.sim_stats[val[i]+' hit']/self.sim_stats[val[i]]*100
            except:
                percent = 0
            item.setText(index,(count))
            item.setText(index+1,(str(round(percent,2))))
            index+=2
        try:
            self.batch_bets()
        except:
            'no bets'
        ### profit/loss
        val = ['1LSP','xLSP','2LSP','1xLSP','x2LSP']
        index = 19
        for i in val:
            profit = str(round(self.sim_stats[i],2))
            item.setText(index,profit)
            index+=1


    def batch_bets(self):
        ''' Gives bets'''
         # bets filter
        bets = open(os.path.join('profiles','bets','')+\
                    self.sim_stats['Bet_selector'],'r')
        load = list(bets)
        bets.close()
        val = []
        for i in range(0,len(load)):
            item = self.rm_lines(load[i])
            item = float(item)
            val.append(item)
        self.acc_1 = val[0]
        self.acc_x = val[1]
        self.acc_2 = val[2]
        self.acc_1x = val[3]
        self.acc_x2 = val[4]
        self.freq = val[5]
        self.spin_odds_1=val[6]
        self.spin_odds_x=val[7]
        self.spin_odds_2=val[8]
        self.spin_odds_1x=val[9]
        self.spin_odds_x2=val[10]

        min_date = self.relations_base.execute('''SELECT min(date_num)
                                    From Results WHERE
                                    gHomeEnd == "NULL"''')
        min_date = min_date.fetchone()
        min_date = min_date[0]
        matches = self.relations_base.execute('''SELECT home,away
                        From Results WHERE
                        gHomeEnd == "NULL" and date_num=%f'''%min_date)

        matches = matches.fetchall()

        self.item_sim = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
        line = str(
        self.sim_stats['Path']+','+\
        self.sim_stats['League']+','+\
        self.sim_stats['Net']+','+\
        self.sim_stats['Filter']+','+\
        self.sim_stats['Ranges']+','+\
        self.sim_stats['Bet_selector']+','+\
        self.sim_stats['R_min']+','+\
        self.sim_stats['R_max'])
        self.item_sim.setText(0,(line))


        for i in matches:
            home,away = i
            self.simulation_prediction(home,away,self.sim_stats['Net'])
            self.filter_status = ''
            self.batch_filters()
            self.ranges_color()
            if self.c_freq>=self.freq and self.filter_status == 'yes':
                self.odds = self.simulation_prediction(home,away,'default',1)
                self.odd_1 = self.odds_rescale(self.odds[0])
                self.odd_x = self.odds_rescale(self.odds[1])
                self.odd_2 = self.odds_rescale(self.odds[2])
                self.odd_1x = 1/((1/self.odd_1) + (1/self.odd_x))
                self.odd_x2 = 1/((1/self.odd_x) + (1/self.odd_2))
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.select_bet(home,away)

    def select_bet(self,home,away):
        ''' Bet filters for selecting bets'''
        try:
            c_acc_1 = self.sim_stats['1 hit']/self.sim_stats['1']*100
        except:
            c_acc_1 = 0
        try:
            c_acc_x = self.sim_stats['x hit']/self.sim_stats['x']*100
        except:
            c_acc_x = 0
        try:
            c_acc_2 = self.sim_stats['2 hit']/self.sim_stats['2']*100
        except:
            c_acc_2 = 0
        try:
            c_acc_1x = self.sim_stats['1x hit']/self.sim_stats['1x']*100
        except:
            c_acc_1x = 0
        try:
            c_acc_x2 = self.sim_stats['x2 hit']/self.sim_stats['x2']*100
        except:
            c_acc_x2 = 0
        ###########
        if self.bet == '1' and c_acc_1>=self.acc_1:
            line = home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_1,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == 'x' and c_acc_x>=self.acc_x:
            line = home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_x,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == '2' and c_acc_2>=self.acc_2:
            line = home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_2,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == '1x' and c_acc_1x>=self.acc_1x:
            line = home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_1x,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))
        if self.bet == 'x2' and c_acc_x2>=self.acc_x2:
            line = home+' - '+away+' :'+self.bet+'  odd: '+\
                                                        str(round(self.odd_x2,2))
            #item = QtGui.QTreeWidgetItem(self.gui.tree_bets_selected)
            QtGui.QTreeWidgetItem(self.item_sim).setText(0, (line))

    def batch_print(self):
        ''' Adds matches to all matches and filtered matches'''

        rows_all = self.gui.table_preview.rowCount()
        rows_filtered = self.gui.table_filtered.rowCount()
        self.filter_status = ''
        self.count_stats = 0
        self.batch_filters()
        if self.filter_status == 'yes':
            self.count_stats = 1
            self.ranges_color()
            self.count_stats = 0
        else:
            self.count_stats = 0
            self.ranges_color()

        tab_all =[self.date,self.home,self.away,str(self.fth)+':'+\
            str(self.fta),self.bet]
        tab_filtered =['self.date','self.home','self.away',"str(self.fth)+':'+\
            str(self.fta)",'self.bet','odd_filter[1]','self.prediction']
        # all matches
        for i in range(0,len(tab_all)):
            self.gui.table_preview.setRowCount(rows_all+1)
            item = QtGui.QTableWidgetItem(str(tab_all[i]))
            self.gui.table_preview.setItem(rows_all, i, item)
            self.gui.table_preview.setItem(rows_all, 4,
                                           QtGui.QTableWidgetItem(self.bet))
            self.gui.table_preview.item(rows_all, i).\
                setBackground(self.prediction_color)
        # filtered list table
        for i in range(0,len(tab_filtered)):
            if self.filter_status == 'yes':
                ####
                # Odds filter
                ####
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    item = QtGui.QTableWidgetItem(str(eval(tab_filtered[i])))
                    self.gui.table_filtered.setRowCount(rows_filtered+1)
                    self.gui.table_filtered.setItem(rows_filtered, i, item)
                    self.gui.table_filtered.item(rows_filtered, i).\
                        setBackground(self.prediction_color)
        self.gui.table_preview.setCurrentCell(rows_all,0)
        self.gui.table_filtered.setCurrentCell(rows_filtered,0)
        QtGui.QApplication.processEvents()
    def odds_filter(self,bet):
        ''' Filters matches by min odds'''
        if bet == '1' and self.odd_1>=float(self.spin_odds_1):
            status = ('yes',self.odd_1)
        elif bet == 'x' and self.odd_x>=float(self.spin_odds_x):
            status = ('yes',self.odd_x)
        elif bet == '2' and self.odd_2>=float(self.spin_odds_2):
            status = ('yes',self.odd_2)
        elif bet == '1x' and self.odd_1x>=float(self.spin_odds_1x):
            status = ('yes',self.odd_1x)
        elif bet == 'x2' and self.odd_x2>=float(self.spin_odds_x2):
            status = ('yes',self.odd_x2)
        else:
            status = 'no'
        return status

    def batch_filters(self):
        ''' Match filters check'''
        self.filter_status = 'yes' # when 'yes' then adds match to filtered
        ############
        ## Points
        ############
        points = [
        (self.check_points,self.t1_points,self.t2_points,self.combo_points,
         self.spin_points,'points'),
        (self.check_points_ha,self.t1_points_h,self.t2_points_a,
         self.combo_points_ha,self.spin_points_ha,'pointsH/A'),
        (self.check_form,self.t1_form,self.t2_form,self.combo_form,
         self.spin_form,'form'),
        (self.check_form_ha,self.t1_form_h,self.t2_form_a,self.combo_form_ha,
         self.spin_form_ha,'formH/A')]

        for i in points:
            if i[0] == 'True' and self.filter_status == 'yes':
                sum_points= i[1]+i[2]
                if sum_points == 0:
                    diff = 0
                else:
                    diff = i[1]/(float(sum_points))*100
                line = str(diff)+i[3]+i[4]
                if eval(line):
                    pass
                else:
                    self.filter_status = 'no'

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
    def odds_rescale(self,val):
        ''' Rescaling odds from [-1,1]'''
        old_range = 2
        new_range = 19
        odd = (((val + 1) * new_range) / old_range) + 1
        odd = round(odd,2)
        if odd<1:
            odd = 1
        return odd
    def simulation_profit(self,bet):
        '''Counts profit'''
        odds = self.simulation_prediction(self.home,self.away,'default',mode=1)
        odd_1 = self.odds_rescale(odds[0])*0.9
        odd_x = self.odds_rescale(odds[1])*0.9
        odd_2 = self.odds_rescale(odds[2])*0.9
        odd_1x = 1/((1/odd_1) + (1/odd_x))
        odd_x2 = 1/((1/odd_x) + (1/odd_2))
        if odd_1x<1:
            odd_1x=1
        if odd_x2<1:
            odd_x2=1
        if bet == '1':
            profit = 100*odd_1-100
            self.sim_stats['1LSP'] = self.sim_stats['1LSP'] + profit
        if bet == 'x':
            profit = 100*odd_x-100
            self.sim_stats['xLSP'] = self.sim_stats['xLSP'] + profit
        if bet == '2':
            profit = 100*odd_2-100
            self.sim_stats['2LSP'] = self.sim_stats['2LSP'] + profit
        if bet == '1x':
            profit = 100*odd_1x-100
            self.sim_stats['1xLSP'] = self.sim_stats['1xLSP'] + profit
        if bet == 'x2':
            print 'odd_x2',odd_x2
            profit = 100*odd_x2-100
            self.sim_stats['x2LSP'] = self.sim_stats['x2LSP'] + profit

    def ranges_color(self):
        ''' Gives colours to matches when hit , miss or no bet'''
        green = QtGui.QColor('#11BD00')
        red = QtGui.QColor('#C40202')
        grey = QtGui.QColor('#7C7C7C')
        if self.fth == self.fta:
            result = 'draw'
        elif self.fth > self.fta:
            result = 'home'
        elif self.fth < self.fta:
            result = 'away'

        if self.min_1<=self.prediction and self.prediction<self.max_1:
            self.bet = '1'
            if self.count_stats == 1:
                 odd_filter =self.odds_filter(self.bet)
                 if odd_filter[0] == 'yes':
                    self.sim_stats['1']+=1
                    self.sim_stats['bets']+=1
            if result == 'home':
                self.prediction_color = green
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['1 hit']+=1
                        self.simulation_profit(self.bet)
            else:
                self.prediction_color = red
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['1LSP'] = self.sim_stats['1LSP'] - 100
        elif self.min_1x<=self.prediction and self.prediction<self.max_1x:
            self.bet = '1x'
            if self.count_stats == 1:
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['1x']+=1
                    self.sim_stats['bets']+=1
            if result == 'home' or result == 'draw':
                self.prediction_color = green
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['1x hit']+=1
                        self.simulation_profit(self.bet)
            else:
                self.prediction_color = red
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['1xLSP'] = self.sim_stats['1xLSP'] - 100
        elif self.min_x<=self.prediction and self.prediction<self.max_x:
            self.bet = 'x'
            if self.count_stats == 1:
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['x']+=1
                    self.sim_stats['bets']+=1
            if result == 'draw':
                self.prediction_color = green
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['x hit']+=1
                        self.simulation_profit(self.bet)
            else:
                self.prediction_color = red
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['xLSP'] = self.sim_stats['xLSP'] - 100
        elif self.min_x2<=self.prediction and self.prediction<self.max_x2:
            self.bet = 'x2'
            if self.count_stats == 1:
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['x2']+=1
                    self.sim_stats['bets']+=1
            if result == 'draw' or result == 'away':
                self.prediction_color = green
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['x2 hit']+=1
                        self.simulation_profit(self.bet)
            else:
                self.prediction_color = red
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['x2LSP'] = self.sim_stats['x2LSP'] -100

        elif self.min_2<=self.prediction and self.prediction<self.max_2:
            self.bet = '2'
            if self.count_stats == 1:
                odd_filter =self.odds_filter(self.bet)
                if odd_filter[0] == 'yes':
                    self.sim_stats['2']+=1
                    self.sim_stats['bets']+=1
            if result == 'away':
                self.prediction_color = green
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['2 hit']+=1
                        self.simulation_profit(self.bet)
            else:
                self.prediction_color = red
                if self.count_stats == 1:
                    odd_filter =self.odds_filter(self.bet)
                    if odd_filter[0] == 'yes':
                        self.sim_stats['2LSP'] = self.sim_stats['2LSP'] - 100
        else:
            self.prediction_color = grey
            self.bet = 'None'

    def filters_tree(self):
        ''' Tree with saved match filters'''
        self.gui.tree_filters.clear()
        self.gui.tree_filters.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters.setSortingEnabled(1)
        self.gui.tree_filters.headerItem().setText(0, ('Match filters'))
        dir_exports = os.listdir(os.path.join('profiles','filters'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters)
            item_exp.setText(0, (i))
        self.gui.tree_filters.setCurrentItem(item_exp)
        self.gui.tree_filters.setSortingEnabled(1)
        self.gui.tree_filters_profile.clear()
        self.gui.tree_filters_profile.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_filters_profile.setSortingEnabled(1)
        self.gui.tree_filters_profile.headerItem().setText(0, ('Match filters'))
        dir_exports = os.listdir(os.path.join('profiles','filters'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_filters_profile)
            item_exp.setText(0, (i))
        self.gui.tree_filters_profile.setCurrentItem(item_exp)

    def filters_save(self):
        ''' Save match filter'''
        # stats diffrences
        check_points = self.gui.check_points.isChecked()
        check_points_ha = self.gui.check_points_ha.isChecked()
        check_form = self.gui.check_form.isChecked()
        check_form_ha = self.gui.check_form_ha.isChecked()
        combo_points = self.gui.combo_points.currentText()
        combo_points_ha = self.gui.combo_points_ha.currentText()
        combo_form = self.gui.combo_form.currentText()
        combo_form_ha = self.gui.combo_form_ha.currentText()
        spin_points = self.gui.spin_points.value()
        spin_points_ha = self.gui.spin_points_ha.value()
        spin_form = self.gui.spin_form.value()
        spin_form_ha = self.gui.spin_form_ha.value()
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
        check_points,
        check_points_ha,
        check_form,
        check_form_ha,
        combo_points,
        combo_points_ha,
        combo_form,
        combo_form_ha,
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
        spin_points,
        spin_points_ha,
        spin_form,
        spin_form_ha,
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
        save = open(os.path.join('profiles','filters','')+file_name,'w')
        for i in val:
            save.write(str(i)+new_line)
        save.close()
        self.filters_tree()

    def filters_load(self):
        ''' Load match filter'''
        val =[
        self.gui.check_points,
        self.gui.check_points_ha,
        self.gui.check_form,
        self.gui.check_form_ha,
        self.gui.combo_points,
        self.gui.combo_points_ha,
        self.gui.combo_form,
        self.gui.combo_form_ha,
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
        self.gui.combo_a_nolosesaway,
        self.gui.spin_points,
        self.gui.spin_points_ha,
        self.gui.spin_form,
        self.gui.spin_form_ha,
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
        item = self.gui.tree_filters_profile.currentItem()
        file_name = item.text(0)
        load = open(os.path.join('profiles','filters','')+file_name,'r')
        load = list(load)
        for i in range(0,len(val)):
            if i <=3:  #checkbutton
                state = self.rm_lines(load[i])
                if state == 'True':
                    state = 2
                else:
                    state = 0
                state =QtCore.Qt.CheckState(state)
                val[i].setCheckState(state)
            if i >3 and i <= 31:  #combobox
                item =self.rm_lines(load[i])
                index = val[i].findText(item)
                val[i].setCurrentIndex(index)
            if i > 31:
                item =self.rm_lines(load[i])
                item =float(item)
                val[i].setValue(item)

    def filters_delete(self):
        ''' Deletes match filter'''
        path = os.path.join('profiles','filters','')
        item = self.gui.tree_filters_profile.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete,path)
        self.filters_tree()

    def rm_lines(self, item):
        ''' Removes new lines from string'''
        rem = item.replace('\n', '')
        rem = rem.replace('\r', '')
        rem = rem.replace(' ', '')
        return rem



if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = SimulatorApp()
    MYAPP.show()
    sys.exit(APP.exec_())
