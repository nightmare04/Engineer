from functools import partial
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt
from PyQt6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox

from custom_widgets.tables import LCTableView, PlaneTableView
from custom_widgets.combobox import PlaneFilterComboBox
from ui import Ui_MainWindow
from database.lc import create_tables, add_lc
from database.models import ListControl, Plane, PlaneType, Unit, Spec, OsobPlane, VypZav, RemZav, RemType
from windows.adds import AddPlane, AddOsob, AddAll
from windows.lc import AddLC, ExecLC
from windows.lists import Lists


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")

        self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page)
        self.lc_table = LCTableView()
        self.ui.lk_page.layout().addWidget(self.lc_table)

        self.filter_layout = QHBoxLayout()
        self.btn_filter_ex = QPushButton("Только не &выполненные")
        self.btn_filter_ex.setCheckable(True)
        self.btn_filter_ex.clicked.connect(lambda: self.set_filter_by_btn(1, self.btn_filter_ex))

        self.btn_filter_de = QPushButton("Только &просроченные")
        self.btn_filter_de.setCheckable(True)
        self.btn_filter_de.clicked.connect(lambda: self.set_filter_by_btn(2, self.btn_filter_de))

        self.plane_combo = PlaneFilterComboBox(Plane.select().where(Plane.not_delete == True))
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
        self.connect_signals()

    def connect_signals(self):
        self.ui.planes_action.triggered.connect(self.open_planes)
        self.ui.units_action.triggered.connect(self.open_units)
        self.ui.type_plane_action.triggered.connect(self.open_planeType)
        self.ui.spec_action.triggered.connect(self.open_specs)
        self.ui.osob_plane_action.triggered.connect(self.open_osobs)
        self.ui.vypZav_action.triggered.connect(self.open_vypZav)
        self.ui.rem_zav_action.triggered.connect(self.open_remZav)
        self.ui.remType_action.triggered.connect(self.open_remType)

    def open_units(self):
        Lists(title="Подразделения", basemodel=Unit, header=["Подразделение", ""], table=None).exec()

    def open_planeType(self):
        Lists(title="Типы самолетов", basemodel=PlaneType, header=["Тип", ""], table=None).exec()

    def open_osobs(self):
        Lists(title="Особенности", header=["Особенность", ""], basemodel=OsobPlane, add_form=AddOsob).exec()

    def open_vypZav(self):
        Lists(title="Заводы изготовители", basemodel=VypZav, header=["Завод", ""], table=None).exec()

    def open_specs(self):
        Lists(title="Специальности", basemodel=Spec, header=["Специальность", ""], table=None).exec()

    def open_planes(self):
        Lists("Самолеты", basemodel=Plane, add_form=AddPlane, table=PlaneTableView).exec()
        self.plane_combo.model.updateData(Plane.select().where(Plane.not_delete == True))

    def open_remZav(self):
        Lists(title="Заводы изготовители", basemodel=RemZav, header=["Завод", ""], table=None).exec()

    def open_remType(self):
        Lists(title="Тип ремонта", basemodel=RemType, header=["Наименование", ""], table=None).exec()

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
