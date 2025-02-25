from functools import partial
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt
from PyQt6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox

from custom_widgets.tables import LCTableView
from custom_widgets.combobox import PlaneComboBox
from ui import Ui_MainWindow
from database.lc import create_tables, add_lc
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
        self.lc_table = LCTableView()
        self.ui.lk_page.setLayout(QVBoxLayout())
        self.ui.lk_page.layout().addWidget(self.lc_table)

        self.filter_layout = QHBoxLayout()
        self.btn_filter_ex = QPushButton("Только не &выполненные")
        self.btn_filter_ex.setCheckable(True)
        self.btn_filter_ex.clicked.connect(lambda: self.set_filter_by_btn(1, self.btn_filter_ex))

        self.btn_filter_de = QPushButton("Только &просроченные")
        self.btn_filter_de.setCheckable(True)
        self.btn_filter_de.clicked.connect(lambda: self.set_filter_by_btn(2, self.btn_filter_de))

        self.plane_combo = PlaneComboBox()
        self.plane_combo.currentIndexChanged.connect(lambda index: self.set_filter_by_combo(index))
        self.filter_layout.addWidget(self.btn_filter_ex)
        self.filter_layout.addWidget(self.btn_filter_de)
        self.filter_layout.addWidget(self.plane_combo)
        self.ui.lk_page.layout().addLayout(self.filter_layout)

        self.btn_layout = QHBoxLayout()
        self.btn_add_lc = QPushButton("Добавить")
        self.btn_layout.addWidget(self.btn_add_lc)
        self.ui.lk_page.layout().addLayout(self.btn_layout)

        self.lc_table.doubleClicked.connect(self.exec_lc)
        self.btn_add_lc.clicked.connect(self.add_lc_w)
        self.ui.btn_pki.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.pki_page))
        self.ui.btn_lk.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.lk_page))
        self.ui.btn_ispr.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.ispr_page))
        self.ui.btn_rekl.clicked.connect(partial(self.ui.stackedWidget.setCurrentWidget, self.ui.rekl_page))
        self.ui.planes_action.triggered.connect(lambda: PlanesList().exec())
        self.ui.units_action.triggered.connect(lambda: UnitList().exec())
        self.ui.type_plane_action.triggered.connect(lambda: TypesList().exec())
        self.ui.spec_action.triggered.connect(lambda: SpecList().exec())

    def set_filter_by_combo(self, index):
        data = self.plane_combo.itemData(index, role=Qt.ItemDataRole.DisplayRole)
        self.set_filter(data, 5)

    def set_filter_by_btn(self, case, btn):
        if case == 1 and btn.isChecked():
            self.set_filter("Не выполнено на ВС", 5)
            return
        if case == 2 and btn.isChecked():
            self.set_filter('Просрочен', 3)
            return
        if not btn.isChecked():
            self.set_filter('', 0)
            return


    def set_filter(self, data, col):
        if data == "Все":
            self.lc_table.proxy_model.setFilterRegularExpression('')
        else:
            self.lc_table.proxy_model.setFilterRegularExpression(data)
            self.lc_table.proxy_model.setFilterKeyColumn(col)


    def fill_lc(self):
        pass

    def add_lc_w(self):
        lcw = AddLC()
        if lcw.exec():
            add_lc(lcw)
            self.lc_table.model.updateData(ListControl.select())

    def exec_lc(self, item):
        lc_id = item.siblingAtColumn(6).data()
        exlcw = ExecLC(lc_id)
        if exlcw.exec():
            self.lc_table.model.updateData(ListControl.select())
