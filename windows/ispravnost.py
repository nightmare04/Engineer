from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog

from custom_widgets.buttons import PlaneBtn
from custom_widgets.groupboxs import UnitPlaneGroupBox
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
