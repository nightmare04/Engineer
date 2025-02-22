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
