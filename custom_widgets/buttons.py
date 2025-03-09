from operator import truediv

from PyQt6.QtCore import QSize, Qt, QMimeData
from PyQt6.QtGui import QPalette, QBrush, QColor, QDrag, QPixmap
from PyQt6.QtWidgets import QPushButton
from database.models import Plane, Spec, Unit, ListControlExec, PlaneType, OsobPlane, Agregate


class PlaneBtn(QPushButton):
    def __init__(self, plane: Plane, lc=None, parent=None):
        self.plane = plane
        self.lc = lc
        if len(PlaneType.select().where(PlaneType.not_delete == True)) > 1:
            name_btn = f'{self.plane.typeId.name}\n{self.plane.name}'
            super().__init__(name_btn, parent)
        else:
            super().__init__(self.plane.name, parent)
        self.setFixedSize(QSize(60, 40))
        self.setCheckable(True)
        if self.lc is not None:
            self.check_exec(lc)
        self.setStyleSheet("PlaneBtn{background-color: red;}"
                           "PlaneBtn:checked{background-color: green;}")

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)

    def check_ispr(self):
        if len(Agregate.select().where(self.plane.id == Agregate.planeId, Agregate.state > 1)) > 0:
            self.setStyleSheet("background-color: red")
        else:
            self.setStyleSheet("background-color: green")

    def check_exec(self, lc):
        specs_for_exec = lc.specs["to_exec"]
        exec_specs = (ListControlExec
                      .select(ListControlExec.specId)
                      .where(ListControlExec.lcId == lc.id,
                             ListControlExec.planeId == self.plane.id).order_by(+ListControlExec.specId).tuples())
        spec_exec = []
        if len(exec_specs) == 0:
            self.setStyleSheet("background-color: red")
            return

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
        self.setText(type_plane.name)


class OsobBtn(QPushButton):
    def __init__(self, osob_plane: OsobPlane, parent=None):
        super().__init__(parent)
        self.osob_plane = osob_plane
        self.setText(osob_plane.name)
        self.setCheckable(True)
        self.setStyleSheet("OsobBtn:checked{background-color: green;}")
