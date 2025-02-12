from operator import truediv

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton
from database.database import Plane, Spec


class PlaneBtn(QPushButton):
    def __init__(self, plane: str, parent=None):
        self.plane = Plane.get(Plane.bort_num == plane)
        super().__init__(self.plane.bort_num, parent)
        self.setFixedSize(QSize(40, 40))
        self.setCheckable(True)
        self.setAcceptDrops(True)


class SpecBtn(QPushButton):
    def __init__(self, spec: str, parent=None):
        self.spec = Spec.get(Spec.name == spec)
        super().__init__(self.spec.name, parent)
        self.spec_name = self.spec.name
        self.setFixedSize(QSize(80, 30))
        self.setCheckable(True)
