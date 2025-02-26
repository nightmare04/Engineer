from functools import partial

from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFormLayout, QComboBox, QLineEdit, QCheckBox, QDateEdit
from PyQt6.QtCore import Qt

from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox, RemZavComboBox, VypZavComboBox
from custom_widgets.groupboxs import OsobGroupBox
from database.models import PlaneType, Plane, Unit, Spec, RemType, RemZav, VypZav, OsobPlane


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

        self.type_combobox = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.zavNum = QLineEdit()
        self.bortNum = QLineEdit()
        self.dateVyp = QDateEdit()
        self.dateRem = QDateEdit()
        self.remType = QLineEdit()
        self.remZav = RemZavComboBox(RemZav.select())
        self.vypZav = VypZavComboBox(VypZav.select())
        self.unit_combobox = UnitComboBox(Unit.select().where(Unit.not_delete == True))
        self.osobPlane = OsobGroupBox()

        self.formlayout.addRow("Тип самолета", self.type_combobox)
        self.formlayout.addRow("Подразделение", self.unit_combobox)
        self.formlayout.addRow("Бортовой номер", self.bortNum)
        self.formlayout.addRow("Заводской номер", self.zavNum)
        self.formlayout.addRow("Дата выпуска", self.dateVyp)
        self.formlayout.addRow("Завод изготовитель", self.vypZav)
        self.formlayout.addRow("Дата ремонта", self.dateRem)
        self.formlayout.addRow("АРЗ", self.remZav)
        self.formlayout.addRow("Вид ремонта", self.remType)
        self.formlayout.addRow("Особенности самолета", self.osobPlane)

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
        plane.bortNum = self.bortNum.text()
        plane.zavNum = self.zavNum.text()
        plane.unit = self.unit_combobox.currentData()
        plane.planeType = self.type_combobox.currentData()
        plane.save()
        self.clean()

    def clean(self):
        self.bortNum.setText("")
        self.zavNum.setText("")

    def load(self):
        self.bortNum.setText(self.plane.bortNum)
        self.zavNum.setText(self.plane.zavNum)
        self.type_combobox.setCurrentIndex(self.type_combobox.findData(str(self.plane.planeType)))
        self.unit_combobox.setCurrentIndex(self.unit_combobox.findData(str(self.plane.unit)))
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.update_plane)

    def update_plane(self):
        self.plane.bortNum = self.bortNum.text()
        self.plane.zavNum = self.zavNum.text()
        self.plane.unit = self.unit_combobox.currentData()
        self.plane.planeType = self.type_combobox.currentData()
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
        planetype.name = self.type_plane_edit.text()
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
        self.formlayout.addRow("&Временное нахождение самолетов", self.reglament)
        if self.unit is not None:
            self.setWindowTitle("Изменить подразделение")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

            self.btn_delete = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_delete)
            self.btn_delete.clicked.connect(partial(self.delete, self.unit))

    def add(self):
        unit = Unit()
        unit.name = self.unit_edit.text()
        unit.reglament = self.reglament.isChecked()
        unit.save()
        self.accept()

    def save(self):
        self.unit.name = self.unit_edit.text()
        self.unit.reglament = self.reglament.isChecked()
        self.unit.save()
        self.accept()

    def load(self):
        self.unit_edit.setText(self.unit.name)
        if self.unit.reglament:
            self.reglament.setCheckState(Qt.CheckState.Checked)


class AddOsob(Adds):
    def __init__(self, osob: OsobPlane = None, parent=None):
        super().__init__(parent)
        self.osob = osob
        self.setWindowTitle("Добавить особенность")
        self.osob_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.formlayout.addRow("Тип самолета", self.plane_type)
        self.formlayout.addRow("&Наименование", self.osob_edit)
        if self.osob is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.osob))

    def add(self):
        osob = OsobPlane()
        osob.name = self.osob_edit.text()
        osob.planeType = self.plane_type.currentData(role=Qt.ItemDataRole.UserRole)
        osob.save()
        self.accept()

    def load(self):
        self.osob_edit.setText(self.osob.name)

    def save(self):
        self.osob.name = self.osob_edit.text()
        self.osob.save()
        self.accept()