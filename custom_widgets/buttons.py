from operator import truediv

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton
from database.models import Plane, Spec, Unit


class PlaneBtn(QPushButton):
    def __init__(self, plane: Plane, parent=None):
        self.plane = plane
        super().__init__(self.plane.bort_num, parent)
        self.setFixedSize(QSize(40, 40))
        self.setCheckable(True)
        self.setAcceptDrops(True)


class SpecBtn(QPushButton):
    def __init__(self, spec: Spec, lc=None):
        self.spec = spec
        super().__init__()
        self.setText(spec.name)
        self.lc = lc
        self.setFixedSize(QSize(80, 30))
        self.setCheckable(True)


class UnitBtn(QPushButton):
    def __init__(self, unit: Unit, parent=None):
        self.unit = unit
        super().__init__(parent)
        self.setText(unit.name)

