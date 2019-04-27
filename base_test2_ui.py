#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
This is the running window module of the plug-in,
mainly the interface module of interacting with artists.

There are three classes defined：
    Main window class: Window(): main operating interface.
    Export widget class: ExportWidget(): Export widget layout and related link functions.
    Import widget class: ImportWidget(): Import widget layout and related link functions.

There is a function defined：
    parent_window(): Call the parent class of Maya created in the mat_dev_api
                    for the parent window of the program's main window.
"""
import os
# sys.path.append(r'C:/Users/benja/Documents/maya/2018/scripts/base_test_2/')
from PySide2 import QtWidgets
from PySide2 import QtCore
from shiboken2 import wrapInstance
import material_lookdev_api as mat_dev_api
import xml_api

# Gets the current project workspace for Maya as a global variable for backup.
workspace = mat_dev_api.get_workspace()


def parent_window():
    """
    Call the parent class of Maya created in the mat_dev_api
    for the parent window of the program's main window.
    :return: QWidget controls
    :rtype: QtWidgets.QWidget
    """
    main_window = mat_dev_api.maya_main_window()

    return wrapInstance(long(main_window), QtWidgets.QWidget)


class Window(QtWidgets.QDialog):
    def __init__(self, parent=parent_window()):
        super(Window, self).__init__(parent)
        self.setWindowTitle('XML Window')
        self.resize(450, 150)

        # Call the child window control of the ExportWidget() class.
        self.export_widget = ExportWidget()

        # Call the child window control of the ImportWidget() class.
        self.import_widget = ImportWidget()
        self.main_ui()

    def main_ui(self):
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        main_splitter.setOpaqueResize(True)

        self.list_widget = QtWidgets.QListWidget(main_splitter)
        main_splitter.setStretchFactor(0, 2)
        self.list_widget.insertItem(0, u"Export")
        self.list_widget.insertItem(1, u"Import")

        frame = QtWidgets.QFrame(main_splitter)
        main_splitter.setStretchFactor(1, 8)
        
        self.stack = QtWidgets.QStackedWidget(frame)
        self.stack.addWidget(self.export_widget)
        self.stack.addWidget(self.import_widget)
        self.stack.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)

        right_layout = QtWidgets.QVBoxLayout(frame)
        right_layout.setSpacing(4)
        right_layout.addWidget(self.stack)

        lay = QtWidgets.QHBoxLayout(self)
        lay.addWidget(main_splitter)
        self.setLayout(lay)

        self.list_widget.itemPressed.connect(self.stack_change)

    def stack_change(self):
        """
        Click on the listWidgetItem to switch the current stack state.
        :return: None
        """
        index = self.list_widget.currentRow()
        self.stack.setCurrentIndex(index)


class ExportWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ExportWidget, self).__init__(parent)
        self.resize(300, 200)
        self._xml_api = xml_api
        self.main_ui()

    def main_ui(self):
        xml_name_label = QtWidgets.QLabel(u"XML File Name :  ")
        self.xml_name = QtWidgets.QLineEdit()
        self.xml_name.setMinimumWidth(200)

        xml_format_label = QtWidgets.QLabel(u".xml")

        export_label = QtWidgets.QLabel(u"XML Export Path:")

        self.xml_path = QtWidgets.QLineEdit()
        self.xml_path.setMinimumWidth(200)
        self.xml_path.setText(workspace)

        browse_button = QtWidgets.QPushButton(u" . . . ")

        export_button = QtWidgets.QPushButton(u"Export")
        export_button.setMaximumWidth(90)

        xml_name_layout = QtWidgets.QHBoxLayout()
        xml_name_layout.addWidget(xml_name_label)
        xml_name_layout.addWidget(self.xml_name)
        xml_name_layout.addWidget(xml_format_label)
        xml_name_layout.addSpacing(150)

        xml_path_layout = QtWidgets.QHBoxLayout()
        xml_path_layout.addWidget(export_label)
        xml_path_layout.addWidget(self.xml_path)
        xml_path_layout.addWidget(browse_button)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(export_button)
        button_layout.addStretch(1)

        total_layout = QtWidgets.QVBoxLayout()
        total_layout.addLayout(xml_name_layout)
        total_layout.addLayout(xml_path_layout)
        total_layout.addLayout(button_layout)

        self.setLayout(total_layout)

        browse_button.clicked.connect(self.save_file)
        export_button.clicked.connect(self.export_start)

    def save_file(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Save XML", workspace)
        self.xml_path.setText(file_path.replace("\\", "/"))

    def export_start(self):
        xml_name = self.xml_name.text()
        xml_full_name = '{}.xml'.format(xml_name)

        xml_path = self.xml_path.text()
        xml_full_path = os.path.join(xml_path, xml_full_name)

        if xml_name != "" and xml_path != "":
            result = self._xml_api.xml_write(xml_full_path)
            if result:
                self.xml_name.clear()
                QtWidgets.QMessageBox.information(self,
                                                  "Tip",
                                                  "Write complete, please note to view.",
                                                  QtWidgets.QMessageBox.Yes)

        else:
            QtWidgets.QMessageBox.information(self,
                                              "Tip",
                                              "Please fill in the file name and file path.",
                                              QtWidgets.QMessageBox.Yes)


class ImportWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImportWidget, self).__init__(parent)
        self.resize(300, 200)
        self._xml_api = xml_api
        self.main_ui()

    def main_ui(self):
        import_label = QtWidgets.QLabel(u"Choose XML Path:")
        self.xml_path = QtWidgets.QLineEdit()
        self.xml_path.setMinimumWidth(200)

        browse_button = QtWidgets.QPushButton(u" . . . ")

        import_button = QtWidgets.QPushButton(u"Import")
        import_button.setMaximumWidth(90)

        xml_path_layout = QtWidgets.QHBoxLayout()
        xml_path_layout.addWidget(import_label)
        xml_path_layout.addWidget(self.xml_path)
        xml_path_layout.addWidget(browse_button)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(import_button)
        button_layout.addStretch(1)

        total_layout = QtWidgets.QVBoxLayout()
        total_layout.addLayout(xml_path_layout)
        total_layout.addLayout(button_layout)

        self.setLayout(total_layout)

        browse_button.clicked.connect(self.open_file)
        import_button.clicked.connect(self.import_start)

    def open_file(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select XML", workspace, "XML Files(*.xml)")
        print file_path[0]
        self.xml_path.setText(file_path[0])

    def import_start(self):
        import_path = self.xml_path.text()
        if import_path == "":
            QtWidgets.QMessageBox.information(self,
                                              "Tip",
                                              "Please select the XML file first.",
                                              QtWidgets.QMessageBox.Yes)
        else:
            result = self._xml_api.xml_read(import_path)
            self.xml_path.clear()
            if result:
                QtWidgets.QMessageBox.information(self,
                                                  "Tip",
                                                  "Import completed, please note to view.",
                                                  QtWidgets.QMessageBox.Yes)


if __name__ == "__main__":
    win = Window()
    win.show()

