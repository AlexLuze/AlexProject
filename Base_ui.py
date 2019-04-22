#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author  : Alex
@Time    : 2019/4/22 10:45
"""
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui, QtCore
import BaseApi as base_api

class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self._base_api = base_api
        self.setWindowTitle("Realign UV")
        self.resize(300, 100)
        self.main_ui()

    def main_ui(self):
        start_button = QtWidgets.QPushButton("Start")
        start_button.setFixedHeight(30)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setFixedHeight(30)
        information_label = QtWidgets.QLabel('Please click the start button')
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)
        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addWidget(information_label)
        master_layout.addLayout(button_layout)
        self.setLayout(master_layout)

        start_button.clicked.connect(self.start_function)
        cancel_button.clicked.connect(self.close)

    def start_function(self):
        status = self._base_api.arrange_uv()
        if status:
            QtWidgets.QMessageBox.information(self,
                "That`s OK!",
                "The rearrangement has been completed, please go to check.",
                QtWidgets.QMessageBox.Yes)

if __name__ == '__main__':
    window = MainWindow()
    window.show()
