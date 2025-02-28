from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTableView

from custom_widgets.buttons import UnitBtn, PlaneBtn, TypeBtn, SpecBtn
from custom_widgets.tables import AllTableView, PlaneTableView
from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox
from database.models import Plane, Unit, PlaneType, Spec, OsobPlane
from windows.adds import AddPlane, AddOsob, AddAll
from peewee import *
from functools import partial


class Lists(QDialog):
    def __init__(self, title, basemodel, header=None, table=None, add_form=AddAll, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        if basemodel == Plane:
            self.resize(1100, 500)
        self.setWindowTitle(title)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        if table is None:
            self.table = AllTableView(header, basemodel)
        else:
            self.table = table(header, basemodel)
        self.table.doubleClicked.connect(self.edit)
        self.basemodel = basemodel
        self.query = basemodel.select().where(basemodel.not_delete == True)
        self.addForm = add_form(basemodel)
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
        self.addForm.exec()
        self.table.model.updateData(self.query)

    def edit(self, item):
        if self.basemodel == Plane:
            edit_item = self.basemodel.get_by_id(item.siblingAtColumn(10).data())
            AddPlane(self.basemodel, edit_item).exec()
        else:
            edit_item = self.basemodel.get_by_id(item.siblingAtColumn(1).data())
            AddAll(self.basemodel, edit_item).exec()
        self.table.model.updateData(Plane.select().where(Plane.not_delete == True))
