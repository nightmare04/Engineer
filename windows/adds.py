from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFormLayout, QComboBox, QLineEdit, QCheckBox

from database import PlaneType, Plane, Unit, Spec


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

        self.plane = Plane()
        self.type_combobox = QComboBox()
        self.zav_num = QLineEdit()
        self.bort_num = QLineEdit()
        self.unit_combobox = QComboBox()

        self.formlayout.addRow("&Тип самолета", self.type_combobox)
        self.formlayout.addRow("&Заводской номер", self.zav_num)
        self.formlayout.addRow("&Бортовой номер", self.bort_num)
        self.formlayout.addRow("&Подразделение", self.unit_combobox)

        for unit in Unit.select():
            self.unit_combobox.addItem(unit.name, unit.id)

        for type_plane in PlaneType.select():
            self.type_combobox.addItem(type_plane.type, type_plane.id)

    def add(self):
        plane = Plane()
        plane.bort_num = self.bort_num.text()
        plane.zav_num = self.zav_num.text()
        plane.unit = self.unit_combobox.currentData()
        plane.type = self.type_combobox.currentData()
        plane.save()
        self.accept()

    def load(self, plane: Plane):
        self.plane = plane
        self.bort_num.setText(plane.bort_num)
        self.zav_num.setText(plane.zav_num)
        self.type_combobox.setCurrentIndex(self.type_combobox.findData(str(plane.type)))
        self.unit_combobox.setCurrentIndex(self.unit_combobox.findData(str(plane.unit)))
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.update_plane)

    def update_plane(self):
        self.plane.bort_num = self.bort_num.text()
        self.plane.zav_num = self.zav_num.text()
        self.plane.unit = self.unit_combobox.currentData()
        self.plane.type = self.type_combobox.currentData()
        self.plane.save()
        self.accept()


class AddType(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить тип самолета")
        self.type_plane = None
        self.type_plane_edit = QLineEdit()
        self.formlayout.addRow("&Тип самолета", self.type_plane_edit)

    def add(self):
        planetype = PlaneType()
        planetype.type = self.type_plane_edit.text()
        planetype.save()
        self.accept()

    def load(self, type_plane: PlaneType):
        self.type_plane = type_plane
        self.type_plane_edit.setText(type_plane.type)
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.update_type)

    def update_type(self):
        self.type_plane.type = self.type_plane_edit.text()
        self.type_plane.save()
        self.accept()


class AddSpec(Adds):
    def __init__(self, spec: Spec = None, parent=None):
        super().__init__(parent)
        self.spec=spec
        self.setWindowTitle("Добавить специальность")
        self.spec_edit = QLineEdit()
        self.formlayout.addRow("&Наименование", self.spec_edit)
        if self.spec is not None:
            self.setWindowTitle("Изменить подразделение")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.load)

    def add(self):
        spec = Spec()
        spec.name = self.spec_edit.text()
        spec.save()
        self.accept()

    def load(self):
        self.spec_edit.setText(self.spec.name)

    def save(self):
        self.spec.save()
        self.accept()


class AddUnit(Adds):
    def __init__(self, unit: Unit = None, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setWindowTitle("Добавить подразделение")
        self.unit_edit = QLineEdit()
        self.reglament = QCheckBox()
        self.formlayout.addRow("&Наименование", self.unit_edit)
        self.formlayout.addRow("&Регламент", self.reglament)
        if self.unit is not None:
            self.setWindowTitle("Изменить подразделение")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

    def add(self):
        unit = Unit()
        unit.name = self.unit_edit.text()
        unit.reglament = self.reglament.checkState()
        unit.save()
        self.accept()

    def load(self):
        self.unit_edit.setText(self.unit.name)
        self.reglament.setChecked(self.unit.reglament)

    def save(self):
        self.unit.save()
        self.accept()

