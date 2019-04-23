#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
This is about finishing model UV and mapping an operation interface
"""
import sys
from PySide2 import QtWidgets
import BaseApi as base_api


class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Realign UV")
        self.resize(300, 100)
        self._base_api = base_api
        self.main_ui()

    def main_ui(self):
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.setFixedHeight(30)

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setFixedHeight(30)

        information_label = QtWidgets.QLabel('Please click the start button')

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(cancel_button)

        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addWidget(information_label)
        master_layout.addLayout(button_layout)

        self.setLayout(master_layout)

        self.start_button.clicked.connect(self.start_function)
        cancel_button.clicked.connect(self.close)

    def start_function(self):
        # Gets the processing status of the file.
        status = self._base_api.arrange_uv()

        if status:
            QtWidgets.QMessageBox.information(self,
                                              "That`s OK!",
                                              "The rearrangement has been completed, please go to check.",
                                              QtWidgets.QMessageBox.Yes)

            self.start_button.setEnabled(False)


if __name__ == '__main__':
    window = MainWindow()
    window.show()
