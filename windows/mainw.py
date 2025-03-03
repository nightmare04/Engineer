from PyQt6.QtGui import QAction
from PyQt6.QtCore import QRect
from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtWidgets import QWidget, QMainWindow, QMenu, QHBoxLayout, QStackedWidget, QFrame, QMenuBar

from windows.lc import ListLC
from windows.leftdock import *
from windows.lists import Lists, PlaneTableView
from windows.adds import AddPlane
from windows.ispravnost import *
from database.models import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1024, 768)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.setMenuBar(self.menubar)

        self.settings_menu = QMenu("Настройки", parent=self.menubar)

        self.plane_menu = QMenu("Самолеты")

        self.unit_menu = QMenu("Подразделения")

        self.agregate_menu = QMenu("Блоки/Агрегаты")

        self.type_plane_menu = QAction("Типы самолетов", parent=self)
        self.type_plane_menu.triggered.connect(self.open_planeType)
        self.plane_menu.addAction(self.type_plane_menu)

        self.osob_plane_menu = QAction("Особенности самолетов", parent=self)
        self.osob_plane_menu.triggered.connect(self.open_osobs)
        self.plane_menu.addAction(self.osob_plane_menu)

        self.vypZav_menu = QAction("Заводы изготовители", parent=self)
        self.vypZav_menu.triggered.connect(self.open_vypZav)
        self.plane_menu.addAction(self.vypZav_menu)

        self.rem_zav_menu = QAction("Ремонтные заводы", parent=self)
        self.rem_zav_menu.triggered.connect(self.open_remZav)
        self.plane_menu.addAction(self.rem_zav_menu)

        self.remType_menu = QAction("Типы ремонта", parent=self)
        self.remType_menu.triggered.connect(self.open_remType)
        self.plane_menu.addAction(self.remType_menu)

        self.planes_menu = QAction("Список самолетов", parent=self)
        self.planes_menu.triggered.connect(self.open_planes)
        self.plane_menu.addAction(self.planes_menu)

        self.units_menu = QAction("Подразделения", parent=self)
        self.units_menu.triggered.connect(self.open_units)
        self.unit_menu.addAction(self.units_menu)

        self.spec_menu = QAction("Специальности", parent=self)
        self.spec_menu.triggered.connect(self.open_specs)
        self.unit_menu.addAction(self.spec_menu)

        QSqlTableModel

        self.system_menu = QAction("Системы", parent=self)
        self.system_menu.triggered.connect(self.open_systems)
        self.agregate_menu.addAction(self.system_menu)

        self.agregates_menu = QAction("Блоки/Агрегаты", parent=self)
        self.system_menu.triggered.connect(self.open_agregates)
        self.agregate_menu.addAction(self.agregates_menu)


        self.settings_menu.addAction(self.plane_menu.menuAction())
        self.settings_menu.addAction(self.unit_menu.menuAction())
        self.settings_menu.addAction(self.agregate_menu.menuAction())
        self.menubar.addAction(self.settings_menu.menuAction())

        self.centralWidget = QWidget(self)
        self.mainLayout = QHBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)

        self.leftDock = LeftDock(self)
        self.mainLayout.addWidget(self.leftDock)

        self.line = QFrame(parent=self.centralWidget)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mainLayout.addWidget(self.line)

        self.stack = QStackedWidget()
        self.lcWidget = ListLC()
        self.ispravnost = Ispravnost()
        self.stack.addWidget(self.lcWidget)
        self.stack.addWidget(self.ispravnost)
        self.mainLayout.addWidget(self.stack)

        self.leftDock.btnLC.clicked.connect(lambda: self.stack.setCurrentWidget(self.lcWidget))
        self.leftDock.btnIspr.clicked.connect(lambda: self.stack.setCurrentWidget(self.ispravnost))

    def open_systems(self):
        pass

    def open_agregates(self):
        pass

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
        self.lcWidget.filterPlaneCombo.model.updateData(Plane.select().where(Plane.not_delete == True))

    @staticmethod
    def open_remZav():
        Lists(title="Заводы изготовители", basemodel=RemZav, header=["Завод", ""], table=None).exec()

    @staticmethod
    def open_remType():
        Lists(title="Тип ремонта", basemodel=RemType, header=["Наименование", ""], table=None).exec()