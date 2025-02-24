from PyQt6.QtWidgets import QGroupBox
from database.models import Unit


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




