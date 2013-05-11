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
import platform

from PySide import QtGui
from data.ui.bet_boy import Ui_BetTools
from data.export_manager import ExportApp
from data.learning_manager import LearningApp
from data.update_manager import UpdateApp
from data.leagues_creator import LeaguesApp
from data.links_creator import LinksApp
from data.statistics_main import StatisticsApp
from data.simulator_window import SimulatorApp
from data.ui.about import Ui_About
from data.match_selector import SelectorApp
from data.bb_shared import Shared

class AboutApp(QtGui.QWidget):
   def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.gui = Ui_About()
        self.gui.setupUi(self)

class BBApp(QtGui.QMainWindow, Shared):
    '''Creates gui and events  '''
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        Shared.__init__(self)
        self.gui = Ui_BetTools()
        self.gui.setupUi(self)
        ### Set style
        system = platform.system()
        if system == 'Windows':
            f_style="windows"
        elif system == 'Linux':
            f_style="ubuntu"
        elif system == 'Darwin':
            f_style="mac"
        else:
            f_style="Ubuntu"
        with open(os.path.join('data','ui','')+f_style,"r") as style:
            self.setStyleSheet(style.read())
        ### Set working directory
        os.chdir(os.path.join(os.getcwd(),'data',''))
        ### Checks default directiories and create missing
        self.default_directories()
        self.bindings()
        self.win_about()
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'BetBoy',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def bindings(self):
        self.gui.actionSimulator.triggered.connect(self.win_simulator)
        self.gui.actionStats_central.triggered.connect(self.win_stats)
        self.gui.actionExport_manager.triggered.connect(self.win_export)
        self.gui.actionLeagues_creator.triggered.connect(self.win_leagues)
        self.gui.actionLearning_manager.triggered.connect(self.win_learning)
        self.gui.actionLinks_creator.triggered.connect(self.win_links)
        self.gui.actionUpdate_manager.triggered.connect(self.win_update)
        self.gui.actionAbout.triggered.connect(self.win_about)
        self.gui.actionMatch_selector.triggered.connect(self.win_selector)

    def win_stats(self):
        self.stats_app=StatisticsApp()
        self.stats = self.gui.mdiArea.addSubWindow(self.stats_app)
        self.stats.showMaximized()

    def win_update(self):
        self.update_app=UpdateApp()
        self.update = self.gui.mdiArea.addSubWindow(self.update_app)
        self.update.showMaximized()

    def win_links(self):
        self.links_app=LinksApp()
        self.links = self.gui.mdiArea.addSubWindow(self.links_app)
        self.links.showMaximized()

    def win_leagues(self):
        self.leagues_app=LeaguesApp()
        self.leagues = self.gui.mdiArea.addSubWindow(self.leagues_app)
        self.leagues.showMaximized()

    def win_export(self):
        self.export_app=ExportApp()
        self.export = self.gui.mdiArea.addSubWindow(self.export_app)
        self.export.showMaximized()

    def win_learning(self):
        self.learning_app=LearningApp()
        self.learning = self.gui.mdiArea.addSubWindow(self.learning_app)
        self.learning.showMaximized()

    def win_simulator(self):
        self.simulator_app=SimulatorApp()
        self.simulator = self.gui.mdiArea.addSubWindow(self.simulator_app)
        self.simulator.showMaximized()

    def win_selector(self):
        self.selector_app=SelectorApp()
        self.selector = self.gui.mdiArea.addSubWindow(self.selector_app)
        self.selector.showMaximized()

    def win_about(self):
        self.about_app=AboutApp()
        self.about = self.gui.mdiArea.addSubWindow(self.about_app)
        self.about.showMaximized()

if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = BBApp()
    MYAPP.showMaximized()
    sys.exit(APP.exec_())
