from PyQt6.QtWidgets import QGroupBox


class PlaneGroupBox (QGroupBox):
    def __init__(self, unit, checkable=False, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setTitle(unit.name)
        if checkable:
            self.setCheckable(True)
        self.setChecked(True)
