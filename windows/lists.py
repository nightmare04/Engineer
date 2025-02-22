from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

from custom_widgets import UnitBtn, PlaneBtn, TypeBtn, SpecBtn
from database.models import Plane, Unit, PlaneType, Spec
from windows.adds import AddPlane, AddUnit, AddType, AddSpec
from peewee import *
from functools import partial


class Lists(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.table = QTableWidget()
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
        pass


class PlanesList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Тип", "Подразделение", "Бортовой номер", "Заводской номер", ""])
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        self.table.setSortingEnabled(False)
        self.table.sortByColumn(1, Qt.SortOrder.AscendingOrder)
        self.fill()

    def fill(self):
        planes = Plane.select().where(Plane.not_deleted == True)
        row_count = planes.count()
        self.table.setRowCount(row_count)
        i = 0
        for plane in planes:
            if not plane.not_delete:
                continue
            plane_btn = PlaneBtn(plane)
            plane_btn.clicked.connect(partial(self.edit, plane_btn.plane))
            plane_btn.setText("Изменить")
            plane_btn.setCheckable(False)
            plane_btn.setFixedSize(QSize(100, 30))
            self.table.setItem(i, 0, QTableWidgetItem(str(plane.type.type)))
            self.table.setItem(i, 1, QTableWidgetItem(str(plane.unit.name)))
            self.table.setItem(i, 2, QTableWidgetItem(str(plane.bort_num)))
            self.table.setItem(i, 3, QTableWidgetItem(str(plane.zav_num)))
            self.table.setCellWidget(i, 4, plane_btn)
            i += 1

    def edit(self, plane: Plane):
        plane_w = AddPlane(plane)
        if plane_w.exec():
            self.fill()

    def add(self):
        if AddPlane().exec():
            self.fill()


class UnitList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Наименование", ""])
        self.table.resizeColumnsToContents()
        self.btn_add.clicked.connect(self.add)
        self.fill()

    def fill(self):
        units = Unit.select().where(Unit.not_deleted == True)
        row_count = units.count()
        self.table.setRowCount(row_count)
        i, count = 0, row_count
        while i < count:
            for unit in units:
                if not unit.not_delete:
                    continue
                unit_btn = UnitBtn(unit)
                unit_btn.setFixedSize(QSize(100, 30))
                unit_btn.setText("Изменить")
                unit_btn.clicked.connect(lambda: self.edit(unit_btn.unit))
                self.table.setItem(i, 0, QTableWidgetItem(unit.name))
                self.table.setCellWidget(i, 1, unit_btn)
                i += 1

    def add(self):
        unitadd = AddUnit()
        unitadd.exec()
        self.fill()

    def edit(self, unit: Unit):
        pass


class TypesList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Типы самолетов")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Наименование", ""])
        self.table.resizeColumnsToContents()
        self.fill()

    def fill(self):
        types = PlaneType.select().where(PlaneType.not_deleted == True)
        row_count = types.count()
        self.table.setRowCount(row_count)
        i, count = 0, row_count
        while i < count:
            for type_plane in types:
                if not type_plane.not_delete:
                    continue
                type_btn = TypeBtn(type_plane)
                type_btn.setFixedSize(QSize(100, 30))
                type_btn.setText("Изменить")
                type_btn.clicked.connect(lambda: self.edit(type_btn.type_plane))
                self.table.setItem(i, 0, QTableWidgetItem(type_plane.type))
                self.table.setCellWidget(i, 1, type_btn)
                i += 1

    def edit(self, type_plane: PlaneType):
        plane_type_w = AddType(type_plane)
        if plane_type_w.exec():
            self.fill()

    def add(self):
        plane_type_w = AddType()
        plane_type_w.setWindowTitle("Добавить тип")
        if AddType().exec():
            self.fill()


class SpecList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Специалтьности")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Наименование", ""])
        self.table.resizeColumnsToContents()
        self.btn_add.clicked.connect(self.add)
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
