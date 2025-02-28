from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import QAbstractListModel, Qt
from database.models import Plane


class MyComboModel(QAbstractListModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query = query

    def rowCount(self, parent=...):
        return len(self._query)

    def updateData(self, query):
        self.beginResetModel()
        self._query = query
        self.endResetModel()

    def data(self, index, role=...):
        if not index.isValid():
            return

        if role == Qt.ItemDataRole.DisplayRole:
            return self._query[index.row()].name

        if role == Qt.ItemDataRole.UserRole:
            return self._query[index.row()].id


class PlaneFilterComboModel(MyComboModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rowCount(self, parent=...):
        return len(self._query) + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if index.row() == 0:
            if role == Qt.ItemDataRole.DisplayRole:
                return 'Все'

        if role == Qt.ItemDataRole.DisplayRole:
            return self._query[index.row() - 1].name

        if role == Qt.ItemDataRole.UserRole:
            return self._query[index.row() - 1].id


class MyComboBox(QComboBox):
    def __init__(self, query, parent=None):
        super().__init__(parent)
        self.model = MyComboModel(query)
        self.setModel(self.model)


class PlaneFilterComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)
        self.model = PlaneFilterComboModel(query)
        self.setModel(self.model)


class TypePlaneComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)


class UnitComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)


class RemZavComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)


class RemTypeComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)


class VypZavComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)


class SpecComboBox(MyComboBox):
    def __init__(self, query, parent=None):
        super().__init__(query, parent)