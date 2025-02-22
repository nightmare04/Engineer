from functools import partial

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

    def delete(self, model):
        model.not_delete = False
        model.save()
        self.accept()


class AddPlane(Adds):
    def __init__(self, plane: Plane = None, parent=None):
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle("Добавить самолет")

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

        if self.plane is not None:
            self.setWindowTitle("Изменить самолет")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.update_plane)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.plane))

    def add(self):
        plane = Plane()
        plane.bort_num = self.bort_num.text()
        plane.zav_num = self.zav_num.text()
        plane.unit = self.unit_combobox.currentData()
        plane.type = self.type_combobox.currentData()
        plane.save()
        self.accept()

    def load(self):
        self.bort_num.setText(self.plane.bort_num)
        self.zav_num.setText(self.plane.zav_num)
        self.type_combobox.setCurrentIndex(self.type_combobox.findData(str(self.plane.type)))
        self.unit_combobox.setCurrentIndex(self.unit_combobox.findData(str(self.plane.unit)))
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
    def __init__(self, type_plane: PlaneType = None, parent=None):
        super().__init__(parent)
        self.type_plane = type_plane
        self.setWindowTitle("Добавить тип самолета")
        self.type_plane_edit = QLineEdit()
        self.formlayout.addRow("&Тип самолета", self.type_plane_edit)
        if self.type_plane is not None:
            self.setWindowTitle("Изменить тип самолета")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.update_type)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.type_plane))

    def add(self):
        planetype = PlaneType()
        planetype.type = self.type_plane_edit.text()
        planetype.save()
        self.accept()

    def load(self):
        self.type_plane_edit.setText(self.type_plane.type)

    def update_type(self):
        self.type_plane.type = self.type_plane_edit.text()
        self.type_plane.save()
        self.accept()


class AddSpec(Adds):
    def __init__(self, spec: Spec = None, parent=None):
        super().__init__(parent)
        self.spec = spec
        self.setWindowTitle("Добавить специальность")
        self.spec_edit = QLineEdit()
        self.formlayout.addRow("&Наименование", self.spec_edit)
        if self.spec is not None:
            self.setWindowTitle("Изменить подразделение")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.spec))

    def add(self):
        spec = Spec()
        spec.name = self.spec_edit.text()
        spec.save()
        self.accept()

    def load(self):
        self.spec_edit.setText(self.spec.name)

    def save(self):
        self.spec.name = self.spec_edit.text()
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

            self.btn_delete = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_delete)
            self.btn_del.clicked.connect(partial(self.delete, self.unit))

    def add(self):
        unit = Unit()
        unit.name = self.unit_edit.text()
        unit.reglament = self.reglament.checkState()
        unit.save()
        self.accept()

    def save(self):
        self.unit.name = self.unit_edit.text()
        self.unit.reglament = self.reglament.checkState()
        self.unit.save()
        self.accept()

    def load(self):
        self.unit_edit.setText(self.unit.name)
        self.reglament.setChecked(self.unit.reglament)
