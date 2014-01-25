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
import locale
from PySide import QtCore, QtGui

from ui.statistics import Ui_MainWindow
import bb_engine
from bb_shared import Shared

class StatisticsApp(QtGui.QMainWindow, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        Shared.__init__(self)
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.database = bb_engine.Database()
        self.combo_nets_fill()
        self.combo_ranges_fill()
        #main tab variables
        self.v = {
        'mode_std': self.gui.combo_standings_mode.currentIndex,
        'mode_form': self.gui.combo_form_mode.currentIndex,
        'mode_date': self.gui.combo_scheudle_dates.currentText,
        'mode_home': self.gui.combo_home_mode.currentIndex,
        'mode_away': self.gui.combo_away_mode.currentIndex,
        'home_team': self.gui.main_combo_home.currentText,
        'away_team': self.gui.main_combo_away.currentText,
        'net': self.gui.main_combo_nets.currentText,
        'ranges': self.gui.main_combo_ranges.currentText,
        'c_1': QtGui.QColor('#E6E6FA'),
        'c_2': QtGui.QColor('#BFBFBF'),
        'c_home': QtGui.QColor('#71CA80'),
        'c_away': QtGui.QColor('#E1571F'),
        'c_win': QtGui.QColor('#90D889'),
        'c_draw': QtGui.QColor('#9894EB'),
        'c_lose': QtGui.QColor('#DE7C7C'),
        'palette': '#39A1B2'}
        self.leagues_tree()
        try:
            self.tree_return()
        except:
            pass
        self.bindings()
        self.prediction()
    def bindings(self):
        '''Bindings for app widgets.
         QtCore.QObject.connect(widget,QtCore.SIGNAL("clicked()"),command)
         or
         widget.event.connect(function)'''
        self.gui.main_combo_home.currentIndexChanged.connect\
                                                    (self.combo_team_change)
        self.gui.main_combo_away.currentIndexChanged.connect\
                                                    (self.combo_team_change)
        self.gui.combo_standings_mode.activated.connect(self.standings)
        self.gui.combo_form_mode.activated.connect(self.form)
        self.gui.combo_scheudle_dates.activated.connect(self.scheudle)
        self.gui.combo_home_mode.activated.connect(self.main_home)
        self.gui.combo_away_mode.activated.connect(self.main_away)
        self.gui.treeLeagues.itemClicked.connect(self.tree_return)
        self.gui.main_combo_ranges.activated.connect(self.prediction)
        self.gui.main_combo_nets.activated.connect(self.prediction)
        self.gui.spin_series.valueChanged.connect(self.tree_series)
        self.gui.main_table_scheudle.clicked.connect(self.scheudle_teams)
    
    def combo_team_change(self):
        self.tables_fill()
        self.prediction()
    def scheudle_teams(self):
        ''' Changes teams when clicked match'''
        row = self.gui.main_table_scheudle.currentRow()
        home = self.gui.main_table_scheudle.item(row, 1).text()
        away = self.gui.main_table_scheudle.item(row, 2).text()
        index_home = self.gui.main_combo_home.findText(home)
        index_away = self.gui.main_combo_away.findText(away)
        self.gui.main_combo_home.setCurrentIndex(index_home)
        self.gui.main_combo_away.setCurrentIndex(index_away)
    def leagues_tree(self):
        ''' Creates leageues tree'''
        self.gui.treeLeagues.headerItem().setText(0, ('Leagues'))
        self.gui.treeLeagues.sortItems(0, QtCore.Qt.SortOrder(0))

        paths = []
        for i in os.walk("leagues/"):
            paths.append(i[0])
        paths.pop(0)
        paths.reverse()
        for i in paths:
            name = os.path.split(i)
            name = name[1]
            item = QtGui.QTreeWidgetItem(self.gui.treeLeagues)
            item.setText(0, (name))
            files = os.listdir(i)
            for f in files:
                QtGui.QTreeWidgetItem(item).setText(0, f)
        self.gui.treeLeagues.setSortingEnabled(0)
        item.setExpanded(1)
        self.gui.treeLeagues.setCurrentItem(item.child(0))
        self.gui.treeLeagues.setSortingEnabled(1)

    def tree_return(self):
        ''' Calls ng_engine module and loads csv file dependly of path
        and league name'''
        child = self.gui.treeLeagues.currentItem()
        try:
            parent = child.parent()
            switch = parent.text(0)
            path = str(os.path.join('leagues', switch, ''))
            name = child.text(0)
        except:
            path = False
        if path:
            try:
                self.database.load_csv(path, name)
            except:
                self.find_broken_leagues()
                self.database.load_csv(path, name)
            self.combo_teams_fill()
            self.combo_scheudle_dates()
            self.tables_fill()

    def combo_teams_fill(self):
        ''' Fills combos with team names(home and away)'''
        self.gui.main_combo_home.clear()
        self.gui.main_combo_away.clear()
        data = self.database.relations_base.execute('''Select
        team
        From league Order BY team ASC''')
        data = data.fetchall()
        teams = []
        for i in data:
            teams.append(i[0])
        self.gui.main_combo_home.addItems(teams)
        self.gui.main_combo_away.addItems(teams)
        self.gui.main_combo_home.setCurrentIndex(0)
        self.gui.main_combo_away.setCurrentIndex(1)

    def combo_nets_fill(self):
        ''' Fills combos with nets'''
        self.gui.main_combo_nets.clear()
        data = os.listdir(os.path.join('net'))
        nets = []
        for i in data:
            nets.append(i)
        self.gui.main_combo_nets.addItems(nets)
        self.gui.main_combo_nets.setCurrentIndex(0)

    def combo_ranges_fill(self):
        ''' Fills combos with ranges'''
        self.gui.main_combo_ranges.clear()
        data = os.listdir(os.path.join('profiles','ranges'))
        ranges = []
        for i in data:
            ranges.append(i)
        self.gui.main_combo_ranges.addItems(ranges)
        self.gui.main_combo_ranges.setCurrentIndex(0)

    def combo_scheudle_dates(self):
        '''Insert dates into scheudle combo '''
        self.gui.combo_scheudle_dates.clear()
        data = self.database.relations_base.execute('''SELECT DISTINCT date_txt
                                            FROM results ORDER BY id ASC''')
        dates = []
        for i in data:
            date = str(i[0])
            if len(date)<9:
                date = date+'0'
            dates.append(date)
        self.gui.combo_scheudle_dates.addItems(dates)
        # Sets current date
        data = self.database.relations_base.execute('''SELECT min(id)
                                    FROM results
                                    WHERE gHomeEnd="NULL"''')
        data = data.fetchone()
        if data[0]:
            min_id = data[0]
            data = self.database.relations_base.execute('''SELECT date_txt
                                            FROM results
                                            WHERE id=?''', [(min_id)])
            data = data.fetchone()
            min_date = str(data[0])
            date_id = self.gui.combo_scheudle_dates.findText(min_date)
            self.gui.combo_scheudle_dates.setCurrentIndex(date_id)
            text = self.gui.combo_scheudle_dates.itemText(date_id)
            self.gui.combo_scheudle_dates.setItemText(date_id, '>>>'+text+'<<<')
        else:
            date_id = self.gui.combo_scheudle_dates.findText(dates[-1])
            self.gui.combo_scheudle_dates.setCurrentIndex(date_id)

    def tables_fill(self):
        ''' Fills all tables with data'''
        self.standings()
        self.form()
        self.scheudle()
        self.main_home()
        self.main_away()
        try:
            self.tree_series()
        except:
            pass

    def s_f(self, data, labels, table):
        ''' Creates table for standings and form'''
        table.clear()
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        data = data.fetchall()
        table.setRowCount(len(data))
        row = -1
        col = -1
        for i in data:
            row += 1
            if i[0] == self.v['home_team']():
                color = self.v['c_home']
            elif i[0] == self.v['away_team']():
                color = self.v['c_away']
            elif row % 2:
                color = self.v['c_1']
            else:
                color = self.v['c_2']
            for lin in i:
                col += 1
                line = QtGui.QTableWidgetItem(str(lin))
                table.setItem(row, col, line)
                table.item(row, col).setBackground(color)
                table.item(row, col).setTextAlignment(QtCore.Qt.AlignHCenter)
            col = -1
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        table.verticalHeader().setDefaultSectionSize(20)
        #self.table_color(table, 10, self.main_v['palette'])

    def standings(self):
        ''' Table standings in main tab'''
        if self.v['mode_std']() == 0: #Overall
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'Wins',
            'Draws',
            'Loses',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matches,ROUND(points,2),goalsscored,goalslost,
            (winhome+winaway),(drawhome+drawaway),(losehome+loseaway),
            bts,over25,under25
            From league Order by points DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)
        elif self.v['mode_std']() == 1: #Home
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'WinsH',
            'DrawsH',
            'LosesH',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matchesHome,ROUND(pointsHome,2),goalsscoredhome,
            goalslosthome,winhome,drawhome,losehome,btsHome,over25Home,under25Home
            From league Order by pointsHome DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)
        elif self.v['mode_std']() == 2: #Away
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'WinsA',
            'DrawsA',
            'LosesA',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matchesAway,ROUND(pointsAway,2),goalsscoredaway,
            goalslostaway,winaway,drawaway,loseaway,btsAway,over25Away,under25Away
            From league Order by pointsAway DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)

        #############3
        if self.v['mode_std']() == 3: #Overall BB
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'MOW',
            'MOL',
            'Wins',
            'Draws',
            'Loses',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matches,ROUND(pointsBB,2),goalsscored,goalslost,ROUND(mowins,2),ROUND(moloses,2),(winhome+winaway),(drawhome+drawaway),
            (losehome+loseaway),bts,over25,under25
            From league Order by pointsBB DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)
        elif self.v['mode_std']() == 4: #Home BB
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'MOW',
            'MOL',
            'WinsH',
            'DrawsH',
            'LosesH',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matchesHome,ROUND(pointsBBHome,2),goalsscoredhome,
            goalslosthome,ROUND(mowinsHome,2),ROUND(molosesHome,2),
            winhome,drawhome,losehome,btsHome,over25Home,under25Home
            From league Order by pointsBBHome DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)
        elif self.v['mode_std']() == 5: #Away BB
            labels = [
            'Team',
            'Matches',
            'Pts',
            'GS',
            'GL',
            'MOW',
            'MOL',
            'WinsA',
            'DrawsA',
            'LosesA',
            'BTS',
            'over2.5',
            'under2.5']
            data = self.database.relations_base.execute('''Select
            team,matchesAway,ROUND(pointsBBAway,2),goalsscoredaway,
            goalslostaway,ROUND(mowinsAway,2),ROUND(molosesAway,2),
            winaway,drawaway,loseaway,btsAway,over25Away,under25Away
            From league Order by pointsBBAway DESC''')
            self.s_f(data, labels, self.gui.main_table_standings)

    def form(self):
        ''' Table form in main tab'''
        if self.v['mode_form']() == 0: #Overall
            labels = [
            'Team',
            'Form',
            'F1',
            'F1opp',
            'F2',
            'F2opp',
            'F3',
            'F3opp',
            'F4',
            'F4opp',]
            data = self.database.relations_base.execute('''Select
            team,form,f1,f1op,f2,f2op,f3,f3op,f4,f4op
            From league Order by form DESC''')
            self.s_f(data, labels, self.gui.main_table_form)
        elif self.v['mode_form']() == 1: #Home
            labels = [
            'Team',
            'FormHome',
            'F1',
            'F1opp',
            'F2',
            'F2opp']
            data = self.database.relations_base.execute('''Select
            team,formHome,f1Home,f1opHome,f2Home,f2opHome
            From league Order by formHome DESC''')
            self.s_f(data, labels, self.gui.main_table_form)
        elif self.v['mode_form']() == 2: #Away
            labels = [
            'Team',
            'FormAway',
            'F1',
            'F1opp',
            'F2',
            'F2opp']
            data = self.database.relations_base.execute('''Select
            team,formAway,f1Away,f1opAway,f2Away,f2opAway
            From league Order by formAway DESC''')
            self.s_f(data, labels, self.gui.main_table_form)
        if self.v['mode_form']() == 3: #Overall BB
            labels = [
            'Team',
            'Form',
            'F1',
            'F1opp',
            'F2',
            'F2opp',
            'F3',
            'F3opp',
            'F4',
            'F4opp',]
            data = self.database.relations_base.execute('''Select
            team,ROUND(formBB,2),ROUND(f1BB,2),f1op,ROUND(f2BB,2),
            f2op,ROUND(f3BB,2),f3op,ROUND(f4BB,2),f4op
            From league Order by formBB DESC''')
            self.s_f(data, labels, self.gui.main_table_form)
        elif self.v['mode_form']() == 4: #Home BB
            labels = [
            'Team',
            'FormHome',
            'F1',
            'F1opp',
            'F2',
            'F2opp']
            data = self.database.relations_base.execute('''Select
            team,ROUND(formBBHome,2),ROUND(f1BBHome,2),f1opHome,ROUND(f2BBHome,2),f2opHome
            From league Order by formBBHome DESC''')
            self.s_f(data, labels, self.gui.main_table_form)
        elif self.v['mode_form']() == 5: #Away BB
            labels = [
            'Team',
            'FormAway',
            'F1',
            'F1opp',
            'F2',
            'F2opp']
            data = self.database.relations_base.execute('''Select
            team,ROUND(formBBAway,2),ROUND(f1BBAway,2),f1opAway,ROUND(f2BBAway,2),f2opAway
            From league Order by formBBAway DESC''')
            self.s_f(data, labels, self.gui.main_table_form)

    def scheudle(self):
        ''' Table scheudle in main tab'''
        date = str(self.v['mode_date']())
        date = date.replace('>','')
        date = date.replace('<','')
        self.gui.main_table_scheudle.clear()
        labels = [
        'Date',
        'Home',
        'Away',
        'Result']
        self.gui.main_table_scheudle.setColumnCount(len(labels))
        self.gui.main_table_scheudle.setHorizontalHeaderLabels(labels)
        data = self.database.relations_base.execute('''Select
        date_txt,
        home,
        away,
        gHomeEnd,
        gAwayEnd
        From results WHERE date_txt=?''', [(date)])
        data = data.fetchall()
        data = self.matches_list_fix(data)
        self.gui.main_table_scheudle.setRowCount(len(data))
        row = -1
        col = -1
        for i in data:
            row += 1
            if row % 2:
                color = self.v['c_1']
            else:
                color = self.v['c_2']
            for lin in i:
                col += 1
                line = QtGui.QTableWidgetItem(str(lin))
                self.gui.main_table_scheudle.setItem(row, col, line)
                self.gui.main_table_scheudle.item(row, col).\
                                setBackground(color)
                self.gui.main_table_scheudle.item(row, col).\
                                setTextAlignment(QtCore.Qt.AlignHCenter)
            col = -1
        self.gui.main_table_scheudle.resizeRowsToContents()
        self.gui.main_table_scheudle.resizeColumnsToContents()
        self.gui.main_table_scheudle.verticalHeader().\
                                                setDefaultSectionSize(20)

    def h_a(self, team, mode, table):
        ''' Creates table for home and away'''
        table.clear()
        labels = [
            'Date',
            'Home',
            'Away',
            'Result']
        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        if mode == 0:  #Overall
            data = self.database.relations_base.execute('''Select
            date_txt,
            home,
            away,
            gHomeEnd,
            gAwayEnd
            From results WHERE home=? or away=?''',(
                                                str(team),
                                                str(team)
                                                                    ))
            data = data.fetchall()
            data = self.matches_list_fix(data)
            table.setRowCount(len(data))

            #Inserting items into table
            row = -1
            col = -1
            for i in data:
                row += 1
                for lin in i:
                    col += 1
                    line = QtGui.QTableWidgetItem(str(lin))
                    table.setItem(row, col, line)
                    goals_h, goals_a = i[-1].split(':')
                    if i[1] == str(team):
                        if goals_h == '-' or goals_a == '-':
                            table.item(row, col).\
                            setBackground(self.v['c_1'])
                        elif int(goals_h)>int(goals_a):
                            table.item(row, col).\
                            setBackground(self.v['c_win'])
                        elif int(goals_h)<int(goals_a):
                            table.item(row, col).\
                            setBackground(self.v['c_lose'])
                        elif int(goals_h) == int(goals_a):
                            table.item(row, col).\
                            setBackground(self.v['c_draw'])
                    if i[2] == str(team):
                        if goals_h == '-' or goals_a == '-':
                            table.item(row, col).\
                                setBackground(self.v['c_1'])
                        elif int(goals_h)<int(goals_a):
                            table.item(row, col).\
                                setBackground(self.v['c_win'])
                        elif int(goals_h)>int(goals_a):
                            table.item(row, col).\
                                setBackground(self.v['c_lose'])
                        elif int(goals_h) == int(goals_a):
                            table.item(row, col).\
                                setBackground(self.v['c_draw'])
                    table.item(row, col).\
                        setTextAlignment(QtCore.Qt.AlignHCenter)
                col = -1
        if mode == 1:  #Home
            # SQL statement
            data = self.database.relations_base.execute('''Select
            date_txt,
            home,
            away,
            gHomeEnd,
            gAwayEnd
            From results WHERE home=?''', [(str(team)
                                                                    )])
            data = data.fetchall()
            data = self.matches_list_fix(data)
            table.setRowCount(len(data))

            #Inserting items into table
            row = -1
            col = -1
            for i in data:
                row += 1
                for lin in i:
                    col += 1
                    line = QtGui.QTableWidgetItem(str(lin))
                    table.setItem(row, col, line)
                    goals_h, goals_a = i[-1].split(':')
                    if goals_h == '-' or goals_a == '-':
                        table.item(row, col).\
                                setBackground(self.v['c_1'])
                    elif int(goals_h)>int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_win'])
                    elif int(goals_h)<int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_lose'])
                    elif int(goals_h) == int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_draw'])
                    table.item(row, col).\
                        setTextAlignment(QtCore.Qt.AlignHCenter)
                col = -1
        if mode == 2:  #Away
            # SQL statement
            data = self.database.relations_base.execute('''Select
            date_txt,
            home,
            away,
            gHomeEnd,
            gAwayEnd
            From results WHERE away=?''', [(str(team)
                                                                    )])
            data = data.fetchall()
            data = self.matches_list_fix(data)
            table.setRowCount(len(data))

            #Inserting items into table
            row = -1
            col = -1
            for i in data:
                row += 1
                for lin in i:
                    col += 1
                    line = QtGui.QTableWidgetItem(str(lin))
                    table.setItem(row, col, line)
                    goals_h, goals_a = i[-1].split(':')
                    if goals_h == '-' or goals_a == '-':
                        table.item(row, col).\
                                setBackground(self.v['c_1'])
                    elif int(goals_h)<int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_win'])
                    elif int(goals_h)>int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_lose'])
                    elif int(goals_h) == int(goals_a):
                        table.item(row, col).\
                            setBackground(self.v['c_draw'])
                    table.item(row, col).\
                        setTextAlignment(QtCore.Qt.AlignHCenter)
                col = -1
        # Final configuring table
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        
    def prediction(self):
        ''' Gives prediction for match'''
        locale.setlocale(locale.LC_ALL, "C")
        home = self.v['home_team']()
        away = self.v['away_team']()
        

        odds = self.database.relations_base.execute('''SELECT odd_1,odd_x,odd_2,date_txt
        FROM results WHERE (home="%s" AND away="%s" AND gHomeEnd = "NULL")'''%(home,away))
        try: #match in database
            odds = odds.fetchone()
            odd_1,odd_x,odd_2,dt = odds
        except: # didn't match
            odd_1 = 0
        if odd_1>0: # odds in file
            print 'prediction using odds from file'
            prediction = self.database.simulation_prediction(home,
                                                         away,
                                                             self.v['net'](),date=dt,mode=2)
        else: # use predicted odds
            print 'prediction using predicted odds'
            prediction = self.database.simulation_prediction(home,
                                                         away,
                                                             self.v['net']())
        # ranges
        with open(os.path.join('profiles', 'ranges', '')+self.v['ranges'](),'r') as ranges:
            load = list(ranges)
        val = []
        for i in range(0, len(load)):
            item = load[i].replace('\n', '')
            item = float(item)
            val.append(item)
        min_1 = val[0]
        max_1 = val[1]
        min_1x = val[2]
        max_1x = val[3]
        min_x = val[4]
        max_x = val[5]
        min_x2 = val[6]
        max_x2 = val[7]
        min_2 = val[8]
        max_2 = val[9]
        if min_1 <= prediction and prediction < max_1:
            bet = '1'
        elif min_1x <= prediction and prediction < max_1x:
            bet = '1x'
        elif min_x <= prediction and prediction < max_x:
            bet = 'x'
        elif min_x2 <= prediction and prediction < max_x2:
            bet = 'x2'
        elif min_2 <= prediction and prediction < max_2:
            bet = '2'
        else:
            bet = 'None'
        line = home+' - '+away+' : '+bet+' net: '+str(round(prediction,3))
        self.gui.label_prediction.setText(line)
        self.gui.label_home.setText(home)
        self.gui.label_away.setText(away)

        ####
        # Odds
        ####
        odds = self.database.relations_base.execute('''SELECT odd_1,odd_x,odd_2,gHomeEnd
        FROM results WHERE (home="%s" AND away="%s" AND gHomeEnd = "NULL")'''%(home,away))
        try: #match in database
            odds = odds.fetchone()
            odd_1,odd_x,odd_2,gh = odds
        except: # didn't match
            odd_1 = 0
        if odd_1>0:
            # odds in file
            print 'use odds'
            odd_1x = round(1/((1/odd_1) + (1/odd_x)),2)
            odd_x2 = round(1/((1/odd_x) + (1/odd_2)),2)
            line ='1: '+str(odd_1)+'  x: '+str(odd_x)+'  2: '+str(odd_2)+self.nl+\
                ' 1x: '+str(odd_1x)+'  x2: '+str(odd_x2)
            
        else: #predict odds
            print 'predict odds'
            odds = self.database.simulation_prediction(home, away,
                                                         'default',mode=1)
            print 'odds',prediction
            odd_1 = self.odds_rescale(odds[0],100)
            odd_x = self.odds_rescale(odds[1],100)
            odd_2 = self.odds_rescale(odds[2],100)
            odd_1x = round(1/((1/odd_1) + (1/odd_x)),2)
            odd_x2 = round(1/((1/odd_x) + (1/odd_2)),2)
            if odd_1x < 1:
                odd_1x = 1
            if odd_x2 < 1:
                odd_x2 = 1
            line ='1: '+str(odd_1)+'  x: '+str(odd_x)+'  2: '+str(odd_2)+self.nl+\
                ' 1x: '+str(odd_1x)+'  x2: '+str(odd_x2)
        self.gui.label_odds.setText(line)
        print odd_1,odd_x,odd_2,odd_1x,odd_x2

    def main_home(self):
        ''' Table home in main tab'''
        self.h_a(self.v['home_team'](),
                      self.v['mode_home'](),
                      self.gui.main_table_home)

    def main_away(self):
        ''' Table away in main tab'''
        self.h_a(self.v['away_team'](),
                      self.v['mode_away'](),
                      self.gui.main_table_away)

    def matches_list_fix(self, data):
        '''Joins two items in every row:"gHomeEnd:gAwayEnd"'''
        match_list = []
        for i in data:
            line = list(i[0:3])
            if i[3] == 'NULL':
                goals_str = '-:-'
            else:
                goals_str = str(i[3])+':'+str(i[4])
            line.append(goals_str)
            match_list.append(line)
        return match_list

    def table_color(self, table, size, color):
        '''Font size and background color of specified table
        not in use since stylesheets'''
        #font change size
        font = QtGui.QFont(table.font())
        font.setPointSize(size)
        table.setFont(font)
        #background color outside table
        palette = table.palette()
        palette.setColor( QtGui.QPalette.Base, QtGui.QColor(color))
        table.setPalette(palette)
    def tree_series(self):
        ''' Fills tree series dependly on min value'''
        home = self.v['home_team']()
        away = self.v['away_team']()
        min_val = self.gui.spin_series.value()
        self.gui.tree_series_home.headerItem().setText(0, home)
        self.gui.tree_series_away.headerItem().setText(0, away)
        self.gui.tree_series_home.clear()
        self.gui.tree_series_away.clear()
        ## Home
        series_home = self.database.relations_base.execute('''SELECT
        series_wins,
        series_winshome,
        series_draws,
        series_drawshome,
        series_loses,
        series_loseshome,
        series_nowins,
        series_nowinshome,
        series_nodraws,
        series_nodrawshome,
        series_noloses,
        series_noloseshome,
        series_bts,
        series_btsHome,
        series_over25,
        series_over25Home,
        series_under25,
        series_under25Home
        FROM series WHERE team="%s"'''%home)
        series_wins, series_winshome, series_draws, series_drawshome,\
        series_loses, series_loseshome, series_nowins, series_nowinshome,\
        series_nodraws, series_nodrawshome, series_noloses,series_noloseshome,\
        series_bts,series_btsHome,series_over25,series_over25Home,\
        series_under25,series_under25Home= series_home.fetchone()


        series_home_val = [series_wins, series_winshome, series_draws,
                           series_drawshome,series_loses, series_loseshome,
                           series_nowins, series_nowinshome,series_nodraws,
                           series_nodrawshome, series_noloses,
                           series_noloseshome,series_bts,series_btsHome,
                           series_over25,series_over25Home,series_under25,
                           series_under25Home]
        series_home_str = ['Wins', 'Wins home', 'Draws', 'Draws home', 'Loses',
                           'Loses home', 'No wins', 'No wins home', 'No draws',
                           'No draws home', 'No loses', 'No loses home',
                           'BTS','BTS home','over2.5','over2.5 home',
                           'under2.5','under2.5 home']

        for i in range(0, len(series_home_val)):
            if series_home_val[i] >= min_val:
                line = series_home_str[i]+': '+str(series_home_val[i])
                item = QtGui.QTreeWidgetItem(self.gui.tree_series_home)
                item.setText(0, line)

        ## away
        series_away = self.database.relations_base.execute('''SELECT
        series_wins,
        series_winsaway,
        series_draws,
        series_drawsaway,
        series_loses,
        series_losesaway,
        series_nowins,
        series_nowinsaway,
        series_nodraws,
        series_nodrawsaway,
        series_noloses,
        series_nolosesaway,
        series_bts,
        series_btsAway,
        series_over25,
        series_over25Away,
        series_under25,
        series_under25Away
        FROM series WHERE team="%s"'''%away)
        series_wins, series_winsaway, series_draws, series_drawsaway, \
        series_loses, series_losesaway, series_nowins, series_nowinsaway,\
        series_nodraws, series_nodrawsaway, series_noloses,series_nolosesaway,\
        series_bts,series_btsAway,series_over25,series_over25Away,\
        series_under25,series_under25Away= series_away.fetchone()


        series_away_val = [series_wins, series_winsaway, series_draws,
                           series_drawsaway,series_loses, series_losesaway,
                           series_nowins, series_nowinsaway,series_nodraws,
                           series_nodrawsaway, series_noloses,series_nolosesaway,
                           series_bts,series_btsHome,
                           series_over25,series_over25Home,series_under25,
                           series_under25Home]
        series_away_str = ['Wins', 'Wins away', 'Draws', 'Draws away', 'Loses',
                           'Loses away', 'No wins', 'No wins away', 'No draws',
                           'No draws away', 'No loses', 'No loses away',
                           'BTS','BTS away','over2.5','over2.5 away',
                           'under2.5','under2.5 away']

        for i in range(0, len(series_away_val)):
            if series_away_val[i] >= min_val:
                line = series_away_str[i]+': '+str(series_away_val[i])
                item = QtGui.QTreeWidgetItem(self.gui.tree_series_away)
                item.setText(0, line)



if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = StatisticsApp()
    MYAPP.show()
    sys.exit(APP.exec_())
