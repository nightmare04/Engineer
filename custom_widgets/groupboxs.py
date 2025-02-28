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

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        plane_btn = e.source()
        self.layout().removeWidget(plane_btn)

    def dropEvent(self, e):
        plane_btn = e.source()
        plane_btn.plane.unit = self.unit.id
        self.layout().addWidget(plane_btn)


class OsobGroupBox(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainlayout = QGridLayout()
        self.setLayout(self.mainlayout)
        self.osob_fill()

    def osob_fill(self):
        i = 0
        j = 0
        for osob in OsobPlane.select().where(OsobPlane.not_delete == True):
            i += 1
            btn_osob = OsobBtn(osob)
            self.mainlayout.addWidget(btn_osob, j, i)
            if i > 2:
                j += 1
                i = 0
