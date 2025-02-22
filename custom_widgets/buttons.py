from operator import truediv

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPalette, QBrush, QColor
from PyQt6.QtWidgets import QPushButton

from database import PlaneType
from database.models import Plane, Spec, Unit, ListControlExec


class PlaneBtn(QPushButton):
    def __init__(self, plane: Plane, lc=None, parent=None):
        self.plane = plane
        self.lc = lc
        super().__init__(self.plane.bort_num, parent)
        self.setFixedSize(QSize(40, 40))
        self.setCheckable(True)
        self.setAcceptDrops(True)
        if self.lc is not None:
            self.check_exec(lc)
        self.setStyleSheet("PlaneBtn{background-color: red;}"
                           "PlaneBtn:checked{background-color: green;}")

    def check_exec(self, lc):
        specs_for_exec = lc.spec_for_exec
        exec_specs = (ListControlExec
                      .select(ListControlExec.spec_id)
                      .where(ListControlExec.lc_id == lc.id,
                             ListControlExec.plane_id == self.plane.id).order_by(+ListControlExec.spec_id).tuples())
        spec_exec = []
        for row in exec_specs:
            spec_exec.append(row[0])

        if specs_for_exec == spec_exec:
            self.setStyleSheet("background-color: green")

        else:
            self.setStyleSheet("background-color: red")
        self.update()


class SpecBtn(QPushButton):
    def __init__(self, spec: Spec, lc=None):
        self.spec = spec
        super().__init__()
        self.setText(spec.name)
        self.lc = lc
        self.setFixedSize(QSize(80, 30))
        self.setCheckable(True)
        self.setStyleSheet("SpecBtn{background-color: red;}"
                           "SpecBtn:checked{background-color: green;}")


class UnitBtn(QPushButton):
    def __init__(self, unit: Unit, parent=None):
        self.unit = unit
        super().__init__(parent)
        self.setText(unit.name)


class TypeBtn(QPushButton):
    def __init__(self, type_plane: PlaneType, parent=None):
        self.type_plane = type_plane
        super().__init__(parent)
        self.setText(type_plane.type)
