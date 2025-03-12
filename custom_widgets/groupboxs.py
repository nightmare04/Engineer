from PyQt6.QtWidgets import QGroupBox, QGridLayout
from database.models import Unit, OsobPlane, Plane
from custom_widgets.buttons import OsobBtn, PlaneBtn


class UnitPlaneGroupBox (QGroupBox):
    def __init__(self, unit: Unit, fill_plane=False, checkable=False, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setTitle(unit.name)
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        if checkable:
            self.setCheckable(True)
            self.setChecked(True)
        if fill_plane:
            self.fill_plane()
        self.setAcceptDrops(True)

    def fill_plane(self):
        i = 0
        j = 0
        for plane in Plane.select().where(Plane.not_delete == True, Plane.unit == self.unit.id):
            plane_btn = PlaneBtn(plane)
            plane_btn.check_ispr()
            self.mainLayout.addWidget(plane_btn, i, j)
            i += 1
            if i > 3:
                i = 0
                j += 1


class PlaneGroupBox (QGroupBox):
    def __init__(self, unit: Unit, checkable=False, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setTitle(unit.name)
        if checkable:
            self.setCheckable(True)
        self.setChecked(True)
        self.setAcceptDrops(True)


class OsobGroupBox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)