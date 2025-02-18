
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from database.models import Plane

class Lists(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 600)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)
        self.table = QTableWidget()
        self.mainlayout.addWidget(self.table)
        self.btnlayout = QHBoxLayout(self.mainlayout)
        self.mainlayout.addLayout(self.btnlayout)
        self.btn_ok = QPushButton("Ок")
        self.btn_add = QPushButton("Добавить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_add)
        self.fill()
        self.btn_ok.clicked.connect(self.accept)
        self.btn_add.clicked.connect(self.add)

    def fill(self):
        pass

    def add(self):
        pass

class PlanesList(Lists):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Самолеты")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["№ п/п", "Тип", "Бортовой номер", "Заводской номер", ""])

    def fill(self):
        planes = Plane.select()
        row_count = planes.count()
        self.table.setRowCount(row_count)
        for plane in planes:
            i, count = 0, row_count
            while i < count:
                self.table.setItem(count, 0, QTableWidgetItem(str(count+1)))
                self.table.setItem(count, 1, QTableWidgetItem(plane.type))
                self.table.setItem(count, 2, QTableWidgetItem(plane.bort_num))
                self.table.setItem(count, 3, QTableWidgetItem(plane.zav_num))
                i += 1

    def add(self):
        pass



