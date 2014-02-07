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
import os
import shutil
import platform
from csv import reader

from PySide import QtGui, QtCore

class Shared(object):
    def __init__(self):
        self.new_lines()

    def delete_file(self, file_delete, path):
        ''' Delete file dialog'''
        reply = QtGui.QMessageBox.question(self, 'Delete?',
            "Are you sure to delete %s?"%file_delete, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if file_delete != 'default':
                os.remove(path+file_delete)

    def rm_lines(self, item):
        ''' Removes new lines from string'''
        rem = item.replace('\n', '')
        rem = rem.replace('\r', '')
        rem = rem.replace(' ', '')
        return rem

    def new_lines(self):
        ''' Sets newline style for os'''
        system = platform.system()
        if system == 'Windows':
            new_line = '\r\n'
        elif system == 'Linux':
            new_line = '\n'
        else:
            new_line = '\n'
        self.nl = new_line

    def default_directories(self):
        ''' Creates or recreates default directories'''
        paths = ('export', 'tmp', 'profiles', 'leagues')
        for i in paths:
            if os.path.isdir(os.path.join(os.getcwd(),i,'')):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(),i,''))
        profiles = ('bets', 'export', 'filters', 'links',
                    'ranges', 'selector', 'simulation', 'teams','auto_save')
        for i in profiles:
            if os.path.isdir(os.path.join(os.getcwd(), 'profiles', i, '')):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(), 'profiles', i, ''))

        leagues = ('current', 'own', 'old')
        for i in leagues:
            if os.path.isdir(os.path.join(os.getcwd(), 'leagues', i, '')):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(), 'leagues', i, ''))
        tmp = ('leagues', 'simulations')
        for i in tmp:
            if os.path.isdir(os.path.join(os.getcwd(), 'tmp', i, '')):
                pass
            else:
                os.mkdir(os.path.join(os.getcwd(), 'tmp', i, ''))

    def odds_rescale(self,val,odds_level):
        ''' Rescaling odds from [-1,1]'''
        # OldRange = (OldMax - OldMin)
        # NewRange = (NewMax - NewMin)
        # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        old_range = 2
        new_range = 14
        odd = ((((val + 1) * new_range) / old_range) + 1)*odds_level/100.0
        odd = round(odd,2)
        if odd < 1:
            odd = 1
        return odd

    def find_broken_leagues(self):
        leagues = os.listdir('leagues')
        paths = []
        for i in leagues:
            paths.append(i)
            if os.path.isdir(os.path.join('tmp','leagues','')+i):
                pass
            else:
                os.mkdir(os.path.join('tmp','leagues','')+i)
        with open(os.path.join('tmp','leagues','')+'log.txt','w') as log:
            errors = 0
            for path in paths:
                files =[]
                leagues = os.listdir(os.path.join('leagues','')+path)
                for i in leagues:
                    with open(os.path.join('leagues',path,'')+i,'r') as f:
                        for a in reader(f):
                            if len(a[3])> 4 or len(a[4])> 4:
                                errors += 1
                                line = path+self.nl+i+'>>>'+str(a)+self.nl
                                QtGui.QApplication.processEvents()
                                log.write(line)
                                file_path = os.path.join(path,'')+i
                                if not file_path in files[:]:
                                    files.append(file_path)
                for i in files:
                    src = os.path.join('leagues','')+i
                    dst = os.path.join('tmp','leagues','')+i
                    shutil.copy(src, dst)
                    self.fix_broken_leagues(src)

    def fix_broken_leagues(self,path):
        ''' Removes too long lines from csv file'''
        with open(path,'r') as csv_file:
            tmp_file_open = reader(csv_file)
            tmp_file = list(tmp_file_open)
        match_list = []
        for t in xrange(0, len(tmp_file)):
            if len(tmp_file[t][3]) > 4 or len(tmp_file[t][4]) > 4:
                print tmp_file[t][3]
                print tmp_file[t][4]
            else:
                match_list.append(tmp_file[t])
        with open(path,'w') as fix_file:
            for i in xrange(0, len(match_list)):
                line = str(match_list[i])
                line = line.replace('[','')
                line = line.replace(']','')
                line = line.replace("'",'')
                line = line.replace(' ','')
                #print 'write', line
                fix_file.write(line+self.nl)

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
        # series home
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
        #bts,under,over
        combo_h_bts = self.gui.combo_h_bts.currentText()
        combo_h_btshome = self.gui.combo_h_btshome.currentText()
        combo_h_over = self.gui.combo_h_over.currentText()
        combo_h_overhome = self.gui.combo_h_overhome.currentText()
        combo_h_under = self.gui.combo_h_under.currentText()
        combo_h_underhome = self.gui.combo_h_underhome.currentText()
        # series away
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
        #bts,under,over
        combo_a_bts = self.gui.combo_a_bts.currentText()
        combo_a_btsaway = self.gui.combo_a_btsaway.currentText()
        combo_a_over = self.gui.combo_a_over.currentText()
        combo_a_overaway = self.gui.combo_a_overaway.currentText()
        combo_a_under = self.gui.combo_a_under.currentText()
        combo_a_underaway = self.gui.combo_a_underaway.currentText()
        #
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
        spin_h_bts = self.gui.spin_h_bts.value()
        spin_h_btshome = self.gui.spin_h_btshome.value()
        spin_h_over = self.gui.spin_h_over.value()
        spin_h_overhome = self.gui.spin_h_overhome.value()
        spin_h_under = self.gui.spin_h_under.value()
        spin_h_underhome = self.gui.spin_h_underhome.value()
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
        spin_a_bts = self.gui.spin_a_bts.value()
        spin_a_btsaway = self.gui.spin_a_btsaway.value()
        spin_a_over = self.gui.spin_a_over.value()
        spin_a_overaway = self.gui.spin_a_overaway.value()
        spin_a_under = self.gui.spin_a_under.value()
        spin_a_underaway = self.gui.spin_a_underaway.value()
        # odds
        spin_odd_1_min = self.gui.spin_odd_1_min.value()
        spin_odd_x_min = self.gui.spin_odd_x_min.value()
        spin_odd_2_min = self.gui.spin_odd_2_min.value()
        spin_odd_1x_min = self.gui.spin_odd_1x_min.value()
        spin_odd_x2_min = self.gui.spin_odd_x2_min.value()

        spin_odd_1_max = self.gui.spin_odd_1_max.value()
        spin_odd_x_max = self.gui.spin_odd_x_max.value()
        spin_odd_2_max = self.gui.spin_odd_2_max.value()
        spin_odd_1x_max = self.gui.spin_odd_1x_max.value()
        spin_odd_x2_max = self.gui.spin_odd_x2_max.value()

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
        combo_h_bts,
        combo_h_btshome,
        combo_h_over,
        combo_h_overhome,
        combo_h_under,
        combo_h_underhome,
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
        combo_a_bts,
        combo_a_btsaway,
        combo_a_over,
        combo_a_overaway,
        combo_a_under,
        combo_a_underaway,
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
        spin_h_bts,
        spin_h_btshome,
        spin_h_over,
        spin_h_overhome,
        spin_h_under,
        spin_h_underhome,
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
        spin_a_bts,
        spin_a_btsaway,
        spin_a_over,
        spin_a_overaway,
        spin_a_under,
        spin_a_underaway,
        spin_odd_1_min,
        spin_odd_x_min,
        spin_odd_2_min,
        spin_odd_1x_min,
        spin_odd_x2_min,
        spin_odd_1_max,
        spin_odd_x_max,
        spin_odd_2_max,
        spin_odd_1x_max,
        spin_odd_x2_max
        ]
        file_name = self.gui.line_filters.text()
        if self.app == 'simulator':
            path = os.path.join('profiles','filters','')
        elif self.app == 'selector':
            path = os.path.join('profiles','selector','')
        with open(path+file_name,'w') as save:
            for i in val:
                save.write(str(i)+self.nl)
        self.filters_tree()

    def filters_load(self,file_name=None):
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
        self.gui.combo_h_bts,
        self.gui.combo_h_btshome,
        self.gui.combo_h_over,
        self.gui.combo_h_overhome,
        self.gui.combo_h_under,
        self.gui.combo_h_underhome,
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
        self.gui.combo_a_bts,
        self.gui.combo_a_btsaway,
        self.gui.combo_a_over,
        self.gui.combo_a_overaway,
        self.gui.combo_a_under,
        self.gui.combo_a_underaway,
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
        self.gui.spin_h_bts,
        self.gui.spin_h_btshome,
        self.gui.spin_h_over,
        self.gui.spin_h_overhome,
        self.gui.spin_h_under,
        self.gui.spin_h_underhome,
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
        self.gui.spin_a_bts,
        self.gui.spin_a_btsaway,
        self.gui.spin_a_over,
        self.gui.spin_a_overaway,
        self.gui.spin_a_under,
        self.gui.spin_a_underaway,
        self.gui.spin_odd_1_min,
        self.gui.spin_odd_x_min,
        self.gui.spin_odd_2_min,
        self.gui.spin_odd_1x_min,
        self.gui.spin_odd_x2_min,
        self.gui.spin_odd_1_max,
        self.gui.spin_odd_x_max,
        self.gui.spin_odd_2_max,
        self.gui.spin_odd_1x_max,
        self.gui.spin_odd_x2_max
        ]

        if file_name == None:
            item = self.gui.tree_filters_profile.currentItem()
            file_name = str(item.text(0))
            print file_name, '<'
        if self.app == 'simulator':
            path = os.path.join('profiles','filters','')
        elif self.app == 'selector':
            path = os.path.join('profiles','selector','')
        print path,'<'
        with open(path+file_name,'r') as f:
            load = list(f)
        for i in range(0,len(val)):
            if i <=3:  #checkbutton
                state = self.rm_lines(load[i])
                if state == 'True':
                    state = 2
                else:
                    state = 0
                state =QtCore.Qt.CheckState(state)
                val[i].setCheckState(state)
            if i >3 and i <= 43:  #combobox
                item =self.rm_lines(load[i])
                index = val[i].findText(item)
                val[i].setCurrentIndex(index)
            if i > 43:
                item =self.rm_lines(load[i])
                item =float(item)
                val[i].setValue(item)

        if file_name == None:
            item = self.gui.tree_filters_profile.currentItem()
            file_name = str(item.text(0))
        with open(path+file_name,'r') as f:
            val = list(f)
        filter_vars =(
            'check_points',
            'check_points_ha',
            'check_form',
            'check_form_ha',
            'combo_points',
            'combo_points_ha',
            'combo_form',
            'combo_form_ha',
            'combo_h_wins',
            'combo_h_winshome',
            'combo_h_draws',
            'combo_h_drawshome',
            'combo_h_loses',
            'combo_h_loseshome',
            'combo_h_nowins',
            'combo_h_nowinshome',
            'combo_h_nodraws',
            'combo_h_nodrawshome',
            'combo_h_noloses',
            'combo_h_noloseshome',
            'combo_h_bts',
            'combo_h_btshome',
            'combo_h_over',
            'combo_h_overhome',
            'combo_h_under',
            'combo_h_underhome',
            'combo_a_wins',
            'combo_a_winsaway',
            'combo_a_draws',
            'combo_a_drawsaway',
            'combo_a_loses',
            'combo_a_losesaway',
            'combo_a_nowins',
            'combo_a_nowinsaway',
            'combo_a_nodraws',
            'combo_a_nodrawsaway',
            'combo_a_noloses',
            'combo_a_nolosesaway',
            'combo_a_bts',
            'combo_a_btsaway',
            'combo_a_over',
            'combo_a_overaway',
            'combo_a_under',
            'combo_a_underaway',
            'spin_points',
            'spin_points_ha',
            'spin_form',
            'spin_form_ha',
            'spin_h_wins',
            'spin_h_winshome',
            'spin_h_draws',
            'spin_h_drawshome',
            'spin_h_loses',
            'spin_h_loseshome',
            'spin_h_nowins',
            'spin_h_nowinshome',
            'spin_h_nodraws',
            'spin_h_nodrawshome',
            'spin_h_noloses',
            'spin_h_noloseshome',
            'spin_h_bts',
            'spin_h_btshome',
            'spin_h_over',
            'spin_h_overhome',
            'spin_h_under',
            'spin_h_underhome',
            'spin_a_wins',
            'spin_a_winsaway',
            'spin_a_draws',
            'spin_a_drawsaway',
            'spin_a_loses',
            'spin_a_losesaway',
            'spin_a_nowins',
            'spin_a_nowinsaway',
            'spin_a_nodraws',
            'spin_a_nodrawsaway',
            'spin_a_noloses',
            'spin_a_nolosesaway',
            'spin_a_bts',
            'spin_a_btsaway',
            'spin_a_over',
            'spin_a_overaway',
            'spin_a_under',
            'spin_a_underaway',
            'spin_odd_1_min',
            'spin_odd_x_min',
            'spin_odd_2_min',
            'spin_odd_1x_min',
            'spin_odd_x2_min',
            'spin_odd_1_max',
            'spin_odd_x_max',
            'spin_odd_2_max',
            'spin_odd_1x_max',
            'spin_odd_x2_max')
        for i in xrange(0,len(val)):
            vars(self)[filter_vars[i]] = val[i]



    def simulation_match_filters(self):
        ''' Match filters check'''
        self.filter_status = 'yes' # when 'yes' then adds match to filtered

        ############
        ## Points
        ############
        points = [
        (self.check_points,self.t1_points,self.t2_points,self.combo_points,
         self.spin_points,'T-points'),
        (self.check_points_ha,self.t1_points_h,self.t2_points_a,
         self.combo_points_ha,self.spin_points_ha,'T-pointsH/A'),
        (self.check_form,self.t1_form,self.t2_form,self.combo_form,
         self.spin_form,'T-form'),
        (self.check_form_ha,self.t1_form_h,self.t2_form_a,self.combo_form_ha,
         self.spin_form_ha,'T-formH/A')]

        for i in points:
            if i[0] == 'True':
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
                    # filter reports count
                    self.sim_stats[i[5]] = self.sim_stats[i[5]] + 1

        ############
        ## Series
        ############
        T12 = (
        (str(self.t1_wins)+self.combo_h_wins+self.spin_h_wins,'T1-wins'),
        (str(self.t1_winshome)+self.combo_h_winshome+self.spin_h_winshome,
         'T1-wins_home'),
        (str(self.t1_draws)+self.combo_h_draws+self.spin_h_draws,
         'T1-draws'),
        (str(self.t1_drawshome)+self.combo_h_drawshome+self.spin_h_drawshome,
         'T1-draws_home'),
        (str(self.t1_loses)+self.combo_h_loses+self.spin_h_loses,
         'T1-loses'),
        (str(self.t1_loseshome)+self.combo_h_loseshome+self.spin_h_loseshome,
         'T1-loses_home'),
        (str(self.t1_nowins)+self.combo_h_nowins+self.spin_h_nowins,
         'T1-nowins'),
        (str(self.t1_nowinshome)+self.combo_h_nowinshome+self.spin_h_nowinshome,
         'T1-nowins_home'),
        (str(self.t1_nodraws)+self.combo_h_nodraws+self.spin_h_nodraws,
         'T1-nodraws'),
        (str(self.t1_nodrawshome)+self.combo_h_nodrawshome+self.spin_h_nodrawshome,
         'T1-nodraws_home'),
        (str(self.t1_noloses)+self.combo_h_noloses+self.spin_h_noloses,
         'T1-noloses'),
        (str(self.t1_noloseshome)+self.combo_h_noloseshome+self.spin_h_noloseshome,
         'T1-noloses_home'),
        (str(self.t1_bts)+self.combo_h_bts+self.spin_h_bts,
         'T1-bts'),
        (str(self.t1_btshome)+self.combo_h_btshome+self.spin_h_btshome,
         'T1-bts_home'),
        (str(self.t1_over)+self.combo_h_over+self.spin_h_over,
         'T1-over'),
        (str(self.t1_overhome)+self.combo_h_overhome+self.spin_h_overhome,
         'T1-over_home'),
        (str(self.t1_under)+self.combo_h_under+self.spin_h_under,
         'T1-under'),
        (str(self.t1_underhome)+self.combo_h_underhome+self.spin_h_underhome,
         'T1-under_home'),
        (str(self.t2_wins)+self.combo_a_wins+self.spin_a_wins,'T2-wins'),
        (str(self.t2_winsaway)+self.combo_a_winsaway+self.spin_a_winsaway,
         'T2-wins_away'),
        (str(self.t2_draws)+self.combo_a_draws+self.spin_a_draws,
         'T2-draws'),
        (str(self.t2_drawsaway)+self.combo_a_drawsaway+self.spin_a_drawsaway,
         'T2-draws_away'),
        (str(self.t2_loses)+self.combo_a_loses+self.spin_a_loses,
         'T2-loses'),
        (str(self.t2_losesaway)+self.combo_a_losesaway+self.spin_a_losesaway,
         'T2-loses_away'),
        (str(self.t2_nowins)+self.combo_a_nowins+self.spin_a_nowins,
         'T2-nowins'),
        (str(self.t2_nowinsaway)+self.combo_a_nowinsaway+self.spin_a_nowinsaway,
         'T2-nowin_saway'),
        (str(self.t2_nodraws)+self.combo_a_nodraws+self.spin_a_nodraws,
         'T2-nodraws'),
        (str(self.t2_nodrawsaway)+self.combo_a_nodrawsaway+self.spin_a_nodrawsaway,
         'T2-nodraws_away'),
        (str(self.t2_noloses)+self.combo_a_noloses+self.spin_a_noloses,
         'T2-noloses'),
        (str(self.t2_nolosesaway)+self.combo_a_nolosesaway+self.spin_a_nolosesaway,
         'T2-noloses_away'),
        (str(self.t2_bts)+self.combo_a_bts+self.spin_a_bts,
         'T2-bts'),
        (str(self.t2_btsaway)+self.combo_a_btsaway+self.spin_a_btsaway,
         'T2-bts_away'),
        (str(self.t2_over)+self.combo_a_over+self.spin_a_over,
         'T2-over'),
        (str(self.t2_overaway)+self.combo_a_overaway+self.spin_a_overaway,
         'T2-over_away'),
        (str(self.t2_under)+self.combo_a_under+self.spin_a_under,
         'T2-under'),
        (str(self.t2_underaway)+self.combo_a_underaway+self.spin_a_underaway,
         'T2-under_away'))
        # HomeAway-series

        for i in T12:
            line=i[0]
            'When getting file from linux on windows'
            line = self.rm_lines(line)

            if eval(line):
                pass
            else:
                self.filter_status = 'no'
                # for fiters report
                self.sim_stats[i[1]] = self.sim_stats[i[1]] + 1

        if self.app == 'selector':
            ######
            # Odds - in match selector only !!!!
            ######
            odds = [
            (self.spin_odd_1_max,self.odd_1,self.spin_odd_1_min),
            (self.spin_odd_x_max,self.odd_x,self.spin_odd_x_min),
            (self.spin_odd_2_max,self.odd_2,self.spin_odd_2_min),
            (self.spin_odd_1x_max,self.odd_1x,self.spin_odd_1x_min),
            (self.spin_odd_x2_max,self.odd_x2,self.spin_odd_x2_min)]
            for i in odds:
                if self.filter_status == 'yes':
                    if float(i[0])>=float(i[1])>=float(i[2]):
                        pass
                    else:
                        self.filter_status = 'no'
                        #print float(i[0]),float(i[1]),float(i[2])
                        print 'sada'





