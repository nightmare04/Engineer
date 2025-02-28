from PyQt6.QtWidgets import QGroupBox, QGridLayout
from database.models import Unit, OsobPlane
from custom_widgets.buttons import OsobBtn


class PlaneGroupBox (QGroupBox):
    def __init__(self, unit: Unit, checkable=False, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setTitle(unit.name)
        if checkable:
            self.setCheckable(True)
        self.setChecked(True)
        self.setAcceptDrops(True)

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
