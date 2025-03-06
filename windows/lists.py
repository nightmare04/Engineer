from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTableView

from custom_widgets.buttons import *
from custom_widgets.tables import *
from custom_widgets.combobox import *
from database.models import *
from windows.adds import *
from peewee import *
from functools import partial


class ListAll(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.btnLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.btnLayout)
        self.btnOk = QPushButton("Ок")
        self.btnOk.clicked.connect(self.accept)
        self.btnAdd = QPushButton("Добавить")
        self.btnAdd.clicked.connect(self.add)
        self.btnLayout.addWidget(self.btnOk)
        self.btnLayout.addWidget(self.btnAdd)


class UnitList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список подразделений")
        self.table = AllTableView(["", "Подразделения"], Unit)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = Unit.get_by_id(item.siblingAtColumn(0).data())
        AddUnit(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddUnit().exec()
        self.table.model.updateData()


class PlaneTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов самолетов")
        self.table = AllTableView(["", "Тип"], PlaneType)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = PlaneType.get_by_id(item.siblingAtColumn(0).data())
        AddPlaneType(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddPlaneType().exec()
        self.table.model.updateData()


class OsobList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список особенностей самолетов")
        self.table = OsobPlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = OsobPlane.get_by_id(item.siblingAtColumn(0).data())
        AddOsob(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddOsob().exec()
        self.table.model.updateData()


class ZavodIzg(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список заводов изготовителей")
        self.table = ZavodIzgTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = VypZav.get_by_id(item.siblingAtColumn(0).data())
        AddZavodIzg(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddZavodIzg().exec()
        self.table.model.updateData()