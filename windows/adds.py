from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFormLayout, QComboBox, QLineEdit

from database import PlaneType, Plane, Unit


class Adds(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)

        self.formlayout = QFormLayout()
        self.btnlayout = QHBoxLayout()

        self.btn_ok = QPushButton("Ок")
        self.btn_cancel = QPushButton("Отменить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_cancel)

        self.mainlayout.addLayout(self.formlayout)
        self.mainlayout.addLayout(self.btnlayout)

        self.btn_ok.clicked.connect(self.add)
        self.btn_cancel.clicked.connect(self.reject)

    def add(self):
        pass


class AddPlane(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить самолет")

        self.type_combobox = QComboBox()
        self.zav_num = QLineEdit()
        self.bort_num = QLineEdit()
        self.unit_combobox = QComboBox()

        self.formlayout.addRow("&Тип самолета", self.type_combobox)
        self.formlayout.addRow("&Заводской номер", self.zav_num)
        self.formlayout.addRow("&Бортовой номер", self.bort_num)
        self.formlayout.addRow("&Подразделение", self.unit_combobox)

    def add(self):
        plane = Plane()
        plane.bort_num = self.bort_num.text()
        plane.zav_num = self.zav_num.text()
        plane.unit = self.unit_combobox.currentText()
        plane.type = self.type_combobox.currentText()
        plane.save()
        self.accept()


class AddType(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить тип самолета")

        self.type = QLineEdit()
        self.formlayout.addRow("&Тип самолета", self.type)

    def add(self):
        typeplane = PlaneType()
        typeplane.type = self.type.text()
        typeplane.save()
        self.accept()


class AddUnit(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить подразделение")

        self.unit = QLineEdit()
        self.formlayout.addRow("&Наименование", self.unit)

    def add(self):
        unit = Unit()
        unit.name = self.unit.text()
        unit.save()
        self.accept()