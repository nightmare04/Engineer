from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTableView

from custom_widgets.buttons import UnitBtn, PlaneBtn, TypeBtn, SpecBtn
from custom_widgets.tables import AllTableView, PlaneTableView, OsobPlaneTableView
from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox
from database.models import *
from windows.adds import AddPlane, AddOsob, AddUnit, AddPlaneType
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

# class Lists(QDialog):
#     def __init__(self, title, basemodel, header=None, table=None, add_form=AddAll, parent=None):
#         super().__init__(parent)
#         self.resize(500, 500)
#         if basemodel == Plane:
#             self.resize(1100, 500)
#         self.setWindowTitle(title)
#         self.mainlayout = QVBoxLayout(self)
#         self.setLayout(self.mainlayout)
#         if table is None:
#             self.table = AllTableView(header, basemodel)
#         else:
#             self.table = table(header, basemodel)
#         self.table.doubleClicked.connect(self.edit)
#         self.basemodel = basemodel
#         self.query = basemodel.select().where(basemodel.not_delete == True)
#         self.addForm = add_form(basemodel)
#         self.mainlayout.addWidget(self.table)
#         self.btnlayout = QHBoxLayout()
#         self.mainlayout.addLayout(self.btnlayout)
#         self.btn_ok = QPushButton("Ок")
#         self.btn_add = QPushButton("Добавить")
#         self.btnlayout.addWidget(self.btn_ok)
#         self.btnlayout.addWidget(self.btn_add)
#         self.btn_ok.clicked.connect(self.accept)
#         self.btn_add.clicked.connect(self.add)
#
#     def add(self):
#         self.addForm.exec()
#         self.table.model.updateData(self.query)
#
#     def edit(self, item):
#         if self.basemodel == Plane:
#             edit_item = self.basemodel.get_by_id(item.siblingAtColumn(10).data())
#             AddPlane(self.basemodel, edit_item).exec()
#         else:
#             edit_item = self.basemodel.get_by_id(item.siblingAtColumn(1).data())
#             AddAll(self.basemodel, edit_item).exec()
#         self.table.model.updateData()
