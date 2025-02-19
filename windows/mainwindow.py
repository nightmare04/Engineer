from functools import partial
from PyQt6 import QtWidgets, QtGui
from ui import Ui_MainWindow
from database.lc import create_tables, fill_lc, add_lc
from windows.lc import AddLC
from windows.lists import PlanesList, UnitList


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")
        self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page)
        fill_lc(self.ui.tableView)
        self.ui.btn_add_lk.clicked.connect(self.add_lc_w)
        self.ui.btn_pki.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.pki_page))
        self.ui.btn_lk.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.lk_page))
        self.ui.btn_ispr.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.ispr_page))
        self.ui.btn_rekl.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.rekl_page))
        self.ui.planes_action.triggered.connect(lambda: PlanesList().exec())
        self.ui.units_action.triggered.connect(lambda: UnitList().exec())

    def add_lc_w(self):
        lcw = AddLC()
        if lcw.exec():
            add_lc(lcw)
        fill_lc(self.ui.tableView)
