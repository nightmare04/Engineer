from functools import partial
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSortFilterProxyModel, QRegularExpression, Qt
from PyQt6.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QStackedWidget

from custom_widgets.tables import LCTableView, PlaneTableView
from custom_widgets.combobox import PlaneFilterComboBox
from ui import Ui_MainWindow
from database.lc import create_tables, add_lc
from database.models import ListControl, Plane, PlaneType, Unit, Spec, OsobPlane, VypZav, RemZav, RemType
from windows.adds import AddPlane, AddOsob, AddAll
from windows.lc import AddLC, ExecLC
from windows.lists import Lists
from windows import lc


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")

        self.stack = QStackedWidget(self)
        self.lc = lc.MainLC()
        self.stack.addWidget(self.lc)
        self.ui.horizontalLayout.addWidget(self.stack)

        self.ui.horizontalLayout.setStretch(0, 1)
        self.ui.horizontalLayout.setStretch(2, 4)

        self.ui.btn_pki.clicked.connect(partial(self.stack.setCurrentWidget, self.lc))
        # self.ui.btn_lk.clicked.connect(partial(self.stack.setCurrentWidget, self.ui.lk_page))
        # self.ui.btn_rekl.clicked.connect(partial(self.stack.setCurrentWidget, self.ui.rekl_page))
        # self.ui.btn_ispr.clicked.connect(partial(self.stack.setCurrentWidget, self.ui.ispr_page))

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

    @staticmethod
    def open_units():
        Lists(title="Подразделения", basemodel=Unit, header=["Подразделение", ""], table=None).exec()

    @staticmethod
    def open_planeType():
        Lists(title="Типы самолетов", basemodel=PlaneType, header=["Тип", ""], table=None).exec()

    @staticmethod
    def open_osobs():
        Lists(title="Особенности", header=["Особенность", ""], basemodel=OsobPlane, add_form=AddOsob).exec()

    @staticmethod
    def open_vypZav():
        Lists(title="Заводы изготовители", basemodel=VypZav, header=["Завод", ""], table=None).exec()

    @staticmethod
    def open_specs():
        Lists(title="Специальности", basemodel=Spec, header=["Специальность", ""], table=None).exec()

    def open_planes(self):
        Lists("Самолеты", basemodel=Plane, add_form=AddPlane, table=PlaneTableView).exec()
        self.plane_combo.model.updateData(Plane.select().where(Plane.not_delete == True))

    @staticmethod
    def open_remZav():
        Lists(title="Заводы изготовители", basemodel=RemZav, header=["Завод", ""], table=None).exec()

    @staticmethod
    def open_remType():
        Lists(title="Тип ремонта", basemodel=RemType, header=["Наименование", ""], table=None).exec()
