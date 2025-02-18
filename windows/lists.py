from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

from custom_widgets import UnitBtn, PlaneBtn
from database.models import Plane, Unit
from windows.adds import AddPlane, AddUnit


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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Тип", "Бортовой номер", "Заводской номер", ""])
        self.table.resizeColumnsToContents()
        self.fill()

    def fill(self):
        planes = Plane.select()
        row_count = planes.count()
        self.table.setRowCount(row_count)
        i = 0
        for plane in planes:
            plane_btn = PlaneBtn(plane)
            plane_btn.setText("Изменить")
            plane_btn.setCheckable(False)
            plane_btn.setFixedSize(QSize(100,30))
            self.table.setItem(i, 0, QTableWidgetItem(str(plane.type)))
            self.table.setItem(i, 1, QTableWidgetItem(str(plane.bort_num)))
            self.table.setItem(i, 2, QTableWidgetItem(str(plane.zav_num)))
            self.table.setCellWidget(i, 3, plane_btn)
            i += 1

    def add(self):
        planeadd = AddPlane()
        planeadd.exec()
        self.fill()

    def edit(self, plane:Plane):
        pass


class UnitList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подразделения")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Наименование", ""])
        self.table.resizeColumnsToContents()
        self.fill()

    def fill(self):
        units = Unit.select()
        row_count = units.count()
        self.table.setRowCount(row_count)
        i, count = 0, row_count
        while i < count:
            for unit in units:
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

    def edit(self, unit:Unit):
        pass
