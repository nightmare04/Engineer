from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QTableView

from custom_widgets.buttons import UnitBtn, PlaneBtn, TypeBtn, SpecBtn
from custom_widgets.tables import PlaneTableView, PlaneTypeTableView, UnitTableView, OsobTableView
from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox
from database.models import Plane, Unit, PlaneType, Spec, OsobPlane
from windows.adds import AddPlane, AddUnit, AddType, AddSpec, AddOsob
from peewee import *
from functools import partial


class Lists(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.btnlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.btnlayout)
        self.btn_ok = QPushButton("Ок")
        self.btn_add = QPushButton("Добавить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_add)
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add.clicked.connect(self.add)

    def add(self):
        pass


class PlanesList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = Plane.select().where(Plane.not_delete == True)
        self.setWindowTitle("Самолеты")
        self.table = PlaneTableView()
        self.mainlayout.insertWidget(0, self.table)
        self.table.setSortingEnabled(False)
        self.table.sortByColumn(1, Qt.SortOrder.AscendingOrder)

    def edit(self, plane: Plane):
        if AddPlane(plane).exec():
            self.table.model.updateData(self.query)

    def add(self):
        if AddPlane().exec():
            self.table.model.updateData(self.query)


class UnitList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.table = UnitTableView()
        self.mainlayout.insertWidget(0, self.table)

    def add(self):
        unitadd = AddUnit()
        if unitadd.exec():
            self.table.model.updateData(Unit.select().where(Unit.not_delete == True))

    def edit(self, unit: Unit):
        unitedit = AddUnit(unit)
        if unitedit.exec():
            self.table.model.updateData(Unit.select().where(Unit.not_delete == True))


class TypesList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.table = PlaneTypeTableView()
        self.mainlayout.insertWidget(0, self.table)
        self.query = PlaneType.select().where(PlaneType.not_delete == True)

    def edit(self, type_plane: PlaneType):
        plane_type_w = AddType(type_plane)
        if plane_type_w.exec():
            self.table.model.updateData(query=self.query)

    def add(self):
        plane_type_w = AddType()
        plane_type_w.setWindowTitle("Добавить тип")
        if AddType().exec():
            self.table.model.updateData(query=self.query)


class SpecList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Специалтьности")
        self.table =
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Наименование", ""])
        self.table.resizeColumnsToContents()
        self.fill()

    def fill(self):
        specs = Spec.select().where(Spec.not_delete == True)
        row_count = specs.count()
        self.table.setRowCount(row_count)
        i, count = 0, row_count
        while i < count:
            for spec in specs:
                if not spec.not_delete:
                    continue
                spec_btn = SpecBtn(spec)
                spec_btn.setStyleSheet(QPushButton().styleSheet())
                spec_btn.setFixedSize(QSize(100, 30))
                spec_btn.setText("Изменить")
                spec_btn.clicked.connect(partial(self.edit, spec_btn.spec))
                self.table.setItem(i, 0, QTableWidgetItem(spec.name))
                self.table.setCellWidget(i, 1, spec_btn)
                i += 1

    def add(self):
        specadd_w = AddSpec()
        if specadd_w.exec():
            self.fill()

    def edit(self, spec: Spec):
        specadd_w = AddSpec(spec)
        if specadd_w.exec():
            self.fill()


class OsobList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Особенности")
        self.table = OsobTableView()
        self.table.doubleClicked.connect(self.edit)
        self.mainlayout.insertWidget(0, self.table)

    def add(self):
        if AddOsob().exec():
            self.table.model.updateData(OsobPlane.select().where(OsobPlane.not_delete == True))

    def edit(self, item):
        osob = OsobPlane.get_by_id(item.siblingAtColumn(2).data())
        if AddOsob(osob=osob).exec():
            self.table.model.updateData(OsobPlane.select().where(OsobPlane.not_delete == True))