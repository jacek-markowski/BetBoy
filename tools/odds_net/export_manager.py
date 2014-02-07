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

from PySide import QtCore, QtGui
from ui.export import Ui_Export
from bb_engine import Database

system = platform.system()
if system == 'Windows':
    new_line = '\r\n'
elif system == 'Linux':
    new_line = '\n'
elif system == 'Darwin':
    new_line = '\r'
else:
    new_line = '\r\n'

class DoThread(QtCore.QThread):
    ''' New thread, export process'''
    def __init__(self, cmd, parent=None):
        QtCore.QThread.__init__(self)
        self.cmd = cmd
    def run(self):
        x = Database()
        x.load_csv(self.cmd[0], self.cmd[1], self.cmd[2], self.cmd[3],
                   self.cmd[4], self.cmd[5])


class ExportApp(QtGui.QWidget):
    '''Creates gui and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.gui = Ui_Export()
        self.gui.setupUi(self)
        # Calls ---------------------
        self.leagues_tree()
        self.profiles_tree()
        self.export_bindings()

    def delete_file(self, file_delete, path):
        ''' Deletes file'''
        reply = QtGui.QMessageBox.question(self, 'Delete?',
            "Are you sure to delete %s?"%file_delete, QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            if file_delete != 'default':
                os.remove(path+file_delete)

    def export_bindings(self):
        '''Bindings for app widgets.
         QtCore.QObject.connect(widget,QtCore.SIGNAL("clicked()"),command)
         or  widget.event.connect(function)'''
        self.gui.button_add.clicked.connect(self.leagues_add)
        self.gui.tree_leagues.doubleClicked.connect(self.leagues_add)
        self.gui.button_clear.clicked.connect(self.leagues_clear)
        self.gui.button_remove.clicked.connect(self.leagues_remove)
        self.gui.button_export.clicked.connect(self.leagues_export)
        self.gui.button_save.clicked.connect(self.profile_save)
        self.gui.button_load.clicked.connect(self.profile_load)
        self.gui.tree_profiles.doubleClicked.connect(self.profile_load)
        self.gui.button_delete.clicked.connect(self.profile_delete)

    def leagues_tree(self):
        ''' Fills tree with available csv files'''
        self.gui.tree_leagues.headerItem().setText(0, ('Leagues'))
        self.gui.tree_leagues.sortItems(0, QtCore.Qt.SortOrder(0))

        paths = []
        for path, folder, name in os.walk("converted/"):
            paths.append(path)
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

    def profiles_tree(self):
        ''' Fills tree with available profile files'''
        self.gui.tree_profiles.clear()
        self.gui.tree_profiles.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_profiles.setSortingEnabled(1)
        self.gui.tree_profiles.headerItem().setText(0, 'Profiles')
        dir_profiles = os.listdir(os.path.join('profiles'))
        for i in dir_profiles:
            item_pro = QtGui.QTreeWidgetItem(self.gui.tree_profiles)
            item_pro.setText(0, i)
        pass

    def leagues_add(self):
        ''' Adds csv file to leagues to export table'''
        rows =  self.gui.table_leagues.rowCount()+1
        self.gui.table_leagues.setRowCount(rows)
        self.gui.table_leagues.setColumnCount(4)
        child = self.gui.tree_leagues.currentItem()
        league = child.text(0)
        parent = child.parent()
        dir_name = parent.text(0)
        line1 = league
        line2 = dir_name
        r_min = self.gui.spin_min.value()
        r_max = self.gui.spin_max.value()
        r_min = self.gui.spin_min.textFromValue(r_min)
        r_max = self.gui.spin_max.textFromValue(r_max)

        if dir_name:
            self.gui.table_leagues.setItem(int(rows-1), 0, \
                                        QtGui.QTableWidgetItem(line1))
            self.gui.table_leagues.setItem(int(rows-1), 1, \
                                        QtGui.QTableWidgetItem(line2))
            self.gui.table_leagues.setItem(int(rows-1), 2, \
                                        QtGui.QTableWidgetItem(r_min))
            self.gui.table_leagues.setItem(int(rows-1), 3, \
                                        QtGui.QTableWidgetItem(r_max))
        labels = [
                'league',
                'directory',
                'r_min',
                'r_max']
        self.gui.table_leagues.setHorizontalHeaderLabels(labels)
        self.gui.table_leagues.resizeColumnsToContents()

    def leagues_remove(self):
        ''' Removes row from table leagues'''
        row = self.gui.table_leagues.currentRow()
        self.gui.table_leagues.removeRow(row)

    def leagues_clear(self):
        ''' Clears table leagues'''
        self.gui.table_leagues.clear()
        self.gui.table_leagues.setRowCount(0)
        self.gui.table_leagues.setColumnCount(0)

    def leagues_export(self):
        ''' 'Starts Export of selected leagues'''
        try:
            os.remove(os.path.join('tmp','')+'export')
        except:
            pass
        self.gui.expt_name = self.gui.line_export_name.text()
        rows = self.gui.table_leagues.rowCount()
        self.gui.progress_2.setValue(0)
        self.threads = []
        self.program_stop = 0
        for i in range(0, rows):
            if self.program_stop == 0:
                self.gui.name = self.gui.table_leagues.item(i, 0).text()
                self.gui.path = self.gui.table_leagues.item(i, 1).text()
                self.gui.r_min = self.gui.table_leagues.item(i, 2).text()
                self.gui.r_max = self.gui.table_leagues.item(i, 3).text()
                self.gui.mode = 1

                path = str(os.path.join('converted', self.gui.path, ''))
                self.gui.progress_2_val = float(i+1) / (rows)*100
                self.gui.progress_2_txt = self.gui.name
                cmd = (
                path,
                self.gui.name,
                self.gui.expt_name,
                int(self.gui.r_min),
                int(self.gui.r_max),
                self.gui.mode
                )
                self.gui.progress_2.setFormat('%p% '+self.gui.progress_2_txt)
                self.x = DoThread(cmd, self)
                self.x.start()
                while self.x.isRunning():
                    QtGui.QApplication.processEvents()
                self.gui.progress_2.setValue(self.gui.progress_2_val)
        export_fix = Database()
        export_fix.export_fix(self.gui.expt_name)

    def profile_save(self):
        ''' Saves profile of leagues to export'''
        f_name = self.gui.line_export.text()
        with open(os.path.join('profiles', '')+f_name, 'w') as f_save:
            rows = self.gui.table_leagues.rowCount()
            for i in range(0, rows):
                name = self.gui.table_leagues.item(i, 0).text()
                path = self.gui.table_leagues.item(i, 1).text()
                r_min = self.gui.table_leagues.item(i, 2).text()
                r_max = self.gui.table_leagues.item(i, 3).text()
                f_save.write(name+','+path+','+r_min+','+r_max+new_line)
            f_save.close()
            self.profiles_tree()

    def profile_load(self):
        ''' Loads profile into leagues table'''
        self.gui.table_leagues.clear()
        self.gui.table_leagues.setColumnCount(4)
        self.gui.table_leagues.setRowCount(0)
        child = self.gui.tree_profiles.currentItem()
        profile = child.text(0)
        with open (os.path.join('profiles', '')+profile, 'r') as f_load:
            for i in f_load:
                i = self.rm_lines(i)
                league, folder, r_min, r_max = i.split(',')
                rows =  self.gui.table_leagues.rowCount()+1
                self.gui.table_leagues.setRowCount(rows)
                self.gui.table_leagues.setItem(int(rows-1), 0, \
                                            QtGui.QTableWidgetItem(league))
                self.gui.table_leagues.setItem(int(rows-1), 1, \
                                            QtGui.QTableWidgetItem(folder))
                self.gui.table_leagues.setItem(int(rows-1), 2, \
                                            QtGui.QTableWidgetItem(r_min))
                self.gui.table_leagues.setItem(int(rows-1), 3, \
                                            QtGui.QTableWidgetItem(r_max))
            labels = [
                    'league',
                    'date',
                    'r_min',
                    'r_max']
            self.gui.table_leagues.setHorizontalHeaderLabels(labels)
            self.gui.table_leagues.resizeColumnsToContents()

    def profile_delete(self):
        ''' Delete selected profile'''
        path = os.path.join('profiles', '')
        item = self.gui.tree_profiles.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.profiles_tree()

    def rm_lines(self, item):
        ''' Removes new lines from string'''
        rem = item.replace('\n', '')
        rem = rem.replace('\r', '')
        rem = rem.replace(' ', '')
        return rem


if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = ExportApp()
    MYAPP.show()
    sys.exit(APP.exec_())
