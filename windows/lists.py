from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTableView

from custom_widgets.buttons import UnitBtn, PlaneBtn, TypeBtn, SpecBtn
from custom_widgets.tables import PlaneTableView, PlaneTypeTableView, UnitTableView, OsobTableView, SpecTableView
from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox
from database.models import Plane, Unit, PlaneType, Spec, OsobPlane
from windows.adds import AddPlane, AddUnit, AddType, AddSpec, AddOsob
from peewee import *
from functools import partial


class Lists(QDialog):
    def __init__(self, title, table, basemodel, form, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.setWindowTitle(title)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.table = table()
        self.table.doubleClicked.connect(self.edit)
        self.basemodel = basemodel
        self.query = basemodel.select().where(basemodel.not_delete == True)
        self.addForm = form
        self.mainlayout.addWidget(self.table)
        self.btnlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.btnlayout)
        self.btn_ok = QPushButton("Ок")
        self.btn_add = QPushButton("Добавить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_add)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add.clicked.connect(self.add)

    def add(self):
        if self.addForm().exec():
            self.table.model.updateData(self.query)

    def edit(self, item):
        edit_item = self.basemodel.get_by_id(item.siblingAtColumn(1).data())
        if self.addForm(edit_item).exec():
            self.table.model.updateData(self.query)

class OsobList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Особенности")
        self.table = OsobTableView()
        self.table.doubleClicked.connect(self.edit)
        self.mainlayout.insertWidget(0, self.table)
        self.query = OsobPlane.select().where(OsobPlane.not_delete == True)

    def add(self):
        if AddOsob().exec():
            self.table.model.updateData(self.query)

    def edit(self, item):
        osob = OsobPlane.get_by_id(item.siblingAtColumn(2).data())
        if AddOsob(osob=osob).exec():
            self.table.model.updateData(self.query)