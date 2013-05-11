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
import subprocess
import platform
system = platform.system()

from PySide import QtCore, QtGui
from ui.learning import Ui_Learn
from bb_shared import Shared

class LearningApp(QtGui.QWidget, Shared):
    '''Creates gui form and events  '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        Shared.__init__(self)
        self.gui = Ui_Learn()
        self.gui.setupUi(self)
        self.bindings()
        self.exports_tree()
        self.nets_tree()

    def bindings(self):
        '''Bindings for app widgets.
         QtCore.QObject.connect(widget,QtCore.SIGNAL("clicked()"),command)
         or  widget.event.connect(function)'''
        self.gui.button_learn.clicked.connect(self.learn_process)
        self.gui.tree_exports.clicked.connect(self.set_name)
        self.gui.button_delete.clicked.connect(self.nets_delete)
        self.gui.button_exp_delete.clicked.connect(self.exports_delete)

    def learn_process(self):
        ''' Start Learning calls learny.py with args'''
        item = self.gui.tree_exports.currentItem()
        file_in = item.text(0)
        file_out = self.gui.line_learn.text()
        hidden = self.gui.spin_hidden.value()
        error = self.gui.spin_error.value()
        epochs = self.gui.spin_epochs.value()
        rate = self.gui.spin_rate.value()
        reports = self.gui.spin_reports.value()
        algorithm = self.gui.combo_algorithm.currentText()
        hidden_func = self.gui.combo_hidden.currentText()
        output_func = self.gui.combo_output.currentText()
        if system == 'Linux':
            args =  ['-u',
                     'learn.py',
                     str(file_in),
                     str(rate),
                     str(hidden),
                     str(error),
                     str(epochs),
                     str(reports),
                     str(output_func),
                     str(hidden_func),
                     str(algorithm),
                     str(file_out)]
            self.processes = []
            path = os.getcwd()
            self.proc = QtCore.QProcess()
            self.proc.setWorkingDirectory(path)
            self.proc.readyReadStandardOutput.connect(self.on_out)
            self.proc.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            self.processes.append(self.proc)
            self.proc.start('python', args)
            self.proc.finished.connect(self.finished)

        elif system == 'Windows':
            args =  [sys.executable,
                     '-u',
                    'learn.py',
                     str(file_in),
                     str(rate),
                     str(hidden),
                     str(error),
                     str(epochs),
                     str(reports),
                     str(output_func),
                     str(hidden_func),
                     str(algorithm),
                     str(file_out)]
            proc = subprocess.Popen(args,stderr=subprocess.STDOUT)
            self.gui.text_learning.append('Change window to python.exe for realtime output')

    def on_out(self):
        ''' Print stdout to textbox'''
        text = str(
            (self.proc.readAllStandardOutput())).strip('\n')
        text = text.replace('Epochs    ','Epochs')
        self.gui.text_learning.append(text)

    def finished(self):
        ''' When learning finished'''
        self.nets_tree()
        self.proc

    def exports_tree(self):
        ''' Fills tree with available csv files'''
        self.gui.tree_exports.clear()
        self.gui.tree_exports.sortItems(0, QtCore.Qt.SortOrder(0))
        self.gui.tree_exports.setSortingEnabled(1)
        self.gui.tree_exports.headerItem().setText(0, ('Exports'))
        dir_exports = os.listdir(os.path.join('export'))
        for i in dir_exports:
            item_exp = QtGui.QTreeWidgetItem(self.gui.tree_exports)
            item_exp.setText(0, (i))

    def set_name(self):
        ''' Sets name for net , adds .net to export file name'''
        item = self.gui.tree_exports.currentItem()
        text = item.text(0)+'.net'
        self.gui.line_learn.setText(text)

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

    def nets_delete(self):
        ''' Deletes net'''
        path = os.path.join('net','')
        item = self.gui.tree_nets.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.nets_tree()

    def exports_delete(self):
        ''' Deletes export'''
        path = os.path.join('export','')
        item = self.gui.tree_exports.currentItem()
        file_delete = item.text(0)
        self.delete_file(file_delete, path)
        self.exports_tree()
if __name__ == "__main__":
    APP = QtGui.QApplication(sys.argv)
    MYAPP = LearningApp()
    MYAPP.show()
    sys.exit(APP.exec_())


