from functools import partial
from PyQt6 import QtWidgets, QtGui
from ui import Ui_MainWindow
from database.lc import create_tables, add_lc, ListControlModel
from database.models import ListControl
from windows.adds import AddType
from windows.lc import AddLC, ExecLC
from windows.lists import PlanesList, UnitList, TypesList, SpecList


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")
        self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page)
        self.fill_lc()
        self.ui.tableView.clicked.connect(self.exec_lc)
        self.ui.btn_add_lk.clicked.connect(self.add_lc_w)
        self.ui.btn_pki.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.pki_page))
        self.ui.btn_lk.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.lk_page))
        self.ui.btn_ispr.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.ispr_page))
        self.ui.btn_rekl.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.rekl_page))
        self.ui.planes_action.triggered.connect(lambda: PlanesList().exec())
        self.ui.units_action.triggered.connect(lambda: UnitList().exec())
        self.ui.type_plane_action.triggered.connect(lambda: TypesList().exec())
        self.ui.spec_action.triggered.connect(lambda: SpecList().exec())

    def fill_lc(self):
        model = ListControlModel(select=ListControl.select())
        self.ui.tableView.setModel(model)
        self.ui.tableView.hideColumn(6)

    def add_lc_w(self):
        lcw = AddLC()
        if lcw.exec():
            add_lc(lcw)
            self.fill_lc()

    def exec_lc(self, item):
        lc_id = item.siblingAtColumn(6).data()
        exlcw = ExecLC(lc_id)
        if exlcw.exec():
            self.fill_lc()
