# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski

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

from PySide import QtCore, QtGui
from ui.leagues import Ui_Leagues
import bb_engine
from bb_shared import Shared

class LeaguesApp(QtGui.QWidget,Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        Shared.__init__(self)
        self.database = bb_engine.Database()
        QtGui.QWidget.__init__(self, parent)
        self.gui = Ui_Leagues()
        self.gui.setupUi(self)
        self.gui.tree_matches.headerItem().setText(0, ('Date'))
        self.gui.tree_matches.headerItem().setText(1, ('Home'))
        self.gui.tree_matches.headerItem().setText(2, ('Away'))
        self.gui.tree_matches.headerItem().setText(3, ('FTH'))
        self.gui.tree_matches.headerItem().setText(4, ('FTA'))
        self.gui.tree_teams_home.headerItem().setText(0, ('Home'))
        self.gui.tree_teams_away.headerItem().setText(0, ('Away'))
        self.gui.tree_leagues.headerItem().setText(0, ('Leagues'))
        self.gui.tree_leagues_own.headerItem().setText(0, ('Leagues'))
        self.gui.tree_teams.headerItem().setText(0, ('Teams'))
        self.gui.tree_team_profiles.headerItem().setText(0, ('Profiles'))
        self.bindings()
        self.tree_leagues_teams()
        self.tree_profiles()
        self.line_to_add()

    def bindings(self):
        ''' Widgets connections'''
        # tab teams
        self.gui.button_from_league.clicked.connect(self.teams_from_league_load)
        self.gui.tree_leagues.doubleClicked.connect(self.teams_from_league_load)
        self.gui.button_teams_clear.clicked.connect(self.team_clear)
        self.gui.button_teams_remove.clicked.connect(self.team_remove)
        self.gui.button_teams_add.clicked.connect(self.team_add)
        self.gui.button_profile_save.clicked.connect(self.profile_save)
        self.gui.button_profile_load.clicked.connect(self.profile_load)
        self.gui.tree_team_profiles.doubleClicked.connect(self.profile_load)
        self.gui.button_profile_delete.clicked.connect(self.profile_delete)
        self.gui.line_team.returnPressed.connect(self.team_add)
        #tab leauges
        self.gui.tree_teams.itemChanged.connect(self.teams_home_away)
        self.gui.button_league_load.clicked.connect(self.league_load)
        self.gui.tree_leagues_own.doubleClicked.connect(self.league_load)
        self.gui.button_up.clicked.connect(self.move_up)
        self.gui.button_down.clicked.connect(self.move_down)
        self.gui.calendarWidget.clicked.connect(self.line_to_add)
        self.gui.tree_teams_home.clicked.connect(self.line_to_add)
        self.gui.tree_teams_away.clicked.connect(self.line_to_add)
        self.gui.spin_home.valueChanged.connect(self.line_to_add)
        self.gui.spin_away.valueChanged.connect(self.line_to_add)
        self.gui.button_match_add.clicked.connect(self.match_add)
        self.gui.button_match_remove.clicked.connect(self.match_remove)
        self.gui.button_league_save.clicked.connect(self.league_save)
        self.gui.button_league_delete.clicked.connect(self.league_delete)

    def team_add(self):
        ''' Adds team to tree'''
        name = str(self.gui.line_team.text())
        if not len(name.strip(' '))<3:
            item = QtGui.QTreeWidgetItem(self.gui.tree_teams)
            item.setText(0, self.gui.line_team.text())
            self.gui.line_team.setText((''))
        else:
            print "Can't be empty or too short"

    def team_remove(self):
        ''' Remove team from tree'''
        item = self.gui.tree_teams.currentItem()
        index = self.gui.tree_teams.indexOfTopLevelItem(item)
        self.gui.tree_teams.takeTopLevelItem(index)

    def team_clear(self):
        ''' Clear tree_teams'''
        self.gui.tree_teams.clear()
        self.teams_home_away()

    def profile_save(self):
        ''' Saves teams to file'''
        file_name = self.gui.line_teams_save.text()
        with open(os.path.join('profiles', 'teams', '')+\
                                str(file_name), 'w') as file_save:
            count = self.gui.tree_teams.topLevelItemCount()
            for i in range(0, count):
                item = self.gui.tree_teams.topLevelItem(i)
                name = item.text(0)
                if i == count-1:
                    line = str(name)
                else:
                    line = str(name+self.nl)
                file_save.write(line)
            self.tree_profiles()

    def profile_load(self):
        ''' Loads profile of teams'''
        self.gui.tree_teams.clear()
        child = self.gui.tree_team_profiles.currentItem()
        file_name = str(child.text(0))
        with open(os.path.join('profiles', 'teams', '')+\
                            file_name, 'r') as file_load:
            for i in file_load:
                team = self.rm_lines(i)
                item = QtGui.QTreeWidgetItem(self.gui.tree_teams)
                item.setText(0, team)

    def profile_delete(self):
        ''' Deletes profile of teams'''
        path = os.path.join('profiles', 'teams', '')
        item = self.gui.tree_team_profiles.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.tree_profiles()

    def tree_profiles(self):
        ''' Show list of files with saved teams'''
        self.gui.tree_team_profiles.clear()
        self.gui.tree_team_profiles.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_team_profiles.setSortingEnabled(1)
        dir_bases = os.listdir(os.path.join('profiles','teams'))
        for i in dir_bases:
            item = QtGui.QTreeWidgetItem(self.gui.tree_team_profiles)
            item.setText(0, i)

    def teams_from_league_load(self):
        ''' Loads teams form league file'''
        self.gui.tree_teams.clear()
        child = self.gui.tree_leagues.currentItem()
        parent = child.parent()
        if parent:
            switch = parent.text(0)
            path = str(os.path.join('leagues', switch, ''))
            name = child.text(0)
        teams=self.database.return_teams(path, name)
        for i in teams:
            item = QtGui.QTreeWidgetItem(self.gui.tree_teams)
            item.setText(0, (i[0]))

    def tree_leagues_teams(self):
        ''' Fills trees on both tabs with league names'''
        self.gui.tree_leagues.clear()  #tab teams
        self.gui.tree_leagues_own.clear()  #tab leagues
        self.gui.tree_leagues.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_leagues_own.sortItems(0, QtCore.Qt.SortOrder(0))

        paths = []
        for i in os.walk("leagues/"):
            paths.append(i[0])
        paths.pop(0)
        paths.reverse()
        for i in paths:
            print i
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

        paths = []
        for path,folder,name in os.walk("leagues/"):
            paths.append(path)
        paths.pop(0)
        paths.reverse()
        for i in paths:
            name = os.path.split(i)
            name = name[1]
            item = QtGui.QTreeWidgetItem(self.gui.tree_leagues_own)
            item.setText(0, (name))
            files = os.listdir(i)
            for f in files:
                QtGui.QTreeWidgetItem(item).setText(0, f)
        self.gui.tree_leagues_own.setSortingEnabled(0)
        item.setExpanded(1)
        self.gui.tree_leagues_own.setCurrentItem(item.child(0))
        self.gui.tree_leagues_own.setSortingEnabled(1)

    def teams_home_away(self):
        ''' Fills home away trees with teams from team tree in tab teams'''
        self.gui.tree_teams_away.clear()
        self.gui.tree_teams_home.clear()
        count = self.gui.tree_teams.topLevelItemCount()
        for i in range(0, count):
            name = self.gui.tree_teams.topLevelItem(i)
            name = name.text(0)
            item_home = QtGui.QTreeWidgetItem(self.gui.tree_teams_home)
            item_home.setText(0, (name))

            item_away = QtGui.QTreeWidgetItem(self.gui.tree_teams_away)
            item_away.setText(0, (name))

    def league_load(self):
        ''' Loads league for edit'''
        child = self.gui.tree_leagues_own.currentItem()
        parent = child.parent()
        if parent:
            switch = parent.text(0)
            path = str(os.path.join('leagues', switch, ''))
            name = child.text(0)
        with open(path+name,'r') as item:
            league = reader(item)
            league = list(league)
        self.gui.tree_matches.clear()
        for i in league:
            item_match = QtGui.QTreeWidgetItem(self.gui.tree_matches)
            item_match.setFlags(item_match.flags() | QtCore.Qt.ItemIsEditable)
            item_match.setText(0, (i[0]))
            item_match.setText(1, (i[1]))
            item_match.setText(2, (i[2]))
            item_match.setText(3, (i[3]))
            item_match.setText(4, (i[4]))
        self.gui.tree_matches.setCurrentItem(item_match)

    def move_up(self):
        ''' Moves match up in league editor'''
        item = self.gui.tree_matches.currentItem()
        row  = self.gui.tree_matches.currentIndex().row()
        if row > 0:
            self.gui.tree_matches.takeTopLevelItem(row)
            self.gui.tree_matches.insertTopLevelItem(row - 1, item)
            self.gui.tree_matches.setCurrentItem(item)

    def move_down(self):
        ''' Moves match down in league editor'''
        item = self.gui.tree_matches.currentItem()
        row  = self.gui.tree_matches.currentIndex().row()
        count = self.gui.tree_matches.topLevelItemCount()
        if row < count-1:
            self.gui.tree_matches.takeTopLevelItem(row)
            self.gui.tree_matches.insertTopLevelItem(row + 1, item)
            self.gui.tree_matches.setCurrentItem(item)

    def line_to_add(self):
        ''' Show selected items to add : date,home,away, result'''
        date = self.gui.calendarWidget.selectedDate()
        self.date = date.toString('yyyy.MM.dd')

        home = self.gui.tree_teams_home.currentItem()
        try:
            self.home = home.text(0)
        except:
            self.home = 'Home'

        away = self.gui.tree_teams_away.currentItem()
        try:
            self.away = away.text(0)
        except:
            self.away = 'Away'
        self.fth = self.gui.spin_home.value()
        if self.fth == -1:
            self.fth = 'NULL'
        self.fta = self.gui.spin_away.value()
        if self.fta == -1:
            self.fta = 'NULL'
        line = str(self.date)+' '+str(self.home)+' '+str(self.away)+' '+\
                                            str(self.fth)+' '+str(self.fta)
        self.gui.line_match.setText(line)

    def match_add(self):
        ''' Adds selected items to add : date,home,away, result'''
        item_match = QtGui.QTreeWidgetItem(self.gui.tree_matches)
        item_match.setFlags(item_match.flags() | QtCore.Qt.ItemIsEditable)
        item_match.setText(0, (self.date))
        item_match.setText(1, (self.home))
        item_match.setText(2, (self.away))
        item_match.setText(3, (str(self.fth)))
        item_match.setText(4, (str(self.fta)))
        self.gui.spin_away.setValue(-1)
        self.gui.spin_home.setValue(-1)
        self.gui.tree_matches.setCurrentItem(item_match)

    def match_remove(self):
        ''' Removes match from tree'''
        item = self.gui.tree_matches.currentItem()
        index = self.gui.tree_matches.indexOfTopLevelItem(item)
        self.gui.tree_matches.takeTopLevelItem(index)

    def league_save(self):
        ''' Saves edited league'''
        name = self.gui.line_league_save.text()
        with open(os.path.join('leagues', 'current', '')+name, 'w') as save:
            count = self.gui.tree_matches.topLevelItemCount()
            for i in range(0, count):
                item = self.gui.tree_matches.topLevelItem(i)
                date = str(item.text(0))
                home = str(item.text(1))
                away = str(item.text(2))
                fth = str(item.text(3))
                fta = str(item.text(4))
                line = date+','+home+','+away+','+fth+','+fta+self.nl
                save.write(line)
            self.tree_leagues_teams()

    def league_delete(self):
        ''' Delete league'''
        item = self.gui.tree_leagues_own.currentItem()
        file_delete = item.text(0)
        path_name = item.parent()
        if path_name:
            path_name = str(path_name.text(0))
            path = os.path.join('leagues', path_name.lower(), '')
            self.delete_file(file_delete, path)
            self.tree_leagues_teams()


if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = LeaguesApp()
    MYAPP.show()
    sys.exit(APP.exec_())

