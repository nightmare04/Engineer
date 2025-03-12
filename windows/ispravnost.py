from functools import partial

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog, QPushButton

from custom_widgets.buttons import PlaneBtn
from custom_widgets.groupboxs import PlaneGroupBox, UnitPlaneGroupBox
from custom_widgets.tables import IspravnostPlaneTableView
from database.models import *


class Ispravnost(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.unitLayout = QHBoxLayout()
        for unit in Unit.select().where(Unit.not_delete == True):
            unit_gb = UnitPlaneGroupBox(unit, fill_plane=True, parent=self)
            self.unitLayout.addWidget(unit_gb)
        self.mainLayout.addLayout(self.unitLayout)
        self.add_connect()

    def add_connect(self):
        planes_btn = self.findChildren(PlaneBtn)
        for btn in planes_btn:
            btn.clicked.connect(partial(IspravnostPlane, plane=btn.plane))


class IspravnostPlane(QDialog):
    def __init__(self, plane: Plane, parent=None):
        super().__init__(parent)
        self.resize(1024, 768)
        self.plane = plane
        self.setWindowTitle(f'Исправность самолета {plane.name}')
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.table = IspravnostPlaneTableView(plane)
        self.mainLayout.addWidget(self.table)

        self.btnLayout = QHBoxLayout()
        self.btnAdd = QPushButton("Добавить")
        self.btnOk = QPushButton("Ок")
        self.btnOk.clicked.connect(self.accept)
        self.btnLayout.addWidget(self.btnAdd)
        self.btnLayout.addWidget(self.btnOk)
        self.mainLayout.addLayout(self.btnLayout)

        self.exec()
