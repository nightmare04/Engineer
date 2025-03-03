from PyQt6.QtGui import QAction
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QMainWindow, QMenu, QHBoxLayout, QStackedWidget, QFrame, QMenuBar

from windows.lc import ListLC
from windows.leftdock import *
from windows.lists import Lists

from database.models import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1024, 768)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.setMenuBar(self.menubar)

        self.menu = QMenu("Настройки", parent=self.menubar)

        self.type_plane_menu = QAction("Типы самолетов", parent=self)
        self.type_plane_menu.triggered.connect(self.open_planeType)

        self.planes_menu = QAction("Самолеты", parent=self)
        self.planes_menu.triggered.connect(self.open_planes)

        self.spec_menu = QAction("Специальности", parent=self)
        self.spec_menu.triggered.connect(self.open_specs)

        self.units_menu = QAction("Подразделения", parent=self)
        self.units_menu.triggered.connect(self.open_units)

        self.osob_plane_menu = QAction("Особенности самолетов", parent=self)
        self.osob_plane_menu.triggered.connect(self.open_osobs)

        self.rem_zav_menu = QAction("Ремонтные заводы", parent=self)
        self.rem_zav_menu.triggered.connect(self.open_remZav)

        self.vypZav_menu = QAction("Заводы изготовители", parent=self)
        self.vypZav_menu.triggered.connect(self.open_vypZav)

        self.remType_menu = QAction("Типы ремонта", parent=self)
        self.remType_menu.triggered.connect(self.open_remType)


        self.menu.addAction(self.units_menu)
        self.menu.addAction(self.spec_menu)
        self.menu.addAction(self.type_plane_menu)
        self.menu.addAction(self.osob_plane_menu)
        self.menu.addAction(self.vypZav_menu)
        self.menu.addAction(self.rem_zav_menu)
        self.menu.addAction(self.remType_menu)
        self.menu.addAction(self.planes_menu)
        self.menubar.addAction(self.menu.menuAction())

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
        self.stack.addWidget(self.lcWidget)
        self.mainLayout.addWidget(self.stack)

        self.leftDock.btnLC.clicked.connect(lambda: self.stack.setCurrentWidget(self.lcWidget))

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