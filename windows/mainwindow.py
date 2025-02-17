import datetime
from functools import partial

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QGroupBox

from custom_widgets import PlaneGroupBox, PlaneBtn, SpecBtn
from database.models import *
from database.lc import *
from ui import Ui_MainWindow
import windows.lc
from windows.lc import EditLC, AddLC, ExecLC


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")
        self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page)
        fill_lc(self.ui.tableView)
        self.ui.btn_add_lk.clicked.connect(self.add_lc)
        self.ui.btn_pki.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.pki_page))
        self.ui.btn_lk.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.lk_page))
        self.ui.btn_ispr.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.ispr_page))
        self.ui.btn_rekl.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.rekl_page))

    def add_lc(self):
        lcw = AddLC()
        if lcw.exec():
            add_lc(lcw)
        fill_lc(self.ui.tableView)





