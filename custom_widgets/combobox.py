from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QAbstractListModel, Qt
from database.models import Plane


class PlaneComboModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = Plane.select().where(Plane.not_delete == True)

    def rowCount(self, parent=...):
        return len(self.query)

    def data(self, index, role=...):
        if not index.isValid():
            return

        if index.row() == 0:
            if role == Qt.ItemDataRole.DisplayRole:
                return 'Все'

        if role == Qt.ItemDataRole.DisplayRole:
            return self.query[index.row()-1].bort_num

        if role == Qt.ItemDataRole.UserRole:
            return self.query[index.row()-1].id


class PlaneComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = PlaneComboModel()
        self.setModel(self.model)
